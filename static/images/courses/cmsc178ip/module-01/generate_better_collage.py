#!/usr/bin/env python3
"""
Generate better DIP application images with correct context.
Fixes: face detection (front-facing), medical imaging (actual scan).
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image
import urllib.request
import ssl

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def download_image(url, filename):
    """Download image from URL."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
        with open(filename, 'wb') as f:
            f.write(response.read())
    return filename


def generate_face_detection():
    """Generate face detection with FRONT-FACING faces."""
    print("  Generating face detection (front-facing faces)...")

    # Use a group selfie/front-facing group photo
    url = "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=1200"

    # Try alternative URLs for front-facing group photos
    urls_to_try = [
        "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?w=1200",  # Friends selfie
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1200",  # Team meeting
        "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=1200",  # Professional woman
    ]

    img = None
    for url in urls_to_try:
        try:
            temp_path = f"{OUTPUT_DIR}/temp_faces.jpg"
            download_image(url, temp_path)
            img = cv2.imread(temp_path)
            if img is not None:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                )
                faces = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))
                if len(faces) >= 1:
                    print(f"    Found {len(faces)} faces!")
                    break
        except Exception as e:
            print(f"    Failed {url}: {e}")
            continue

    if img is None or len(faces) == 0:
        print("    Could not find image with detectable faces, creating synthetic demo")
        # Create a synthetic visualization
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_facecolor('#2a2a2a')

        # Draw placeholder faces with boxes
        face_positions = [(100, 80, 120, 150), (280, 100, 110, 140), (450, 90, 115, 145)]
        for i, (x, y, w, h) in enumerate(face_positions):
            # Draw face placeholder
            circle = plt.Circle((x + w/2, y + h/2), w/2, color='#555', fill=True)
            ax.add_patch(circle)
            # Draw bounding box
            rect = plt.Rectangle((x, y), w, h, fill=False, edgecolor='#00ff00', linewidth=3)
            ax.add_patch(rect)
            ax.text(x, y - 10, f'Face {i+1}: 0.9{i+2}', color='#00ff00', fontsize=10, fontweight='bold')

        ax.set_xlim(0, 640)
        ax.set_ylim(400, 0)
        ax.set_title('Face Detection with Bounding Boxes', color='white', fontsize=14, fontweight='bold', pad=10)
        ax.axis('off')

        output_path = f"{OUTPUT_DIR}/face_detection_fixed.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#2a2a2a')
        plt.close()
        return output_path

    # Draw green bounding boxes
    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
        conf = 0.92 + np.random.random() * 0.07
        cv2.putText(img, f'Face {i+1}: {conf:.2f}',
                    (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.putText(img, 'Face Detection with Bounding Boxes',
                (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    output_path = f"{OUTPUT_DIR}/face_detection_fixed.png"
    cv2.imwrite(output_path, img)
    os.remove(temp_path)
    print(f"    Saved: {output_path}")
    return output_path


def generate_medical_scan():
    """Download actual CT scan / X-ray image."""
    print("  Downloading CT scan image...")

    # Pexels free images - actual X-rays and scans
    urls_to_try = [
        # Chest X-ray (actual scan)
        "https://images.pexels.com/photos/4226219/pexels-photo-4226219.jpeg?w=800",
        # X-ray image
        "https://images.pexels.com/photos/4226256/pexels-photo-4226256.jpeg?w=800",
        # Spine X-ray
        "https://images.pexels.com/photos/4226264/pexels-photo-4226264.jpeg?w=800",
        # Medical scan
        "https://images.pexels.com/photos/4226218/pexels-photo-4226218.jpeg?w=800",
    ]

    output_path = f"{OUTPUT_DIR}/medical_ct_scan.png"

    for url in urls_to_try:
        try:
            temp_path = f"{OUTPUT_DIR}/temp_ct.jpg"
            download_image(url, temp_path)

            img = cv2.imread(temp_path)
            if img is not None:
                cv2.imwrite(output_path, img)
                os.remove(temp_path)
                print(f"    Saved: {output_path}")
                return output_path
        except Exception as e:
            print(f"    Failed {url}: {e}")
            continue

    print("    All URLs failed")
    return None


def generate_object_detection():
    """Generate cleaner object detection visualization."""
    print("  Generating object detection...")

    # Use existing if good, or regenerate
    existing = f"{OUTPUT_DIR}/object_detection_demo.png"
    if os.path.exists(existing):
        print(f"    Using existing: {existing}")
        return existing

    # Download street scene
    url = "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1200"
    img_path = download_image(url, f"{OUTPUT_DIR}/temp_street.jpg")

    img = cv2.imread(img_path)
    h, w = img.shape[:2]

    detections = [
        {"class": "car", "conf": 0.94, "box": (int(w*0.05), int(h*0.4), int(w*0.25), int(h*0.35)), "color": (0, 255, 255)},
        {"class": "car", "conf": 0.91, "box": (int(w*0.35), int(h*0.35), int(w*0.18), int(h*0.25)), "color": (0, 255, 255)},
        {"class": "person", "conf": 0.87, "box": (int(w*0.7), int(h*0.3), int(w*0.08), int(h*0.35)), "color": (0, 255, 0)},
        {"class": "bus", "conf": 0.89, "box": (int(w*0.55), int(h*0.25), int(w*0.15), int(h*0.3)), "color": (255, 128, 0)},
    ]

    for det in detections:
        x, y, bw, bh = det["box"]
        color = det["color"]
        cv2.rectangle(img, (x, y), (x+bw, y+bh), color, 3)
        label = f'{det["class"]} {det["conf"]:.2f}'
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(img, (x, y-th-10), (x+tw+10, y), color, -1)
        cv2.putText(img, label, (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    cv2.putText(img, 'Object Detection (YOLO-style)',
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

    output_path = f"{OUTPUT_DIR}/object_detection_fixed.png"
    cv2.imwrite(output_path, img)
    os.remove(img_path)
    print(f"    Saved: {output_path}")
    return output_path


def generate_ocr_demo():
    """Generate cleaner OCR visualization."""
    print("  Generating OCR demo...")

    fig = plt.figure(figsize=(10, 5), facecolor='white')
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1], wspace=0.05)

    # Left: Document
    ax1 = fig.add_subplot(gs[0])
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.set_facecolor('#fafafa')

    # Draw document with text regions
    lines = [
        (8, 82, 84, 10, "Digital Image Processing"),
        (8, 65, 75, 8, "Introduction to computer vision"),
        (8, 50, 70, 8, "and image analysis techniques"),
        (8, 35, 78, 8, "for real-world applications."),
    ]

    for x, y, w, h, text in lines:
        rect = plt.Rectangle((x, y), w, h, fill=False, edgecolor='#00aa00', linewidth=2)
        ax1.add_patch(rect)
        ax1.text(x + 2, y + h/2, text, fontsize=11, va='center', family='serif', color='#333')

    ax1.set_title('Input Document', fontsize=11, fontweight='bold', pad=8)
    ax1.axis('off')

    # Right: Extracted text
    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.set_facecolor('#1e1e1e')

    extracted = """EXTRACTED TEXT:
────────────────────────

Digital Image Processing

Introduction to computer vision
and image analysis techniques
for real-world applications.

────────────────────────
Confidence: 97.3%
Words: 14 | Time: 0.23s"""

    ax2.text(5, 92, extracted, fontsize=10, va='top', family='monospace', color='#00ff00')
    ax2.set_title('OCR Output', fontsize=11, fontweight='bold', pad=8)
    ax2.axis('off')

    fig.suptitle('Optical Character Recognition (OCR)', fontsize=13, fontweight='bold', y=0.98)

    output_path = f"{OUTPUT_DIR}/ocr_fixed.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"    Saved: {output_path}")
    return output_path


def generate_enhancement_demo():
    """Generate cleaner enhancement before/after."""
    print("  Generating enhancement demo...")

    # Download landscape image
    url = "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600"
    img_path = download_image(url, f"{OUTPUT_DIR}/temp_enhance.jpg")

    img = cv2.imread(img_path)
    img = cv2.resize(img, (400, 300))

    # Create dark version
    dark = cv2.convertScaleAbs(img, alpha=0.4, beta=-40)

    # Enhance with CLAHE
    lab = cv2.cvtColor(dark, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # Create side-by-side
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    axes[0].imshow(cv2.cvtColor(dark, cv2.COLOR_BGR2RGB))
    axes[0].set_title('Before (Underexposed)', fontsize=11, fontweight='bold')
    axes[0].axis('off')

    axes[1].imshow(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))
    axes[1].set_title('After (CLAHE Enhanced)', fontsize=11, fontweight='bold')
    axes[1].axis('off')

    fig.suptitle('Image Enhancement', fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()

    output_path = f"{OUTPUT_DIR}/enhancement_fixed.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    os.remove(img_path)
    print(f"    Saved: {output_path}")
    return output_path


def create_collage(images, output_path):
    """Create 2x3 collage with consistent sizing."""
    print("  Creating final collage...")

    fig = plt.figure(figsize=(14, 9), facecolor='white')
    fig.suptitle('Real-World Applications of Digital Image Processing',
                 fontsize=16, fontweight='bold', y=0.98)

    gs = gridspec.GridSpec(2, 3, figure=fig, wspace=0.08, hspace=0.15,
                           left=0.02, right=0.98, top=0.92, bottom=0.02)

    titles = [
        "Medical Imaging\n(AI-Assisted Analysis)",
        "Satellite Imagery\n(Remote Sensing)",
        "Biometric Systems\n(Face Detection)",
        "Autonomous Vehicles\n(Object Detection)",
        "Document Analysis\n(OCR)",
        "Image Enhancement\n(Photo Editing)"
    ]

    keys = ["medical", "satellite", "face", "object", "ocr", "enhancement"]
    positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]

    for idx, key in enumerate(keys):
        row, col = positions[idx]
        ax = fig.add_subplot(gs[row, col])

        img_path = images.get(key)
        if img_path and os.path.exists(img_path):
            try:
                img = Image.open(img_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # Resize to consistent aspect ratio
                img.thumbnail((500, 350), Image.LANCZOS)
                ax.imshow(np.array(img))
            except Exception as e:
                print(f"    Error loading {key}: {e}")
                ax.text(0.5, 0.5, 'Image\nUnavailable', ha='center', va='center',
                        fontsize=12, transform=ax.transAxes)
                ax.set_facecolor('#f0f0f0')
        else:
            ax.text(0.5, 0.5, 'Image\nUnavailable', ha='center', va='center',
                    fontsize=12, transform=ax.transAxes)
            ax.set_facecolor('#f0f0f0')

        ax.set_title(titles[idx], fontsize=10, fontweight='bold', pad=6)
        ax.axis('off')

    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"    Saved: {output_path}")


def main():
    print("=" * 60)
    print("Generating Better DIP Application Images")
    print("=" * 60)

    images = {}

    # Generate each image
    images["medical"] = generate_medical_scan()
    images["face"] = generate_face_detection()
    images["object"] = generate_object_detection()
    images["ocr"] = generate_ocr_demo()
    images["enhancement"] = generate_enhancement_demo()

    # Use existing satellite image
    satellite_path = f"{OUTPUT_DIR}/satellite_demo.jpg"
    if os.path.exists(satellite_path):
        images["satellite"] = satellite_path
    else:
        url = "https://eoimages.gsfc.nasa.gov/images/imagerecords/55000/55167/earth_lights.jpg"
        images["satellite"] = download_image(url, satellite_path)

    # Create collage
    create_collage(images, f"{OUTPUT_DIR}/applications_collage.png")

    print("\n" + "=" * 60)
    print("Done! Collage saved as: applications_collage.png")
    print("=" * 60)


if __name__ == "__main__":
    main()
