#!/usr/bin/env python3
"""
Generate statistical visualizations for CMSC 178DA Week 2.
Creates publication-quality figures for probability and statistics concepts.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 12

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Color palette matching CMSC 178DA theme
COLORS = {
    'primary': '#2563EB',      # Blue
    'secondary': '#7C3AED',    # Purple
    'accent': '#10B981',       # Green
    'warning': '#F59E0B',      # Amber
    'danger': '#EF4444',       # Red
    'dark': '#1E293B',         # Slate
}


def generate_normal_distribution():
    """Generate normal distribution with 68-95-99.7 rule visualization."""
    print("Generating normal distribution (68-95-99.7 rule)...")

    fig, ax = plt.subplots(figsize=(12, 7))

    # Generate normal distribution
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x, 0, 1)

    # Plot the main curve
    ax.plot(x, y, color=COLORS['primary'], linewidth=3, label='Normal Distribution')

    # Fill regions for 68-95-99.7 rule
    # 99.7% (3 sigma)
    x_fill = np.linspace(-3, 3, 100)
    ax.fill_between(x_fill, stats.norm.pdf(x_fill), alpha=0.15, color=COLORS['secondary'], label='99.7% (±3σ)')

    # 95% (2 sigma)
    x_fill = np.linspace(-2, 2, 100)
    ax.fill_between(x_fill, stats.norm.pdf(x_fill), alpha=0.25, color=COLORS['primary'], label='95% (±2σ)')

    # 68% (1 sigma)
    x_fill = np.linspace(-1, 1, 100)
    ax.fill_between(x_fill, stats.norm.pdf(x_fill), alpha=0.4, color=COLORS['accent'], label='68% (±1σ)')

    # Add vertical lines at sigma boundaries
    for sigma in [-3, -2, -1, 0, 1, 2, 3]:
        ax.axvline(x=sigma, color='gray', linestyle='--', alpha=0.5, linewidth=1)

    # Labels
    ax.set_xlabel('Standard Deviations from Mean (σ)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Probability Density', fontsize=14, fontweight='bold')
    ax.set_title('The 68-95-99.7 Rule (Empirical Rule)', fontsize=18, fontweight='bold', pad=20)

    # X-axis labels
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_xticklabels(['-3σ', '-2σ', '-1σ', 'μ', '+1σ', '+2σ', '+3σ'], fontsize=12)

    # Add percentage annotations
    ax.annotate('68%', xy=(0, 0.15), fontsize=16, fontweight='bold', ha='center', color=COLORS['dark'])
    ax.annotate('95%', xy=(0, 0.05), fontsize=14, fontweight='bold', ha='center', color=COLORS['primary'])
    ax.annotate('99.7%', xy=(0, 0.01), fontsize=12, fontweight='bold', ha='center', color=COLORS['secondary'])

    ax.legend(loc='upper right', fontsize=11)
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 0.45)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/normal_distribution_68_95_99.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: normal_distribution_68_95_99.png")


def generate_clt_demonstration():
    """Generate Central Limit Theorem demonstration with different sample sizes."""
    print("Generating CLT demonstration...")

    fig, axes = plt.subplots(2, 3, figsize=(14, 9))

    # Generate exponential population (clearly non-normal)
    np.random.seed(42)
    population = np.random.exponential(scale=2, size=100000)

    sample_sizes = [1, 5, 30]
    n_samples = 1000

    # Top row: Sample distributions
    for i, n in enumerate(sample_sizes):
        ax = axes[0, i]

        # Take samples and compute means
        sample_means = [np.random.choice(population, n).mean() for _ in range(n_samples)]

        # Plot histogram
        ax.hist(sample_means, bins=40, density=True, alpha=0.7, color=COLORS['primary'], edgecolor='white')

        # Overlay normal curve for comparison
        mu, std = np.mean(sample_means), np.std(sample_means)
        x = np.linspace(min(sample_means), max(sample_means), 100)
        ax.plot(x, stats.norm.pdf(x, mu, std), color=COLORS['danger'], linewidth=2, linestyle='--', label='Normal fit')

        ax.set_title(f'Sample Size n = {n}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Sample Mean', fontsize=11)
        ax.set_ylabel('Density', fontsize=11)
        if i == 2:
            ax.legend(fontsize=10)

    # Bottom left: Original population
    ax = axes[1, 0]
    ax.hist(population[:5000], bins=50, density=True, alpha=0.7, color=COLORS['secondary'], edgecolor='white')
    ax.set_title('Original Population\n(Exponential Distribution)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Value', fontsize=11)
    ax.set_ylabel('Density', fontsize=11)

    # Bottom middle: Explanation
    ax = axes[1, 1]
    ax.axis('off')
    explanation = """
    Central Limit Theorem
    ─────────────────────

    As sample size increases,
    the distribution of sample
    means approaches NORMAL,

    regardless of the original
    population distribution!

    n ≥ 30 is typically sufficient
    """
    ax.text(0.5, 0.5, explanation, transform=ax.transAxes, fontsize=14,
            verticalalignment='center', horizontalalignment='center',
            fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='#F0F9FF', edgecolor=COLORS['primary']))

    # Bottom right: Comparison of variances
    ax = axes[1, 2]
    sample_sizes_var = [5, 10, 30, 50, 100]
    variances = []
    for n in sample_sizes_var:
        means = [np.random.choice(population, n).mean() for _ in range(500)]
        variances.append(np.var(means))

    theoretical = [np.var(population) / n for n in sample_sizes_var]

    ax.plot(sample_sizes_var, variances, 'o-', color=COLORS['primary'], linewidth=2, markersize=8, label='Observed')
    ax.plot(sample_sizes_var, theoretical, 's--', color=COLORS['accent'], linewidth=2, markersize=8, label='σ²/n (Theory)')
    ax.set_title('Variance of Sample Means', fontsize=14, fontweight='bold')
    ax.set_xlabel('Sample Size (n)', fontsize=11)
    ax.set_ylabel('Variance', fontsize=11)
    ax.legend(fontsize=10)

    plt.suptitle('Central Limit Theorem Demonstration', fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/clt_demonstration.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: clt_demonstration.png")


def generate_bayes_visualization():
    """Generate Bayes theorem visualization with medical test example."""
    print("Generating Bayes theorem visualization...")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: Tree diagram / probability breakdown
    ax = axes[0]
    ax.axis('off')

    # Medical test example values
    p_disease = 0.01
    p_positive_given_disease = 0.95
    p_positive_given_no_disease = 0.10

    p_no_disease = 1 - p_disease
    p_positive = p_positive_given_disease * p_disease + p_positive_given_no_disease * p_no_disease
    p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive

    tree_text = f"""
    BAYES' THEOREM: Medical Test Example
    ════════════════════════════════════════

    Prior:     P(Disease) = {p_disease:.2f} (1%)

    Likelihood:
      P(+|Disease)    = {p_positive_given_disease:.2f} (Sensitivity)
      P(+|No Disease) = {p_positive_given_no_disease:.2f} (False Positive)

    ────────────────────────────────────────

    Evidence: P(+) = P(+|D)·P(D) + P(+|D')·P(D')
                   = {p_positive_given_disease:.2f}×{p_disease:.2f} + {p_positive_given_no_disease:.2f}×{p_no_disease:.2f}
                   = {p_positive:.4f}

    ────────────────────────────────────────

    Posterior: P(Disease|+) = P(+|Disease)·P(Disease)
                              ─────────────────────────
                                      P(+)

                            = {p_positive_given_disease:.2f} × {p_disease:.2f}
                              ─────────────
                                {p_positive:.4f}

                            = {p_disease_given_positive:.3f} ({p_disease_given_positive*100:.1f}%)
    """

    ax.text(0.05, 0.95, tree_text, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#FFFBEB', edgecolor=COLORS['warning'], linewidth=2))

    # Right: Bar chart comparison
    ax = axes[1]

    categories = ['Prior\nP(Disease)', 'Intuition\n(~90%?)', 'Actual\nP(D|+)']
    values = [p_disease * 100, 90, p_disease_given_positive * 100]
    colors = [COLORS['secondary'], COLORS['danger'], COLORS['accent']]

    bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=2)

    # Add value labels
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=14, fontweight='bold')

    ax.set_ylabel('Probability (%)', fontsize=12, fontweight='bold')
    ax.set_title('The Base Rate Fallacy', fontsize=16, fontweight='bold')
    ax.set_ylim(0, 110)

    # Add annotation
    ax.annotate('Most people guess ~90%\nbut it\'s only 8.8%!',
                xy=(1, 90), xytext=(1.5, 70),
                fontsize=11, ha='center',
                arrowprops=dict(arrowstyle='->', color=COLORS['danger']),
                bbox=dict(boxstyle='round', facecolor='#FEE2E2', edgecolor=COLORS['danger']))

    plt.suptitle("Bayes' Theorem in Action", fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/bayes_theorem_medical.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: bayes_theorem_medical.png")


def generate_hypothesis_testing_errors():
    """Generate Type I and Type II error visualization."""
    print("Generating hypothesis testing errors visualization...")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: Distribution overlap showing errors
    ax = axes[0]

    x = np.linspace(-4, 8, 1000)
    null_dist = stats.norm.pdf(x, 0, 1)
    alt_dist = stats.norm.pdf(x, 3, 1)

    # Critical value (alpha = 0.05, one-tailed)
    critical = stats.norm.ppf(0.95)

    # Plot distributions
    ax.plot(x, null_dist, color=COLORS['primary'], linewidth=3, label='H₀: Null Distribution')
    ax.plot(x, alt_dist, color=COLORS['accent'], linewidth=3, label='H₁: Alternative Distribution')

    # Fill Type I error (alpha)
    x_fill = x[x >= critical]
    ax.fill_between(x_fill, stats.norm.pdf(x_fill, 0, 1), alpha=0.4, color=COLORS['danger'], label=f'Type I Error (α)')

    # Fill Type II error (beta)
    x_fill = x[x <= critical]
    ax.fill_between(x_fill, stats.norm.pdf(x_fill, 3, 1), alpha=0.4, color=COLORS['warning'], label=f'Type II Error (β)')

    # Critical value line
    ax.axvline(x=critical, color='black', linestyle='--', linewidth=2, label=f'Critical Value')

    ax.set_xlabel('Test Statistic', fontsize=12, fontweight='bold')
    ax.set_ylabel('Probability Density', fontsize=12, fontweight='bold')
    ax.set_title('Type I and Type II Errors', fontsize=16, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.set_xlim(-4, 8)

    # Add region labels
    ax.annotate('Reject H₀', xy=(2.5, 0.02), fontsize=11, ha='center', fontweight='bold')
    ax.annotate('Fail to Reject H₀', xy=(-1, 0.02), fontsize=11, ha='center', fontweight='bold')

    # Right: Error table
    ax = axes[1]
    ax.axis('off')

    # Create table
    table_data = [
        ['', 'H₀ True', 'H₀ False'],
        ['Reject H₀', 'Type I Error\n(α = 0.05)\nFalse Positive', 'Correct!\n(Power = 1-β)\nTrue Positive'],
        ['Fail to Reject', 'Correct!\n(1-α = 0.95)\nTrue Negative', 'Type II Error\n(β)\nFalse Negative']
    ]

    colors_table = [
        ['white', '#E0E7FF', '#E0E7FF'],
        ['#E0E7FF', '#FEE2E2', '#DCFCE7'],
        ['#E0E7FF', '#DCFCE7', '#FEF3C7']
    ]

    table = ax.table(cellText=table_data, cellColours=colors_table,
                     loc='center', cellLoc='center',
                     colWidths=[0.25, 0.35, 0.35])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 2.5)

    ax.set_title('Decision Matrix', fontsize=16, fontweight='bold', pad=20)

    plt.suptitle('Understanding Hypothesis Testing Errors', fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/hypothesis_testing_errors.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: hypothesis_testing_errors.png")


def generate_confidence_interval():
    """Generate confidence interval visualization."""
    print("Generating confidence interval visualization...")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: Multiple CI simulation
    ax = axes[0]

    np.random.seed(42)
    true_mean = 100
    true_std = 15
    n_samples = 30
    n_simulations = 20

    contains_true = 0

    for i in range(n_simulations):
        sample = np.random.normal(true_mean, true_std, n_samples)
        sample_mean = np.mean(sample)
        sample_se = stats.sem(sample)
        ci = stats.t.interval(0.95, n_samples-1, sample_mean, sample_se)

        color = COLORS['accent'] if ci[0] <= true_mean <= ci[1] else COLORS['danger']
        if ci[0] <= true_mean <= ci[1]:
            contains_true += 1

        ax.plot([ci[0], ci[1]], [i, i], color=color, linewidth=2)
        ax.plot(sample_mean, i, 'o', color=color, markersize=6)

    ax.axvline(x=true_mean, color=COLORS['primary'], linestyle='--', linewidth=2, label=f'True Mean (μ={true_mean})')
    ax.set_xlabel('Value', fontsize=12, fontweight='bold')
    ax.set_ylabel('Sample Number', fontsize=12, fontweight='bold')
    ax.set_title(f'95% Confidence Intervals\n({contains_true}/{n_simulations} contain true mean)', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')

    # Right: Single CI explanation
    ax = axes[1]

    sample = np.random.normal(200, 30, 50)
    mean = np.mean(sample)
    se = stats.sem(sample)
    ci = stats.t.interval(0.95, len(sample)-1, mean, se)

    x = np.linspace(mean - 4*se, mean + 4*se, 100)
    y = stats.norm.pdf(x, mean, se)

    ax.plot(x, y, color=COLORS['primary'], linewidth=3)
    ax.fill_between(x[(x >= ci[0]) & (x <= ci[1])],
                    stats.norm.pdf(x[(x >= ci[0]) & (x <= ci[1])], mean, se),
                    alpha=0.3, color=COLORS['primary'], label='95% CI')

    ax.axvline(x=mean, color=COLORS['accent'], linestyle='-', linewidth=2, label=f'Sample Mean: {mean:.1f}')
    ax.axvline(x=ci[0], color=COLORS['secondary'], linestyle='--', linewidth=2)
    ax.axvline(x=ci[1], color=COLORS['secondary'], linestyle='--', linewidth=2)

    ax.annotate(f'Lower: {ci[0]:.1f}', xy=(ci[0], 0.001), xytext=(ci[0]-15, 0.015),
                fontsize=10, arrowprops=dict(arrowstyle='->', color=COLORS['secondary']))
    ax.annotate(f'Upper: {ci[1]:.1f}', xy=(ci[1], 0.001), xytext=(ci[1]+5, 0.015),
                fontsize=10, arrowprops=dict(arrowstyle='->', color=COLORS['secondary']))

    ax.set_xlabel('Sample Mean', fontsize=12, fontweight='bold')
    ax.set_ylabel('Probability Density', fontsize=12, fontweight='bold')
    ax.set_title('95% Confidence Interval', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')

    plt.suptitle('Understanding Confidence Intervals', fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/confidence_interval.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: confidence_interval.png")


def generate_distributions_comparison():
    """Generate comparison of common distributions."""
    print("Generating distributions comparison...")

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Binomial
    ax = axes[0, 0]
    n, p = 20, 0.3
    x = np.arange(0, n+1)
    pmf = stats.binom.pmf(x, n, p)
    ax.bar(x, pmf, color=COLORS['primary'], alpha=0.7, edgecolor='white')
    ax.set_title(f'Binomial (n={n}, p={p})', fontsize=14, fontweight='bold')
    ax.set_xlabel('Number of Successes')
    ax.set_ylabel('Probability')
    ax.annotate(f'E[X] = np = {n*p:.1f}', xy=(0.7, 0.85), xycoords='axes fraction', fontsize=11)

    # Poisson
    ax = axes[0, 1]
    lambdas = [2, 5, 10]
    x = np.arange(0, 20)
    for lam in lambdas:
        pmf = stats.poisson.pmf(x, lam)
        ax.plot(x, pmf, 'o-', label=f'λ={lam}', linewidth=2, markersize=5)
    ax.set_title('Poisson Distribution', fontsize=14, fontweight='bold')
    ax.set_xlabel('Count')
    ax.set_ylabel('Probability')
    ax.legend()

    # Normal
    ax = axes[1, 0]
    x = np.linspace(-5, 5, 100)
    params = [(0, 1), (0, 2), (2, 1)]
    for mu, sigma in params:
        ax.plot(x, stats.norm.pdf(x, mu, sigma), linewidth=2, label=f'μ={mu}, σ={sigma}')
    ax.set_title('Normal Distribution', fontsize=14, fontweight='bold')
    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    ax.legend()

    # Exponential
    ax = axes[1, 1]
    x = np.linspace(0, 5, 100)
    scales = [0.5, 1, 2]
    for scale in scales:
        ax.plot(x, stats.expon.pdf(x, scale=scale), linewidth=2, label=f'λ={1/scale:.1f}')
    ax.set_title('Exponential Distribution', fontsize=14, fontweight='bold')
    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    ax.legend()

    plt.suptitle('Common Probability Distributions', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/distributions_comparison.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: distributions_comparison.png")


def main():
    print("=" * 60)
    print("Generating Week 2 Statistical Visualizations")
    print("=" * 60)

    generate_normal_distribution()
    generate_clt_demonstration()
    generate_bayes_visualization()
    generate_hypothesis_testing_errors()
    generate_confidence_interval()
    generate_distributions_comparison()

    print("\n" + "=" * 60)
    print(f"All images saved to: {OUTPUT_DIR}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
