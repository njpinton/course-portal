#!/usr/bin/env python3
"""
Part 0: Generate fundamental image processing examples.
Creates images for testing basic operations.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from skimage import data, color, filters, transform
from skimage.util import random_noise
import warnings
warnings.filterwarnings('ignore')

def ensure_output_dir():
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir

def generate_test_images(output_dir):
    """Generate various test images for fundamentals section."""

    # 1. Original clean image (astronaut)
    astronaut = data.astronaut()
    plt.imsave(output_dir / "original_astronaut.png", astronaut)

    # 2. Grayscale version
    astronaut_gray = color.rgb2gray(astronaut)
    plt.imsave(output_dir / "grayscale_astronaut.png", astronaut_gray, cmap='gray')

    # 3. Different noise types
    noisy_gaussian = random_noise(astronaut, mode='gaussian', var=0.02)
    noisy_sp = random_noise(astronaut, mode='s&p', amount=0.05)
    noisy_poisson = random_noise(astronaut, mode='poisson')

    plt.imsave(output_dir / "noisy_gaussian.png", np.clip(noisy_gaussian, 0, 1))
    plt.imsave(output_dir / "noisy_salt_pepper.png", np.clip(noisy_sp, 0, 1))
    plt.imsave(output_dir / "noisy_poisson.png", np.clip(noisy_poisson, 0, 1))

    # 4. Blurred images
    blurred_gaussian = filters.gaussian(astronaut, sigma=3, channel_axis=-1)
    plt.imsave(output_dir / "blurred_gaussian.png", np.clip(blurred_gaussian, 0, 1))

    # 5. Low resolution versions
    small = transform.resize(astronaut, (64, 64), anti_aliasing=True)
    upscaled = transform.resize(small, astronaut.shape[:2], order=0)  # nearest neighbor
    plt.imsave(output_dir / "low_resolution.png", np.clip(upscaled, 0, 1))

    # 6. Histogram equalization candidate (low contrast)
    low_contrast = astronaut_gray * 0.3 + 0.3
    plt.imsave(output_dir / "low_contrast.png", low_contrast, cmap='gray')

    # 7. Camera image for edge detection
    camera = data.camera()
    plt.imsave(output_dir / "camera.png", camera, cmap='gray')

    # 8. Coins for segmentation preview
    coins = data.coins()
    plt.imsave(output_dir / "coins.png", coins, cmap='gray')

    print(f"Generated {len(list(output_dir.glob('*.png')))} images in {output_dir}")

def create_comparison_figure(output_dir):
    """Create a comparison figure showing different processing effects."""
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))

    astronaut = data.astronaut()
    astronaut_gray = color.rgb2gray(astronaut)

    images = [
        (astronaut, "Original RGB"),
        (astronaut_gray, "Grayscale"),
        (random_noise(astronaut, mode='gaussian', var=0.02), "Gaussian Noise"),
        (random_noise(astronaut, mode='s&p', amount=0.05), "Salt & Pepper"),
        (filters.gaussian(astronaut, sigma=3, channel_axis=-1), "Gaussian Blur"),
        (astronaut_gray * 0.3 + 0.3, "Low Contrast"),
        (filters.sobel(astronaut_gray), "Edge Detection"),
        (data.coins(), "Coins (Segmentation)")
    ]

    for ax, (img, title) in zip(axes.flat, images):
        if img.ndim == 2:
            ax.imshow(img, cmap='gray')
        else:
            ax.imshow(np.clip(img, 0, 1))
        ax.set_title(title)
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(output_dir / "overview_comparison.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Created overview comparison figure")

def main():
    output_dir = ensure_output_dir()
    generate_test_images(output_dir)
    create_comparison_figure(output_dir)
    print("✅ Part 0 materials generated successfully!")

if __name__ == "__main__":
    main()
