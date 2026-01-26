#!/usr/bin/env python3
"""
Part 3: Generate materials for generative models section.
Creates visualizations for VAE and GAN understanding.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def ensure_output_dir():
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir

def generate_autoencoder_diagram(output_dir):
    """Generate autoencoder architecture visualization."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))

    # Draw encoder
    encoder_layers = [784, 256, 64, 16]
    decoder_layers = [16, 64, 256, 784]

    y_positions = np.linspace(0.9, 0.1, max(len(encoder_layers), len(decoder_layers)))

    # Encoder side
    for i, (size, y) in enumerate(zip(encoder_layers, y_positions[:len(encoder_layers)])):
        width = size / 1000
        rect = plt.Rectangle((0.1, y - 0.03), width, 0.06, color='steelblue', alpha=0.7)
        ax.add_patch(rect)
        ax.text(0.1 + width/2, y, str(size), ha='center', va='center', fontsize=10, color='white', fontweight='bold')
        if i < len(encoder_layers) - 1:
            ax.annotate('', xy=(0.1 + encoder_layers[i+1]/1000/2, y_positions[i+1]),
                       xytext=(0.1 + width, y),
                       arrowprops=dict(arrowstyle='->', color='gray'))

    # Latent space (bottleneck)
    ax.add_patch(plt.Rectangle((0.45, 0.35), 0.1, 0.3, color='red', alpha=0.7))
    ax.text(0.5, 0.5, 'Latent\nSpace\n(z)', ha='center', va='center', fontsize=10, color='white', fontweight='bold')

    # Decoder side
    for i, (size, y) in enumerate(zip(decoder_layers, y_positions[:len(decoder_layers)])):
        width = size / 1000
        x_start = 0.9 - width
        rect = plt.Rectangle((x_start, y - 0.03), width, 0.06, color='forestgreen', alpha=0.7)
        ax.add_patch(rect)
        ax.text(x_start + width/2, y, str(size), ha='center', va='center', fontsize=10, color='white', fontweight='bold')

    # Labels
    ax.text(0.05, 0.95, 'ENCODER', fontsize=12, fontweight='bold', color='steelblue')
    ax.text(0.85, 0.95, 'DECODER', fontsize=12, fontweight='bold', color='forestgreen')
    ax.text(0.05, 0.05, 'Input\n(28×28)', fontsize=10)
    ax.text(0.85, 0.05, 'Output\n(28×28)', fontsize=10)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Autoencoder Architecture', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_dir / "autoencoder_architecture.png", dpi=150, bbox_inches='tight')
    plt.close()

    print("Generated autoencoder architecture diagram")

def generate_vae_latent_space(output_dir):
    """Generate visualization of VAE latent space concept."""
    np.random.seed(42)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Regular autoencoder latent space (scattered, holes)
    n_points = 200
    ae_points = np.random.randn(n_points, 2) * 2
    # Add some clusters with gaps
    ae_points[:50] += [3, 3]
    ae_points[50:100] += [-3, -3]
    ae_points[100:150] += [3, -3]
    ae_points[150:] += [-3, 3]

    axes[0].scatter(ae_points[:, 0], ae_points[:, 1], c=np.arange(n_points), cmap='viridis', alpha=0.6)
    axes[0].set_title('Autoencoder Latent Space\n(Has "holes" - bad for sampling)')
    axes[0].set_xlabel('z₁')
    axes[0].set_ylabel('z₂')

    # VAE latent space (smooth, continuous)
    vae_points = np.random.randn(n_points, 2)
    axes[1].scatter(vae_points[:, 0], vae_points[:, 1], c=np.arange(n_points), cmap='viridis', alpha=0.6)
    # Add unit circle
    theta = np.linspace(0, 2*np.pi, 100)
    axes[1].plot(2*np.cos(theta), 2*np.sin(theta), 'r--', alpha=0.5, label='Prior N(0,1)')
    axes[1].set_title('VAE Latent Space\n(Continuous - good for sampling)')
    axes[1].set_xlabel('z₁')
    axes[1].set_ylabel('z₂')
    axes[1].legend()

    # Interpolation in latent space
    # Create a grid
    x = np.linspace(-2, 2, 8)
    y = np.linspace(-2, 2, 8)
    xx, yy = np.meshgrid(x, y)
    axes[2].scatter(xx, yy, c='steelblue', s=50, alpha=0.8)
    axes[2].set_title('Latent Space Grid Sampling\n(Each point → generated image)')
    axes[2].set_xlabel('z₁')
    axes[2].set_ylabel('z₂')

    # Draw arrows showing interpolation
    axes[2].annotate('', xy=(1.5, 1.5), xytext=(-1.5, -1.5),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2))
    axes[2].text(0, -0.5, 'Interpolation\nPath', color='red', ha='center')

    for ax in axes:
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / "latent_space_comparison.png", dpi=150, bbox_inches='tight')
    plt.close()

    print("Generated latent space comparison")

