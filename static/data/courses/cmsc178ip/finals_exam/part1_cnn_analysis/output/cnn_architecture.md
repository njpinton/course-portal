
# CNN Architecture for Analysis

## Model: SimpleCNN for CIFAR-10

### Layer Structure:
```
Input: (32, 32, 3)
    ↓
Conv2D(32, kernel=3x3, padding='same') + ReLU
    → Output: (32, 32, 32)
    ↓
MaxPool2D(pool_size=2x2)
    → Output: (16, 16, 32)
    ↓
Conv2D(64, kernel=3x3, padding='same') + ReLU
    → Output: (16, 16, 64)
    ↓
MaxPool2D(pool_size=2x2)
    → Output: (8, 8, 64)
    ↓
Conv2D(128, kernel=3x3, padding='same') + ReLU
    → Output: (8, 8, 128)
    ↓
MaxPool2D(pool_size=2x2)
    → Output: (4, 4, 128)
    ↓
Flatten
    → Output: (2048,)
    ↓
Dense(256) + ReLU + Dropout(0.5)
    → Output: (256,)
    ↓
Dense(10) + Softmax
    → Output: (10,)
```

### Questions for Analysis:
1. Calculate the total number of trainable parameters
2. What is the receptive field after each conv layer?
3. Why do we increase filters (32→64→128) as we go deeper?
4. What would happen if we removed all pooling layers?
5. How does dropout help prevent overfitting?
