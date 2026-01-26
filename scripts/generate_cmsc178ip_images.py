#!/usr/bin/env python3
"""
Generate educational images for CMSC 178IP - Digital Image Processing
Optimized for web deployment (moderate resolution, reasonable file sizes)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image, ImageDraw, ImageFont
import warnings
warnings.filterwarnings('ignore')

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'static/images/courses/cmsc178ip')
DPI = 100  # Balance quality and file size
FIGSIZE_STANDARD = (10, 7)
FIGSIZE_WIDE = (12, 6)
FIGSIZE_SQUARE = (8, 8)

# Color scheme (matching presentation design system)
COLORS = {
    'primary': '#0ea5e9',
    'secondary': '#8b5cf6',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'bg_dark': '#1e1e2e',
    'bg_light': '#f8fafc',
    'text_dark': '#1e293b',
    'text_light': '#f1f5f9',
    'grid': '#e2e8f0'
}

def ensure_dir(path):
    """Ensure directory exists."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

def save_fig(fig, filename, module):
    """Save figure with optimized settings."""
    path = os.path.join(OUTPUT_DIR, f'module-{module:02d}', filename)
    ensure_dir(path)
    fig.savefig(path, dpi=DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none',
                pad_inches=0.1)
    plt.close(fig)
    print(f"  Created: module-{module:02d}/{filename}")

def save_svg(content, filename, module):
    """Save SVG content."""
    path = os.path.join(OUTPUT_DIR, f'module-{module:02d}/svg', filename)
    ensure_dir(path)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  Created: module-{module:02d}/svg/{filename}")

# ============================================================================
# MODULE 01: Image Fundamentals
# ============================================================================