def generate_gan_training_diagram(output_dir):
    """Generate GAN training dynamics visualization."""
    np.random.seed(42)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Training curves
    epochs = np.arange(100)
    d_loss = 0.7 - 0.3 * (1 - np.exp(-epochs/30)) + 0.1 * np.random.randn(100)
    g_loss = 2.0 - 1.2 * (1 - np.exp(-epochs/40)) + 0.15 * np.random.randn(100)

    axes[0].plot(epochs, d_loss, 'b-', label='Discriminator Loss', linewidth=2)
    axes[0].plot(epochs, g_loss, 'r-', label='Generator Loss', linewidth=2)
    axes[0].axhline(y=0.69, color='gray', linestyle='--', alpha=0.5, label='Optimal D (log(2))')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('GAN Training Dynamics')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Real vs Fake distribution
    real_samples = np.random.randn(500) * 1.5 + 5
    fake_early = np.random.randn(500) * 2 + 0  # Early training
    fake_late = np.random.randn(500) * 1.6 + 4.5  # Later training

    axes[1].hist(real_samples, bins=30, alpha=0.5, label='Real Data', color='green', density=True)
    axes[1].hist(fake_early, bins=30, alpha=0.5, label='Fake (Epoch 10)', color='red', density=True)
    axes[1].hist(fake_late, bins=30, alpha=0.5, label='Fake (Epoch 90)', color='blue', density=True)
    axes[1].set_xlabel('Value')
    axes[1].set_ylabel('Density')
    axes[1].set_title('Generator Learning to Match Real Distribution')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(output_dir / "gan_training_dynamics.png", dpi=150, bbox_inches='tight')
    plt.close()

    print("Generated GAN training dynamics")

