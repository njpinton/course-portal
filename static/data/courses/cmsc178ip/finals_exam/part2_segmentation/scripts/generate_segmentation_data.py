#!/usr/bin/env python3
"""
Part 2: Generate segmentation dataset and materials.
Creates images for segmentation and morphology tasks.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from skimage import data, color, filters, morphology, measure, segmentation
from skimage.draw import disk, rectangle
import warnings
warnings.filterwarnings('ignore')

def ensure_output_dir():
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir

def generate_coins_dataset(output_dir):
    """Generate coins images for segmentation tasks."""
    coins = data.coins()

    # Save original
    plt.imsave(output_dir / "coins_original.png", coins, cmap='gray')

    # Create a noisy version
    noisy_coins = coins + np.random.normal(0, 20, coins.shape)
    noisy_coins = np.clip(noisy_coins, 0, 255).astype(np.uint8)
    plt.imsave(output_dir / "coins_noisy.png", noisy_coins, cmap='gray')

    # Create ground truth segmentation (approximate)
    thresh = filters.threshold_otsu(coins)
    binary = coins > thresh
    plt.imsave(output_dir / "coins_binary_otsu.png", binary.astype(float), cmap='gray')

    # Label connected components
    labeled = measure.label(binary)
    plt.imsave(output_dir / "coins_labeled.png", labeled, cmap='nipy_spectral')

    print("Generated coins segmentation dataset")

def generate_synthetic_shapes(output_dir):
    """Generate synthetic shapes for segmentation practice."""
    np.random.seed(42)

    # Create image with multiple shapes
    img = np.zeros((256, 256), dtype=np.uint8)

    # Add circles
    for _ in range(5):
        rr, cc = disk((np.random.randint(40, 216), np.random.randint(40, 216)),
                      np.random.randint(15, 35), shape=img.shape)
        img[rr, cc] = np.random.randint(150, 255)

    # Add rectangles
    for _ in range(3):
        start = (np.random.randint(20, 180), np.random.randint(20, 180))
        extent = (np.random.randint(30, 60), np.random.randint(30, 60))
        rr, cc = rectangle(start, extent=extent, shape=img.shape)
        img[rr, cc] = np.random.randint(100, 200)

    # Add noise
    noisy = img + np.random.normal(0, 10, img.shape)
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)

    plt.imsave(output_dir / "shapes_clean.png", img, cmap='gray')
    plt.imsave(output_dir / "shapes_noisy.png", noisy, cmap='gray')

    # Create ground truth mask
    gt_mask = img > 50
    plt.imsave(output_dir / "shapes_ground_truth.png", gt_mask.astype(float), cmap='gray')

    print("Generated synthetic shapes dataset")

def generate_cell_like_images(output_dir):
    """Generate cell-like images for biomedical segmentation task."""
    np.random.seed(123)

    img = np.zeros((256, 256), dtype=np.float32)

    # Add cell-like blobs
    cells = []
    for _ in range(12):
        center = (np.random.randint(30, 226), np.random.randint(30, 226))
        radius = np.random.randint(12, 25)
        rr, cc = disk(center, radius, shape=img.shape)
        intensity = np.random.uniform(0.6, 1.0)
        img[rr, cc] = intensity
        cells.append({'center': center, 'radius': radius})

    # Add gradient background
    x, y = np.meshgrid(np.linspace(0, 1, 256), np.linspace(0, 1, 256))
    background = 0.1 + 0.1 * (x + y) / 2

    # Combine
    combined = np.maximum(img, background)

    # Add noise
    noisy = combined + np.random.normal(0, 0.05, combined.shape)
    noisy = np.clip(noisy, 0, 1)

    plt.imsave(output_dir / "cells_image.png", noisy, cmap='gray')

    # Create ground truth
    gt = img > 0.5
    plt.imsave(output_dir / "cells_ground_truth.png", gt.astype(float), cmap='gray')

    # Save cell info
    np.save(output_dir / "cells_info.npy", cells)

    print("Generated cell-like images")

def generate_morphology_examples(output_dir):
    """Generate examples for morphology operations."""
    # Create a binary image with text-like features
    img = np.zeros((128, 256), dtype=bool)

    # Add some shapes that benefit from morphology
    img[30:50, 30:60] = True
    img[30:50, 80:85] = True  # thin line
    img[30:50, 100:130] = True
    img[30:50, 103:127] = False  # hole
    img[60:100, 50:90] = True
    img[70:90, 60:80] = False  # internal hole

    # Add some noise (small dots)
    noise_coords = np.random.randint(0, 128, (20, 2))
    for r, c in noise_coords:
        if c < 256:
            img[r, min(c, 255)] = True

    plt.imsave(output_dir / "morphology_input.png", img.astype(float), cmap='gray')

    # Apply different morphology operations
    selem = morphology.disk(3)

    eroded = morphology.erosion(img, selem)
    dilated = morphology.dilation(img, selem)
    opened = morphology.opening(img, selem)
    closed = morphology.closing(img, selem)

    # Create comparison figure
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title("Original")

    axes[0, 1].imshow(eroded, cmap='gray')
    axes[0, 1].set_title("Erosion (disk, r=3)")

    axes[0, 2].imshow(dilated, cmap='gray')
    axes[0, 2].set_title("Dilation (disk, r=3)")

    axes[1, 0].imshow(opened, cmap='gray')
    axes[1, 0].set_title("Opening (erosion→dilation)")

    axes[1, 1].imshow(closed, cmap='gray')
    axes[1, 1].set_title("Closing (dilation→erosion)")

    # Difference image
    diff = np.abs(img.astype(float) - opened.astype(float))
    axes[1, 2].imshow(diff, cmap='hot')
    axes[1, 2].set_title("Difference (Original - Opened)")

    for ax in axes.flat:
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(output_dir / "morphology_comparison.png", dpi=150, bbox_inches='tight')
    plt.close()

    print("Generated morphology examples")

def generate_watershed_example(output_dir):
    """Generate example for watershed segmentation."""
    # Create overlapping circles (touching cells)
    img = np.zeros((200, 200), dtype=np.float32)

    centers = [(60, 60), (60, 140), (140, 60), (140, 140), (100, 100)]
    for cx, cy in centers:
        rr, cc = disk((cx, cy), 35, shape=img.shape)
        img[rr, cc] = 1.0

    # Add gradient to make it interesting
    x, y = np.meshgrid(np.linspace(0, 1, 200), np.linspace(0, 1, 200))
    img = img * (0.7 + 0.3 * np.sin(x * np.pi) * np.sin(y * np.pi))

    # Add noise
    noisy = img + np.random.normal(0, 0.1, img.shape)
    noisy = np.clip(noisy, 0, 1)

    plt.imsave(output_dir / "watershed_input.png", noisy, cmap='gray')

    # Create distance transform for watershed demo
    binary = noisy > 0.3
    from scipy import ndimage
    distance = ndimage.distance_transform_edt(binary)

    plt.imsave(output_dir / "watershed_distance.png", distance, cmap='viridis')

    print("Generated watershed example")

def main():
    output_dir = ensure_output_dir()
    generate_coins_dataset(output_dir)
    generate_synthetic_shapes(output_dir)
    generate_cell_like_images(output_dir)
    generate_morphology_examples(output_dir)
    generate_watershed_example(output_dir)
    print("✅ Part 2 Segmentation materials generated successfully!")

if __name__ == "__main__":
    main()
