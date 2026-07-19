#!/usr/bin/env python3
"""Generate an image via render-farm (Google Flow, Nano Banana) and save as WebP.

Заменяет прежний Gemini-API путь: генерация идёт через ~/Projects/render-farm
(bun + playwright, залогиненный Chrome-профиль, квота подписки Flow).
CLI совместим со старой версией — auto-articles/tools/image_gen.py зовёт как раньше.

Usage:
    python3 scripts/generate-image.py \
        --prompt "Editorial illustration of..." \
        --output assets/covers/some-slug.webp \
        [--model nano-banana-pro] \
        [--aspect 16:9]
"""

import argparse
import glob
import os
import re
import subprocess
import sys

RENDER_FARM = os.path.expanduser("~/Projects/render-farm")
DEFAULT_MODEL = "nano-banana-pro"
MAX_SIDE = 1200
WEBP_QUALITY = 80

# Flow генерит нативно 16:9 | 4:3 | 1:1 | 3:4 | 9:16; render-farm слоты: 1:1 | 3:4 | 16:9
ASPECT_TO_SLOT = {
    "16:9": "16:9",
    "3:2": "16:9",  # старый Gemini-аспект обложек precogs
    "4:3": "16:9",
    "1:1": "1:1",
    "3:4": "3:4",
    "2:3": "3:4",
    "9:16": "3:4",
}


def run_render_farm(prompt, model, slot):
    """bun gen → путь к скачанному raw-файлу."""
    if not os.path.isdir(RENDER_FARM):
        print(f"Error: render-farm не найден: {RENDER_FARM}", file=sys.stderr)
        sys.exit(1)

    cmd = [
        "bun", "gen", prompt,
        "--type", "image",
        "--slot", slot,
        "--model", model,
        "--variants", "1",
    ]
    proc = subprocess.run(cmd, cwd=RENDER_FARM, capture_output=True, text=True)
    sys.stderr.write(proc.stderr)
    print(proc.stdout)
    if proc.returncode != 0:
        print(f"Error: bun gen exited {proc.returncode}", file=sys.stderr)
        sys.exit(1)

    m = re.search(r"Батч: (.+)", proc.stdout)
    if not m:
        print("Error: не нашёл строку 'Батч:' в выводе bun gen", file=sys.stderr)
        sys.exit(1)
    raw_dir = os.path.join(m.group(1).strip(), "raw")
    files = sorted(glob.glob(os.path.join(raw_dir, "*")))
    if not files:
        print(f"Error: пустой {raw_dir} — генерация не скачалась", file=sys.stderr)
        sys.exit(1)
    return files[0]


def convert_to_webp(src_path, output_path):
    """ImageMagick: resize до 1200px по большей стороне → WebP q80."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cmd = [
        "magick", src_path,
        "-resize", f"{MAX_SIDE}x{MAX_SIDE}>",
        "-quality", str(WEBP_QUALITY),
        output_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return os.path.getsize(output_path) / 1024


def main():
    parser = argparse.ArgumentParser(description="Generate image via render-farm (Flow)")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--output", required=True, help="Output file path (.webp)")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="Flow model: nano-banana-pro | nano-banana-2 | nano-banana-2-lite")
    parser.add_argument("--aspect", default="16:9", help="Aspect ratio (16:9, 3:4, 1:1...)")
    args = parser.parse_args()

    slot = ASPECT_TO_SLOT.get(args.aspect)
    if slot is None:
        print(f"Error: аспект {args.aspect} не маппится на слот Flow "
              f"({', '.join(sorted(ASPECT_TO_SLOT))})", file=sys.stderr)
        sys.exit(1)

    print(f"Generating: {os.path.basename(args.output)}")
    print(f"  Prompt: {args.prompt[:80]}...")
    raw_path = run_render_farm(args.prompt, args.model, slot)
    print(f"  Raw: {raw_path}")

    size_kb = convert_to_webp(raw_path, args.output)
    print(f"  Saved: {args.output} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
