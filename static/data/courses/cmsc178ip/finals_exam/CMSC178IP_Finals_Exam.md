# CMSC 178IP - Digital Image Processing
# Final Examination (Take-Home)

**Course:** CMSC 178IP - Digital Image Processing
**Institution:** University of the Philippines - Cebu
**Exam Type:** Take-Home, Theory-Focused
**Total Points:** 75
**Time Allocation:** 3-4 hours (self-paced)
**Deadline:** 1 week from release date

---

## Instructions

1. Answer all questions in this document or a separate document clearly labeled with your name and student number
2. Write concise, focused answers - quality over quantity
3. You may use course materials, textbooks, and online resources
4. LLM usage (ChatGPT, Claude, etc.) is permitted for clarification, but your answers must reflect YOUR understanding
5. An oral examination (10-15 minutes) will follow submission to verify understanding
6. Submit as PDF via the designated platform

---

## Part 1: Image Fundamentals (12 points)

### Question 1.1 (4 points)
**Image Representation and Quantization**

A grayscale image uses 8-bit quantization (256 gray levels).

a) If we reduce the quantization to 4 bits, how many gray levels would be available? (1 pt)

b) Describe TWO visible artifacts that would appear when reducing from 8-bit to 2-bit quantization. (2 pts)

c) Why does the human eye perceive these artifacts more strongly in smooth gradient regions than in textured regions? (1 pt)

---

### Question 1.2 (4 points)
**Sampling and Aliasing**

a) State the Nyquist-Shannon sampling theorem in your own words. (1 pt)

b) A camera captures an image of a striped shirt. The stripes have a spatial frequency of 50 cycles per cm. If the camera samples at 80 samples per cm, will aliasing occur? Explain your reasoning. (2 pts)

c) Describe ONE practical method to prevent aliasing in digital cameras. (1 pt)

---

### Question 1.3 (4 points)
**Color Spaces and Compression**

a) Why is YCbCr color space preferred over RGB for image/video compression? (2 pts)

b) JPEG compression applies 4:2:0 chroma subsampling. Explain what this means and why it's perceptually acceptable. (2 pts)

---

## Part 2: Image Processing Operations (15 points)

### Question 2.1 (5 points)
**Convolution and Correlation**

a) What is the fundamental difference between convolution and correlation? When does this difference matter? (2 pts)

b) Given a 3x3 kernel, explain why we need to "flip" it for convolution but not for correlation. (1 pt)

c) A separable 5x5 filter can be decomposed into two 1D filters. How many multiplications are saved when applying a separable filter to a 512x512 image compared to a non-separable filter? Show your calculation. (2 pts)

---

### Question 2.2 (5 points)
**Frequency Domain Processing**

a) What type of image features correspond to LOW frequencies in the Fourier domain? What about HIGH frequencies? (2 pts)

b) A researcher applies an ideal low-pass filter (sharp cutoff) in the frequency domain. They observe "ringing" artifacts in the output image. Explain why this occurs. (2 pts)

c) What filter shape would reduce ringing while still removing high frequencies? (1 pt)

---

### Question 2.3 (5 points)
**Histogram Operations**

a) An image appears "washed out" with pixel values concentrated between 100-150 (out of 0-255). Describe how histogram equalization would improve this image. (2 pts)

b) Histogram equalization sometimes produces unnatural results. Describe a scenario where adaptive histogram equalization (CLAHE) would be preferred. (2 pts)

c) Can histogram equalization ever make an image look worse? Give an example. (1 pt)

---

## Part 3: Enhancement and Restoration (12 points)

### Question 3.1 (4 points)
**Noise Reduction**

A medical X-ray image is corrupted by both Gaussian noise AND salt-and-pepper noise.

a) Which filter would you apply FIRST - Gaussian blur or median filter? Justify your choice. (2 pts)

b) Why is a bilateral filter often preferred over Gaussian blur for denoising photographs of faces? (2 pts)

---

### Question 3.2 (4 points)
**Image Restoration**

An old photograph suffers from motion blur (the camera moved horizontally during exposure).

a) Explain the concept of the Point Spread Function (PSF) and how it relates to motion blur. (2 pts)

b) A student attempts Wiener filtering to restore the image but gets poor results. List TWO possible reasons for the failure and how to address each. (2 pts)

---

### Question 3.3 (4 points)
**Geometric Transformations**

a) Explain the difference between forward mapping and inverse mapping when applying geometric transformations. Why is inverse mapping typically preferred? (2 pts)

