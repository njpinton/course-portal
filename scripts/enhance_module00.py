#!/usr/bin/env python3
"""
Enhance Module 00 slides with proper images, code snippets, and tables.
"""

import json
import re

def load_slides(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_slides(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def replace_figure_placeholder(content, old_path, new_img_html):
    """Replace [Figure: path] with actual img HTML."""
    pattern = rf'<div class="figure"><p><em>\[Figure: {re.escape(old_path)}\]</em></p></div>'
    return re.sub(pattern, new_img_html, content)

def make_img(src, alt, caption=None, width=80):
    """Generate figure HTML."""
    cap = f'<figcaption>{caption}</figcaption>' if caption else ''
    return f'''<figure class="slide-figure">
<img src="{src}" alt="{alt}" style="max-width: {width}%;">
{cap}
</figure>'''

def make_code_block(code, language="python"):
    """Generate syntax-highlighted code block."""
    return f'<pre class="code-block"><code class="language-{language}">{code}</code></pre>'

def make_table(headers, rows):
    """Generate HTML table."""
    header_html = ''.join(f'<th>{h}</th>' for h in headers)
    rows_html = ''.join(
        '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
        for row in rows
    )
    return f'''<table class="comparison-table">
<thead><tr>{header_html}</tr></thead>
<tbody>{rows_html}</tbody>
</table>'''

def enhance_slides(data):
    """Apply all enhancements to slides."""
    slides = data['slides']

    # Image mappings: old path -> (new src, alt, caption, width)
    image_map = {
        '../figures/aihistory.jpg': ('/static/images/courses/cmsc173/module-00/aihistory.jpg', 'AI History Timeline', 'History of AI and Machine Learning', 75),
        '../figures/mlapps.jpg': ('/static/images/courses/cmsc173/module-00/mlapps.jpg', 'ML Applications', 'Machine Learning Applications', 85),
        '../figures/supervised.jpg': ('/static/images/courses/cmsc173/module-00/supervised_vs_unsupervised.png', 'Supervised vs Unsupervised', 'Supervised vs Unsupervised Learning', 90),
        '../figures/regression.jpg': ('/static/images/courses/cmsc173/module-00/regression_example.png', 'Regression Example', 'Linear Regression with Fitted Line', 85),
        '../figures/classification.jpg': ('/static/images/courses/cmsc173/module-00/classification_example.png', 'Classification Example', 'Classification with Decision Boundary', 85),
        '../figures/clustering.jpg': ('/static/images/courses/cmsc173/module-00/clustering_example.png', 'Clustering Example', 'K-Means Clustering with Centroids', 85),
        '../figures/dimension.jpg': ('/static/images/courses/cmsc173/module-00/pca_visualization.png', 'PCA Visualization', 'Principal Component Analysis', 90),
        '../figures/robot.jpg': ('/static/images/courses/cmsc173/module-00/robot.jpg', 'Reinforcement Learning Robot', 'RL Agent Interacting with Environment', 70),
        '../figures/dataprep.jpg': ('/static/images/courses/cmsc173/module-00/dataprep.jpg', 'Data Preprocessing', 'Data Preprocessing Pipeline', 75),
        '../figures/workflow.jpg': ('/static/images/courses/cmsc173/module-00/ml_workflow_diagram.png', 'ML Workflow', 'Machine Learning Workflow', 95),
        '../figures/ethics.jpg': ('/static/images/courses/cmsc173/module-00/ethics.jpg', 'AI Ethics', 'Ethical Considerations in AI', 75),
    }

    for slide in slides:
        content = slide['content']

        # Replace image placeholders
        for old_path, (new_src, alt, caption, width) in image_map.items():
            img_html = make_img(new_src, alt, caption, width)
            content = replace_figure_placeholder(content, old_path, img_html)

        slide['content'] = content

    # Add code snippets to specific slides

    # Slide 2: What is ML - add comparison table
    slides[1]['content'] += '''

<div class="code-example">
<h4>Traditional Programming vs ML</h4>
''' + make_table(
    ['Aspect', 'Traditional', 'Machine Learning'],
    [
        ['Input', 'Rules + Data', 'Data + Labels'],
        ['Output', 'Answers', 'Rules/Model'],
        ['Example', 'if price > 1000: expensive', 'Learn threshold from examples'],
    ]
) + '''
</div>'''

    # Slide 7: Supervised Learning - add sklearn code
    slides[6]['content'] += '''

<div class="code-example">
<h4>Python Example: Supervised Learning</h4>
''' + make_code_block('''from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, predictions):.2f}")''') + '''
</div>'''

    # Slide 8: Regression - add sklearn code
    slides[7]['content'] += '''

<div class="code-example">
<h4>Python Example: Linear Regression</h4>
''' + make_code_block('''from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Create and train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"MSE: {mse:.4f}, R²: {r2:.4f}")''') + '''
</div>'''

    # Slide 9: Classification - add sklearn code
    slides[8]['content'] += '''

<div class="code-example">
<h4>Python Example: Classification</h4>
''' + make_code_block('''from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Train classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict and evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))''') + '''
</div>'''

    # Slide 10: Unsupervised - add comparison table
    slides[9]['content'] += '''

<div class="code-example">
<h4>Supervised vs Unsupervised Comparison</h4>
''' + make_table(
    ['Aspect', 'Supervised', 'Unsupervised'],
    [
        ['Data', 'Labeled (X, y)', 'Unlabeled (X only)'],
        ['Goal', 'Predict y from X', 'Find hidden patterns'],
        ['Evaluation', 'Compare to true labels', 'Internal metrics'],
        ['Examples', 'Classification, Regression', 'Clustering, PCA'],
    ]
) + '''
</div>'''

    # Slide 11: Clustering - add sklearn code
    slides[10]['content'] += '''

<div class="code-example">
<h4>Python Example: K-Means Clustering</h4>
''' + make_code_block('''from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Fit K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)

# Evaluate clustering quality
score = silhouette_score(X, clusters)
print(f"Silhouette Score: {score:.3f}")

# Get cluster centers
centers = kmeans.cluster_centers_''') + '''
</div>'''

    # Slide 12: Dimensionality Reduction - add sklearn code
    slides[11]['content'] += '''

<div class="code-example">
<h4>Python Example: PCA</h4>
''' + make_code_block('''from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Reduce to 2 dimensions
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

# Check variance explained
print(f"Variance explained: {pca.explained_variance_ratio_}")

# Visualize
plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()''') + '''
</div>'''

    # Slide 17: Data Preprocessing - add sklearn code
    slides[16]['content'] += '''

<div class="code-example">
<h4>Python Example: Data Preprocessing</h4>
''' + make_code_block('''from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import pandas as pd

# Handle missing values
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Scale features (Z-score normalization)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Encode categorical labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)''') + '''
</div>'''

    # Slide 19: Model Evaluation - add metrics table
    slides[18]['content'] += '''

<div class="code-example">
<h4>When to Use Each Metric</h4>
''' + make_table(
    ['Metric', 'Use When', 'Avoid When'],
    [
        ['Accuracy', 'Balanced classes', 'Imbalanced data'],
        ['Precision', 'False positives costly', 'Need recall'],
        ['Recall', 'False negatives costly', 'Need precision'],
        ['F1-Score', 'Balance precision/recall', 'Clear preference'],
        ['RMSE', 'Penalize large errors', 'Robust to outliers'],
        ['MAE', 'All errors equal', 'Large errors matter'],
    ]
) + '''
</div>'''

    # Slide 20: Bias-Variance - add visualization reference
    slides[19]['content'] = '''<figure class="slide-figure">
<img src="/static/images/courses/cmsc173/module-00/bias_variance_tradeoff.png" alt="Bias-Variance Tradeoff" style="max-width: 90%;">
<figcaption>Bias-Variance Tradeoff: Finding the Sweet Spot</figcaption>
</figure>

<figure class="slide-figure">
<img src="/static/images/courses/cmsc173/module-00/overfitting_example.png" alt="Overfitting Example" style="max-width: 95%;">
<figcaption>Underfitting vs Good Fit vs Overfitting</figcaption>
</figure>

''' + slides[19]['content']

    slides[19]['hasVisualization'] = True

    # Slide 21: Regularization - add code
    slides[20]['content'] += '''

<div class="code-example">
<h4>Python Example: Ridge and Lasso</h4>
''' + make_code_block('''from sklearn.linear_model import Ridge, Lasso, ElasticNet

# Ridge (L2 regularization)
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)

# Lasso (L1 regularization)
lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)

# Elastic Net (L1 + L2)
elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)
elastic.fit(X_train, y_train)

# Lasso creates sparse solutions (feature selection)
print(f"Non-zero coefficients: {sum(lasso.coef_ != 0)}")''') + '''
</div>'''

    return data


def main():
    input_path = 'static/data/courses/cmsc173/module-00-slides.json'
    output_path = 'static/data/courses/cmsc173/module-00-slides.json'

    print(f"Loading {input_path}...")
    data = load_slides(input_path)

    print("Enhancing slides with images, code, and tables...")
    enhanced_data = enhance_slides(data)

    print(f"Saving to {output_path}...")
    save_slides(enhanced_data, output_path)

    print("Done! Module 00 slides enhanced with:")
    print("  - 11 proper image references")
    print("  - 8 Python code examples")
    print("  - 3 comparison tables")
    print("  - Bias-variance visualizations")


if __name__ == "__main__":
    main()
