#!/usr/bin/env python3
"""
Download real-world images for DIP Applications Collage
Sources: Unsplash (free, no attribution required), NASA (public domain), NCI (public domain)
"""

import os
import urllib.request
import ssl
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# Output directory
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Image sources - all free and legitimate
# Unsplash direct download: https://images.unsplash.com/photo-{ID}?w={width}
IMAGES = {
    "medical": {
        # Doctor looking at X-ray/CT scan - shows actual medical imaging
        "url": "https://images.unsplash.com/photo-1516549655169-df83a0774514?w=800",
        "fallback": "https://images.unsplash.com/photo-1530497610245-94d3c16cda28?w=800",
        "label": "Medical Imaging\n(CT, MRI, X-Ray)",
        "credit": "Unsplash"
    },
    "satellite": {
        # NASA Earth at Night - public domain
        "url": "https://eoimages.gsfc.nasa.gov/images/imagerecords/55000/55167/earth_lights.jpg",
        "fallback": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=800",
        "label": "Satellite Imagery\n(Remote Sensing)",
        "credit": "NASA"
    },
    "face_recognition": {
        # Clear portrait face for face detection/recognition demo
        "url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800",
        "fallback": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=800",
        "label": "Biometric Systems\n(Face Recognition)",
        "credit": "Unsplash"
    },
    "autonomous": {
        # Tesla car driving on street
        "url": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800",
        "fallback": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800",
        "label": "Autonomous Vehicles\n(Object Detection)",
        "credit": "Unsplash"
    },
    "document": {
        # Printed text/documents for OCR
        "url": "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=800",
        "fallback": "https://images.unsplash.com/photo-1456324504439-367cee3b3c32?w=800",
        "label": "Document Analysis\n(OCR)",
        "credit": "Unsplash"
    },
    "social_media": {
        # Phone with social media / camera app
        "url": "https://images.unsplash.com/photo-1611162618071-b39a2ec055fb?w=800",
        "fallback": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800",
        "label": "Digital Photography\n(Social Media)",
        "credit": "Unsplash"
    }
}

def download_image(url, filepath, fallback_url=None):
    """Download image from URL with fallback support."""
    # Create SSL context that doesn't verify (for some image servers)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        print(f"  Downloaded: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"  Failed to download from primary URL: {e}")
        if fallback_url:
            try:
                req = urllib.request.Request(fallback_url, headers=headers)
                with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
                    with open(filepath, 'wb') as f:
                        f.write(response.read())
                print(f"  Downloaded (fallback): {os.path.basename(filepath)}")
                return True
            except Exception as e2:
                print(f"  Fallback also failed: {e2}")
        return False

def create_collage(image_paths, labels, output_path):
    """Create a 2x3 collage of application images."""
    fig = plt.figure(figsize=(14, 10), facecolor='white')

    # Title
    fig.suptitle('Real-World Applications of Digital Image Processing',
                 fontsize=18, fontweight='bold', y=0.98)

    # Create 2x3 grid
    gs = gridspec.GridSpec(2, 3, figure=fig, wspace=0.15, hspace=0.25,
                          left=0.05, right=0.95, top=0.90, bottom=0.05)

    positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    keys = ["medical", "satellite", "face_recognition", "autonomous", "document", "social_media"]

    for idx, key in enumerate(keys):
        row, col = positions[idx]
        ax = fig.add_subplot(gs[row, col])

        img_path = image_paths.get(key)
        if img_path and os.path.exists(img_path):
            try:
                img = Image.open(img_path)
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # Resize to consistent size
                img = img.resize((400, 300), Image.LANCZOS)
                ax.imshow(np.array(img))
            except Exception as e:
                print(f"Error loading {key}: {e}")
                ax.text(0.5, 0.5, 'Image\nUnavailable', ha='center', va='center',
                       fontsize=14, transform=ax.transAxes)
                ax.set_facecolor('#f0f0f0')
        else:
            ax.text(0.5, 0.5, 'Image\nUnavailable', ha='center', va='center',
                   fontsize=14, transform=ax.transAxes)
            ax.set_facecolor('#f0f0f0')

        ax.set_title(labels[key], fontsize=11, fontweight='bold', pad=8)
        ax.axis('off')

    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"\nCollage saved: {output_path}")

def main():
    print("=" * 60)
    print("Downloading Real-World Images for DIP Applications")
    print("=" * 60)

    # Download each image
    image_paths = {}
    labels = {}

    for key, info in IMAGES.items():
        print(f"\n[{key.upper()}] - Source: {info['credit']}")
        filepath = os.path.join(OUTPUT_DIR, f"real_{key}.jpg")
        success = download_image(info['url'], filepath, info.get('fallback'))
        if success:
            image_paths[key] = filepath
        labels[key] = info['label']

    # Create collage
    print("\n" + "=" * 60)
    print("Creating Applications Collage")
    print("=" * 60)

    collage_path = os.path.join(OUTPUT_DIR, "applications_collage_real.png")
    create_collage(image_paths, labels, collage_path)

    print("\n" + "=" * 60)
    print("Done! New collage saved as: applications_collage_real.png")
    print("=" * 60)

if __name__ == "__main__":
    main()