b) When rotating an image by 30 degrees, why does nearest-neighbor interpolation produce jagged edges while bilinear interpolation produces smoother results? (2 pts)

---

## Part 4: Feature Extraction and Segmentation (12 points)

### Question 4.1 (4 points)
**Edge Detection**

a) The Canny edge detector uses non-maximum suppression. What is its purpose and how does it improve edge detection compared to simple thresholding? (2 pts)

b) Compare the Sobel operator and the Laplacian of Gaussian (LoG) for edge detection. When would you choose one over the other? (2 pts)

---

### Question 4.2 (4 points)
**Feature Descriptors**

a) SIFT (Scale-Invariant Feature Transform) is described as "invariant to scale and rotation." Explain how SIFT achieves scale invariance. (2 pts)

b) Why are feature descriptors like SIFT/ORB useful for image stitching (creating panoramas)? What could go wrong if the images have very different lighting conditions? (2 pts)

---

### Question 4.3 (4 points)
**Segmentation**

a) Otsu's thresholding automatically selects a threshold value. What criterion does it optimize, and why might it fail on images with uneven illumination? (2 pts)

b) Compare region-based segmentation (e.g., region growing) with edge-based segmentation. Give one advantage and one disadvantage of each approach. (2 pts)

---

## Part 5: Deep Learning for Computer Vision (12 points)

### Question 5.1 (4 points)
**CNN Fundamentals**

a) A convolutional layer uses 32 filters of size 3x3 on an input with 3 channels (RGB). How many learnable parameters does this layer have (including biases)? Show your calculation. (2 pts)

b) Explain the purpose of pooling layers in CNNs. What is the trade-off between using max pooling vs. average pooling? (2 pts)

---

### Question 5.2 (4 points)
**Training Deep Networks**

a) A student trains a CNN on a small dataset of 500 images. The training accuracy reaches 99% but validation accuracy is only 60%. Diagnose the problem and suggest TWO concrete solutions. (2 pts)

b) Explain how transfer learning works and why it's especially valuable when you have limited training data. (2 pts)

---

### Question 5.3 (4 points)
**Object Detection and Segmentation**

a) Compare two-stage detectors (like Faster R-CNN) with one-stage detectors (like YOLO). What is the main trade-off between them? (2 pts)

b) What is the difference between semantic segmentation and instance segmentation? Give an example scenario where instance segmentation would be necessary but semantic segmentation would be insufficient. (2 pts)

---

## Part 6: Generative Models (12 points)

### Question 6.1 (4 points)
**Autoencoders and VAEs**

a) A standard autoencoder can compress and reconstruct images, but it's not good for generating NEW images. Explain why. (2 pts)

b) How does a Variational Autoencoder (VAE) solve this problem? Specifically, explain the role of the KL divergence term in the VAE loss function. (2 pts)

---

### Question 6.2 (4 points)
**Generative Adversarial Networks**

a) Describe the "adversarial game" between the generator and discriminator in a GAN. What is each network trying to optimize? (2 pts)

b) "Mode collapse" is a common problem in GAN training. What is mode collapse and what causes it? (2 pts)

---

### Question 6.3 (4 points)
**Comparing Generative Models**

Complete the following comparison table and briefly justify ONE of your entries:

| Aspect | Autoencoder | VAE | GAN |
|--------|-------------|-----|-----|
| Training stability | ? | ? | ? |
| Output quality (sharpness) | ? | ? | ? |
| Latent space interpolation | ? | ? | ? |

(2 pts for table, 2 pts for justification)

---

## Bonus Question (5 points)

**Integrated Application**

You are tasked with building an automated quality control system for a manufacturing line that produces printed circuit boards (PCBs). The system must detect defects such as missing components, misaligned parts, and solder bridges.

Design a complete image processing pipeline that addresses this problem. Your answer should include:

a) Image acquisition considerations (lighting, camera setup) (1 pt)

b) Preprocessing steps to normalize images and reduce noise (1 pt)

c) The main detection approach (traditional CV, deep learning, or hybrid) with justification (2 pts)

d) How you would handle the challenge of limited defect samples for training (1 pt)

---

## Submission Checklist

- [ ] All questions answered
- [ ] Name and student number included
- [ ] Answers are clear and concise
- [ ] Submitted as PDF
- [ ] Submitted before deadline

---

**Good luck!**

*Remember: The oral examination will assess your understanding of your written answers. Be prepared to explain and expand on any of your responses.*
