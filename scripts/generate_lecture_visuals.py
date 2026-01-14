#!/usr/bin/env python3
"""
Generate professional visualizations for Module 0: Intro to ML
Run this script to generate static images for the lecture slides.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')

# Color palette matching UP Cebu design system
COLORS = {
    'up_green': '#1A6B5C',
    'up_green_dark': '#145549',
    'up_green_light': '#E8F5F2',
    'up_maroon': '#8C2448',
    'up_maroon_light': '#F8E8ED',
    'up_gold': '#D4A017',
    'up_gold_light': '#FDF6E3',
    'text_primary': '#1F2937',
    'text_muted': '#6B7280',
    'bg_light': '#F8FAFB',
}

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'lectures')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_fig(fig, name):
    """Save figure as PNG and SVG"""
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(f'{path}.png', dpi=150, bbox_inches='tight', transparent=True)
    fig.savefig(f'{path}.svg', bbox_inches='tight', transparent=True)
    print(f"Saved: {path}.png and {path}.svg")
    plt.close(fig)


def generate_bias_variance_tradeoff():
    """Generate the classic bias-variance tradeoff graph"""
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.linspace(0, 10, 100)

    # Bias decreases with complexity
    bias = 5 * np.exp(-0.3 * x) + 0.5

    # Variance increases with complexity
    variance = 0.3 * np.exp(0.35 * x) - 0.2
    variance = np.clip(variance, 0, 10)

    # Total error is sum (with some noise for realism)
    total_error = bias + variance + 0.8

    # Find optimal point
    optimal_idx = np.argmin(total_error)
    optimal_x = x[optimal_idx]
    optimal_y = total_error[optimal_idx]

    # Plot curves
    ax.plot(x, bias, color=COLORS['up_green'], linewidth=3, label='Bias²')
    ax.plot(x, variance, color=COLORS['up_maroon'], linewidth=3, label='Variance')
    ax.plot(x, total_error, color=COLORS['up_gold'], linewidth=4, label='Total Error')

    # Mark optimal point
    ax.scatter([optimal_x], [optimal_y], color=COLORS['up_gold'], s=150, zorder=5, edgecolor='white', linewidth=2)
    ax.axvline(x=optimal_x, color=COLORS['text_muted'], linestyle='--', alpha=0.5)
    ax.annotate('Optimal\nComplexity', xy=(optimal_x, optimal_y), xytext=(optimal_x + 1, optimal_y + 1),
                fontsize=10, ha='left', fontweight='bold')

    # Add regions
    ax.axvspan(0, 3, alpha=0.1, color=COLORS['up_maroon'], label='_')
    ax.axvspan(7, 10, alpha=0.1, color=COLORS['up_green'], label='_')

    ax.text(1.5, 0.5, 'Underfitting\n(High Bias)', fontsize=10, ha='center', color=COLORS['up_maroon'])
    ax.text(8.5, 0.5, 'Overfitting\n(High Variance)', fontsize=10, ha='center', color=COLORS['up_green'])

    ax.set_xlabel('Model Complexity →', fontsize=12, fontweight='bold')
    ax.set_ylabel('Error', fontsize=12, fontweight='bold')
    ax.set_title('Bias-Variance Tradeoff', fontsize=16, fontweight='bold', color=COLORS['text_primary'])
    ax.legend(loc='upper right', fontsize=11)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_xticks([])
    ax.set_yticks([])

    save_fig(fig, 'bias_variance_tradeoff')


def generate_overfitting_comparison():
    """Generate underfitting, good fit, overfitting comparison"""
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    # Generate true data
    np.random.seed(42)
    x = np.linspace(0, 10, 15)
    y_true = 2 * np.sin(x * 0.8) + 3
    y = y_true + np.random.normal(0, 0.4, len(x))

    x_smooth = np.linspace(0, 10, 100)
    y_smooth_true = 2 * np.sin(x_smooth * 0.8) + 3

    titles = ['Underfitting\n(High Bias)', 'Good Fit', 'Overfitting\n(High Variance)']
    colors = [COLORS['up_maroon'], COLORS['up_green'], COLORS['up_maroon']]

    for idx, (ax, title, color) in enumerate(zip(axes, titles, colors)):
        ax.scatter(x, y, color=COLORS['up_green'], s=80, zorder=5, edgecolor='white', linewidth=1.5)

        if idx == 0:  # Underfitting - linear
            coeffs = np.polyfit(x, y, 1)
            y_pred = np.polyval(coeffs, x_smooth)
            ax.plot(x_smooth, y_pred, color=color, linewidth=3)
        elif idx == 1:  # Good fit
            ax.plot(x_smooth, y_smooth_true, color=color, linewidth=3)
        else:  # Overfitting
            from scipy.interpolate import make_interp_spline
            # High degree polynomial
            coeffs = np.polyfit(x, y, 12)
            y_pred = np.polyval(coeffs, x_smooth)
            y_pred = np.clip(y_pred, -2, 10)
            ax.plot(x_smooth, y_pred, color=color, linewidth=3)

        ax.set_title(title, fontsize=13, fontweight='bold', color=color)
        ax.set_xlim(-0.5, 10.5)
        ax.set_ylim(-1, 7)
        ax.set_xticks([])
        ax.set_yticks([])

        if idx == 1:
            ax.patch.set_facecolor(COLORS['up_green_light'])
            ax.patch.set_alpha(0.3)

    fig.suptitle('Model Complexity Comparison', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    save_fig(fig, 'overfitting_comparison')


def generate_supervised_learning_visual():
    """Generate regression vs classification visual"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Regression
    np.random.seed(42)
    x_reg = np.linspace(0, 10, 30)
    y_reg = 0.8 * x_reg + 2 + np.random.normal(0, 0.8, len(x_reg))

    axes[0].scatter(x_reg, y_reg, color=COLORS['up_green'], s=60, alpha=0.8, edgecolor='white')

    # Fit line
    coeffs = np.polyfit(x_reg, y_reg, 1)
    axes[0].plot(x_reg, np.polyval(coeffs, x_reg), color=COLORS['up_gold'], linewidth=3,
                 linestyle='--', label='Prediction line')

    axes[0].set_title('Regression\nPredict Continuous Values', fontsize=13, fontweight='bold',
                      color=COLORS['up_green'])
    axes[0].set_xlabel('Feature (e.g., House Size)', fontsize=10)
    axes[0].set_ylabel('Target (e.g., Price)', fontsize=10)
    axes[0].legend()

    # Classification
    np.random.seed(42)
    x1 = np.random.normal(3, 1, 20)
    y1 = np.random.normal(3, 1, 20)
    x2 = np.random.normal(7, 1, 20)
    y2 = np.random.normal(7, 1, 20)

    axes[1].scatter(x1, y1, color=COLORS['up_green'], s=80, label='Class A (e.g., Not Spam)',
                    edgecolor='white', linewidth=1.5)
    axes[1].scatter(x2, y2, color=COLORS['up_maroon'], s=80, label='Class B (e.g., Spam)',
                    edgecolor='white', linewidth=1.5)

    # Decision boundary
    axes[1].plot([0, 10], [10, 0], color=COLORS['up_gold'], linewidth=3, linestyle='--',
                 label='Decision boundary')

    axes[1].set_title('Classification\nPredict Categories', fontsize=13, fontweight='bold',
                      color=COLORS['up_maroon'])
    axes[1].set_xlabel('Feature 1', fontsize=10)
    axes[1].set_ylabel('Feature 2', fontsize=10)
    axes[1].legend(loc='upper left')
    axes[1].set_xlim(0, 10)
    axes[1].set_ylim(0, 10)

    plt.tight_layout()
    save_fig(fig, 'supervised_learning')


