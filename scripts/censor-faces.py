#!/usr/bin/env python3
"""Censor faces with a black rectangle overlay.

Usage:
    python3 scripts/censor-faces.py input.webp output.webp [--auto-head] [--region x,y,w,h]

--auto-head: Heuristic for a standing full-body figure — black rectangle
             in top 2-18% height, central 30-65% width.
--region:    Manual rectangle as x,y,w,h (percentages of image dimensions).
"""

import argparse
import json
import os
import subprocess
import sys


def get_image_dimensions(path):
    """Get image width and height via ImageMagick."""
    result = subprocess.run(
        ["magick", "identify", "-format", "%w %h", path],
        capture_output=True, text=True, check=True
    )
    w, h = result.stdout.strip().split()
    return int(w), int(h)


def draw_censored_rectangle(input_path, output_path, x1, y1, x2, y2, border=True):
    """Draw a black rectangle (with optional white border) on the image."""
    commands = []

    # White border for 'redacted' effect
    if border:
        border_px = 3
        commands.extend([
            "-fill", "white",
            "-draw", f"rectangle {x1 - border_px},{y1 - border_px} {x2 + border_px},{y2 + border_px}",
        ])

    # Black rectangle
    commands.extend([
        "-fill", "black",
        "-draw", f"rectangle {x1},{y1} {x2},{y2}",
    ])

    cmd = ["magick", input_path] + commands + [output_path]
    subprocess.run(cmd, check=True, capture_output=True)


def auto_head_region(width, height):
    """Heuristic: head region for a standing full-body figure."""
    x1 = int(width * 0.30)
    x2 = int(width * 0.65)
    y1 = int(height * 0.02)
    y2 = int(height * 0.18)
    return x1, y1, x2, y2


def parse_region(region_str, width, height):
    """Parse 'x,y,w,h' as percentages → pixel coordinates."""
    parts = [float(x) for x in region_str.split(",")]
    if len(parts) != 4:
        print("Error: --region must be x,y,w,h (percentages)", file=sys.stderr)
        sys.exit(1)
    x, y, w, h = parts
    x1 = int(width * x / 100)
    y1 = int(height * y / 100)
    x2 = int(width * (x + w) / 100)
    y2 = int(height * (y + h) / 100)
    return x1, y1, x2, y2


def main():
    parser = argparse.ArgumentParser(description="Censor faces with black rectangle")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("--auto-head", action="store_true",
                        help="Auto-detect head region for standing figure")
    parser.add_argument("--region", type=str, default=None,
                        help="Manual region as x,y,w,h (percentages)")
    parser.add_argument("--no-border", action="store_true",
                        help="Skip white border around black rectangle")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    width, height = get_image_dimensions(args.input)

    if args.region:
        x1, y1, x2, y2 = parse_region(args.region, width, height)
    elif args.auto_head:
        x1, y1, x2, y2 = auto_head_region(width, height)
    else:
        print("Error: Specify --auto-head or --region", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    draw_censored_rectangle(args.input, args.output, x1, y1, x2, y2,
                            border=not args.no_border)

    size_kb = os.path.getsize(args.output) / 1024
    print(f"Censored: {args.output} (rect: {x1},{y1} → {x2},{y2}, {size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