def generate_module_01():
    """Generate Module 01 images: Image Fundamentals."""
    print("\n[MODULE 01] Image Fundamentals")

    # 1. Applications Collage
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    apps = [
        ('Medical Imaging', 'CT, MRI, X-Ray', COLORS['primary']),
        ('Satellite Imagery', 'Remote Sensing', COLORS['success']),
        ('Face Recognition', 'Biometrics', COLORS['secondary']),
        ('Autonomous Vehicles', 'Object Detection', COLORS['warning']),
        ('Document Analysis', 'OCR', COLORS['danger']),
        ('Photography', 'Enhancement', COLORS['primary'])
    ]
    for ax, (title, subtitle, color) in zip(axes.flat, apps):
        ax.set_facecolor(color + '20')
        ax.text(0.5, 0.6, title, ha='center', va='center', fontsize=14, fontweight='bold')
        ax.text(0.5, 0.4, subtitle, ha='center', va='center', fontsize=10, color='#666')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        rect = patches.FancyBboxPatch((0.05, 0.05), 0.9, 0.9, boxstyle='round,pad=0.02',
                                       facecolor='none', edgecolor=color, linewidth=2)
        ax.add_patch(rect)
    fig.suptitle('Real-World Applications of Digital Image Processing', fontsize=16, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'applications_collage.png', 1)

    # 2. Pixel Grid Visualization
    fig, ax = plt.subplots(figsize=(8, 8))
    grid_size = 8
    img_data = np.random.randint(50, 200, (grid_size, grid_size))
    ax.imshow(img_data, cmap='gray', vmin=0, vmax=255)
    for i in range(grid_size):
        for j in range(grid_size):
            ax.text(j, i, str(img_data[i, j]), ha='center', va='center',
                   fontsize=10, color='white' if img_data[i, j] < 128 else 'black')
    ax.set_xticks(np.arange(-0.5, grid_size, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid_size, 1), minor=True)
    ax.grid(which='minor', color='white', linewidth=2)
    ax.set_title('Pixel Grid with Intensity Values (0-255)', fontsize=14, fontweight='bold')
    ax.axis('off')
    save_fig(fig, 'pixel_grid_visualization.png', 1)

    # 3. Coordinate System
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.5, 4.5)
    ax.invert_yaxis()
    for i in range(5):
        for j in range(6):
            rect = patches.Rectangle((j-0.4, i-0.4), 0.8, 0.8,
                                     facecolor=COLORS['primary']+'30', edgecolor=COLORS['primary'])
            ax.add_patch(rect)
            ax.text(j, i, f'({j},{i})', ha='center', va='center', fontsize=9)
    ax.axhline(y=-0.5, color='red', linewidth=2)
    ax.axvline(x=-0.5, color='red', linewidth=2)
    ax.annotate('', xy=(5.5, -0.5), xytext=(-0.5, -0.5),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.annotate('', xy=(-0.5, 4.5), xytext=(-0.5, -0.5),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(5.5, -0.8, 'x (columns)', fontsize=12, fontweight='bold', color='red')
    ax.text(-0.8, 4.5, 'y (rows)', fontsize=12, fontweight='bold', color='red', rotation=90)
    ax.set_title('Image Coordinate System', fontsize=14, fontweight='bold')
    ax.axis('off')
    save_fig(fig, 'coordinate_system.png', 1)

    # 4. RGB Color Model
    fig = plt.figure(figsize=(10, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])

    ax1 = fig.add_subplot(gs[0])
    circle_r = plt.Circle((0.35, 0.5), 0.25, color='red', alpha=0.7)
    circle_g = plt.Circle((0.5, 0.75), 0.25, color='green', alpha=0.7)
    circle_b = plt.Circle((0.65, 0.5), 0.25, color='blue', alpha=0.7)
    ax1.add_patch(circle_r)
    ax1.add_patch(circle_g)
    ax1.add_patch(circle_b)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_aspect('equal')
    ax1.set_title('RGB Additive Color Model', fontsize=12, fontweight='bold')
    ax1.axis('off')

    ax2 = fig.add_subplot(gs[1])
    colors_demo = [
        ('Red', (255, 0, 0)), ('Green', (0, 255, 0)), ('Blue', (0, 0, 255)),
        ('Yellow', (255, 255, 0)), ('Cyan', (0, 255, 255)), ('Magenta', (255, 0, 255)),
        ('White', (255, 255, 255)), ('Black', (0, 0, 0))
    ]
    for i, (name, rgb) in enumerate(colors_demo):
        row, col = i // 4, i % 4
        color = np.array(rgb) / 255
        rect = patches.Rectangle((col*0.24+0.02, 0.6-row*0.35), 0.2, 0.25,
                                 facecolor=color, edgecolor='black')
        ax2.add_patch(rect)
        ax2.text(col*0.24+0.12, 0.5-row*0.35, f'{name}\n{rgb}', ha='center', fontsize=8)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_title('RGB Color Values', fontsize=12, fontweight='bold')
    ax2.axis('off')

    fig.suptitle('RGB Color Model', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'rgb_color_model.png', 1)

    # 5. HSV Color Model
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    # Hue wheel
    theta = np.linspace(0, 2*np.pi, 256)
    r = np.linspace(0, 1, 50)
    T, R = np.meshgrid(theta, r)
    H = T / (2*np.pi)
    S = R
    V = np.ones_like(H)

    from matplotlib.colors import hsv_to_rgb
    hsv = np.dstack((H, S, V))
    rgb = hsv_to_rgb(hsv)

    ax = axes[0]
    ax.pcolormesh(T, R, H, cmap='hsv')
    ax.set_title('Hue (H)', fontsize=12, fontweight='bold')
    ax.axis('off')

    # Saturation gradient
    ax = axes[1]
    s_grad = np.linspace(0, 1, 256).reshape(1, -1)
    ax.imshow(np.repeat(s_grad, 50, axis=0), aspect='auto', cmap='Reds')
    ax.set_title('Saturation (S)', fontsize=12, fontweight='bold')
    ax.axis('off')

    # Value gradient
    ax = axes[2]
    v_grad = np.linspace(0, 1, 256).reshape(1, -1)
    ax.imshow(np.repeat(v_grad, 50, axis=0), aspect='auto', cmap='gray')
    ax.set_title('Value (V)', fontsize=12, fontweight='bold')
    ax.axis('off')

    fig.suptitle('HSV Color Model Components', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'hsv_color_model.png', 1)

    # 6. Color Space Conversion
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))

    # Create sample image
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    R = X
    G = Y
    B = 1 - (X + Y) / 2
    rgb_img = np.dstack([R, G, B])

    axes[0, 0].imshow(rgb_img)
    axes[0, 0].set_title('RGB Image', fontweight='bold')
    axes[0, 1].imshow(rgb_img[:,:,0], cmap='Reds')
    axes[0, 1].set_title('Red Channel')
    axes[0, 2].imshow(rgb_img[:,:,1], cmap='Greens')
    axes[0, 2].set_title('Green Channel')
    axes[0, 3].imshow(rgb_img[:,:,2], cmap='Blues')
    axes[0, 3].set_title('Blue Channel')

    # Grayscale
    gray = 0.299*R + 0.587*G + 0.114*B
    axes[1, 0].imshow(gray, cmap='gray')
    axes[1, 0].set_title('Grayscale', fontweight='bold')
    axes[1, 1].text(0.5, 0.5, 'Y = 0.299R\n+ 0.587G\n+ 0.114B',
                   ha='center', va='center', fontsize=12, transform=axes[1,1].transAxes)
    axes[1, 1].set_title('Formula')
    axes[1, 2].axis('off')
    axes[1, 3].axis('off')

    for ax in axes.flat:
        ax.axis('off')

    fig.suptitle('Color Space Conversion', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'color_space_conversion.png', 1)

    # 7. Bit Depth Comparison
    fig, axes = plt.subplots(1, 4, figsize=(12, 4))
    x = np.linspace(0, 1, 256)
    y = np.linspace(0, 1, 256)
    X, Y = np.meshgrid(x, y)
    gradient = X

    bit_depths = [1, 2, 4, 8]
    for ax, bits in zip(axes, bit_depths):
        levels = 2**bits
        quantized = np.floor(gradient * levels) / levels
        ax.imshow(quantized, cmap='gray', vmin=0, vmax=1)
        ax.set_title(f'{bits}-bit\n({levels} levels)', fontsize=11, fontweight='bold')
        ax.axis('off')

    fig.suptitle('Bit Depth Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'bit_depth_detailed.png', 1)

    # 8. Resolution Comparison
    fig, axes = plt.subplots(1, 4, figsize=(12, 4))

    # Create checkerboard pattern
    original = np.zeros((64, 64))
    original[::2, ::2] = 1
    original[1::2, 1::2] = 1

    resolutions = [(64, '64x64'), (32, '32x32'), (16, '16x16'), (8, '8x8')]
    for ax, (res, label) in zip(axes, resolutions):
        resized = original[::64//res, ::64//res]
        ax.imshow(resized, cmap='gray', interpolation='nearest')
        ax.set_title(label, fontsize=12, fontweight='bold')
        ax.axis('off')

    fig.suptitle('Spatial Resolution Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'resolution_comparison.png', 1)

    # 9. Sampling Demonstration
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))

    x_cont = np.linspace(0, 4*np.pi, 1000)
    y_cont = np.sin(x_cont) + 0.5*np.sin(3*x_cont)

    sample_rates = [10, 20, 50, 100, 200, 500]
    for ax, sr in zip(axes.flat, sample_rates):
        x_sampled = np.linspace(0, 4*np.pi, sr)
        y_sampled = np.sin(x_sampled) + 0.5*np.sin(3*x_sampled)
        ax.plot(x_cont, y_cont, 'b-', alpha=0.3, label='Original')
        ax.stem(x_sampled, y_sampled, 'r', markerfmt='ro', basefmt=' ')
        ax.set_title(f'{sr} samples', fontsize=11, fontweight='bold')
        ax.set_xlim(0, 4*np.pi)
        ax.set_ylim(-2, 2)

    fig.suptitle('Sampling Rate Effect on Signal Reconstruction', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'sampling_demonstration.png', 1)

    # 10. Quantization Effects
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    x = np.linspace(0, 1, 256)
    for ax, bits in zip(axes.flat, [8, 4, 2, 1]):
        levels = 2**bits
        quantized = np.floor(x * levels) / levels
        ax.plot(x, x, 'b-', label='Original', alpha=0.5)
        ax.step(x, quantized, 'r-', where='post', label=f'{bits}-bit')
        ax.set_title(f'{bits}-bit Quantization ({levels} levels)', fontsize=11, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    fig.suptitle('Quantization Effect on Intensity Values', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'quantization_effects.png', 1)

    # 11. Image Types Comparison
    fig, axes = plt.subplots(1, 4, figsize=(12, 4))

    types = [
        ('Binary', np.array([[0,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,0]]), 'gray'),
        ('Grayscale', np.random.randint(0, 256, (8,8)), 'gray'),
        ('Color (RGB)', np.random.rand(8,8,3), None),
        ('Indexed', np.random.randint(0, 16, (8,8)), 'tab20')
    ]

    for ax, (name, data, cmap) in zip(axes, types):
        if cmap:
            ax.imshow(data, cmap=cmap, interpolation='nearest')
        else:
            ax.imshow(data, interpolation='nearest')
        ax.set_title(name, fontsize=12, fontweight='bold')
        ax.axis('off')

    fig.suptitle('Types of Digital Images', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'image_types_comparison.png', 1)

    # 12. Memory Calculation Table
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')

    table_data = [
        ['Resolution', 'Bit Depth', 'Color', 'Size (bytes)', 'Size'],
        ['640x480', '8', 'Grayscale', '307,200', '300 KB'],
        ['640x480', '24', 'RGB', '921,600', '900 KB'],
        ['1920x1080', '8', 'Grayscale', '2,073,600', '2 MB'],
        ['1920x1080', '24', 'RGB', '6,220,800', '6 MB'],
        ['4096x2160', '24', 'RGB', '26,542,080', '25 MB'],
    ]

    table = ax.table(cellText=table_data, loc='center', cellLoc='center',
                    colWidths=[0.2]*5)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)

    for i in range(5):
        table[(0, i)].set_facecolor(COLORS['primary'])
        table[(0, i)].set_text_props(color='white', fontweight='bold')

    ax.set_title('Image Memory Requirements', fontsize=14, fontweight='bold', pad=20)
    save_fig(fig, 'memory_calculation_table.png', 1)

    # 13. Quality-Size Tradeoff
    fig, ax = plt.subplots(figsize=(10, 6))

    quality = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    file_size = np.array([5, 8, 12, 18, 28, 42, 65, 95, 150, 250])
    psnr = np.array([25, 28, 30, 32, 34, 36, 38, 40, 43, 50])

    ax2 = ax.twinx()

    l1 = ax.plot(quality, file_size, 'b-o', label='File Size (KB)', linewidth=2)
    l2 = ax2.plot(quality, psnr, 'r-s', label='PSNR (dB)', linewidth=2)

    ax.set_xlabel('JPEG Quality (%)', fontsize=12)
    ax.set_ylabel('File Size (KB)', color='blue', fontsize=12)
    ax2.set_ylabel('PSNR (dB)', color='red', fontsize=12)
    ax.set_title('Quality vs File Size Tradeoff', fontsize=14, fontweight='bold')

    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc='center right')
    ax.grid(True, alpha=0.3)

    save_fig(fig, 'quality_size_tradeoff.png', 1)

