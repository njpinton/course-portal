# CMSC 178IP - Finals Exam Materials (Practical)

**Course:** Digital Image Processing
**Exam Type:** Take-Home, Practical (Jupyter Notebook)
**Total Points:** 80 (70 base + 10 bonus)
**Duration:** 1 week deadline

---

## Overview

This directory contains all materials for the CMSC 178IP final examination - a practical, notebook-based exam that tests both implementation skills and conceptual understanding.

### Key Features

- **Practical Format:** Jupyter Notebook with code and analysis
- **Hands-On Tasks:** Implement image processing techniques
- **Comprehensive Coverage:** Fundamentals through generative models
- **LLM-Enabled:** Students may use AI tools for coding help
- **Learning-Focused:** Reflection questions and comparison requirements

---

## Directory Structure

```
finals_exam/
├── README.md                           # This file
├── scripts/
│   └── generate_all_exam_materials.py  # Master generation script
│
├── part0_fundamentals/                 # Image basics review
│   ├── scripts/
│   └── output/
│
├── part1_cnn_analysis/                 # CNN architecture analysis
│   ├── scripts/
│   └── output/
│
├── part2_segmentation/                 # Segmentation & morphology
│   ├── scripts/
│   └── output/
│
├── part3_generative/                   # Generative models (VAE, GAN)
│   ├── scripts/
│   └── output/
│
├── bonus_application/                  # End-to-end pipeline
│   ├── scripts/
│   └── output/
│
├── student_template/
│   └── finals_exam_template.ipynb      # STUDENT WORKSPACE
│
└── instructions/
    ├── exam_instructions.md            # Student instructions
    └── grading_rubric.md               # Instructor rubric (keep private)
```

---

## Exam Structure

| Part | Topic | Points | Time |
|------|-------|--------|------|
| **Part 0** | Image Fundamentals Review | 10 | 20-30 min |
| **Part 1** | CNN Architecture Analysis | 20 | 45-60 min |
| **Part 2** | Image Segmentation | 20 | 45-60 min |
| **Part 3** | Generative Models | 20 | 45-60 min |
| **Bonus** | End-to-End Application | 10 | 30-45 min |

**Total:** 80 points, ~3-4 hours

---

## Quick Start for Instructors

### 1. Generate All Exam Materials

```bash
cd finals_exam
python scripts/generate_all_exam_materials.py
```

This creates all images and datasets needed for the exam (~2-3 minutes).

### 2. Verify Materials

Check that all `output/` directories contain generated images.

### 3. Customize Instructions

Edit `instructions/exam_instructions.md`:
- Add exam date and deadline
- Add submission platform details
- Add your contact information

### 4. Deploy to Students

**Provide to students:**
- `student_template/finals_exam_template.ipynb`
- `instructions/exam_instructions.md`
- All `output/` directories with images

**Keep for yourself:**
- `instructions/grading_rubric.md`
- Generation scripts (students don't need these)

### 5. Google Colab Option

Students can upload the notebook to Google Colab. All required libraries are available. Images can be uploaded to Colab or mounted from Google Drive.

---

## Exam Topics

### Part 0: Image Fundamentals (10 pts)
- Noise identification and filtering
- Histogram equalization vs CLAHE

### Part 1: CNN Analysis (20 pts)
- 2D convolution implementation from scratch
- CNN parameter calculation
- Feature map visualization

### Part 2: Segmentation (20 pts)
- Thresholding methods (Otsu, adaptive)
- Morphological operations (opening, closing)
- Watershed segmentation

### Part 3: Generative Models (20 pts)
- Autoencoder architecture design
- VAE loss function implementation
- GAN training dynamics analysis

### Bonus: Application (10 pts)
- Document restoration pipeline
- Multi-stage processing design

---

## Grading Summary

- **Implementation (40%):** Does the code work correctly?
- **Analysis (60%):** Does the student understand WHY?

See `instructions/grading_rubric.md` for detailed rubric.

---

## Technical Requirements

**Python Packages:**
```bash
pip install numpy matplotlib scikit-image scipy scikit-learn jupyter
# Optional for deep learning sections:
pip install torch torchvision
```

**Tested Environments:**
- Python 3.8+
- macOS, Linux, Windows
- Google Colab

---

## Version History

- **v2.0 (January 2026):** Practical notebook format
  - Jupyter notebook with code tasks
  - Image generation scripts
  - Hands-on implementation + analysis
  - Oral exam follow-up

- **v1.0 (January 2026):** Initial theory-focused version
  - Written questions only
  - Replaced by practical format

---

## License

**For Educational Use Only**

CMSC 178IP - Digital Image Processing
University of the Philippines - Cebu

---

## Contact

For questions about exam design, contact the course instructor.
