#!/usr/bin/env python3
"""
Bonus: Generate materials for end-to-end application task.
Creates a realistic image processing scenario.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from skimage import data, transform, filters, exposure
from skimage.util import random_noise
import warnings
warnings.filterwarnings('ignore')

def ensure_output_dir():
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir

def generate_document_scan(output_dir):
    """Generate a degraded document scan for restoration pipeline task."""
    # Create a synthetic document-like image
    np.random.seed(42)

    # Start with text-like image
    doc = np.ones((400, 300)) * 0.95  # white background

    # Add some "text lines"
    for row in range(50, 350, 25):
        # Random line lengths
        line_length = np.random.randint(50, 250)
        start_col = np.random.randint(20, 50)
        doc[row:row+8, start_col:start_col+line_length] = 0.1

    # Add a "title" at top
    doc[20:35, 50:250] = 0.05

    # Add some "paragraphs" with varying intensity
    doc[70:180, 30:270] = np.where(doc[70:180, 30:270] < 0.5, 0.15, doc[70:180, 30:270])

    # Save clean version
    plt.imsave(output_dir / "document_clean.png", doc, cmap='gray')

    # Create degraded version
    degraded = doc.copy()

    # 1. Uneven illumination (simulate bad scanner light)
    x, y = np.meshgrid(np.linspace(0, 1, 300), np.linspace(0, 1, 400))
    illumination = 0.7 + 0.3 * np.sin(x * np.pi) * (0.8 + 0.2 * y)
    degraded = degraded * illumination

    # 2. Add noise
    degraded = random_noise(degraded, mode='gaussian', var=0.01)

    # 3. Slight blur
    degraded = filters.gaussian(degraded, sigma=1)

    # 4. Reduce contrast
    degraded = exposure.rescale_intensity(degraded, out_range=(0.2, 0.85))

    # 5. Add some specks (dust)
    speck_coords = np.random.randint(0, min(degraded.shape), (30, 2))
    for r, c in speck_coords:
        if r < 400 and c < 300:
            degraded[r, c] = np.random.uniform(0, 0.3)

    degraded = np.clip(degraded, 0, 1)
    plt.imsave(output_dir / "document_degraded.png", degraded, cmap='gray')

    print("Generated document scan images")

def generate_medical_image(output_dir):
    """Generate a synthetic medical-like image for analysis."""
    np.random.seed(123)

    # Create circular structure (like a cell or tumor)
    img = np.zeros((256, 256))

    # Background tissue texture
    noise = filters.gaussian(np.random.randn(256, 256), sigma=5)
    img = 0.3 + 0.1 * noise

    # Add main structure (tumor-like)
    center = (128, 128)
    for r in range(256):
        for c in range(256):
            dist = np.sqrt((r - center[0])**2 + (c - center[1])**2)
            if dist < 60:
                img[r, c] = 0.7 + 0.1 * np.sin(dist/10)
            elif dist < 70:
                img[r, c] = 0.5  # boundary

    # Add some smaller structures
    for _ in range(5):
        cx, cy = np.random.randint(50, 200, 2)
        radius = np.random.randint(10, 20)
        for r in range(max(0, cx-radius), min(256, cx+radius)):
            for c in range(max(0, cy-radius), min(256, cy+radius)):
                if (r-cx)**2 + (c-cy)**2 < radius**2:
                    img[r, c] = np.random.uniform(0.4, 0.6)

    img = np.clip(img, 0, 1)
    plt.imsave(output_dir / "medical_scan.png", img, cmap='gray')

    # Create a noisy version
    noisy = random_noise(img, mode='gaussian', var=0.02)
    plt.imsave(output_dir / "medical_scan_noisy.png", np.clip(noisy, 0, 1), cmap='gray')

    print("Generated medical image samples")

def generate_satellite_like(output_dir):
    """Generate satellite-like imagery for object detection task."""
    np.random.seed(456)

    # Create terrain background
    img = np.zeros((300, 400, 3))

    # Green vegetation areas
    for _ in range(20):
        cx, cy = np.random.randint(0, 300), np.random.randint(0, 400)
        for r in range(max(0, cx-30), min(300, cx+30)):
            for c in range(max(0, cy-40), min(400, cy+40)):
                if np.random.rand() > 0.3:
                    img[r, c] = [0.2 + np.random.rand()*0.2,
                                 0.4 + np.random.rand()*0.3,
                                 0.1 + np.random.rand()*0.1]

    # Brown/tan areas (buildings, roads)
    for _ in range(10):
        cx, cy = np.random.randint(0, 300), np.random.randint(0, 400)
        w, h = np.random.randint(20, 50), np.random.randint(20, 50)
        img[max(0,cx):min(300,cx+h), max(0,cy):min(400,cy+w)] = [
            0.6 + np.random.rand()*0.2,
            0.5 + np.random.rand()*0.2,
            0.4 + np.random.rand()*0.2
        ]

    # Add some "objects" (vehicles/structures)
    objects = []
    for _ in range(8):
        cx, cy = np.random.randint(30, 270), np.random.randint(30, 370)
        w, h = np.random.randint(8, 15), np.random.randint(8, 15)
        color = [0.3 + np.random.rand()*0.3] * 3  # grayish
        img[cx:cx+h, cy:cy+w] = color
        objects.append({'x': cy, 'y': cx, 'w': w, 'h': h})

    # Add noise
    img = img + np.random.randn(*img.shape) * 0.05
    img = np.clip(img, 0, 1)

    plt.imsave(output_dir / "satellite_image.png", img)

    # Save object annotations
    np.save(output_dir / "satellite_objects.npy", objects)

    print("Generated satellite-like image")

def create_pipeline_challenge(output_dir):
    """Create a multi-degradation image for pipeline design task."""
    # Use astronaut image
    img = data.astronaut()
    img = img / 255.0

    # Apply multiple degradations
    # 1. Reduce resolution
    small = transform.resize(img, (128, 128), anti_aliasing=True)
    degraded = transform.resize(small, img.shape[:2], order=1)

    # 2. Add noise
    degraded = random_noise(degraded, mode='gaussian', var=0.01)

    # 3. Reduce contrast
    degraded = exposure.rescale_intensity(degraded, out_range=(0.15, 0.85))

    # 4. Color cast (yellowish)
    degraded[:, :, 0] = degraded[:, :, 0] * 1.1  # More red
    degraded[:, :, 2] = degraded[:, :, 2] * 0.85  # Less blue

    # 5. Slight blur
    for c in range(3):
        degraded[:, :, c] = filters.gaussian(degraded[:, :, c], sigma=1.5)

    degraded = np.clip(degraded, 0, 1)

    plt.imsave(output_dir / "pipeline_original.png", (img * 255).astype(np.uint8))
    plt.imsave(output_dir / "pipeline_degraded.png", (degraded * 255).astype(np.uint8))

    # Create info file
    info = """
# Pipeline Challenge

## Degradations Applied (in order):
1. Resolution reduction (512→128→512)
2. Gaussian noise (σ² = 0.01)
3. Contrast reduction (range compressed to 0.15-0.85)
4. Color cast (red +10%, blue -15%)
5. Gaussian blur (σ = 1.5)

## Your Task:
Design a restoration pipeline to recover the image.
Consider the ORDER of operations carefully!
"""
    with open(output_dir / "pipeline_info.md", 'w') as f:
        f.write(info)

    print("Generated pipeline challenge")

def main():
    output_dir = ensure_output_dir()
    generate_document_scan(output_dir)
    generate_medical_image(output_dir)
    generate_satellite_like(output_dir)
    create_pipeline_challenge(output_dir)
    print("✅ Bonus materials generated successfully!")

if __name__ == "__main__":
    main()
