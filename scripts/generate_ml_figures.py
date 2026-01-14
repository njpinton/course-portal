#!/usr/bin/env python3
"""
Generate Machine Learning visualizations for CMSC 173 slides.
Creates matplotlib/seaborn figures for Module 0 and Module 1.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import seaborn as sns
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

OUTPUT_DIR = Path("static/images/courses/cmsc173")

def ensure_dirs():
    """Create output directories if they don't exist."""
    (OUTPUT_DIR / "module-00").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "module-01").mkdir(parents=True, exist_ok=True)


def generate_regression_example():
    """Generate a regression plot with fitted line and residuals."""
    np.random.seed(42)
    X = np.linspace(0, 10, 50)
    y = 2.5 * X + 5 + np.random.normal(0, 3, 50)

    # Fit line
    coeffs = np.polyfit(X, y, 1)
    y_pred = np.polyval(coeffs, X)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot data points
    ax.scatter(X, y, c='#3498db', s=60, alpha=0.7, label='Data points', edgecolors='white')

    # Plot regression line
    ax.plot(X, y_pred, 'r-', linewidth=2.5, label=f'Fitted line: y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}')

    # Plot residuals
    for i in range(0, len(X), 3):
        ax.plot([X[i], X[i]], [y[i], y_pred[i]], 'g--', alpha=0.5, linewidth=1)

    ax.set_xlabel('Feature (X)', fontsize=12)
    ax.set_ylabel('Target (y)', fontsize=12)
    ax.set_title('Linear Regression: Predicting Continuous Values', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "module-00" / "regression_example.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: regression_example.png")


def generate_classification_example():
    """Generate a classification plot with decision boundary."""
    np.random.seed(42)

    # Generate two clusters
    n_points = 50
    class1_x = np.random.normal(2, 0.8, n_points)
    class1_y = np.random.normal(2, 0.8, n_points)
    class2_x = np.random.normal(5, 0.8, n_points)
    class2_y = np.random.normal(5, 0.8, n_points)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot classes
    ax.scatter(class1_x, class1_y, c='#e74c3c', s=60, alpha=0.7, label='Class A (Spam)', edgecolors='white')
    ax.scatter(class2_x, class2_y, c='#2ecc71', s=60, alpha=0.7, label='Class B (Not Spam)', edgecolors='white')

    # Decision boundary
    x_boundary = np.linspace(0, 7, 100)
    y_boundary = x_boundary  # Simple diagonal boundary
    ax.plot(x_boundary, y_boundary, 'k--', linewidth=2, label='Decision Boundary')
    ax.fill_between(x_boundary, y_boundary, 7, alpha=0.1, color='green')
    ax.fill_between(x_boundary, 0, y_boundary, alpha=0.1, color='red')

    ax.set_xlabel('Feature 1', fontsize=12)
    ax.set_ylabel('Feature 2', fontsize=12)
    ax.set_title('Classification: Predicting Categories', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 7)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "module-00" / "classification_example.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: classification_example.png")


def generate_clustering_example():
    """Generate a clustering visualization with centroids."""
    np.random.seed(42)

    # Generate three clusters
    centers = [(2, 2), (6, 6), (2, 6)]
    colors = ['#e74c3c', '#3498db', '#2ecc71']

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (cx, cy) in enumerate(centers):
        x = np.random.normal(cx, 0.6, 40)
        y = np.random.normal(cy, 0.6, 40)
        ax.scatter(x, y, c=colors[i], s=50, alpha=0.6, label=f'Cluster {i+1}', edgecolors='white')
        ax.scatter(cx, cy, c=colors[i], s=200, marker='X', edgecolors='black', linewidths=2)

    ax.set_xlabel('Feature 1', fontsize=12)
    ax.set_ylabel('Feature 2', fontsize=12)
    ax.set_title('Clustering: Grouping Similar Data (K-Means)', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)

    # Add annotation
    ax.annotate('Centroids (X)', xy=(6, 6), xytext=(7, 5),
                fontsize=10, ha='center',
                arrowprops=dict(arrowstyle='->', color='black'))

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "module-00" / "clustering_example.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: clustering_example.png")