def generate_clustering_visual():
    """Generate clustering visualization"""
    fig, ax = plt.subplots(figsize=(8, 6))

    np.random.seed(42)

    # Generate 3 clusters
    clusters = [
        (np.random.normal(2, 0.5, 20), np.random.normal(2, 0.5, 20), COLORS['up_green'], 'Cluster 1'),
        (np.random.normal(7, 0.6, 20), np.random.normal(3, 0.6, 20), COLORS['up_maroon'], 'Cluster 2'),
        (np.random.normal(5, 0.5, 20), np.random.normal(7, 0.5, 20), COLORS['up_gold'], 'Cluster 3'),
    ]

    for x, y, color, label in clusters:
        ax.scatter(x, y, color=color, s=80, alpha=0.8, label=label, edgecolor='white', linewidth=1.5)

        # Draw ellipse around cluster
        from matplotlib.patches import Ellipse
        ellipse = Ellipse(xy=(np.mean(x), np.mean(y)),
                          width=2.5*np.std(x), height=2.5*np.std(y),
                          edgecolor=color, facecolor='none', linewidth=2, linestyle='--')
        ax.add_patch(ellipse)

    ax.set_title('Clustering: Group Similar Data Points', fontsize=14, fontweight='bold')
    ax.set_xlabel('Feature 1', fontsize=11)
    ax.set_ylabel('Feature 2', fontsize=11)
    ax.legend(loc='upper right')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    save_fig(fig, 'clustering')


