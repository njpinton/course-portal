# CMSC 178IP Finals Exam (Practical) - Grading Rubric

**For Instructor Use Only**

---

## Grading Overview

- **Total Points:** 100 (90 base + 10 bonus)
- **Implementation:** 40% | **Analysis:** 60%
- **Time per student:** ~15-20 min grading

## Exam Structure (Ordered by Complexity)

| Part | Topic | Points | Difficulty |
|------|-------|--------|------------|
| Part 0 | Image Representation & Basics | 20 | ⭐ Easiest |
| Part 1 | Spatial Operations | 25 | ⭐⭐ Medium |
| Part 2 | CNN Architecture | 25 | ⭐⭐⭐ Medium-Hard |
| Part 3 | Generative Models | 20 | ⭐⭐⭐⭐ Hardest |
| Bonus | End-to-End Application | 10 | Applied |

## Anti-Copying Measures

### Personalized Parameters
Each student uses their student number as a seed, generating unique:
- Noise variance (0.01-0.06) for Part 1
- S&P amount (0.03-0.08) for Part 1
- Latent dimension (16-48) for Part 3

**Verification:** Check that MY_SEED matches student number.

### Process Log (Required)
Students must document failed attempts and debugging process.

---

## Part 0: Image Representation & Basics (20 points)

### 0.1 Image Properties & Data Types (8 pts)

| Component | Points | Criteria |
|-----------|--------|----------|
| Image exploration code | 2 | Correctly displays properties (shape, dtype, min/max) |
| Color channel extraction | 1.5 | Correctly extracts and displays R, G, B channels |
| Color space conversion | 1.5 | Correctly converts RGB to HSV and displays channels |
| Analysis Q1 | 1 | Explains dimensions for grayscale vs color |
| Analysis Q2 | 1 | Explains dtype conversion (uint8 vs float) |
| Analysis Q3 | 1 | Explains HSV usefulness with example |

### 0.2 Histograms & Intensity Distribution (7 pts)

| Component | Points | Criteria |
|-----------|--------|----------|
| Histogram plotting | 2 | Correctly plots histograms for all 4 images |
| Statistics calculation | 1 | Correctly calculates mean, std, min, max |
| Analysis Q1 | 1.5 | Identifies dark/bright/low-contrast from histogram |
| Analysis Q2 | 1 | Explains standard deviation meaning |
| Comparison table | 1.5 | Describes histogram shapes for all 4 images |

### 0.3 Introduction to Kernels (5 pts)

| Component | Points | Criteria |
|-----------|--------|----------|
| Kernel application | 2 | Correctly applies all kernels and displays results |
| Analysis Q1 | 1 | Describes what each kernel does |
| Analysis Q2 | 1 | Explains sharpen kernel values |
| Analysis Q3 | 1 | Explains why edge detection produces dark images |

---

## Part 1: Spatial Operations (25 points)

### 1.1 Noise Filtering (8 pts)

| Component | Points | Criteria |
|-----------|--------|----------|
| Gaussian noise filter | 2 | Uses Gaussian blur or bilateral filter |
| S&P noise filter | 2 | Uses median filter |
| Visualization | 1 | Displays before/after for both |
| Analysis Q1 | 1.5 | Identifies noise types correctly |
| Analysis Q2 | 1.5 | Explains why median works for S&P |

### 1.2 Edge Detection (8 pts)

| Component | Points | Criteria |
|-----------|--------|----------|
| Sobel magnitude | 2 | Correctly calculates sqrt(sobel_x² + sobel_y²) |
| Canny detection | 2 | Applies Canny with different sigma values |
| Visualization | 1 | Displays all edge results |
| Analysis Q1 | 1.5 | Explains Sobel vs Canny difference |
| Analysis Q2 | 1.5 | Explains sigma trade-off |

### 1.3 Thresholding (9 pts)

| Component | Points | Criteria |
|-----------|--------|----------|
| Manual threshold | 1 | Applies manual threshold correctly |
| Otsu's threshold | 2 | Correctly uses filters.threshold_otsu() |
| Adaptive threshold | 2 | Correctly uses filters.threshold_local() |
| Analysis Q1 | 1.5 | Explains Otsu optimization |
| Analysis Q2 | 1.5 | Explains when to use adaptive |
| Comparison table | 1 | Documents 3 threshold experiments |

---

## Part 2: CNN Architecture Analysis (25 points)

### 2.1 Convolution Operation (10 pts)