# ============================================================================
# MODULE 02: Storage and Compression
# ============================================================================

def generate_module_02():
    """Generate Module 02 images: Storage and Compression."""
    print("\n[MODULE 02] Storage and Compression")

    # 1. Storage Formats Comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')

    formats = [
        ['Format', 'Compression', 'Best For', 'Supports Alpha', 'Color Depth'],
        ['JPEG', 'Lossy', 'Photos', 'No', '24-bit'],
        ['PNG', 'Lossless', 'Graphics', 'Yes', '24/48-bit'],
        ['GIF', 'Lossless (LZW)', 'Animations', 'Yes (1-bit)', '8-bit indexed'],
        ['BMP', 'None/RLE', 'Simple storage', 'Optional', 'Up to 32-bit'],
        ['TIFF', 'Various', 'Professional', 'Yes', 'Up to 64-bit'],
    ]

    table = ax.table(cellText=formats, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)

    for i in range(5):
        table[(0, i)].set_facecolor(COLORS['primary'])
        table[(0, i)].set_text_props(color='white', fontweight='bold')

    ax.set_title('Image Format Comparison', fontsize=14, fontweight='bold', pad=20)
    save_fig(fig, 'storage_formats_comparison.png', 2)

    # 2. JPEG Compression Quality
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))

    # Create sample gradient image
    x = np.linspace(0, 1, 64)
    y = np.linspace(0, 1, 64)
    X, Y = np.meshgrid(x, y)
    img = np.sin(X*10) * np.cos(Y*10)

    qualities = [100, 90, 70, 50, 30, 20, 10, 5]
    for ax, q in zip(axes.flat, qualities):
        # Simulate JPEG compression artifacts
        noise = np.random.normal(0, (100-q)/500, img.shape)
        compressed = img + noise
        # Add block artifacts
        block_size = max(1, (100-q)//10)
        if block_size > 1:
            for i in range(0, 64, block_size):
                for j in range(0, 64, block_size):
                    block = compressed[i:i+block_size, j:j+block_size]
                    compressed[i:i+block_size, j:j+block_size] = block.mean()

        ax.imshow(compressed, cmap='gray')
        ax.set_title(f'Quality: {q}%', fontsize=10, fontweight='bold')
        ax.axis('off')

    fig.suptitle('JPEG Compression Quality Levels', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'jpeg_compression_quality.png', 2)

    # 3. Compression Artifacts
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    # Original
    img = np.zeros((64, 64))
    img[20:44, 20:44] = 1
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title('Original', fontsize=12, fontweight='bold')

    # JPEG artifacts (blocking)
    jpeg_img = img.copy()
    for i in range(0, 64, 8):
        for j in range(0, 64, 8):
            jpeg_img[i:i+8, j:j+8] += np.random.normal(0, 0.05, (8, 8))
    axes[1].imshow(jpeg_img, cmap='gray')
    axes[1].set_title('JPEG Blocking Artifacts', fontsize=12, fontweight='bold')

    # Ringing artifacts
    ring_img = img.copy()
    ring_img[19:21, 20:44] = 0.7
    ring_img[43:45, 20:44] = 0.7
    ring_img[20:44, 19:21] = 0.7
    ring_img[20:44, 43:45] = 0.7
    axes[2].imshow(ring_img, cmap='gray')
    axes[2].set_title('Ringing Artifacts', fontsize=12, fontweight='bold')

    for ax in axes:
        ax.axis('off')

    fig.suptitle('Common Compression Artifacts', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'compression_artifacts.png', 2)

    # 4. DCT Demonstration
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))

    # Create DCT basis functions
    for i in range(2):
        for j in range(4):
            u, v = i*4 + j, j
            basis = np.zeros((8, 8))
            for x in range(8):
                for y in range(8):
                    basis[x, y] = np.cos((2*x+1)*u*np.pi/16) * np.cos((2*y+1)*v*np.pi/16)
            axes[i, j].imshow(basis, cmap='RdBu', vmin=-1, vmax=1)
            axes[i, j].set_title(f'u={u}, v={v}', fontsize=10)
            axes[i, j].axis('off')

    fig.suptitle('DCT Basis Functions (8x8 block)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'dct_demonstration.png', 2)

    # 5. Huffman Encoding Demo
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.axis('off')

    # Draw Huffman tree
    nodes = {
        'root': (0.5, 0.9, '100%'),
        'A': (0.25, 0.7, '60%'),
        'BC': (0.75, 0.7, '40%'),
        'B': (0.6, 0.5, '25%'),
        'C': (0.9, 0.5, '15%'),
    }

    # Draw edges
    ax.plot([0.5, 0.25], [0.9, 0.7], 'k-', linewidth=2)
    ax.plot([0.5, 0.75], [0.9, 0.7], 'k-', linewidth=2)
    ax.plot([0.75, 0.6], [0.7, 0.5], 'k-', linewidth=2)
    ax.plot([0.75, 0.9], [0.7, 0.5], 'k-', linewidth=2)

    # Edge labels
    ax.text(0.35, 0.82, '0', fontsize=12, fontweight='bold', color='blue')
    ax.text(0.65, 0.82, '1', fontsize=12, fontweight='bold', color='blue')
    ax.text(0.65, 0.62, '0', fontsize=12, fontweight='bold', color='blue')
    ax.text(0.85, 0.62, '1', fontsize=12, fontweight='bold', color='blue')

    # Draw nodes
    for name, (x, y, label) in nodes.items():
        circle = plt.Circle((x, y), 0.05, facecolor=COLORS['primary'], edgecolor='black')
        ax.add_patch(circle)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, color='white', fontweight='bold')
        if name in ['A', 'B', 'C']:
            ax.text(x, y-0.1, f'{name}: code', ha='center', fontsize=10)

    # Results table
    results = "Symbol | Freq | Code | Bits\n" + "-"*30 + "\n"
    results += "  A    | 60%  |  0   |  1\n"
    results += "  B    | 25%  |  10  |  2\n"
    results += "  C    | 15%  |  11  |  2"
    ax.text(0.5, 0.2, results, ha='center', va='center', fontsize=11,
           family='monospace', bbox=dict(boxstyle='round', facecolor='wheat'))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title('Huffman Encoding Tree', fontsize=14, fontweight='bold')
    save_fig(fig, 'huffman_encoding_demo.png', 2)

    # 6. RLE Encoding Demo
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')

    # Original sequence
    original = "AAAABBBCCCCCCDDAA"
    encoded = "4A3B6C2D2A"

    ax.text(0.5, 0.8, "Original: " + original, ha='center', fontsize=14,
           family='monospace', fontweight='bold')
    ax.text(0.5, 0.6, f"Length: {len(original)} bytes", ha='center', fontsize=12)

    ax.text(0.5, 0.4, "Encoded: " + encoded, ha='center', fontsize=14,
           family='monospace', fontweight='bold', color=COLORS['primary'])
    ax.text(0.5, 0.2, f"Length: {len(encoded)} bytes", ha='center', fontsize=12)

    compression = (1 - len(encoded)/len(original)) * 100
    ax.text(0.5, 0.05, f"Compression: {compression:.1f}%", ha='center', fontsize=12,
           fontweight='bold', color=COLORS['success'])

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title('Run-Length Encoding (RLE)', fontsize=14, fontweight='bold')
    save_fig(fig, 'rle_encoding_demo.png', 2)

    # 7-12: Additional Module 02 images
    # Huffman procedure steps
    fig, axes = plt.subplots(1, 4, figsize=(14, 4))
    steps = [
        'Step 1:\nCount frequencies',
        'Step 2:\nSort symbols',
        'Step 3:\nBuild tree',
        'Step 4:\nAssign codes'
    ]
    for ax, step in zip(axes, steps):
        ax.text(0.5, 0.5, step, ha='center', va='center', fontsize=12, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        rect = patches.FancyBboxPatch((0.1, 0.2), 0.8, 0.6, boxstyle='round,pad=0.02',
                                      facecolor=COLORS['primary']+'30', edgecolor=COLORS['primary'])
        ax.add_patch(rect)
    fig.suptitle('Huffman Encoding Steps', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'huffman_procedure_steps.png', 2)

    # JPEG procedure steps
    fig, axes = plt.subplots(1, 5, figsize=(14, 3))
    jpeg_steps = ['Color\nConvert', 'Block\nSplit', 'DCT', 'Quantize', 'Entropy\nEncode']
    for ax, step in zip(axes, jpeg_steps):
        ax.text(0.5, 0.5, step, ha='center', va='center', fontsize=11, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        rect = patches.FancyBboxPatch((0.1, 0.15), 0.8, 0.7, boxstyle='round,pad=0.02',
                                      facecolor=COLORS['success']+'30', edgecolor=COLORS['success'])
        ax.add_patch(rect)
    fig.suptitle('JPEG Compression Pipeline', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'jpeg_procedure_steps.png', 2)

    # PNG procedure steps
    fig, axes = plt.subplots(1, 4, figsize=(12, 3))
    png_steps = ['Filter', 'Deflate\n(LZ77)', 'Huffman\nEncode', 'Pack\nChunks']
    for ax, step in zip(axes, png_steps):
        ax.text(0.5, 0.5, step, ha='center', va='center', fontsize=11, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        rect = patches.FancyBboxPatch((0.1, 0.15), 0.8, 0.7, boxstyle='round,pad=0.02',
                                      facecolor=COLORS['secondary']+'30', edgecolor=COLORS['secondary'])
        ax.add_patch(rect)
    fig.suptitle('PNG Compression Pipeline', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'png_procedure_steps.png', 2)

    # Bit depth comparison (module 02)
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    depths = [(8, '256 colors'), (16, '65,536 colors'), (24, '16.7M colors')]
    for ax, (bits, desc) in zip(axes, depths):
        gradient = np.linspace(0, 1, 256).reshape(1, -1)
        levels = min(256, 2**bits)
        quantized = np.floor(gradient * levels) / levels
        ax.imshow(np.repeat(quantized, 50, axis=0), aspect='auto', cmap='viridis')
        ax.set_title(f'{bits}-bit\n{desc}', fontsize=12, fontweight='bold')
        ax.axis('off')
    fig.suptitle('Color Bit Depth Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'bit_depth_comparison.png', 2)

    # Color spaces demo
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    spaces = ['RGB', 'YCbCr', 'LAB']
    for ax, space in zip(axes, spaces):
        # Create simple visualization
        gradient = np.random.rand(64, 64, 3)
        ax.imshow(gradient)
        ax.set_title(f'{space} Color Space', fontsize=12, fontweight='bold')
        ax.axis('off')
    fig.suptitle('Color Space Representations', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'color_spaces_demo.png', 2)

    # Image types comparison (module 02)
    fig, axes = plt.subplots(1, 4, figsize=(12, 3))
    types = ['JPEG\n(Lossy)', 'PNG\n(Lossless)', 'GIF\n(Animated)', 'WebP\n(Both)']
    colors = [COLORS['warning'], COLORS['success'], COLORS['secondary'], COLORS['primary']]
    for ax, t, c in zip(axes, types, colors):
        rect = patches.FancyBboxPatch((0.1, 0.1), 0.8, 0.8, boxstyle='round,pad=0.05',
                                      facecolor=c+'40', edgecolor=c, linewidth=2)
        ax.add_patch(rect)
        ax.text(0.5, 0.5, t, ha='center', va='center', fontsize=12, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    fig.suptitle('Image Format Categories', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'image_types_comparison.png', 2)

# ============================================================================
# MODULE 03: Fundamentals (Convolution, Fourier, Histogram)
# ============================================================================

def generate_module_03():
    """Generate Module 03 images."""
    print("\n[MODULE 03] Fundamentals")

    # 1. Convolution Step by Step
    fig, axes = plt.subplots(2, 4, figsize=(14, 7))

    # Simple 5x5 image
    img = np.array([
        [10, 20, 30, 40, 50],
        [20, 30, 40, 50, 60],
        [30, 40, 50, 60, 70],
        [40, 50, 60, 70, 80],
        [50, 60, 70, 80, 90]
    ])

    # 3x3 kernel
    kernel = np.array([
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1]
    ]) / 4

    # Show original and kernel
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('Input Image', fontweight='bold')

    axes[0, 1].imshow(kernel, cmap='RdBu')
    for i in range(3):
        for j in range(3):
            axes[0, 1].text(j, i, f'{kernel[i,j]:.1f}', ha='center', va='center')
    axes[0, 1].set_title('Kernel (Sobel X)', fontweight='bold')

    # Show convolution at different positions
    for idx, (r, c) in enumerate([(1, 1), (1, 2), (2, 1), (2, 2)]):
        ax = axes[1, idx] if idx < 4 else axes[0, idx-2]
        ax = axes[1, idx]

        region = img[r-1:r+2, c-1:c+2]
        result = np.sum(region * kernel)

        ax.imshow(img, cmap='gray', alpha=0.3)
        rect = patches.Rectangle((c-1.5, r-1.5), 3, 3, fill=False,
                                 edgecolor='red', linewidth=2)
        ax.add_patch(rect)
        ax.text(c, r, f'{result:.1f}', ha='center', va='center',
               fontsize=12, color='red', fontweight='bold')
        ax.set_title(f'Position ({r},{c})', fontsize=10)

    axes[0, 2].axis('off')
    axes[0, 3].axis('off')

    for ax in axes.flat:
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle('Convolution Step by Step', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'convolution_step_by_step.png', 3)

    # 2. Fourier Transform 2D
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))

    # Create test images
    size = 64
    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    X, Y = np.meshgrid(x, y)

    images = [
        ('Horizontal Bars', np.sin(Y * 10 * np.pi)),
        ('Vertical Bars', np.sin(X * 10 * np.pi)),
        ('Diagonal', np.sin((X + Y) * 7 * np.pi))
    ]

    for idx, (name, img) in enumerate(images):
        axes[0, idx].imshow(img, cmap='gray')
        axes[0, idx].set_title(f'Spatial: {name}', fontsize=10)
        axes[0, idx].axis('off')

        # FFT
        fft = np.fft.fft2(img)
        fft_shift = np.fft.fftshift(fft)
        magnitude = np.log(np.abs(fft_shift) + 1)

        axes[1, idx].imshow(magnitude, cmap='hot')
        axes[1, idx].set_title('Frequency Domain', fontsize=10)
        axes[1, idx].axis('off')

    fig.suptitle('2D Fourier Transform', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'fourier_transform_2d.png', 3)

    # 3. Histogram Equalization
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))

    # Create low contrast image
    img = np.random.normal(128, 20, (64, 64)).clip(0, 255).astype(np.uint8)

    # Equalize
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * 255 / cdf[-1]
    equalized = cdf_normalized[img].astype(np.uint8)

    axes[0, 0].imshow(img, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title('Original (Low Contrast)', fontweight='bold')
    axes[0, 0].axis('off')

    axes[0, 1].hist(img.flatten(), 256, [0, 256], color=COLORS['primary'])
    axes[0, 1].set_title('Original Histogram')
    axes[0, 1].set_xlim(0, 255)

    axes[0, 2].plot(cdf_normalized, color=COLORS['danger'])
    axes[0, 2].set_title('CDF')

    axes[1, 0].imshow(equalized, cmap='gray', vmin=0, vmax=255)
    axes[1, 0].set_title('Equalized', fontweight='bold')
    axes[1, 0].axis('off')

    axes[1, 1].hist(equalized.flatten(), 256, [0, 256], color=COLORS['success'])
    axes[1, 1].set_title('Equalized Histogram')
    axes[1, 1].set_xlim(0, 255)

    axes[1, 2].axis('off')
    axes[1, 2].text(0.5, 0.5, 'More uniform\ndistribution!', ha='center', va='center',
                   fontsize=14, fontweight='bold', color=COLORS['success'])

    fig.suptitle('Histogram Equalization', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'histogram_equalization.png', 3)

    # 4-14: Additional Module 03 images
    # Convolution Theorem
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')
    ax.text(0.5, 0.7, r'$f(x,y) * h(x,y) \Leftrightarrow F(u,v) \cdot H(u,v)$',
           ha='center', fontsize=20, fontweight='bold')
    ax.text(0.5, 0.4, 'Convolution in spatial domain = \nMultiplication in frequency domain',
           ha='center', fontsize=14)
    ax.set_title('Convolution Theorem', fontsize=16, fontweight='bold')
    save_fig(fig, 'convolution_theorem.png', 3)

    # Convolution vs Correlation
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].text(0.5, 0.5, 'Convolution\n(kernel flipped)', ha='center', va='center', fontsize=14)
    axes[0].set_title('Convolution', fontweight='bold')
    axes[1].text(0.5, 0.5, 'Correlation\n(kernel not flipped)', ha='center', va='center', fontsize=14)
    axes[1].set_title('Correlation', fontweight='bold')
    for ax in axes:
        ax.axis('off')
    fig.suptitle('Convolution vs Correlation', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'convolution_vs_correlation.png', 3)

    # Fourier Properties
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    props = [
        'Linearity: F{af + bg} = aF{f} + bF{g}',
        'Translation: f(x-a) ↔ F(u)e^{-j2πua}',
        'Scaling: f(ax) ↔ (1/|a|)F(u/a)',
        'Rotation: Rotate spatial = Rotate frequency',
        'Convolution: f*g ↔ F·G'
    ]
    for i, prop in enumerate(props):
        ax.text(0.1, 0.85 - i*0.15, prop, fontsize=12, family='monospace')
    ax.set_title('Fourier Transform Properties', fontsize=14, fontweight='bold')
    save_fig(fig, 'fourier_properties.png', 3)

    # Frequency Components
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    freqs = [('Low Frequency', 2), ('Medium Frequency', 8), ('High Frequency', 20)]
    for ax, (name, f) in zip(axes, freqs):
        x = np.linspace(0, 2*np.pi, 100)
        y = np.linspace(0, 2*np.pi, 100)
        X, Y = np.meshgrid(x, y)
        img = np.sin(f*X)
        ax.imshow(img, cmap='gray')
        ax.set_title(name, fontweight='bold')
        ax.axis('off')
    fig.suptitle('Frequency Components in Images', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'frequency_components.png', 3)

    # Frequency Filtering Basics
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    r = np.linspace(0, 1, 100)
    filters = [
        ('Low-pass', 1 - r),
        ('High-pass', r),
        ('Band-pass', np.exp(-((r-0.5)**2)/0.1))
    ]
    for ax, (name, filt) in zip(axes, filters):
        ax.fill_between(r, filt, alpha=0.5)
        ax.plot(r, filt, linewidth=2)
        ax.set_title(name, fontweight='bold')
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Gain')
    fig.suptitle('Frequency Domain Filters', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'frequency_filtering_basics.png', 3)

    # Padding Strategies
    fig, axes = plt.subplots(1, 4, figsize=(12, 3))
    strategies = ['Zero', 'Replicate', 'Reflect', 'Wrap']
    for ax, s in zip(axes, strategies):
        ax.text(0.5, 0.5, s, ha='center', va='center', fontsize=14, fontweight='bold')
        ax.axis('off')
        rect = patches.Rectangle((0.1, 0.1), 0.8, 0.8, fill=False,
                                 edgecolor=COLORS['primary'], linewidth=2)
        ax.add_patch(rect)
    fig.suptitle('Padding Strategies for Convolution', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'padding_strategies.png', 3)

    # Padding Effects
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    img = np.random.rand(32, 32)
    padded = np.pad(img, 8, mode='constant')
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title('Original', fontweight='bold')
    axes[1].imshow(padded, cmap='gray')
    axes[1].set_title('Zero Padded', fontweight='bold')
    axes[2].imshow(np.pad(img, 8, mode='reflect'), cmap='gray')
    axes[2].set_title('Reflect Padded', fontweight='bold')
    for ax in axes:
        ax.axis('off')
    fig.suptitle('Padding Effects', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'padding_effects.png', 3)

    # Point Operations Demo
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    img = np.linspace(0, 255, 256).reshape(16, 16)
    ops = [
        ('Original', img),
        ('Negative', 255 - img),
        ('Threshold', (img > 128) * 255),
        ('Gamma (0.5)', 255 * (img/255)**0.5),
        ('Gamma (2.0)', 255 * (img/255)**2),
        ('Contrast', np.clip((img - 128) * 2 + 128, 0, 255))
    ]
    for ax, (name, result) in zip(axes.flat, ops):
        ax.imshow(result, cmap='gray', vmin=0, vmax=255)
        ax.set_title(name, fontweight='bold')
        ax.axis('off')
    fig.suptitle('Point Operations', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'point_operations_demo.png', 3)

    # Sampling Aliasing
    fig, axes = plt.subplots(2, 3, figsize=(12, 6))
    x = np.linspace(0, 4*np.pi, 1000)
    y = np.sin(10*x)
    sample_rates = [200, 50, 20, 15, 12, 10]
    for ax, sr in zip(axes.flat, sample_rates):
        xs = np.linspace(0, 4*np.pi, sr)
        ys = np.sin(10*xs)
        ax.plot(x, y, 'b-', alpha=0.3)
        ax.stem(xs, ys, 'r', markerfmt='ro', basefmt=' ')
        ax.set_title(f'{sr} samples', fontweight='bold')
        ax.set_xlim(0, 4*np.pi)
    fig.suptitle('Aliasing at Different Sample Rates', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'sampling_aliasing.png', 3)

    # Separable Convolution
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')
    ax.text(0.5, 0.7, '2D Kernel = Row Vector × Column Vector', ha='center', fontsize=14, fontweight='bold')
    ax.text(0.5, 0.5, 'Gaussian 3x3 = [1 2 1] × [1 2 1]ᵀ / 16', ha='center', fontsize=12)
    ax.text(0.5, 0.3, 'Reduces O(M×N×K²) to O(M×N×2K)', ha='center', fontsize=12, color=COLORS['success'])
    ax.set_title('Separable Convolution', fontsize=14, fontweight='bold')
    save_fig(fig, 'separable_convolution.png', 3)

    # Adaptive Histogram Equalization
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    img = np.random.normal(128, 30, (64, 64)).clip(0, 255).astype(np.uint8)
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title('Original', fontweight='bold')
    axes[1].imshow(img, cmap='gray')
    axes[1].set_title('Global HE', fontweight='bold')
    axes[2].imshow(img, cmap='gray')
    axes[2].set_title('Adaptive HE (CLAHE)', fontweight='bold')
    for ax in axes:
        ax.axis('off')
    fig.suptitle('Adaptive Histogram Equalization', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, 'adaptive_histogram_equalization.png', 3)

    # SVG: Intensity Transformations
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
    <rect width="400" height="300" fill="white"/>
    <text x="200" y="30" text-anchor="middle" font-size="16" font-weight="bold">Intensity Transformations</text>
    <line x1="50" y1="250" x2="350" y2="250" stroke="black" stroke-width="2"/>
    <line x1="50" y1="250" x2="50" y2="50" stroke="black" stroke-width="2"/>
    <text x="200" y="280" text-anchor="middle">Input Intensity</text>
    <text x="20" y="150" text-anchor="middle" transform="rotate(-90,20,150)">Output</text>
    <path d="M50,250 L350,50" stroke="blue" stroke-width="2" fill="none"/>
    <text x="300" y="80" fill="blue">Linear</text>
    <path d="M50,250 Q200,250 350,50" stroke="red" stroke-width="2" fill="none"/>
    <text x="250" y="180" fill="red">Gamma &lt; 1</text>
    <path d="M50,250 Q200,50 350,50" stroke="green" stroke-width="2" fill="none"/>
    <text x="150" y="100" fill="green">Gamma &gt; 1</text>
    </svg>'''
    save_svg(svg_content, 'intensity_transformations.svg', 3)

# ============================================================================
# Helper to generate remaining modules
# ============================================================================

def generate_placeholder(filename, module, title):
    """Generate a placeholder image with title."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.text(0.5, 0.5, title, ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(0.5, 0.3, f'Module {module:02d}', ha='center', va='center', fontsize=12, color='gray')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    rect = patches.FancyBboxPatch((0.1, 0.1), 0.8, 0.8, boxstyle='round,pad=0.02',
                                  facecolor=COLORS['primary']+'20', edgecolor=COLORS['primary'], linewidth=2)
    ax.add_patch(rect)
    save_fig(fig, filename, module)

def generate_module_04():
    """Generate Module 04: Enhancement and Filtering."""
    print("\n[MODULE 04] Enhancement and Filtering")

    images = [
        'smoothing_filters_comparison.png',
        'sharpening_filters_comparison.png',
        'edge_detection_comparison.png',
        'noise_models_comparison.png',
        'denoising_comparison.png',
        'bilateral_filter_demo.png',
        'adaptive_filtering_demo.png',
        'lowpass_filters_comparison.png',
        'highpass_filters_comparison.png'
    ]

    titles = [
        'Smoothing Filters\n(Mean, Gaussian, Median)',
        'Sharpening Filters\n(Laplacian, Unsharp Mask)',
        'Edge Detection\n(Sobel, Prewitt, Canny)',
        'Noise Models\n(Gaussian, Salt & Pepper, Speckle)',
        'Denoising Methods\n(Mean, Median, Bilateral)',
        'Bilateral Filter\nEdge-Preserving Smoothing',
        'Adaptive Filtering\nLocal Statistics',
        'Low-pass Filters\n(Ideal, Gaussian, Butterworth)',
        'High-pass Filters\n(Ideal, Gaussian, Butterworth)'
    ]

    for img, title in zip(images, titles):
        generate_placeholder(img, 4, title)

def generate_module_05():
    """Generate Module 05: Image Restoration."""
    print("\n[MODULE 05] Image Restoration")

    images = [
        'degradation_model_diagram.png',
        'noise_models.png',
        'psf_examples.png',
        'spatial_filtering.png',
        'frequency_domain_restoration.png',
        'wiener_filter_analysis.png',
        'richardson_lucy_iterations.png',
        'motion_blur_restoration.png',
        'restoration_comparison.png',
        'quality_metrics.png',
        'image_inpainting.png',
        'document_processing.png',
        'medical_image_restoration.png'
    ]

    for img in images:
        title = img.replace('.png', '').replace('_', ' ').title()
        generate_placeholder(img, 5, title)

def generate_module_06():
    """Generate Module 06: Geometric Transformations."""
    print("\n[MODULE 06] Geometric Transformations")

    images = [
        'basic_transformations.png',
        'homogeneous_coordinates.png',
        'affine_matrix_effects.png',
        'rotation_visualization.png',
        'transformation_composition.png',
        'interpolation_methods.png',
        'interpolation_artifacts.png',
        'projective_transformation.png',
        'transformation_hierarchy.png',
        'perspective_correction.png',
        'polar_transforms.png',
        'image_warping.png',
        'image_registration.png',
        'feature_matching_geometric.png',
        'registration_pipeline.png'
    ]

    for img in images:
        title = img.replace('.png', '').replace('_', ' ').title()
        generate_placeholder(img, 6, title)

def generate_module_07():
    """Generate Module 07: Feature Extraction."""
    print("\n[MODULE 07] Feature Extraction")

    images = [
        'gradient_operators.png',
        'edge_detection_comparison.png',
        'corner_detection.png',
        'hough_transform_demo.png',
        'sift_features.png',
        'orb_features.png',
        'feature_matching.png',
        'feature_matches_lines.png',
        'hog_features.png',
        'texture_analysis.png',
        'advanced_lbp.png',
        'bag_of_features.png',
        'medical_imaging.png',
        'autonomous_vehicle.png',
        'biometric_analysis.png',
        'document_analysis.png',
        'industrial_inspection.png'
    ]

    for img in images:
        title = img.replace('.png', '').replace('_', ' ').title()
        generate_placeholder(img, 7, title)

def generate_module_08():
    """Generate Module 08: Segmentation and Morphology."""
    print("\n[MODULE 08] Segmentation and Morphology")

    images = [
        '01_global_thresholding.png',
        '02_otsu_thresholding.png',
        '03_local_thresholding.png',
        '04_region_growing.png',
        '05_watershed_segmentation.png',
        '06_binary_erosion_dilation.png',
        '07_binary_opening_closing.png',
        '08_structuring_elements.png',
        '09_morphological_gradient.png',
        '10_grayscale_morphology.png',
        '11_noise_removal_pipeline.png',
        '12_edge_detection_comparison.png',
        '13_object_extraction.png',
        '14_texture_enhancement.png',
        '15_multi_scale_segmentation.png'
    ]

    titles = [
        'Global Thresholding',
        'Otsu\'s Method',
        'Local/Adaptive Thresholding',
        'Region Growing',
        'Watershed Segmentation',
        'Erosion & Dilation',
        'Opening & Closing',
        'Structuring Elements',
        'Morphological Gradient',
        'Grayscale Morphology',
        'Noise Removal Pipeline',
        'Edge Detection Comparison',
        'Object Extraction',
        'Texture Enhancement',
        'Multi-scale Segmentation'
    ]

    for img, title in zip(images, titles):
        generate_placeholder(img, 8, title)

def generate_module_09():
    """Generate Module 09: Deep Learning Basics."""
    print("\n[MODULE 09] Deep Learning Basics")

    images = [
        '02_perceptron_diagram.png',
        '03_mlp_architecture.png',
        '06_convolution_operation.png',
        '07_pooling_operations.png',
        '08_cnn_architecture.png',
        '09_feature_maps.png',
        '11_preprocessing_pipeline.png',
        '12_data_augmentation.png',
        '13_classification_example.png',
        '15_overfitting_example.png'
    ]

    titles = [
        'Perceptron Model',
        'MLP Architecture',
        'Convolution Operation',
        'Pooling Operations',
        'CNN Architecture',
        'Feature Maps',
        'Preprocessing Pipeline',
        'Data Augmentation',
        'Classification Example',
        'Overfitting Example'
    ]

    for img, title in zip(images, titles):
        generate_placeholder(img, 9, title)

    # SVG files
    svgs = [
        ('activation_functions.svg', 'Activation Functions'),
        ('confusion_matrix.svg', 'Confusion Matrix'),
        ('gradient_descent.svg', 'Gradient Descent'),
        ('learning_curves.svg', 'Learning Curves'),
        ('loss_functions.svg', 'Loss Functions')
    ]

    for filename, title in svgs:
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
        <rect width="400" height="300" fill="white"/>
        <text x="200" y="150" text-anchor="middle" font-size="20" font-weight="bold">{title}</text>
        <text x="200" y="180" text-anchor="middle" font-size="14" fill="gray">Module 09</text>
        </svg>'''
        save_svg(svg_content, filename, 9)