def generate_mode_collapse_example(output_dir):
    """Generate visualization of mode collapse problem."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    np.random.seed(42)

    # Real data with multiple modes
    real_data = []
    centers = [(-3, -3), (-3, 3), (3, -3), (3, 3), (0, 0)]
    for cx, cy in centers:
        cluster = np.random.randn(100, 2) * 0.5 + [cx, cy]
        real_data.append(cluster)
    real_data = np.vstack(real_data)

    axes[0].scatter(real_data[:, 0], real_data[:, 1], alpha=0.5, s=10)
    axes[0].set_title('Real Data Distribution\n(5 distinct modes)')
    axes[0].set_xlim(-6, 6)
    axes[0].set_ylim(-6, 6)

    # Mode collapse - generator only produces one mode
    collapsed = np.random.randn(500, 2) * 0.5 + [0, 0]
    axes[1].scatter(collapsed[:, 0], collapsed[:, 1], alpha=0.5, s=10, color='red')
    axes[1].set_title('Mode Collapse\n(Generator stuck on 1 mode)')
    axes[1].set_xlim(-6, 6)
    axes[1].set_ylim(-6, 6)

    # Good generator covering all modes
    good_gen = []
    for cx, cy in centers:
        cluster = np.random.randn(100, 2) * 0.6 + [cx, cy]
        good_gen.append(cluster)
    good_gen = np.vstack(good_gen)

    axes[2].scatter(good_gen[:, 0], good_gen[:, 1], alpha=0.5, s=10, color='green')
    axes[2].set_title('Good Generator\n(Covers all modes)')
    axes[2].set_xlim(-6, 6)
    axes[2].set_ylim(-6, 6)

    for ax in axes:
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / "mode_collapse_example.png", dpi=150, bbox_inches='tight')
    plt.close()

    print("Generated mode collapse example")

def generate_mnist_samples(output_dir):
    """Generate simple MNIST-like digit samples for reconstruction task."""
    np.random.seed(42)

    fig, axes = plt.subplots(2, 10, figsize=(15, 3))

    for i in range(10):
        # Create simple digit representation
        img = np.zeros((28, 28))

        # Very simplified digit shapes
        if i == 0:
            for r in range(5, 23):
                for c in range(8, 20):
                    if 6 <= r <= 22 and 9 <= c <= 19:
                        dist = min(r-6, 22-r, c-9, 19-c)
                        if dist < 3:
                            img[r, c] = 1
        elif i == 1:
            img[5:23, 13:16] = 1
        elif i == 7:
            img[5:8, 8:20] = 1
            for r in range(8, 23):
                img[r, 19 - (r-8)//2] = 1
                img[r, 20 - (r-8)//2] = 1

        # Add noise
        noisy = img + np.random.randn(28, 28) * 0.1
        noisy = np.clip(noisy, 0, 1)

        axes[0, i].imshow(img, cmap='gray')
        axes[0, i].axis('off')
        axes[0, i].set_title(f'{i}')

        axes[1, i].imshow(noisy, cmap='gray')
        axes[1, i].axis('off')

    axes[0, 0].set_ylabel('Clean', rotation=0, labelpad=30)
    axes[1, 0].set_ylabel('Noisy', rotation=0, labelpad=30)

    plt.suptitle('Sample Digit Images for Reconstruction Task', y=1.02)
    plt.tight_layout()
    plt.savefig(output_dir / "mnist_samples.png", dpi=150, bbox_inches='tight')
    plt.close()

    print("Generated MNIST-like samples")

def generate_loss_comparison(output_dir):
    """Generate VAE loss components visualization."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    epochs = np.arange(50)

    # Reconstruction loss
    recon_loss = 150 * np.exp(-epochs/15) + 20 + 5*np.random.randn(50)
    axes[0].plot(epochs, recon_loss, 'b-', linewidth=2)
    axes[0].set_title('Reconstruction Loss\n(MSE between input & output)')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].grid(True, alpha=0.3)

    # KL divergence
    kl_loss = 5 + 15 * (1 - np.exp(-epochs/20)) + 2*np.random.randn(50)
    axes[1].plot(epochs, kl_loss, 'r-', linewidth=2)
    axes[1].set_title('KL Divergence Loss\n(Distance from prior N(0,1))')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].grid(True, alpha=0.3)

    # Total loss
    total_loss = recon_loss + kl_loss
    axes[2].plot(epochs, total_loss, 'g-', linewidth=2, label='Total')
    axes[2].plot(epochs, recon_loss, 'b--', alpha=0.5, label='Recon')
    axes[2].plot(epochs, kl_loss, 'r--', alpha=0.5, label='KL')
    axes[2].set_title('Total VAE Loss\n(Reconstruction + β×KL)')
    axes[2].set_xlabel('Epoch')
    axes[2].set_ylabel('Loss')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / "vae_loss_components.png", dpi=150, bbox_inches='tight')
    plt.close()

    print("Generated VAE loss comparison")

def main():
    output_dir = ensure_output_dir()
    generate_autoencoder_diagram(output_dir)
    generate_vae_latent_space(output_dir)
    generate_gan_training_diagram(output_dir)
    generate_mode_collapse_example(output_dir)
    generate_mnist_samples(output_dir)
    generate_loss_comparison(output_dir)
    print("✅ Part 3 Generative materials generated successfully!")

if __name__ == "__main__":
    main()
