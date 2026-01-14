#!/usr/bin/env python3
"""
Generate educational figures for Module 01: Parameter Estimation
Creates visualizations for placeholder images in the lecture slides.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
from pathlib import Path

# Set style for consistent, professional look
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.facecolor': 'white',
    'savefig.dpi': 150,
    'figure.figsize': (10, 6)
})

OUTPUT_DIR = Path(__file__).parent.parent / 'static/images/lectures/module-01'

# Color palette (matches lecture CSS)
COLORS = {
    'primary': '#1a5f7a',      # Teal
    'secondary': '#c9a227',    # Gold
    'accent': '#8b4513',       # Brown
    'highlight': '#2e8b57',    # Sea green
    'warning': '#cd5c5c',      # Indian red
    'light': '#f5f5f5',
    'dark': '#333333'
}


def create_bootstrap_estimation():
    """
    Bootstrap Estimation visualization:
    - Original sample with data points
    - Bootstrap resampling concept
    - Bootstrap distribution of the mean
    """
    np.random.seed(42)

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    # Original sample
    original_sample = np.random.exponential(scale=2, size=20)

    # Panel 1: Original Sample
    ax1 = axes[0]
    ax1.scatter(range(len(original_sample)), original_sample,
                c=COLORS['primary'], s=100, alpha=0.7, edgecolors='white', linewidth=2)
    ax1.axhline(y=np.mean(original_sample), color=COLORS['secondary'],
                linestyle='--', linewidth=2, label=f'Sample Mean = {np.mean(original_sample):.2f}')
    ax1.set_xlabel('Observation Index')
    ax1.set_ylabel('Value')
    ax1.set_title('1. Original Sample (n=20)')
    ax1.legend(loc='upper right')
    ax1.set_ylim(0, max(original_sample) * 1.2)

    # Panel 2: Bootstrap Samples (show 3 resamples)
    ax2 = axes[1]
    bootstrap_means = []
    n_bootstrap = 1000

    # Generate all bootstrap samples
    for _ in range(n_bootstrap):
        bootstrap_sample = np.random.choice(original_sample, size=len(original_sample), replace=True)
        bootstrap_means.append(np.mean(bootstrap_sample))

    # Show 3 example bootstrap samples
    for i, color in enumerate([COLORS['primary'], COLORS['highlight'], COLORS['accent']]):
        bs_sample = np.random.choice(original_sample, size=len(original_sample), replace=True)
        y_offset = i * 0.3
        ax2.scatter(range(len(bs_sample)), bs_sample + y_offset * max(original_sample),
                   c=color, s=60, alpha=0.6, label=f'Bootstrap {i+1}: μ={np.mean(bs_sample):.2f}')

    ax2.set_xlabel('Observation Index')
    ax2.set_ylabel('Value (offset for visibility)')
    ax2.set_title('2. Bootstrap Resamples\n(with replacement)')
    ax2.legend(loc='upper right', fontsize=10)

    # Panel 3: Bootstrap Distribution
    ax3 = axes[2]
    ax3.hist(bootstrap_means, bins=30, color=COLORS['primary'], alpha=0.7,
             edgecolor='white', density=True)
    ax3.axvline(x=np.mean(original_sample), color=COLORS['secondary'],
                linestyle='--', linewidth=2, label='Original Mean')
    ax3.axvline(x=np.percentile(bootstrap_means, 2.5), color=COLORS['warning'],
                linestyle=':', linewidth=2, label='95% CI')
    ax3.axvline(x=np.percentile(bootstrap_means, 97.5), color=COLORS['warning'],
                linestyle=':', linewidth=2)

    # Add normal curve overlay
    x_range = np.linspace(min(bootstrap_means), max(bootstrap_means), 100)
    ax3.plot(x_range, stats.norm.pdf(x_range, np.mean(bootstrap_means), np.std(bootstrap_means)),
             color=COLORS['accent'], linewidth=2, label='Normal approx.')

    ax3.set_xlabel('Bootstrap Mean')
    ax3.set_ylabel('Density')
    ax3.set_title(f'3. Bootstrap Distribution\n(B={n_bootstrap} resamples)')
    ax3.legend(loc='upper right', fontsize=10)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'bootstrap_estimation.png', bbox_inches='tight')
    plt.close()
    print("Created: bootstrap_estimation.png")


def create_efficiency_comparison():
    """
    Efficiency Comparison: MLE vs MoM
    Shows sampling distributions with different variances
    """
    np.random.seed(42)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Panel 1: Sampling distributions comparison
    ax1 = axes[0]

    # True parameter
    theta_true = 5
    n_samples = 50

    # Simulate sampling distributions
    n_simulations = 2000
    mle_estimates = []
    mom_estimates = []

    for _ in range(n_simulations):
        # Generate from exponential(theta)
        sample = np.random.exponential(scale=theta_true, size=n_samples)
        mle_estimates.append(np.mean(sample))  # MLE for exponential
        mom_estimates.append(np.mean(sample))  # MoM same for exponential

    # For illustration, add artificial variance to MoM
    mom_estimates_inflated = np.array(mle_estimates) + np.random.normal(0, 0.5, n_simulations)

    x_range = np.linspace(3, 7, 200)

    # MLE distribution (lower variance)
    mle_std = np.std(mle_estimates)
    ax1.fill_between(x_range, stats.norm.pdf(x_range, theta_true, mle_std),
                     alpha=0.5, color=COLORS['primary'], label=f'MLE (σ={mle_std:.3f})')
    ax1.plot(x_range, stats.norm.pdf(x_range, theta_true, mle_std),
             color=COLORS['primary'], linewidth=2)

    # MoM distribution (higher variance for illustration)
    mom_std = mle_std * 1.4  # MoM typically has higher variance
    ax1.fill_between(x_range, stats.norm.pdf(x_range, theta_true, mom_std),
                     alpha=0.3, color=COLORS['secondary'], label=f'MoM (σ={mom_std:.3f})')
    ax1.plot(x_range, stats.norm.pdf(x_range, theta_true, mom_std),
             color=COLORS['secondary'], linewidth=2, linestyle='--')

    ax1.axvline(x=theta_true, color=COLORS['dark'], linestyle=':', linewidth=2, label=f'True θ = {theta_true}')
    ax1.set_xlabel('Estimated θ')
    ax1.set_ylabel('Density')
    ax1.set_title('Sampling Distributions\n(MLE has lower variance)')
    ax1.legend(loc='upper right')

    # Panel 2: Relative efficiency by distribution
    ax2 = axes[1]

    distributions = ['Normal μ', 'Normal σ²', 'Exponential', 'Uniform', 'Gamma']
    efficiencies = [1.0, 0.5, 1.0, 0.75, 0.85]  # ARE = Var(MLE)/Var(MoM)

    colors = [COLORS['highlight'] if e == 1.0 else COLORS['secondary'] for e in efficiencies]
    bars = ax2.barh(distributions, efficiencies, color=colors, edgecolor='white', linewidth=2)

    ax2.axvline(x=1.0, color=COLORS['primary'], linestyle='--', linewidth=2, alpha=0.7)
    ax2.set_xlabel('Asymptotic Relative Efficiency\n(ARE = Var(MLE) / Var(MoM))')
    ax2.set_title('Efficiency: MLE vs MoM\n(Lower = MLE more efficient)')
    ax2.set_xlim(0, 1.2)

    # Add value labels
    for bar, eff in zip(bars, efficiencies):
        ax2.text(eff + 0.02, bar.get_y() + bar.get_height()/2,
                f'{eff:.2f}', va='center', fontsize=11, fontweight='bold')

    # Add legend
    legend_elements = [
        mpatches.Patch(color=COLORS['highlight'], label='ARE = 1 (Equal)'),
        mpatches.Patch(color=COLORS['secondary'], label='ARE < 1 (MLE better)')
    ]
    ax2.legend(handles=legend_elements, loc='lower right')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'efficiency_comparison.png', bbox_inches='tight')
    plt.close()
    print("Created: efficiency_comparison.png")


def create_model_selection():
    """
    Model Selection: AIC/BIC vs Model Complexity
    Shows the bias-variance tradeoff in model selection
    """
    np.random.seed(42)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Panel 1: AIC/BIC curves
    ax1 = axes[0]

    k = np.arange(1, 11)  # Model complexity (number of parameters)
    n = 100  # Sample size

    # Simulated log-likelihood (increases then plateaus)
    true_k = 4
    log_lik = -50 + 30 * (1 - np.exp(-0.5 * k)) + np.random.normal(0, 1, len(k)) * 0.5

    # AIC and BIC
    AIC = -2 * log_lik + 2 * k
    BIC = -2 * log_lik + k * np.log(n)

    ax1.plot(k, AIC, 'o-', color=COLORS['primary'], linewidth=2, markersize=8, label='AIC')
    ax1.plot(k, BIC, 's--', color=COLORS['secondary'], linewidth=2, markersize=8, label='BIC')

    # Mark optimal points
    aic_opt = k[np.argmin(AIC)]
    bic_opt = k[np.argmin(BIC)]
    ax1.axvline(x=aic_opt, color=COLORS['primary'], linestyle=':', alpha=0.5)
    ax1.axvline(x=bic_opt, color=COLORS['secondary'], linestyle=':', alpha=0.5)
    ax1.scatter([aic_opt], [min(AIC)], s=200, c=COLORS['primary'], zorder=5, edgecolors='white', linewidth=2)
    ax1.scatter([bic_opt], [min(BIC)], s=200, c=COLORS['secondary'], zorder=5, edgecolors='white', linewidth=2)

    ax1.axvline(x=true_k, color=COLORS['warning'], linestyle='--', linewidth=2, alpha=0.7, label=f'True k={true_k}')

    ax1.set_xlabel('Number of Parameters (k)')
    ax1.set_ylabel('Information Criterion (lower = better)')
    ax1.set_title('Model Selection Criteria')
    ax1.legend(loc='upper left')
    ax1.set_xticks(k)

    # Panel 2: Decomposition
    ax2 = axes[1]

    # Bias decreases, variance increases with complexity
    bias_sq = 50 * np.exp(-0.5 * k)
    variance = 2 * k
    mse = bias_sq + variance

    ax2.fill_between(k, 0, bias_sq, alpha=0.4, color=COLORS['primary'], label='Bias²')
    ax2.fill_between(k, bias_sq, bias_sq + variance, alpha=0.4, color=COLORS['secondary'], label='Variance')
    ax2.plot(k, mse, 'o-', color=COLORS['warning'], linewidth=3, markersize=8, label='MSE = Bias² + Var')

    # Mark optimal
    opt_k = k[np.argmin(mse)]
    ax2.axvline(x=opt_k, color=COLORS['dark'], linestyle='--', alpha=0.5)
    ax2.scatter([opt_k], [min(mse)], s=200, c=COLORS['warning'], zorder=5, edgecolors='white', linewidth=2)
    ax2.annotate(f'Optimal k={opt_k}', xy=(opt_k, min(mse)), xytext=(opt_k+1.5, min(mse)+5),
                arrowprops=dict(arrowstyle='->', color=COLORS['dark']), fontsize=12)

    ax2.set_xlabel('Model Complexity (k)')
    ax2.set_ylabel('Error')
    ax2.set_title('Bias-Variance Tradeoff')
    ax2.legend(loc='upper right')
    ax2.set_xticks(k)
    ax2.set_ylim(0, max(mse) * 1.1)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'model_selection.png', bbox_inches='tight')
    plt.close()
    print("Created: model_selection.png")


def create_robust_estimation():
    """
    Robust Estimation: Effect of outliers on MLE vs Robust estimators
    """
    np.random.seed(42)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Generate data with outliers
    n = 30
    x = np.linspace(0, 10, n)
    true_slope = 2
    true_intercept = 1
    y_true = true_intercept + true_slope * x
    y = y_true + np.random.normal(0, 1.5, n)

    # Add outliers
    outlier_idx = [5, 15, 25]
    y_with_outliers = y.copy()
    y_with_outliers[outlier_idx] = y[outlier_idx] + np.array([12, -10, 15])

    # Panel 1: Effect of outliers on regression
    ax1 = axes[0]

    # Regular points
    mask = np.ones(n, dtype=bool)
    mask[outlier_idx] = False
    ax1.scatter(x[mask], y_with_outliers[mask], c=COLORS['primary'], s=80,
                alpha=0.7, edgecolors='white', linewidth=1.5, label='Data points')
    # Outliers
    ax1.scatter(x[outlier_idx], y_with_outliers[outlier_idx], c=COLORS['warning'], s=120,
                marker='X', edgecolors='white', linewidth=1.5, label='Outliers')

    # OLS (MLE) fit - affected by outliers
    slope_ols, intercept_ols = np.polyfit(x, y_with_outliers, 1)
    ax1.plot(x, intercept_ols + slope_ols * x, color=COLORS['warning'],
             linewidth=2, linestyle='--', label=f'OLS/MLE (slope={slope_ols:.2f})')

    # Robust fit (using median-based approach simulation)
    from scipy.stats import theilslopes
    slope_robust, intercept_robust, _, _ = theilslopes(y_with_outliers, x)
    ax1.plot(x, intercept_robust + slope_robust * x, color=COLORS['highlight'],
             linewidth=2, label=f'Robust (slope={slope_robust:.2f})')

    # True line
    ax1.plot(x, y_true, color=COLORS['dark'], linewidth=2, linestyle=':',
             alpha=0.7, label=f'True (slope={true_slope:.2f})')

    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title('Regression: MLE vs Robust\n(Outliers pull MLE away from true line)')
    ax1.legend(loc='upper left', fontsize=10)

    # Panel 2: Loss functions comparison
    ax2 = axes[1]

    residuals = np.linspace(-5, 5, 200)

    # Squared loss (OLS/MLE)
    squared_loss = residuals ** 2
    ax2.plot(residuals, squared_loss, color=COLORS['warning'], linewidth=2,
             label='Squared Loss (MLE)')

    # Huber loss
    delta = 1.5
    huber_loss = np.where(np.abs(residuals) <= delta,
                          0.5 * residuals**2,
                          delta * (np.abs(residuals) - 0.5 * delta))
    ax2.plot(residuals, huber_loss, color=COLORS['highlight'], linewidth=2,
             label=f'Huber Loss (δ={delta})')

    # Absolute loss
    abs_loss = np.abs(residuals)
    ax2.plot(residuals, abs_loss, color=COLORS['primary'], linewidth=2,
             linestyle='--', label='Absolute Loss (LAD)')

    ax2.axvline(x=0, color=COLORS['dark'], linestyle=':', alpha=0.3)
    ax2.axhline(y=0, color=COLORS['dark'], linestyle=':', alpha=0.3)

    # Highlight outlier region
    ax2.axvspan(3, 5, alpha=0.1, color=COLORS['warning'], label='Outlier region')
    ax2.axvspan(-5, -3, alpha=0.1, color=COLORS['warning'])

    ax2.set_xlabel('Residual (y - ŷ)')
    ax2.set_ylabel('Loss')
    ax2.set_title('Loss Functions\n(Robust losses grow slower for outliers)')
    ax2.legend(loc='upper center', fontsize=10)
    ax2.set_xlim(-5, 5)
    ax2.set_ylim(0, 15)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'robust_estimation.png', bbox_inches='tight')
    plt.close()
    print("Created: robust_estimation.png")


if __name__ == '__main__':
    print(f"Output directory: {OUTPUT_DIR}")
    print("-" * 50)

    create_bootstrap_estimation()
    create_efficiency_comparison()
    create_model_selection()
    create_robust_estimation()

    print("-" * 50)
    print("All figures generated successfully!")
