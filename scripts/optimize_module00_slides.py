#!/usr/bin/env python3
"""
Optimize Module 00 slides:
1. Split long slides into focused chunks
2. Use image-text-layout for slides with figures
3. Reduce content density
4. Apply strategic multi-column layouts
"""

import json
from typing import List, Dict

def load_slides(path: str) -> Dict:
    with open(path, 'r') as f:
        return json.load(f)

def save_slides(data: Dict, path: str):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def make_image_text_layout(image_html: str, text_html: str, reverse: bool = False) -> str:
    """Create image-text side-by-side layout."""
    reverse_class = " reverse" if reverse else ""
    return f'''<div class="image-text-layout{reverse_class}">
    <div class="image-column">{image_html}</div>
    <div class="text-column">{text_html}</div>
</div>'''

def optimize_slides(data: Dict) -> Dict:
    """Restructure slides for minimal scrolling."""
    old_slides = data['slides']
    new_slides = []

    for slide in old_slides:
        slide_id = slide['id']
        title = slide['title']
        content = slide['content']

        # Slide 7: Supervised Learning - Split into Definition + Training
        if slide_id == 7:
            # Part 1: Image + Definition (image-text layout)
            new_slides.append({
                "id": len(new_slides) + 1,
                "title": "Supervised Learning",
                "readingTime": "1 min",
                "content": '''<div class="image-text-layout">
    <div class="image-column">
        <figure class="slide-figure">
            <img src="/static/images/courses/cmsc173/module-00/supervised_vs_unsupervised.png" alt="Supervised vs Unsupervised" style="max-width: 100%;">
            <figcaption>Supervised vs Unsupervised Learning</figcaption>
        </figure>
    </div>
    <div class="text-column">
        <div class="definition">
            <strong>Definition:</strong> Learning from <em>labeled data</em>
        </div>
        <ul>
            <li><strong>Input:</strong> $\\mathbf{x} \\in \\mathbb{R}^d$</li>
            <li><strong>Output:</strong> Label $y$</li>
            <li><strong>Goal:</strong> Learn $f(\\mathbf{x}) \\approx y$</li>
        </ul>
        <div class="highlight">
            <h4>Two Main Tasks</h4>
            <ul>
                <li><strong>Regression:</strong> $y \\in \\mathbb{R}$</li>
                <li><strong>Classification:</strong> $y \\in \\{1,...,K\\}$</li>
            </ul>
        </div>
    </div>
</div>''',
                "hasVisualization": True,
                "knowledgeCheck": None
            })

            # Part 2: Training Process + Code
            new_slides.append({
                "id": len(new_slides) + 1,
                "title": "Supervised Learning: Training",
                "readingTime": "2 min",
                "content": '''<div class="two-column">
    <div class="column">
        <div class="highlight">
            <h4>Training Process</h4>
            <p>Given $\\mathcal{D} = \\{(\\mathbf{x}_i, y_i)\\}_{i=1}^n$:</p>
            <ol>
                <li>Choose hypothesis class $\\mathcal{H}$</li>
                <li>Define loss $\\mathcal{L}(y, \\hat{y})$</li>
                <li>Minimize empirical risk:<br>
                    $$\\hat{f} = \\arg\\min_{f \\in \\mathcal{H}} \\frac{1}{n}\\sum_{i=1}^n \\mathcal{L}(y_i, f(\\mathbf{x}_i))$$
                </li>
            </ol>
        </div>
    </div>
    <div class="column">
        <div class="example">
            <h4>Key Properties</h4>
            <ul>
                <li>Labeled data required</li>
                <li>Teacher signal guides learning</li>
                <li>Generalization to new examples</li>
            </ul>
        </div>
        <div class="warning">
            <h4>Challenge</h4>
            <p>Avoid overfitting to training data!</p>
        </div>
    </div>
</div>

<div class="code-example">
    <h4>Python Example</h4>
    <pre class="code-block"><code class="language-python">from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LogisticRegression().fit(X_train, y_train)
print(f"Accuracy: {model.score(X_test, y_test):.2f}")</code></pre>
</div>''',
                "hasVisualization": False,
                "knowledgeCheck": None
            })
            continue

        # Slide 8: Regression - Split into Concepts + Code
        if slide_id == 8:
            # Part 1: Image + Formulation
            new_slides.append({
                "id": len(new_slides) + 1,
                "title": "Regression: Predicting Continuous Values",
                "readingTime": "1 min",
                "content": '''<div class="image-text-layout">
    <div class="image-column">
        <figure class="slide-figure">
            <img src="/static/images/courses/cmsc173/module-00/regression_example.png" alt="Regression Example" style="max-width: 100%;">
            <figcaption>Linear Regression with Fitted Line</figcaption>
        </figure>
    </div>
    <div class="text-column">
        <div class="definition">
            <strong>Input:</strong> $\\mathbf{x} \\in \\mathbb{R}^d$<br>
            <strong>Output:</strong> $y \\in \\mathbb{R}$ (continuous)<br>
            <strong>Model:</strong> $\\hat{y} = f(\\mathbf{x}; \\theta)$
        </div>
        <div class="highlight">
            <h4>Loss Functions</h4>
            <ul>
                <li><strong>MSE:</strong> $\\frac{1}{n}\\sum (y_i - \\hat{y}_i)^2$</li>
                <li><strong>MAE:</strong> $\\frac{1}{n}\\sum |y_i - \\hat{y}_i|$</li>
            </ul>
        </div>
    </div>
</div>''',
                "hasVisualization": True,
                "knowledgeCheck": None
            })

            # Part 2: Algorithms + Code
            new_slides.append({
                "id": len(new_slides) + 1,
                "title": "Regression: Algorithms & Examples",
                "readingTime": "1 min",
                "content": '''<div class="two-column">
    <div class="column">
        <div class="highlight">
            <h4>Regression Algorithms</h4>
            <ul>
                <li>Linear Regression</li>
                <li>Ridge/Lasso (regularized)</li>
                <li>Polynomial Regression</li>
                <li>SVR, Decision Trees</li>
                <li>Neural Networks</li>
            </ul>
        </div>
    </div>
    <div class="column">
        <div class="example">
            <h4>Real-World Examples</h4>
            <ul>
                <li>House price prediction</li>
                <li>Stock forecasting</li>
                <li>Temperature prediction</li>
                <li>Sales forecasting</li>
            </ul>
        </div>
    </div>
</div>

<div class="code-example">
    <h4>Python Example</h4>
    <pre class="code-block"><code class="language-python">from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

model = LinearRegression().fit(X_train, y_train)
y_pred = model.predict(X_test)
print(f"MSE: {mean_squared_error(y_test, y_pred):.4f}")</code></pre>
</div>''',
                "hasVisualization": False,
                "knowledgeCheck": None
            })
            continue

        # Slide 9: Classification - Split into Concepts + Code
        if slide_id == 9:
            # Part 1: Image + Formulation
            new_slides.append({
                "id": len(new_slides) + 1,
                "title": "Classification: Predicting Categories",
                "readingTime": "1 min",
                "content": '''<div class="image-text-layout">
    <div class="image-column">
        <figure class="slide-figure">
            <img src="/static/images/courses/cmsc173/module-00/classification_example.png" alt="Classification Example" style="max-width: 100%;">
            <figcaption>Decision Boundary Separating Classes</figcaption>
        </figure>
    </div>
    <div class="text-column">
        <div class="definition">
            <strong>Input:</strong> $\\mathbf{x} \\in \\mathbb{R}^d$<br>
            <strong>Output:</strong> $y \\in \\{1,...,K\\}$ (discrete)<br>
            <strong>Model:</strong> $\\hat{y} = \\arg\\max_k P(y=k|\\mathbf{x})$
        </div>
        <div class="highlight">
            <h4>Types</h4>
            <ul>
                <li><strong>Binary:</strong> $K=2$ (spam/not spam)</li>
                <li><strong>Multi-class:</strong> $K>2$ (digits 0-9)</li>
                <li><strong>Multi-label:</strong> Multiple tags per item</li>
            </ul>
        </div>
    </div>
</div>''',
                "hasVisualization": True,
                "knowledgeCheck": None
            })

            # Part 2: Algorithms + Code
            new_slides.append({
                "id": len(new_slides) + 1,
                "title": "Classification: Algorithms & Code",
                "readingTime": "1 min",
                "content": '''<div class="two-column">
    <div class="column">
        <div class="highlight">
            <h4>Classification Algorithms</h4>
            <ul>
                <li>Logistic Regression</li>
                <li>Naive Bayes</li>
                <li>K-Nearest Neighbors</li>
                <li>Decision Trees</li>
                <li>Random Forests, SVM</li>
            </ul>
        </div>
    </div>
    <div class="column">
        <div class="example">
            <h4>Loss Functions</h4>
            <p><strong>Cross-Entropy:</strong></p>
            $$\\mathcal{L} = -\\frac{1}{n}\\sum_{i} y_i \\log \\hat{y}_i$$
            <p><strong>Hinge Loss (SVM):</strong></p>
            $$\\mathcal{L} = \\max(0, 1 - y\\hat{y})$$
        </div>
    </div>
</div>

<div class="code-example">
    <h4>Python Example</h4>
    <pre class="code-block"><code class="language-python">from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

clf = RandomForestClassifier(n_estimators=100).fit(X_train, y_train)
print(classification_report(y_test, clf.predict(X_test)))</code></pre>
</div>''',
                "hasVisualization": False,
                "knowledgeCheck": None
            })
            continue

        # Slide 11: Clustering - Split into K-Means + Other methods
        if slide_id == 11:
            # Part 1: Image + K-Means concept
            new_slides.append({
                "id": len(new_slides) + 1,
                "title": "Clustering: Grouping Similar Data",
                "readingTime": "1 min",
                "content": '''<div class="image-text-layout">
    <div class="image-column">
        <figure class="slide-figure">
            <img src="/static/images/courses/cmsc173/module-00/clustering_example.png" alt="K-Means Clustering" style="max-width: 100%;">
            <figcaption>K-Means with 3 Clusters</figcaption>
        </figure>
    </div>
    <div class="text-column">
        <div class="definition">
            <strong>Goal:</strong> Group similar data points without labels
        </div>
        <div class="highlight">
            <h4>K-Means Objective</h4>
            $$\\min \\sum_{i=1}^n \\|\\mathbf{x}_i - \\mu_{c_i}\\|^2$$
            <ol>
                <li>Initialize K centroids</li>
                <li>Assign points to nearest</li>
                <li>Update centroids</li>
                <li>Repeat until convergence</li>
            </ol>
        </div>
    </div>
</div>''',
                "hasVisualization": True,
                "knowledgeCheck": None
            })

            # Part 2: Other methods + Code
            new_slides.append({
                "id": len(new_slides) + 1,
                "title": "Clustering: Methods & Evaluation",
                "readingTime": "1 min",
                "content": '''<div class="two-column">
    <div class="column">
        <div class="highlight">
            <h4>Other Clustering Methods</h4>
            <ul>
                <li><strong>Hierarchical:</strong> Dendrogram</li>
                <li><strong>DBSCAN:</strong> Density-based, finds arbitrary shapes</li>
                <li><strong>GMM:</strong> Probabilistic, soft assignments</li>
            </ul>
        </div>
    </div>
    <div class="column">
        <div class="example">
            <h4>Evaluation Metrics</h4>
            <ul>
                <li>Silhouette coefficient</li>
                <li>Davies-Bouldin index</li>
                <li>Calinski-Harabasz index</li>
            </ul>
        </div>
    </div>
</div>

<div class="code-example">
    <h4>Python Example</h4>
    <pre class="code-block"><code class="language-python">from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

kmeans = KMeans(n_clusters=3).fit(X)
score = silhouette_score(X, kmeans.labels_)
print(f"Silhouette: {score:.3f}")</code></pre>
</div>''',
                "hasVisualization": False,
                "knowledgeCheck": None
            })
            continue

        # Slide 12: Dimensionality Reduction - Split into PCA + Other methods
        if slide_id == 12:
            # Part 1: Image + PCA concept
            new_slides.append({
                "id": len(new_slides) + 1,
                "title": "Dimensionality Reduction",
                "readingTime": "1 min",
                "content": '''<div class="image-text-layout">
    <div class="image-column">
        <figure class="slide-figure">
            <img src="/static/images/courses/cmsc173/module-00/pca_visualization.png" alt="PCA Visualization" style="max-width: 100%;">
            <figcaption>PCA: Principal Components</figcaption>
        </figure>
    </div>
    <div class="text-column">
        <div class="definition">
            <strong>Goal:</strong> Compress high-dim data while preserving structure
        </div>
        <div class="highlight">
            <h4>Curse of Dimensionality</h4>
            <ul>
                <li>Volume grows exponentially</li>
                <li>Data becomes sparse</li>
                <li>Overfitting risk increases</li>
            </ul>
        </div>
    </div>
</div>''',
                "hasVisualization": True,
                "knowledgeCheck": None
            })

            # Part 2: PCA algorithm + Other methods + Code
            new_slides.append({
                "id": len(new_slides) + 1,
                "title": "PCA & Other Techniques",
                "readingTime": "1 min",
                "content": '''<div class="two-column">
    <div class="column">
        <div class="highlight">
            <h4>PCA Algorithm</h4>
            <ol>
                <li>Center data: $\\tilde{\\mathbf{x}}_i = \\mathbf{x}_i - \\bar{\\mathbf{x}}$</li>
                <li>Compute covariance: $\\mathbf{C} = \\frac{1}{n}\\mathbf{X}^T\\mathbf{X}$</li>
                <li>Find eigenvectors of $\\mathbf{C}$</li>
                <li>Project onto top $k$ eigenvectors</li>
            </ol>
        </div>
    </div>
    <div class="column">
        <div class="example">
            <h4>Other Techniques</h4>
            <ul>
                <li><strong>Linear:</strong> PCA, LDA, ICA</li>
                <li><strong>Non-linear:</strong> t-SNE, UMAP</li>
                <li><strong>Neural:</strong> Autoencoders</li>
            </ul>
        </div>
    </div>
</div>

<div class="code-example">
    <h4>Python Example</h4>
    <pre class="code-block"><code class="language-python">from sklearn.decomposition import PCA

pca = PCA(n_components=2).fit(X)
X_reduced = pca.transform(X)
print(f"Variance explained: {pca.explained_variance_ratio_.sum():.2%}")</code></pre>
</div>''',
                "hasVisualization": False,
                "knowledgeCheck": None
            })
            continue

        # Slide 17: Data Preprocessing - Split into Cleaning/Scaling + Engineering
        if slide_id == 17:
            # Part 1: Data Cleaning + Scaling
            new_slides.append({
                "id": len(new_slides) + 1,
                "title": "Data Preprocessing: Cleaning & Scaling",
                "readingTime": "1 min",
                "content": '''<div class="two-column">
    <div class="column">
        <div class="highlight">
            <h4>Data Cleaning</h4>
            <ul>
                <li><strong>Missing values:</strong> Imputation or deletion</li>
                <li><strong>Outliers:</strong> Detect and handle</li>
                <li><strong>Duplicates:</strong> Remove</li>
                <li><strong>Noise:</strong> Filter/smooth</li>
            </ul>
        </div>
    </div>
    <div class="column">
        <div class="highlight">
            <h4>Feature Scaling</h4>
            <p><strong>Z-score:</strong> $z = \\frac{x - \\mu}{\\sigma}$</p>
            <p><strong>Min-Max:</strong> $x' = \\frac{x - \\min}{\\max - \\min}$</p>
            <p><strong>Robust:</strong> Uses median/IQR</p>
        </div>
    </div>
</div>

<div class="warning">
    <h4>Why Scale?</h4>
    <p>Many algorithms (SVM, KNN, gradient descent) are sensitive to feature scales!</p>
</div>''',
                "hasVisualization": False,
                "knowledgeCheck": None
            })

            # Part 2: Feature Engineering + Code
            new_slides.append({
                "id": len(new_slides) + 1,
                "title": "Feature Engineering & Train/Test Split",
                "readingTime": "1 min",
                "content": '''<div class="two-column">
    <div class="column">
        <div class="highlight">
            <h4>Feature Engineering</h4>
            <ul>
                <li>Polynomial features: $x_1 x_2$, $x^2$</li>
                <li>One-hot encoding</li>
                <li>Date/time extraction</li>
                <li>Text vectorization (TF-IDF)</li>
            </ul>
        </div>
    </div>
    <div class="column">
        <div class="example">
            <h4>Train/Test Split</h4>
            <ul>
                <li>Common: 80/20 or 70/30</li>
                <li>Cross-validation (k-fold)</li>
                <li>Time series: temporal split</li>
            </ul>
            <p><strong>Rule:</strong> Never train on test data!</p>
        </div>
    </div>
</div>

<div class="code-example">
    <h4>Python Example</h4>
    <pre class="code-block"><code class="language-python">from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy='mean')
scaler = StandardScaler()
X_clean = scaler.fit_transform(imputer.fit_transform(X))</code></pre>
</div>''',
                "hasVisualization": False,
                "knowledgeCheck": None
            })
            continue

        # Slide 20: Bias-Variance - Split into two slides (one image each)
        if slide_id == 20:
            # Part 1: Bias-Variance Tradeoff image + formula
            new_slides.append({
                "id": len(new_slides) + 1,
                "title": "Bias-Variance Tradeoff",
                "readingTime": "1 min",
                "content": '''<div class="image-text-layout">
    <div class="image-column">
        <figure class="slide-figure">
            <img src="/static/images/courses/cmsc173/module-00/bias_variance_tradeoff.png" alt="Bias-Variance Tradeoff" style="max-width: 100%;">
            <figcaption>The Bias-Variance Tradeoff</figcaption>
        </figure>
    </div>
    <div class="text-column">
        <div class="highlight">
            <h4>Error Decomposition</h4>
            $$\\text{Error} = \\text{Bias}^2 + \\text{Variance} + \\text{Noise}$$
            <ul>
                <li><strong>Bias:</strong> Error from wrong assumptions</li>
                <li><strong>Variance:</strong> Sensitivity to training set</li>
                <li><strong>Noise:</strong> Irreducible error</li>
            </ul>
        </div>
        <div class="example">
            <h4>The Tradeoff</h4>
            <ul>
                <li>Simple models: High bias, low variance</li>
                <li>Complex models: Low bias, high variance</li>
            </ul>
        </div>
    </div>
</div>''',
                "hasVisualization": True,
                "knowledgeCheck": None
            })

            # Part 2: Overfitting vs Underfitting
            new_slides.append({
                "id": len(new_slides) + 1,
                "title": "Underfitting vs Overfitting",
                "readingTime": "1 min",
                "content": '''<div class="image-text-layout">
    <div class="image-column">
        <figure class="slide-figure">
            <img src="/static/images/courses/cmsc173/module-00/overfitting_example.png" alt="Overfitting Example" style="max-width: 100%;">
            <figcaption>Underfitting vs Good Fit vs Overfitting</figcaption>
        </figure>
    </div>
    <div class="text-column">
        <div class="two-column">
            <div class="column">
                <div class="highlight">
                    <h4>Underfitting</h4>
                    <p>High train & test error</p>
                    <p><strong>Fix:</strong></p>
                    <ul>
                        <li>More features</li>
                        <li>Complex model</li>
                        <li>Less regularization</li>
                    </ul>
                </div>
            </div>
            <div class="column">
                <div class="warning">
                    <h4>Overfitting</h4>
                    <p>Low train, high test error</p>
                    <p><strong>Fix:</strong></p>
                    <ul>
                        <li>More data</li>
                        <li>Regularization</li>
                        <li>Simpler model</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>''',
                "hasVisualization": True,
                "knowledgeCheck": None
            })
            continue

        # Keep other slides as-is, just update ID
        slide['id'] = len(new_slides) + 1
        new_slides.append(slide)

    # Update metadata
    data['slides'] = new_slides
    data['module']['totalSlides'] = len(new_slides)
    data['module']['estimatedDuration'] = f"{len(new_slides) * 2} minutes"

    return data


def main():
    input_path = 'static/data/courses/cmsc173/module-00-slides.json'

    print(f"Loading {input_path}...")
    data = load_slides(input_path)
    original_count = len(data['slides'])

    print("Optimizing slides...")
    optimized_data = optimize_slides(data)
    new_count = len(optimized_data['slides'])

    print(f"Saving to {input_path}...")
    save_slides(optimized_data, input_path)

    print(f"\nOptimization complete!")
    print(f"  Original slides: {original_count}")
    print(f"  Optimized slides: {new_count}")
    print(f"  Slides split: {new_count - original_count}")
    print("\nChanges made:")
    print("  - Slide 7 (Supervised Learning) → split into 2 slides")
    print("  - Slide 8 (Regression) → split into 2 slides")
    print("  - Slide 9 (Classification) → split into 2 slides")
    print("  - Slide 11 (Clustering) → split into 2 slides")
    print("  - Slide 12 (Dimensionality Reduction) → split into 2 slides")
    print("  - Slide 17 (Data Preprocessing) → split into 2 slides")
    print("  - Slide 20 (Bias-Variance) → split into 2 slides")
    print("  - Applied image-text-layout for all figure slides")


if __name__ == "__main__":
    main()