def generate_overfitting_example():
    """Generate overfitting vs good fit comparison."""
    np.random.seed(42)
    X = np.linspace(0, 10, 20)
    y_true = np.sin(X) * 2 + 5
    y = y_true + np.random.normal(0, 0.5, 20)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Underfitting (degree 1)
    coeffs1 = np.polyfit(X, y, 1)
    y_pred1 = np.polyval(coeffs1, X)
    axes[0].scatter(X, y, c='#3498db', s=60, alpha=0.7, edgecolors='white')
    axes[0].plot(X, y_pred1, 'r-', linewidth=2)
    axes[0].set_title('Underfitting\n(High Bias)', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('X')
    axes[0].set_ylabel('y')

    # Good fit (degree 3)
    X_smooth = np.linspace(0, 10, 100)
    coeffs3 = np.polyfit(X, y, 3)
    y_pred3 = np.polyval(coeffs3, X_smooth)
    axes[1].scatter(X, y, c='#3498db', s=60, alpha=0.7, edgecolors='white')
    axes[1].plot(X_smooth, y_pred3, 'g-', linewidth=2)
    axes[1].set_title('Good Fit\n(Balanced)', fontsize=12, fontweight='bold', color='green')
    axes[1].set_xlabel('X')
    axes[1].set_ylabel('y')

    # Overfitting (degree 15)
    coeffs15 = np.polyfit(X, y, 15)
    y_pred15 = np.polyval(coeffs15, X_smooth)
    axes[2].scatter(X, y, c='#3498db', s=60, alpha=0.7, edgecolors='white')
    axes[2].plot(X_smooth, y_pred15, 'r-', linewidth=2)
    axes[2].set_title('Overfitting\n(High Variance)', fontsize=12, fontweight='bold', color='red')
    axes[2].set_xlabel('X')
    axes[2].set_ylabel('y')
    axes[2].set_ylim(-5, 15)

    plt.suptitle('The Bias-Variance Tradeoff', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "module-00" / "overfitting_example.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: overfitting_example.png")


def generate_bias_variance_tradeoff():
    """Generate the classic bias-variance tradeoff curve."""
    complexity = np.linspace(0, 10, 100)

    # Simulated curves
    bias_squared = 5 * np.exp(-0.5 * complexity)
    variance = 0.1 * np.exp(0.4 * complexity)
    total_error = bias_squared + variance + 0.5  # irreducible error

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(complexity, bias_squared, 'b-', linewidth=2.5, label='Bias²')
    ax.plot(complexity, variance, 'r-', linewidth=2.5, label='Variance')
    ax.plot(complexity, total_error, 'g--', linewidth=2.5, label='Total Error')
    ax.axhline(y=0.5, color='gray', linestyle=':', label='Irreducible Error')

    # Mark optimal point
    optimal_idx = np.argmin(total_error)
    ax.axvline(x=complexity[optimal_idx], color='purple', linestyle='--', alpha=0.7)
    ax.scatter([complexity[optimal_idx]], [total_error[optimal_idx]],
               c='purple', s=100, zorder=5, label='Optimal Complexity')

    ax.set_xlabel('Model Complexity', fontsize=12)
    ax.set_ylabel('Error', fontsize=12)
    ax.set_title('Bias-Variance Tradeoff', fontsize=14, fontweight='bold')
    ax.legend(loc='upper center', fontsize=10)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)

    # Add annotations
    ax.annotate('Underfitting\n(High Bias)', xy=(1, 5), fontsize=10, ha='center')
    ax.annotate('Overfitting\n(High Variance)', xy=(9, 5), fontsize=10, ha='center')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "module-00" / "bias_variance_tradeoff.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: bias_variance_tradeoff.png")


def generate_train_test_split():
    """Generate train/test split visualization."""
    fig, ax = plt.subplots(figsize=(12, 4))

    # Create data representation
    total_samples = 100
    train_size = 80

    # Draw rectangles
    ax.barh(0, train_size, height=0.5, color='#3498db', label=f'Training Set ({train_size}%)')
    ax.barh(0, total_samples - train_size, left=train_size, height=0.5, color='#e74c3c', label=f'Test Set ({total_samples - train_size}%)')

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel('Dataset Percentage', fontsize=12)
    ax.set_title('Train-Test Split', fontsize=14, fontweight='bold')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=10)
    ax.set_yticks([])

    # Add text
    ax.text(40, 0, 'Train on this', ha='center', va='center', fontsize=11, color='white', fontweight='bold')
    ax.text(90, 0, 'Test', ha='center', va='center', fontsize=11, color='white', fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "module-00" / "train_test_split.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: train_test_split.png")


