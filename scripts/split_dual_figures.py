#!/usr/bin/env python3
"""
Split dual-panel matplotlib figures into separate images.
For slides that have two charts side-by-side, this splits them
so they can be displayed in a stacked vertical layout for better
use of vertical space on 1920x1080 slides.
"""

from PIL import Image
from pathlib import Path
import sys

# Images to split (identified as having dual panels)
DUAL_PANEL_IMAGES = [
    "parameter_estimation_concept.png",
    "ml_applications.png",
    "estimator_properties.png",
    "estimator_bias_variance.png",
    "moments_illustration.png",
    "mom_visualization.png",
    "mom_poisson_example.png",
    "mom_properties.png",
    "likelihood_concept.png",
    "mle_visualization.png",
    "mle_exponential.png",
    "mle_properties.png",
    "numerical_mle.png",
    "mom_vs_mle_comparison.png",
    "efficiency_comparison.png",
    "linear_regression_estimation.png",
    "logistic_regression_estimation.png",
    "gaussian_mixture_estimation.png",
    "arima_estimation.png",
    "robust_estimation.png",
    "bootstrap_estimation.png",
    "model_selection.png",
    "diagnostic_tools.png",
    "computational_tools.png",
]

INPUT_DIR = Path(__file__).parent.parent / "static/images/courses/cmsc173/module-01"
OUTPUT_DIR = INPUT_DIR  # Same directory, with _left/_right suffixes


def split_image(filepath: Path, split_ratio: float = 0.5) -> tuple[Path, Path]:
    """
    Split an image horizontally into left and right halves.

    Args:
        filepath: Path to the source image
        split_ratio: Where to split (0.5 = middle, default)

    Returns:
        Tuple of (left_path, right_path)
    """
    img = Image.open(filepath)
    width, height = img.size

    # Calculate split point
    split_x = int(width * split_ratio)

    # Crop left and right halves
    left_img = img.crop((0, 0, split_x, height))
    right_img = img.crop((split_x, 0, width, height))

    # Generate output filenames
    stem = filepath.stem
    suffix = filepath.suffix
    left_path = filepath.parent / f"{stem}_left{suffix}"
    right_path = filepath.parent / f"{stem}_right{suffix}"

    # Save with same quality
    left_img.save(left_path, optimize=True)
    right_img.save(right_path, optimize=True)

    # Report dimensions
    print(f"  Original: {width}x{height} (ratio {width/height:.2f}:1)")
    print(f"  Left:     {left_img.size[0]}x{left_img.size[1]} → {left_path.name}")
    print(f"  Right:    {right_img.size[0]}x{right_img.size[1]} → {right_path.name}")

    return left_path, right_path


def analyze_image(filepath: Path) -> dict:
    """Analyze an image to determine if it's a dual-panel figure."""
    img = Image.open(filepath)
    width, height = img.size
    ratio = width / height

    return {
        "path": filepath,
        "width": width,
        "height": height,
        "ratio": ratio,
        "is_wide": ratio > 1.8,  # Likely dual-panel if wider than 1.8:1
    }


def main():
    print("=" * 60)
    print("Dual-Panel Figure Splitter")
    print("=" * 60)

    if not INPUT_DIR.exists():
        print(f"Error: Input directory not found: {INPUT_DIR}")
        sys.exit(1)

    # Process each dual-panel image
    processed = 0
    skipped = 0

    for filename in DUAL_PANEL_IMAGES:
        filepath = INPUT_DIR / filename

        if not filepath.exists():
            print(f"\n⚠ Skipping (not found): {filename}")
            skipped += 1
            continue

        # Check if already split
        left_path = INPUT_DIR / f"{filepath.stem}_left{filepath.suffix}"
        right_path = INPUT_DIR / f"{filepath.stem}_right{filepath.suffix}"

        if left_path.exists() and right_path.exists():
            print(f"\n✓ Already split: {filename}")
            skipped += 1
            continue

        print(f"\n📐 Splitting: {filename}")

        try:
            split_image(filepath)
            processed += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            skipped += 1

    print("\n" + "=" * 60)
    print(f"Complete! Processed: {processed}, Skipped: {skipped}")
    print("=" * 60)


if __name__ == "__main__":
    main()