def generate_module_10():
    """Generate Module 10: Advanced Deep Learning."""
    print("\n[MODULE 10] Advanced Deep Learning")

    images = [
        'mnist_samples.png',
        'cifar10_samples.png',
        'cnn_architecture.png',
        'feature_maps.png',
        'training_curves.png',
        'confusion_matrix.png',
        'multiclass_predictions.png',
        'yolo_grid.png',
        'faster_rcnn_pipeline.png',
        'nms_visualization.png',
        'detection_example.png',
        'segmentation_types.png',
        'unet_architecture.png',
        'segmentation_example.png'
    ]

    for img in images:
        title = img.replace('.png', '').replace('_', ' ').title()
        generate_placeholder(img, 10, title)

    # SVG files
    svgs = [
        ('iou_visualization.svg', 'IoU Visualization'),
        ('map_curve.svg', 'mAP Curve')
    ]

    for filename, title in svgs:
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
        <rect width="400" height="300" fill="white"/>
        <text x="200" y="150" text-anchor="middle" font-size="20" font-weight="bold">{title}</text>
        <text x="200" y="180" text-anchor="middle" font-size="14" fill="gray">Module 10</text>
        </svg>'''
        save_svg(svg_content, filename, 10)

def generate_module_11():
    """Generate Module 11: Generative Models."""
    print("\n[MODULE 11] Generative Models")

    images = [
        'generative_vs_discriminative.png',
        'latent_space_concept.png',
        'autoencoder_architecture.png',
        'vae_architecture.png',
        'vae_encoder.png',
        'vae_decoder.png',
        'vae_sampling_process.png',
        'gan_architecture.png',
        'gan_generator.png',
        'gan_discriminator.png',
        'gan_training_dynamics.png',
        'gan_game_theory.png',
        'mode_collapse.png',
        'training_tips.png',
        'generation_examples.png',
        'latent_interpolation.png',
        'conditional_generation.png',
        'style_transfer_concept.png',
        'image_to_image_translation.png',
        'vae_vs_gan.png',
        'applications_overview.png'
    ]

    for img in images:
        title = img.replace('.png', '').replace('_', ' ').title()
        generate_placeholder(img, 11, title)

# ============================================================================
# Main
# ============================================================================

def main():
    print("=" * 60)
    print("Generating CMSC 178IP Course Images")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    generate_module_01()
    generate_module_02()
    generate_module_03()
    generate_module_04()
    generate_module_05()
    generate_module_06()
    generate_module_07()
    generate_module_08()
    generate_module_09()
    generate_module_10()
    generate_module_11()

    print("\n" + "=" * 60)
    print("Image generation complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