def generate_pca_visualization():
    """Generate PCA dimensionality reduction visualization."""
    np.random.seed(42)

    # Generate correlated 2D data
    n = 100
    x1 = np.random.normal(0, 1, n)
    x2 = 0.8 * x1 + np.random.normal(0, 0.3, n)

    # Compute PCA direction
    data = np.column_stack([x1, x2])
    mean = data.mean(axis=0)
    centered = data - mean
    cov = np.cov(centered.T)
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    pc1 = eigenvectors[:, 0]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Original data with PC1
    axes[0].scatter(x1, x2, c='#3498db', s=40, alpha=0.6, edgecolors='white')
    axes[0].arrow(mean[0], mean[1], pc1[0]*2, pc1[1]*2, head_width=0.1, head_length=0.1, fc='red', ec='red', linewidth=2)
    axes[0].set_xlabel('Feature 1', fontsize=12)
    axes[0].set_ylabel('Feature 2', fontsize=12)
    axes[0].set_title('Original 2D Data\n(with Principal Component)', fontsize=12, fontweight='bold')
    axes[0].set_aspect('equal')

    # Projected data (1D)
    projected = centered @ pc1
    axes[1].scatter(projected, np.zeros_like(projected), c='#e74c3c', s=40, alpha=0.6, edgecolors='white')
    axes[1].axhline(y=0, color='black', linewidth=1)
    axes[1].set_xlabel('Principal Component 1', fontsize=12)
    axes[1].set_title('Reduced to 1D\n(Preserves Maximum Variance)', fontsize=12, fontweight='bold')
    axes[1].set_ylim(-0.5, 0.5)
    axes[1].set_yticks([])

    plt.suptitle('PCA: Dimensionality Reduction', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "module-00" / "pca_visualization.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: pca_visualization.png")


def generate_ml_workflow():
    """Generate ML workflow diagram."""
    fig, ax = plt.subplots(figsize=(14, 6))

    steps = [
        ('1. Data\nCollection', '#3498db'),
        ('2. Data\nPreprocessing', '#9b59b6'),
        ('3. Feature\nEngineering', '#e67e22'),
        ('4. Model\nTraining', '#2ecc71'),
        ('5. Model\nEvaluation', '#e74c3c'),
        ('6. Deployment', '#1abc9c')
    ]

    x_positions = np.linspace(0.1, 0.9, len(steps))

    for i, (label, color) in enumerate(steps):
        # Draw box
        rect = plt.Rectangle((x_positions[i] - 0.06, 0.35), 0.12, 0.3,
                             facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x_positions[i], 0.5, label, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')

        # Draw arrow
        if i < len(steps) - 1:
            ax.annotate('', xy=(x_positions[i+1] - 0.07, 0.5),
                       xytext=(x_positions[i] + 0.07, 0.5),
                       arrowprops=dict(arrowstyle='->', color='black', lw=2))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Machine Learning Workflow', fontsize=14, fontweight='bold', y=0.85)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "module-00" / "ml_workflow_diagram.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: ml_workflow_diagram.png")


def generate_supervised_vs_unsupervised():
    """Generate supervised vs unsupervised comparison."""
    np.random.seed(42)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Supervised: labeled data
    n = 30
    class1_x = np.random.normal(2, 0.5, n)
    class1_y = np.random.normal(3, 0.5, n)
    class2_x = np.random.normal(4, 0.5, n)
    class2_y = np.random.normal(2, 0.5, n)

    axes[0].scatter(class1_x, class1_y, c='#e74c3c', s=80, label='Label: Cat', edgecolors='white', marker='o')
    axes[0].scatter(class2_x, class2_y, c='#3498db', s=80, label='Label: Dog', edgecolors='white', marker='s')
    axes[0].set_xlabel('Feature 1', fontsize=12)
    axes[0].set_ylabel('Feature 2', fontsize=12)
    axes[0].set_title('Supervised Learning\n(Data has Labels)', fontsize=12, fontweight='bold', color='#2ecc71')
    axes[0].legend(fontsize=10)

    # Unsupervised: unlabeled data
    all_x = np.concatenate([class1_x, class2_x])
    all_y = np.concatenate([class1_y, class2_y])

    axes[1].scatter(all_x, all_y, c='gray', s=80, label='Unknown', edgecolors='white')
    axes[1].set_xlabel('Feature 1', fontsize=12)
    axes[1].set_ylabel('Feature 2', fontsize=12)
    axes[1].set_title('Unsupervised Learning\n(No Labels - Find Structure)', fontsize=12, fontweight='bold', color='#9b59b6')
    axes[1].legend(fontsize=10)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "module-00" / "supervised_vs_unsupervised.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: supervised_vs_unsupervised.png")


# Module 1: Parameter Estimation figures

def generate_mle_visualization():
    """Generate MLE likelihood function visualization."""
    np.random.seed(42)

    # Simulated data from normal distribution
    true_mean = 5
    data = np.random.normal(true_mean, 1, 20)
    sample_mean = data.mean()

    # Likelihood as function of mu
    mu_range = np.linspace(3, 7, 100)

    def log_likelihood(mu, data):
        return -0.5 * len(data) * np.log(2 * np.pi) - 0.5 * np.sum((data - mu)**2)

    ll_values = [log_likelihood(mu, data) for mu in mu_range]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(mu_range, ll_values, 'b-', linewidth=2.5, label='Log-Likelihood')
    ax.axvline(x=sample_mean, color='r', linestyle='--', linewidth=2, label=f'MLE: μ = {sample_mean:.2f}')
    ax.axvline(x=true_mean, color='g', linestyle=':', linewidth=2, label=f'True μ = {true_mean}')

    ax.set_xlabel('μ (mean parameter)', fontsize=12)
    ax.set_ylabel('Log-Likelihood', fontsize=12)
    ax.set_title('Maximum Likelihood Estimation', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "module-01" / "mle_visualization.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: mle_visualization.png")


