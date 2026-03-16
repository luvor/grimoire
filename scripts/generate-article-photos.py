#!/usr/bin/env python3
"""Batch-generate all photos for an article from a photos.json manifest.

Usage:
    python3 scripts/generate-article-photos.py articles/wrestling-uniform-revolution/photos.json
"""

import argparse
import json
import os
import subprocess
import sys
import time


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATE_SCRIPT = os.path.join(SCRIPT_DIR, "generate-image.py")
CENSOR_SCRIPT = os.path.join(SCRIPT_DIR, "censor-faces.py")


def run_generate(prompt, output, model=None, aspect=None):
    """Run generate-image.py for a single photo."""
    cmd = [sys.executable, GENERATE_SCRIPT, "--prompt", prompt, "--output", output]
    if model:
        cmd.extend(["--model", model])
    if aspect:
        cmd.extend(["--aspect", aspect])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return False
    print(result.stdout, end="")
    return True


def run_censor(input_path, output_path, auto_head=False, region=None):
    """Run censor-faces.py on a generated photo."""
    cmd = [sys.executable, CENSOR_SCRIPT, input_path, output_path]
    if auto_head:
        cmd.append("--auto-head")
    if region:
        cmd.extend(["--region", region])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return False
    print(result.stdout, end="")
    return True


def main():
    parser = argparse.ArgumentParser(description="Batch-generate article photos")
    parser.add_argument("manifest", help="Path to photos.json")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip photos that already exist")
    args = parser.parse_args()

    with open(args.manifest) as f:
        manifest = json.load(f)

    article_dir = os.path.dirname(os.path.abspath(args.manifest))
    images_dir = os.path.join(article_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    photos = manifest.get("photos", [])
    total = len(photos)
    success = 0
    html_snippets = []

    print(f"\n{'='*50}")
    print(f"Generating {total} photos for: {article_dir}")
    print(f"{'='*50}\n")

    for i, photo in enumerate(photos, 1):
        photo_id = photo["id"]
        output_file = f"{photo_id}.webp"
        output_path = os.path.join(images_dir, output_file)

        if args.skip_existing and os.path.exists(output_path):
            print(f"[{i}/{total}] Skipping (exists): {output_file}")
            success += 1
            continue

        print(f"\n[{i}/{total}] Generating: {photo_id}")
        print(f"  Prompt: {photo['prompt'][:80]}...")

        # Generate to a temp path first (uncensored)
        temp_path = os.path.join(images_dir, f"_tmp_{photo_id}.webp")

        ok = run_generate(
            prompt=photo["prompt"],
            output=temp_path,
            model=photo.get("model"),
            aspect=photo.get("aspect", "3:4")
        )

        if not ok:
            print(f"  FAILED: {photo_id}", file=sys.stderr)
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            continue

        # Apply censoring if configured
        censor = photo.get("censor", {})
        if censor.get("auto_head") or censor.get("region"):
            ok = run_censor(
                temp_path, output_path,
                auto_head=censor.get("auto_head", False),
                region=censor.get("region")
            )
            if ok and os.path.exists(temp_path):
                os.unlink(temp_path)
        else:
            # No censoring needed, just rename
            os.rename(temp_path, output_path)

        if os.path.exists(output_path):
            size_kb = os.path.getsize(output_path) / 1024
            print(f"  Done: {output_file} ({size_kb:.0f} KB)")
            success += 1

            # Collect HTML snippet
            caption = photo.get("caption", "")
            css_class = photo.get("css_class", "figure-wide")
            snippet = f'''<figure class="{css_class}">
  <img src="images/{output_file}" alt="{caption}" loading="lazy">
  <figcaption>{caption}</figcaption>
</figure>'''
            html_snippets.append((photo_id, snippet))

        # Brief pause to avoid rate limits
        if i < total:
            time.sleep(2)

    # Summary
    print(f"\n{'='*50}")
    print(f"Results: {success}/{total} photos generated")
    print(f"{'='*50}")

    if html_snippets:
        print("\n--- HTML snippets for article ---\n")
        for photo_id, snippet in html_snippets:
            print(f"<!-- {photo_id} -->")
            print(snippet)
            print()


if __name__ == "__main__":
    main()
