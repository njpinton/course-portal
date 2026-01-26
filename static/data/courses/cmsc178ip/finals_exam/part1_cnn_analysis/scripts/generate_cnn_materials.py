#!/usr/bin/env python3
"""
Part 1: Generate CNN analysis materials.
Creates visualizations and test images for CNN understanding tasks.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from skimage import data, color, transform
import warnings
warnings.filterwarnings('ignore')

def ensure_output_dir():
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir

def generate_convolution_examples(output_dir):
    """Generate images showing convolution filter effects."""
    # Simple test pattern
    pattern = np.zeros((64, 64))
    pattern[20:44, 20:44] = 1
    pattern[28:36, 28:36] = 0.5

    # Different kernels
    kernels = {
        'identity': np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
        'edge_horizontal': np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]),
        'edge_vertical': np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]),
        'sharpen': np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
        'blur_box': np.ones((3, 3)) / 9,
        'emboss': np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
    }

    # Save test pattern
    plt.imsave(output_dir / "test_pattern.png", pattern, cmap='gray')

    # Create kernel visualization
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    for ax, (name, kernel) in zip(axes.flat, kernels.items()):
        ax.imshow(kernel, cmap='RdBu', vmin=-2, vmax=2)
        ax.set_title(f"{name.replace('_', ' ').title()}\n{kernel.shape}")
        for i in range(kernel.shape[0]):
            for j in range(kernel.shape[1]):
                ax.text(j, i, f'{kernel[i,j]:.1f}', ha='center', va='center', fontsize=10)
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(output_dir / "kernel_examples.png", dpi=150, bbox_inches='tight')
    plt.close()

    # Save kernels as numpy files for students to use
    np.save(output_dir / "kernels.npy", kernels)

    print(f"Generated convolution examples in {output_dir}")

def generate_feature_map_example(output_dir):
    """Generate a visualization showing feature map concept."""
    # Create a simple 'image' with clear features
    img = np.zeros((28, 28))

    # Add a vertical edge
    img[:, 10:14] = 1

    # Add a horizontal edge
    img[10:14, :] = 0.7

    # Add a diagonal
    for i in range(28):
        if 0 <= 27-i < 28:
            img[i, 27-i] = 0.5

    plt.imsave(output_dir / "simple_features.png", img, cmap='gray')

    # Create multi-channel visualization
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))

    axes[0].imshow(img, cmap='gray')
    axes[0].set_title("Input Image")
    axes[0].axis('off')

    # Simulate feature maps (edge detections)
    from scipy import ndimage

    sobel_h = ndimage.sobel(img, axis=0)
    sobel_v = ndimage.sobel(img, axis=1)
    laplacian = ndimage.laplace(img)

    axes[1].imshow(sobel_h, cmap='RdBu')
    axes[1].set_title("Feature Map 1\n(Horizontal Edges)")
    axes[1].axis('off')

    axes[2].imshow(sobel_v, cmap='RdBu')
    axes[2].set_title("Feature Map 2\n(Vertical Edges)")
    axes[2].axis('off')

    axes[3].imshow(laplacian, cmap='RdBu')
    axes[3].set_title("Feature Map 3\n(All Edges)")
    axes[3].axis('off')

    plt.tight_layout()
    plt.savefig(output_dir / "feature_maps_example.png", dpi=150, bbox_inches='tight')
    plt.close()

    print("Generated feature map examples")

def generate_cifar_like_samples(output_dir):
    """Generate sample images similar to CIFAR-10 categories."""
    # Create simple synthetic 32x32 images representing different 'classes'
    np.random.seed(42)

    classes = ['airplane', 'car', 'bird', 'cat', 'dog']
    samples = []

    for i, cls in enumerate(classes):
        # Create a simple shape for each class
        img = np.random.rand(32, 32, 3) * 0.2 + 0.1

        if cls == 'airplane':
            img[12:20, 5:27, :] = [0.7, 0.7, 0.8]  # body
            img[14:18, 10:22, :] = [0.6, 0.6, 0.7]  # wings
        elif cls == 'car':
            img[18:26, 8:24, :] = [0.8, 0.2, 0.2]  # body
            img[22:26, 10:14, :] = [0.1, 0.1, 0.1]  # wheel
            img[22:26, 18:22, :] = [0.1, 0.1, 0.1]  # wheel
        elif cls == 'bird':
            img[10:22, 12:20, :] = [0.9, 0.8, 0.3]  # body
            img[8:12, 14:18, :] = [0.8, 0.7, 0.2]  # head
        elif cls == 'cat':
            img[10:24, 10:22, :] = [0.6, 0.4, 0.2]  # body
            img[6:12, 12:20, :] = [0.6, 0.4, 0.2]  # head
            img[6:9, 11:14, :] = [0.7, 0.5, 0.3]  # ear
            img[6:9, 18:21, :] = [0.7, 0.5, 0.3]  # ear
        elif cls == 'dog':
            img[12:26, 8:24, :] = [0.5, 0.35, 0.2]  # body
            img[8:16, 18:26, :] = [0.5, 0.35, 0.2]  # head

        samples.append((img, cls))
        plt.imsave(output_dir / f"sample_{cls}.png", np.clip(img, 0, 1))

    # Create comparison grid
    fig, axes = plt.subplots(1, 5, figsize=(15, 3))
    for ax, (img, cls) in zip(axes, samples):
        ax.imshow(np.clip(img, 0, 1))
        ax.set_title(cls.capitalize())
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(output_dir / "classification_samples.png", dpi=150, bbox_inches='tight')
    plt.close()

    print("Generated CIFAR-like samples")

def generate_cnn_architecture_diagram(output_dir):
    """Generate a text file describing CNN architecture for analysis."""
    architecture = """
# CNN Architecture for Analysis

## Model: SimpleCNN for CIFAR-10

### Layer Structure:
```
Input: (32, 32, 3)
    ↓
Conv2D(32, kernel=3x3, padding='same') + ReLU
    → Output: (32, 32, 32)
    ↓
MaxPool2D(pool_size=2x2)
    → Output: (16, 16, 32)
    ↓
Conv2D(64, kernel=3x3, padding='same') + ReLU
    → Output: (16, 16, 64)
    ↓
MaxPool2D(pool_size=2x2)
    → Output: (8, 8, 64)
    ↓
Conv2D(128, kernel=3x3, padding='same') + ReLU
    → Output: (8, 8, 128)
    ↓
MaxPool2D(pool_size=2x2)
    → Output: (4, 4, 128)
    ↓
Flatten
    → Output: (2048,)
    ↓
Dense(256) + ReLU + Dropout(0.5)
    → Output: (256,)
    ↓
Dense(10) + Softmax
    → Output: (10,)
```

### Questions for Analysis:
1. Calculate the total number of trainable parameters
2. What is the receptive field after each conv layer?
3. Why do we increase filters (32→64→128) as we go deeper?
4. What would happen if we removed all pooling layers?
5. How does dropout help prevent overfitting?
"""

    with open(output_dir / "cnn_architecture.md", 'w') as f:
        f.write(architecture)

    print("Generated CNN architecture description")

def main():
    output_dir = ensure_output_dir()
    generate_convolution_examples(output_dir)
    generate_feature_map_example(output_dir)
    generate_cifar_like_samples(output_dir)
    generate_cnn_architecture_diagram(output_dir)
    print("✅ Part 1 CNN materials generated successfully!")

if __name__ == "__main__":
    main()