def generate_mom_visualization():
    """Generate Method of Moments visualization."""
    np.random.seed(42)

    # Generate sample data
    n = 50
    true_mu, true_sigma = 5, 2
    data = np.random.normal(true_mu, true_sigma, n)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Histogram with moments
    axes[0].hist(data, bins=15, density=True, alpha=0.7, color='#3498db', edgecolor='white')
    axes[0].axvline(x=data.mean(), color='r', linestyle='--', linewidth=2, label=f'Sample Mean = {data.mean():.2f}')
    axes[0].set_xlabel('x', fontsize=12)
    axes[0].set_ylabel('Density', fontsize=12)
    axes[0].set_title('Sample Distribution', fontsize=12, fontweight='bold')
    axes[0].legend(fontsize=10)

    # Theoretical vs sample moments
    moments = ['1st Moment\n(Mean)', '2nd Central\nMoment (Var)']
    theoretical = [true_mu, true_sigma**2]
    sample = [data.mean(), data.var()]

    x = np.arange(len(moments))
    width = 0.35

    axes[1].bar(x - width/2, theoretical, width, label='Theoretical', color='#2ecc71')
    axes[1].bar(x + width/2, sample, width, label='Sample', color='#e74c3c')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(moments)
    axes[1].set_ylabel('Value', fontsize=12)
    axes[1].set_title('Method of Moments:\nMatch Sample to Theoretical', fontsize=12, fontweight='bold')
    axes[1].legend(fontsize=10)

    plt.suptitle('Method of Moments Estimation', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "module-01" / "mom_visualization.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: mom_visualization.png")


def generate_estimator_properties():
    """Generate visualization of estimator properties: bias and variance."""
    np.random.seed(42)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    true_value = 5
    n_samples = 100

    def draw_target(ax, estimates, title, color):
        # Draw target
        circle_radii = [0.3, 0.6, 0.9, 1.2]
        for r in circle_radii:
            circle = plt.Circle((0, 0), r, fill=False, color='gray', linewidth=1)
            ax.add_patch(circle)

        # Draw true center
        ax.plot(0, 0, 'g+', markersize=20, markeredgewidth=3, label='True Value')

        # Draw estimates
        ax.scatter(estimates[:, 0], estimates[:, 1], c=color, s=30, alpha=0.7, label='Estimates')
        mean_est = estimates.mean(axis=0)
        ax.scatter(mean_est[0], mean_est[1], c='red', s=100, marker='X', edgecolors='black', label='Mean Estimate')

        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.legend(loc='upper right', fontsize=8)

    # High Bias, Low Variance
    estimates = np.random.normal([0.7, 0.7], 0.15, (n_samples, 2))
    draw_target(axes[0, 0], estimates, 'High Bias, Low Variance', '#e74c3c')

    # Low Bias, High Variance
    estimates = np.random.normal([0, 0], 0.5, (n_samples, 2))
    draw_target(axes[0, 1], estimates, 'Low Bias, High Variance', '#3498db')

    # High Bias, High Variance
    estimates = np.random.normal([0.6, 0.6], 0.4, (n_samples, 2))
    draw_target(axes[1, 0], estimates, 'High Bias, High Variance', '#9b59b6')

    # Low Bias, Low Variance (ideal)
    estimates = np.random.normal([0, 0], 0.15, (n_samples, 2))
    draw_target(axes[1, 1], estimates, 'Low Bias, Low Variance ✓', '#2ecc71')

    plt.suptitle('Estimator Properties: Bias vs Variance', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "module-01" / "estimator_bias_variance.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated: estimator_bias_variance.png")


if __name__ == "__main__":
    ensure_dirs()

    print("Generating Module 0 figures...")
    generate_regression_example()
    generate_classification_example()
    generate_clustering_example()
    generate_overfitting_example()
    generate_bias_variance_tradeoff()
    generate_train_test_split()
    generate_pca_visualization()
    generate_ml_workflow()
    generate_supervised_vs_unsupervised()

    print("\nGenerating Module 1 figures...")
    generate_mle_visualization()
    generate_mom_visualization()
    generate_estimator_properties()

    print("\nAll figures generated successfully!")
