#!/usr/bin/env python3
"""Generate an image using Gemini 2.5 Flash Image Generation API.

Usage:
    python3 scripts/generate-image.py \
        --prompt "Professional sports photo of..." \
        --output articles/wrestling-uniform-revolution/images/gladiator-photo.webp \
        [--model gemini-2.5-flash-preview-image-generation] \
        [--aspect 3:4]
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
import urllib.error


API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
DEFAULT_MODEL = "gemini-2.5-flash-image"
MAX_SIDE = 1200
WEBP_QUALITY = 80


def load_api_key():
    """Load GEMINI_API_KEY from environment or .env file."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    # Try .env in project root
    env_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        os.path.join(os.getcwd(), ".env"),
    ]
    for env_path in env_paths:
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY=") and not line.startswith("#"):
                        val = line.split("=", 1)[1].strip().strip("'\"")
                        if val and val != "your_api_key_here":
                            return val

    print("Error: GEMINI_API_KEY not found.", file=sys.stderr)
    print("Set it via environment variable or in .env file.", file=sys.stderr)
    print("Get a free key at: https://aistudio.google.com/apikey", file=sys.stderr)
    sys.exit(1)


def generate_image(prompt, model, api_key, aspect=None):
    """Call Gemini API and return raw PNG bytes."""
    url = f"{API_BASE}/{model}:generateContent?key={api_key}"

    # Build the prompt with aspect ratio hint
    full_prompt = prompt
    if aspect:
        full_prompt += f"\n\nAspect ratio: {aspect}"

    payload = {
        "contents": [
            {
                "parts": [{"text": full_prompt}]
            }
        ],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        if e.code == 429:
            print("Error: Rate limit exceeded. Wait a moment and retry.", file=sys.stderr)
        elif e.code == 400 and "SAFETY" in body.upper():
            print("Error: Prompt blocked by safety filters. Rephrase the prompt.", file=sys.stderr)
        else:
            print(f"Error: HTTP {e.code}: {body[:500]}", file=sys.stderr)
        sys.exit(1)

    # Extract image from response
    candidates = result.get("candidates", [])
    if not candidates:
        print("Error: No candidates in response.", file=sys.stderr)
        print(json.dumps(result, indent=2)[:500], file=sys.stderr)
        sys.exit(1)

    parts = candidates[0].get("content", {}).get("parts", [])
    for part in parts:
        if "inlineData" in part:
            mime = part["inlineData"].get("mimeType", "")
            if mime.startswith("image/"):
                return base64.b64decode(part["inlineData"]["data"])

    print("Error: No image found in response.", file=sys.stderr)
    for part in parts:
        if "text" in part:
            print(f"Model said: {part['text'][:300]}", file=sys.stderr)
    sys.exit(1)


def convert_to_webp(png_bytes, output_path):
    """Convert PNG bytes to WebP using ImageMagick, resize to max 1200px."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(png_bytes)
        tmp_path = tmp.name

    try:
        cmd = [
            "magick", tmp_path,
            "-resize", f"{MAX_SIDE}x{MAX_SIDE}>",
            "-quality", str(WEBP_QUALITY),
            output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
    finally:
        os.unlink(tmp_path)

    size_kb = os.path.getsize(output_path) / 1024
    return size_kb


def main():
    parser = argparse.ArgumentParser(description="Generate image via Gemini API")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--output", required=True, help="Output file path (.webp)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Gemini model name")
    parser.add_argument("--aspect", default=None, help="Aspect ratio hint (e.g. 3:4)")
    args = parser.parse_args()

    api_key = load_api_key()

    print(f"Generating: {os.path.basename(args.output)}")
    print(f"  Prompt: {args.prompt[:80]}...")
    png_bytes = generate_image(args.prompt, args.model, api_key, args.aspect)
    print(f"  Received: {len(png_bytes) / 1024:.0f} KB PNG")

    size_kb = convert_to_webp(png_bytes, args.output)
    print(f"  Saved: {args.output} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