| Component | Points | Criteria |
|-----------|--------|----------|
| Kernel flipping | 2 | Correctly flips kernel (180° rotation) |
| Zero padding | 2 | Correct padding implementation |
| Convolution loop | 2 | Correct nested loop with indexing |
| Validation | 1 | Output matches scipy (diff < 1e-5) |
| Analysis Q1 | 1 | Explains why kernel flipping is needed |
| Analysis Q2 | 1 | Explains purpose of zero-padding |
| Analysis Q3 | 1 | Explains how CNNs make convolution efficient |

### 2.2 CNN Parameters (8 pts)

| Component | Points | Criteria |
|-----------|--------|----------|
| Output shapes | 2 | All shapes correct |
| Parameter calculations | 3 | Correct for all layers |
| Analysis Q1 | 1 | Explains why Conv2D has fewer params than Dense |
| Analysis Q2 | 1 | Explains MaxPooling purpose |
| Analysis Q3 | 1 | Explains effect of doubling filters |

### 2.3 Feature Maps (7 pts)

| Component | Points | Criteria |
|-----------|--------|----------|
| Filter application | 3 | All 5 kernels correctly applied and visualized |
| Analysis Q1 | 1.5 | Identifies which filter responds to tripod |
| Analysis Q2 | 1.5 | Explains what deeper layers learn |
| Analysis Q3 | 1 | Explains hierarchical feature learning importance |

---

## Part 3: Generative Models (20 points)

### 3.1 Autoencoder Architecture (8 pts)

| Component | Points | Criteria |
|-----------|--------|----------|
| Architecture design | 2 | Reasonable encoder-decoder structure |
| Parameter calculation | 2 | Correct calculation with personalized latent dim |
| Analysis Q1 | 2 | Explains bottleneck purpose |
| Analysis Q2 | 2 | Explains latent space issues |

### 3.2 VAE Loss Function (6 pts)

| Component | Points | Criteria |
|-----------|--------|----------|
| Reconstruction loss | 1 | Correct MSE implementation |
| KL divergence | 2 | Correct KL formula |
| Analysis Q1 | 1.5 | Explains KL purpose |
| Analysis Q2 | 1.5 | Explains β trade-off |

### 3.3 GAN Analysis (6 pts)

| Component | Points | Criteria |
|-----------|--------|----------|
| Scenario analysis | 3 | Correctly identifies A/B/C training states |
| Mode collapse Q | 1.5 | Defines and explains mitigation |
| VAE vs GAN Q | 1.5 | Explains sharpness difference |

---

## Bonus: End-to-End Application (10 points)

| Component | Points | Criteria |
|-----------|--------|----------|
| Pipeline design | 3 | Logical order addressing degradations |
| Implementation | 3 | Working code that improves quality |
| Order justification | 2 | Explains operation order |
| Comparison | 2 | Tries 2 orderings, documents results |

---

## Points Summary

| Part | Implementation | Analysis | Total |
|------|---------------|----------|-------|
| Part 0 | 9 | 11 | 20 |
| Part 1 | 12 | 13 | 25 |
| Part 2 | 13 | 12 | 25 |
| Part 3 | 5 | 15 | 20 |
| Bonus | 6 | 4 | 10 |
| **Total** | **45** | **55** | **100** |

### Part 0 Breakdown
- 0.1 Image Properties: 8 pts (5 impl + 3 analysis)
- 0.2 Histograms: 7 pts (3 impl + 4 analysis)
- 0.3 Kernels: 5 pts (2 impl + 3 analysis)

### Part 2 Breakdown
- 2.1 Convolution Operation: 10 pts (10 impl + 0 analysis)
- 2.2 CNN Parameters: 8 pts (5 impl + 3 analysis)
- 2.3 Feature Maps: 7 pts (3 impl + 4 analysis)

---

## Grading Scale

| Score | Grade | Description |
|-------|-------|-------------|
| 90-100% | A | Excellent understanding |
| 80-89% | B | Good understanding, minor gaps |
| 70-79% | C | Satisfactory, some gaps |
| 60-69% | D | Passing, significant gaps |
| <60% | F | Fundamental misunderstandings |

---

## Common Deductions

| Issue | Deduction |
|-------|-----------|
| MY_SEED not changed | -5% overall |
| Process log empty | -5% overall |
| Missing visualizations | -1 pt each |
| Code runs but wrong output | -50% implementation |
| Superficial analysis | -50% analysis points |
| Late submission | -10% per day (max 3 days) |

---

**Last Updated:** January 2026