def generate_confusion_matrix():
    """Generate confusion matrix visualization"""
    fig, ax = plt.subplots(figsize=(8, 6))

    matrix = np.array([[85, 15], [10, 90]])

    im = ax.imshow(matrix, cmap='RdYlGn')

    # Add text annotations
    labels = [['True Positive\n(TP)', 'False Negative\n(FN)'],
              ['False Positive\n(FP)', 'True Negative\n(TN)']]

    for i in range(2):
        for j in range(2):
            color = 'white' if matrix[i, j] > 50 else 'black'
            ax.text(j, i, f'{labels[i][j]}\n{matrix[i, j]}',
                    ha='center', va='center', fontsize=12, color=color, fontweight='bold')

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['Predicted\nPositive', 'Predicted\nNegative'], fontsize=11)
    ax.set_yticklabels(['Actual\nPositive', 'Actual\nNegative'], fontsize=11)
    ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold')

    save_fig(fig, 'confusion_matrix')


def generate_ml_workflow():
    """Generate ML workflow diagram"""
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4)
    ax.axis('off')

    steps = [
        ('Problem\nDefinition', COLORS['up_green']),
        ('Data\nCollection', COLORS['up_green']),
        ('EDA &\nPreprocess', COLORS['up_gold']),
        ('Model\nTraining', COLORS['up_gold']),
        ('Evaluate\n& Tune', COLORS['up_maroon']),
        ('Deploy &\nMonitor', COLORS['up_maroon']),
    ]

    box_width = 1.8
    box_height = 1.2
    spacing = 2.2
    y_center = 2

    for i, (label, color) in enumerate(steps):
        x = 0.5 + i * spacing

        # Draw box
        box = FancyBboxPatch((x, y_center - box_height/2), box_width, box_height,
                              boxstyle="round,pad=0.05,rounding_size=0.2",
                              facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
        ax.add_patch(box)

        # Add text
        ax.text(x + box_width/2, y_center, label, ha='center', va='center',
                fontsize=10, color='white', fontweight='bold')

        # Draw arrow to next box
        if i < len(steps) - 1:
            ax.annotate('', xy=(x + spacing, y_center), xytext=(x + box_width + 0.1, y_center),
                       arrowprops=dict(arrowstyle='->', color=COLORS['text_muted'], lw=2))

    # Add iteration arrow
    ax.annotate('', xy=(0.8, y_center - 1), xytext=(12.5, y_center - 1),
               arrowprops=dict(arrowstyle='<-', color=COLORS['text_muted'],
                              lw=1.5, linestyle='--', connectionstyle='arc3,rad=-0.1'))
    ax.text(6.5, y_center - 1.4, 'Iterate & Improve', ha='center', fontsize=9,
            color=COLORS['text_muted'], style='italic')

    ax.set_title('Machine Learning Workflow', fontsize=14, fontweight='bold', y=0.95)

    save_fig(fig, 'ml_workflow')


def generate_historical_timeline():
    """Generate historical timeline"""
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.set_xlim(1950, 2030)
    ax.set_ylim(-1, 3)
    ax.axis('off')

    # Timeline base
    ax.axhline(y=1, color=COLORS['up_green'], linewidth=4, alpha=0.8)

    events = [
        (1956, 'AI coined\nat Dartmouth', COLORS['up_green'], 'above'),
        (1974, 'First\nAI Winter', COLORS['up_maroon'], 'below'),
        (1997, 'Deep Blue\nbeats Kasparov', COLORS['up_green'], 'above'),
        (2012, 'AlexNet\nDeep Learning', COLORS['up_gold'], 'below'),
        (2017, 'Transformers', COLORS['up_gold'], 'above'),
        (2022, 'ChatGPT\nStable Diffusion', COLORS['up_gold'], 'below'),
        (2024, 'GPT-4\nClaude', COLORS['up_maroon'], 'above'),
    ]

    for year, label, color, pos in events:
        # Dot
        ax.scatter([year], [1], s=150, color=color, zorder=5, edgecolor='white', linewidth=2)

        # Label
        y_offset = 1.7 if pos == 'above' else 0.3
        va = 'bottom' if pos == 'above' else 'top'
        ax.text(year, y_offset, f'{year}\n{label}', ha='center', va=va, fontsize=9,
                color=color, fontweight='bold')

        # Connector line
        line_y = [1.15, 1.5] if pos == 'above' else [0.85, 0.5]
        ax.plot([year, year], line_y, color=color, linewidth=1.5, alpha=0.5)

    ax.set_title('Evolution of AI & Machine Learning', fontsize=14, fontweight='bold', y=0.95)

    save_fig(fig, 'historical_timeline')


if __name__ == '__main__':
    print("Generating lecture visualizations...")
    print(f"Output directory: {OUTPUT_DIR}")
    print("-" * 50)

    generate_bias_variance_tradeoff()
    generate_overfitting_comparison()
    generate_supervised_learning_visual()
    generate_clustering_visual()
    generate_confusion_matrix()
    generate_ml_workflow()
    generate_historical_timeline()

    print("-" * 50)
    print("Done! All visualizations generated.")
