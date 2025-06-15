#!/usr/bin/env python3
"""
checkerboard_generator.py

Generate a black-and-white checkerboard pattern on an A4 canvas, with embedded DPI metadata,
suitable for printing at 100% scale.

Usage:
    python checkerboard_generator.py
        --rows 6 --cols 10
        --square-mm 25
        --margin-mm 10
        --dpi 300
        --output checkerboard.png
"""

import argparse
import numpy as np
from PIL import Image


def mm_to_px(value_mm: float, dpi: int) -> int:
    """Convert millimeters to pixels given DPI."""
    return int(round(dpi * value_mm / 25.4))


def generate_checkerboard(
    rows: int,
    cols: int,
    square_mm: float,
    margin_mm: float,
    dpi: int
) -> Image.Image:
    """
    Generate a PIL Image of a checkerboard with given parameters.
    Returns an RGB Image (mode='L').
    """
    # compute pixel sizes
    square_px = mm_to_px(square_mm, dpi)
    margin_px = mm_to_px(margin_mm, dpi)

    # build pattern of 0/1
    pattern = (np.indices((rows, cols)).sum(axis=0) % 2).astype(np.uint8)
    board = np.kron(pattern, np.ones((square_px, square_px), dtype=np.uint8))

    # add white margin
    h, w = board.shape
    canvas = 255 * np.ones((h + 2 * margin_px, w + 2 * margin_px), dtype=np.uint8)
    canvas[margin_px:margin_px+h, margin_px:margin_px+w] = board * 255

    # convert to PIL image
    return Image.fromarray(canvas)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a checkerboard pattern for A4 printing."
    )
    parser.add_argument("--rows",       type=int,   default=6,      help="Number of squares vertically.")
    parser.add_argument("--cols",       type=int,   default=10,     help="Number of squares horizontally.")
    parser.add_argument("--square-mm",  type=float, default=25.0,   help="Square size in mm.")
    parser.add_argument("--margin-mm",  type=float, default=10.0,   help="Margin around board in mm.")
    parser.add_argument("--dpi",        type=int,   default=300,    help="Printer DPI.")
    parser.add_argument("--output",     type=str,   default=None,   help="Output filename (PNG).")
    return parser.parse_args()


def main():
    args = parse_args()

    # generate image
    img = generate_checkerboard(
        rows=args.rows,
        cols=args.cols,
        square_mm=args.square_mm,
        margin_mm=args.margin_mm,
        dpi=args.dpi
    )

    # determine output filename
    if args.output:
        out_fn = args.output
    else:
        out_fn = f"checkerboard_{args.rows}x{args.cols}_{int(args.square_mm)}mm.png"

    # save with embedded DPI metadata
    img.save(out_fn, dpi=(args.dpi, args.dpi))
    print(f"Saved checkerboard to '{out_fn}' "
          f"({args.cols}×{args.rows} squares, {args.square_mm} mm each, margin {args.margin_mm} mm, {args.dpi} dpi).")


if __name__ == "__main__":
    main()
