# CMSC 178DA: Data Analytics
## Complete Slide Outlines (24 Lectures)

---

# WEEK 1: Foundations & The Data Science Lifecycle

---

## Lecture 1: Introduction to Data Analytics

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 1: Introduction to Data Analytics
- University of the Philippines Cebu

### Slide 2: Learning Objectives
By the end of this lecture, you will be able to:
1. Define data analytics and distinguish it from related fields
2. Explain the data science lifecycle and its five key facets
3. Identify real-world applications of data analytics
4. Understand the role of a data analyst in organizations

### Slide 3: What is Data Analytics?
- **Definition**: The science of analyzing raw data to make conclusions and decisions
- **Key distinction**:
  - Data Analytics: Focus on describing what happened and why
  - Data Science: Broader scope including ML and AI
  - Business Intelligence: Operational reporting and dashboards
- **Visual**: Venn diagram showing overlap

### Slide 4: The Evolution of Analytics
- **Timeline visual**:
  - 1960s: Business reporting
  - 1990s: Data warehousing
  - 2000s: Business intelligence
  - 2010s: Big data & predictive analytics
  - 2020s: AI-augmented analytics
- **Philippine context**: BPO industry growth driving analytics demand

### Slide 5: The Analytics Spectrum
| Type | Question | Example |
|------|----------|---------|
| Descriptive | What happened? | Sales report |
| Diagnostic | Why did it happen? | Root cause analysis |
| Predictive | What will happen? | Demand forecasting |
| Prescriptive | What should we do? | Optimization |
- **Visual**: Pyramid showing complexity vs. value

### Slide 6: The Data Science Lifecycle (Harvard CS109)
**Five Key Facets**:
1. **Data Collection** - Wrangling, cleaning, sampling
2. **Data Management** - Storage, access, reliability
3. **Exploratory Data Analysis** - Hypotheses, intuition
4. **Prediction/Inference** - Models, algorithms
5. **Communication** - Visualization, storytelling

### Slide 7: Data Collection
- **Sources**: APIs, databases, web scraping, surveys, IoT sensors
- **Philippine example**: PSA collecting census data
- **Challenges**:
  - Data quality issues
  - Missing values
  - Inconsistent formats
- **Code preview**: `pd.read_csv()`, `requests.get()`

### Slide 8: Data Management
- **Storage options**: CSV, databases (SQL), cloud (BigQuery, S3)
- **Key considerations**:
  - Scalability
  - Query performance
  - Data governance
- **Philippine context**: Government data portals (OpenSTAT)

### Slide 9: Exploratory Data Analysis (EDA)
- **Purpose**: Understand data before modeling
- **Key activities**:
  - Summary statistics
  - Distribution analysis
  - Correlation exploration
  - Outlier detection
- **Visual**: Example EDA output with histograms

### Slide 10: Prediction & Inference
- **Statistical inference**: Drawing conclusions about populations
- **Machine learning** (refresher): Supervised, unsupervised, reinfortic
- **Key difference**: Inference explains; prediction forecasts
- **Note**: You've covered ML - this course focuses on interpretation

### Slide 11: Communication
- **The most important facet** (often neglected)
- **Components**:
  - Data visualization
  - Storytelling with data
  - Dashboards and reports
  - Stakeholder presentations
- **Quote**: "The goal is not to build models, it's to drive decisions"

### Slide 12: Case Study - Moneyball
- **Context**: Oakland Athletics (2002)
- **Problem**: Limited budget, competing with rich teams
- **Analytics approach**:
  - Identified undervalued statistics (OBP)
  - Built team using data, not scouts' intuition
  - Result: 20-game winning streak, playoffs
- **Lesson**: Data can provide competitive advantage

### Slide 13: Analytics in the Philippines
**Industry Applications**:
| Industry | Application | Company Example |
|----------|-------------|-----------------|
| Finance | Credit scoring | BDO, BPI |
| Retail | Demand forecasting | SM, Puregold |
| Telecom | Churn prediction | Globe, Smart |
| Fintech | Fraud detection | GCash, Maya |
| Transport | Route optimization | Grab, Angkas |

### Slide 14: The Data Analyst Role
**Skills required**:
- **Technical**: Python/R, SQL, visualization tools
- **Statistical**: Probability, hypothesis testing, regression
- **Business**: Domain knowledge, communication, problem-solving

**Career paths**: Analyst → Senior Analyst → Lead → Manager → Director/CDO

### Slide 15: Course Overview
**12 Weeks of Learning**:
- Weeks 1-2: Foundations & Statistics
- Weeks 3-4: Data Wrangling & EDA
- Weeks 5-6: Visualization & Storytelling
- Weeks 7-8: Regression & Trees (ML Refresher)
- Weeks 9-10: Clustering & Time Series
- Weeks 11-12: Text Analytics & Capstone

### Slide 16: Assessment Structure
| Component | Weight |
|-----------|--------|
| Weekly Labs | 25% |
| Midterm Exam | 20% |
| Quizzes (3) | 15% |
| Capstone Project | 30% |
| Participation | 10% |

### Slide 17: Tools We'll Use
- **Programming**: Python (pandas, numpy, scikit-learn)
- **Visualization**: matplotlib, seaborn, Plotly
- **Dashboards**: Streamlit or Tableau Public
- **Environment**: Jupyter Notebooks, Google Colab
- **Version Control**: GitHub

### Slide 18: Philippine Data Sources
**We'll use real Philippine data throughout this course**

| Source | Data Types | URL |
|--------|------------|-----|
| PSA OpenSTAT | GDP, population, labor | openstat.psa.gov.ph |
| BSP Statistics | Exchange rates, remittances | bsp.gov.ph/statistics |
| PAGASA | Weather, typhoons | bagong.pagasa.dost.gov.ph |
| DOH | Health, COVID-19 | doh.gov.ph |
| PSE | Stock prices | edge.pse.com.ph |

**Full dataset guide**: [Philippine Datasets Reference](philippine-datasets.md)

### Slide 19: Live Demo - First Look at Data
```python
import pandas as pd

# Load Philippine GDP data
df = pd.read_csv('ph_gdp_quarterly.csv')

# Quick exploration
print(df.shape)  # Rows, columns
print(df.head())  # First 5 rows
print(df.describe())  # Summary statistics
```

### Slide 20: In-Class Activity
**Task** (10 minutes):
1. Open Google Colab
2. Load a sample dataset
3. Answer: How many rows? Columns? Any missing values?
4. Share one interesting observation

### Slide 21: Key Takeaways
1. Data analytics transforms raw data into actionable insights
2. The lifecycle has 5 facets: Collect → Manage → Explore → Predict → Communicate
3. Communication is often the most critical (and neglected) facet
4. Philippines has growing demand for analytics skills
5. This course balances theory, tools, and Philippine context

### Slide 22: Next Lecture Preview
**Lecture 2: The Analytics Edge in Industry**
- More case studies: Netflix, Spotify, healthcare
- Ethics in data analytics
- Philippine industry deep dive

### Slide 23: References
- MIT OpenCourseWare: The Analytics Edge
- Harvard CS109 Course Materials
- Davenport, T. (2006). Competing on Analytics

---

## Lecture 2: The Analytics Edge in Industry

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 2: The Analytics Edge in Industry
- Week 1, Session 2

### Slide 2: Learning Objectives
1. Analyze real-world case studies of analytics impact
2. Understand how different industries apply analytics
3. Recognize ethical considerations in data analytics
4. Identify analytics opportunities in Philippine context

### Slide 3: Recap - The Analytics Lifecycle
- Quick visual refresher of 5 facets
- Today's focus: Real-world applications

### Slide 4: Case Study 1 - Netflix Recommendations
**The Problem**:
- 200+ million subscribers
- Thousands of titles
- How to keep users engaged?

**The Analytics Solution**:
- Collaborative filtering
- Content-based recommendations
- A/B testing everything
- **Result**: 80% of watched content from recommendations

### Slide 5: Netflix - Technical Deep Dive
**Data used**:
- Viewing history
- Time of day/week
- Device type
- Pause/rewind behavior
- Thumbnail click-through rates

**Impact**: $1 billion/year saved in customer retention

### Slide 6: Case Study 2 - Spotify Wrapped
**Why it works**:
- Personalization at scale
- Creates shareable content (free marketing)
- Drives engagement spike in December

**Analytics behind it**:
- Listening pattern analysis
- Genre classification
- Temporal patterns
- Social comparison

### Slide 7: Case Study 3 - Healthcare Analytics
**Framingham Heart Study** (MIT Analytics Edge):
- Started 1948, still ongoing
- 5,000+ participants tracked for decades
- **Discovery**: Link between cholesterol, blood pressure, and heart disease
- **Impact**: Changed medical practice worldwide

### Slide 8: Case Study 4 - E-commerce
**Amazon's Analytics**:
- "Customers who bought X also bought Y"
- Dynamic pricing
- Warehouse optimization
- Delivery time prediction

**Result**: 35% of revenue from recommendations

### Slide 9: Philippine Case Study - GCash
**Context**:
- 81 million registered users (2023)
- Largest mobile wallet in PH

**Analytics Applications**:
- Fraud detection (real-time)
- Credit scoring (GScore)
- User segmentation
- Transaction pattern analysis

### Slide 10: Philippine Case Study - Grab
**Analytics Use Cases**:
| Function | Analytics Application |
|----------|----------------------|
| Pricing | Surge prediction |
| Matching | Driver-rider optimization |
| ETA | Traffic pattern analysis |
| Safety | Anomaly detection |

### Slide 11: Philippine Case Study - SM Retail
**Retail Analytics**:
- Basket analysis: What products are bought together?
- Store layout optimization
- Inventory management
- Customer loyalty (SM Advantage)

### Slide 12: Industry Analytics Maturity
**Visual**: Analytics maturity model
| Level | Description | % of PH Companies |
|-------|-------------|-------------------|
| 1 | Ad-hoc reporting | 40% |
| 2 | Standardized BI | 35% |
| 3 | Predictive analytics | 20% |
| 4 | AI-driven decisions | 5% |

### Slide 13: Ethics in Data Analytics
**Key Ethical Concerns**:
1. **Privacy**: What data should be collected?
2. **Consent**: Did users agree to this use?
3. **Bias**: Are models fair to all groups?
4. **Transparency**: Can decisions be explained?

### Slide 14: Case Study - Algorithmic Bias
**COMPAS Recidivism Algorithm** (USA):
- Used to predict criminal reoffending
- ProPublica analysis found racial bias
- Black defendants: Higher false positive rate
- **Lesson**: Models inherit biases from data

### Slide 15: Philippine Data Privacy Act (RA 10173)
**Key Provisions**:
- Consent required for data collection
- Right to access personal data
- Right to erasure
- Penalties for violations

**Implications for analysts**:
- Anonymization requirements
- Data minimization principle
- Security obligations

### Slide 16: Ethical Framework for Analysts
**Questions to ask**:
1. Is the data collected ethically?
2. Could this analysis harm any group?
3. Are the results interpretable and explainable?
4. What could go wrong if the model is wrong?
5. Who benefits? Who might be harmed?

### Slide 17: The Analytics Job Market
**Global Demand**:
- 35% projected growth (2022-2032)
- Shortage of qualified analysts

**Philippines**:
- BPO industry driving demand
- Fintech boom creating opportunities
- Average salary: PHP 40,000-80,000/month (entry-level)

### Slide 18: Skills in Demand
**Technical Skills**:
1. Python/R programming
2. SQL and databases
3. Data visualization
4. Statistical analysis
5. Machine learning basics

**Soft Skills**:
1. Communication
2. Business acumen
3. Problem-solving
4. Storytelling

### Slide 19: In-Class Discussion
**Group Activity** (10 minutes):
1. Form groups of 3-4
2. Choose a Philippine company/industry
3. Identify ONE analytics opportunity
4. Present in 2 minutes

**Prompt**: "How could [company] use data to improve [specific outcome]?"

### Slide 20: Key Takeaways
1. Analytics provides competitive advantage across industries
2. Netflix, Spotify, Amazon: Recommendations drive revenue
3. Philippine companies (GCash, Grab, SM) actively using analytics
4. Ethics must be central to analytics practice
5. Growing job market with skills shortage

### Slide 21: Lab Preview
**Lab 1: Introduction to Python for Analytics**
- Setting up environment
- Loading Philippine economic data
- Basic exploration with pandas
- First visualization

### Slide 22: References
- MIT Analytics Edge Case Studies
- ProPublica COMPAS Analysis
- Philippine Data Privacy Act (RA 10173)
- GCash Annual Reports

---

# WEEK 2: Probability & Statistical Foundations

---

## Lecture 3: Probability Review for Data Scientists

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 3: Probability Review for Data Scientists
- Week 2, Session 1

### Slide 2: Learning Objectives
1. Review fundamental probability concepts
2. Apply Bayes' theorem to real-world problems
3. Understand common probability distributions
4. Connect probability to data analytics applications

### Slide 3: Why Probability Matters
- **Uncertainty is everywhere**: Will this customer churn?
- **Data is noisy**: Measurements have errors
- **Samples, not populations**: We rarely have all data
- **Foundation for**: Hypothesis testing, ML, inference

### Slide 4: Basic Probability Rules
**Definitions**:
- **Sample space (S)**: All possible outcomes
- **Event (A)**: Subset of outcomes
- **P(A)**: Probability of event A, 0 ≤ P(A) ≤ 1

**Rules**:
- P(S) = 1
- P(A') = 1 - P(A)
- P(A ∪ B) = P(A) + P(B) - P(A ∩ B)

### Slide 5: Conditional Probability
**Definition**: P(A|B) = P(A ∩ B) / P(B)

**Example**:
- 60% of GCash users are under 35
- 80% of under-35 users use GCredit
- P(GCredit | Under 35) = 0.80

**Visual**: Venn diagram illustration

### Slide 6: Independence
**Definition**: A and B are independent if P(A ∩ B) = P(A) × P(B)

**Example**:
- P(Rain tomorrow) = 0.3
- P(Stock market up) = 0.5
- If independent: P(Rain AND Market up) = 0.15

**Caution**: Independence is often assumed but rarely true

### Slide 7: Bayes' Theorem
$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$

**Components**:
- P(A|B): Posterior probability
- P(B|A): Likelihood
- P(A): Prior probability
- P(B): Evidence

### Slide 8: Bayes' Theorem Example
**Problem**: Medical test for disease
- Disease prevalence: 1% (prior)
- Test sensitivity: 95% (true positive rate)
- Test specificity: 90% (true negative rate)

If test is positive, what's the probability of having disease?

### Slide 9: Bayes' Calculation
Given: P(D) = 0.01, P(+|D) = 0.95, P(+|D') = 0.10

$$P(D|+) = \frac{P(+|D) \cdot P(D)}{P(+)}$$

P(+) = P(+|D)P(D) + P(+|D')P(D')
P(+) = 0.95(0.01) + 0.10(0.99) = 0.1085

$$P(D|+) = \frac{0.95 \times 0.01}{0.1085} = 0.088$$

**Result**: Only 8.8% chance of disease!

### Slide 10: Random Variables
**Discrete**: Countable outcomes
- Number of transactions per day
- Customer complaints count

**Continuous**: Infinite possible values
- Transaction amount
- Customer lifetime value

### Slide 11: Expected Value & Variance
**Expected Value (Mean)**:
$$E[X] = \sum x \cdot P(X=x)$$ (discrete)
$$E[X] = \int x \cdot f(x) dx$$ (continuous)

**Variance**: $$Var(X) = E[(X - \mu)^2] = E[X^2] - (E[X])^2$$

### Slide 12: Common Discrete Distributions
| Distribution | Use Case | Parameters |
|--------------|----------|------------|
| Bernoulli | Single binary outcome | p |
| Binomial | Count of successes in n trials | n, p |
| Poisson | Count of rare events | λ |
| Geometric | Trials until first success | p |

### Slide 13: Binomial Distribution
**When to use**: Counting successes in fixed trials

**Example**: 10 loan applications, 30% approval rate
$$P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}$$

```python
from scipy.stats import binom
# P(exactly 5 approvals)
binom.pmf(5, n=10, p=0.3)  # ≈ 0.103
```

### Slide 14: Poisson Distribution
**When to use**: Rare events in fixed time/space

**Example**: Website receives avg 20 visits/hour
$$P(X=k) = \frac{\lambda^k e^{-\lambda}}{k!}$$

```python
from scipy.stats import poisson
# P(exactly 25 visits)
poisson.pmf(25, mu=20)  # ≈ 0.045
```

### Slide 15: Normal Distribution
**The most important distribution**

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

**Properties**:
- Symmetric, bell-shaped
- Mean = Median = Mode
- 68-95-99.7 rule

### Slide 16: 68-95-99.7 Rule
**Visual**: Bell curve with shaded regions
- 68% within 1σ
- 95% within 2σ
- 99.7% within 3σ

**Application**: Outlier detection
- Values beyond 3σ are unusual

### Slide 17: Central Limit Theorem
**The most important theorem in statistics**

"The sampling distribution of the mean approaches normal as sample size increases, regardless of population distribution"

**Implications**:
- Can use normal-based methods for large samples
- Foundation for hypothesis testing

### Slide 18: CLT Demonstration
```python
import numpy as np
import matplotlib.pyplot as plt

# Exponential population (not normal)
pop = np.random.exponential(scale=2, size=100000)

# Sample means (n=30)
means = [np.random.choice(pop, 30).mean() for _ in range(1000)]

# Plot shows normal shape!
plt.hist(means, bins=30)
```

### Slide 19: Philippine Application
**BPI Credit Card Fraud Detection**:
- Transaction amounts follow log-normal distribution
- Unusual amounts flagged using z-scores
- Bayes' theorem to update fraud probability

**Visual**: Transaction amount distribution

### Slide 20: In-Class Exercise
**Problem**:
- 5% of GCash transactions are flagged for review
- Of flagged transactions, 20% are actually fraudulent
- Of non-flagged transactions, 0.1% are fraudulent

Calculate: P(Fraudulent | Flagged) using Bayes' theorem

### Slide 21: Key Takeaways
1. Probability quantifies uncertainty in data
2. Bayes' theorem updates beliefs with new evidence
3. Different distributions fit different data types
4. CLT enables normal-based inference
5. These concepts underpin all statistical analysis

### Slide 22: Next Lecture
**Lecture 4: Statistical Inference Essentials**
- Hypothesis testing
- Confidence intervals
- A/B testing framework

---

## Lecture 4: Statistical Inference Essentials

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 4: Statistical Inference Essentials
- Week 2, Session 2

### Slide 2: Learning Objectives
1. Conduct and interpret hypothesis tests
2. Construct and interpret confidence intervals
3. Apply A/B testing framework
4. Recognize limitations of p-values

### Slide 3: What is Statistical Inference?
**Definition**: Drawing conclusions about populations from samples

**Two main approaches**:
1. **Estimation**: What's the value? (confidence intervals)
2. **Testing**: Is there an effect? (hypothesis tests)

### Slide 4: The Logic of Hypothesis Testing
**Steps**:
1. State null hypothesis (H₀) and alternative (H₁)
2. Choose significance level (α)
3. Collect data and calculate test statistic
4. Compute p-value
5. Make decision: Reject or fail to reject H₀

### Slide 5: Null vs Alternative Hypothesis
**Null Hypothesis (H₀)**: Status quo, no effect
- "There is no difference between groups"
- "The parameter equals [value]"

**Alternative Hypothesis (H₁)**: What we're testing for
- "There is a difference"
- "The parameter is not equal to [value]"

### Slide 6: Types of Errors
|  | H₀ True | H₀ False |
|--|---------|----------|
| **Reject H₀** | Type I Error (α) | Correct! |
| **Fail to Reject** | Correct! | Type II Error (β) |

**Power** = 1 - β = P(Reject H₀ | H₀ False)

### Slide 7: The p-value
**Definition**: Probability of observing data as extreme as ours, assuming H₀ is true

**Interpretation**:
- Small p-value (< α): Evidence against H₀
- Large p-value: Not enough evidence against H₀

**Common α**: 0.05, 0.01, 0.10

### Slide 8: t-test: Comparing Means
**One-sample t-test**: Compare sample mean to known value
$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

**Two-sample t-test**: Compare two group means
$$t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{s_p^2(1/n_1 + 1/n_2)}}$$

### Slide 9: t-test Example
**Problem**: Do Grab drivers in Cebu earn more than Manila?

```python
from scipy.stats import ttest_ind

cebu_earnings = [850, 920, 780, ...]  # daily PHP
manila_earnings = [800, 850, 750, ...]

t_stat, p_value = ttest_ind(cebu_earnings, manila_earnings)
print(f"t = {t_stat:.3f}, p = {p_value:.3f}")
```

### Slide 10: Chi-Square Test
**Purpose**: Test independence of categorical variables

**Example**: Is payment method independent of age group?

| | Cash | GCash | Card |
|--|------|-------|------|
| Under 30 | 50 | 120 | 30 |
| 30-50 | 80 | 90 | 50 |
| Over 50 | 100 | 40 | 60 |

### Slide 11: Chi-Square Calculation
$$\chi^2 = \sum \frac{(O - E)^2}{E}$$

```python
from scipy.stats import chi2_contingency

table = [[50, 120, 30], [80, 90, 50], [100, 40, 60]]
chi2, p, dof, expected = chi2_contingency(table)
print(f"Chi-square = {chi2:.2f}, p = {p:.4f}")
```

### Slide 12: Confidence Intervals
**Definition**: Range likely to contain true parameter

**For mean**: $$\bar{x} \pm t_{\alpha/2} \cdot \frac{s}{\sqrt{n}}$$

**Interpretation**: 95% CI means if we repeated sampling, 95% of intervals would contain true mean

### Slide 13: CI Example
**Problem**: Estimate average transaction amount on GCash

```python
import numpy as np
from scipy import stats

transactions = [...]  # sample data
mean = np.mean(transactions)
se = stats.sem(transactions)
ci = stats.t.interval(0.95, len(transactions)-1, mean, se)
print(f"95% CI: ({ci[0]:.2f}, {ci[1]:.2f})")
```

### Slide 14: A/B Testing Framework
**Definition**: Controlled experiment comparing two versions

**Steps**:
1. Define metric (conversion, CTR, revenue)
2. Calculate required sample size
3. Randomly assign users to A or B
4. Run experiment for set duration
5. Analyze results with statistical test

### Slide 15: A/B Test Sample Size
**Key factors**:
- Baseline conversion rate
- Minimum detectable effect (MDE)
- Statistical power (typically 80%)
- Significance level (typically 5%)

```python
from statsmodels.stats.power import proportion_effectsize, tt_ind_solve_power

effect = proportion_effectsize(0.10, 0.12)  # 10% to 12%
n = tt_ind_solve_power(effect, alpha=0.05, power=0.8)
```

### Slide 16: A/B Test Example
**Scenario**: Lazada tests new checkout button

- Control (A): Blue button, 10% conversion
- Treatment (B): Green button, 11% conversion
- Sample: 10,000 users each

**Result**: p = 0.04 → Green button wins!

### Slide 17: Multiple Testing Problem
**Problem**: Running many tests increases false positives

**10 tests at α = 0.05**:
- P(at least one false positive) = 1 - 0.95¹⁰ = 40%!

**Solutions**:
- Bonferroni correction: α' = α/n
- False Discovery Rate (FDR)

### Slide 18: p-value Criticisms
**Common misinterpretations**:
- ❌ P-value is probability H₀ is true
- ❌ 1 - p = probability effect exists
- ❌ p < 0.05 means practically significant

**Better practice**:
- Report effect sizes
- Use confidence intervals
- Consider practical significance

### Slide 19: Effect Size
**Why it matters**: Statistical significance ≠ practical significance

**Common measures**:
- Cohen's d: (mean₁ - mean₂) / pooled SD
- Correlation coefficient (r)
- Odds ratio

**Guideline**: d = 0.2 (small), 0.5 (medium), 0.8 (large)

### Slide 20: In-Class Exercise
**A/B Test Analysis**:
- Control: 500 users, 45 conversions (9%)
- Treatment: 500 users, 60 conversions (12%)

Tasks:
1. Conduct chi-square test
2. Calculate 95% CI for difference
3. Is this practically significant?

### Slide 21: Key Takeaways
1. Hypothesis testing quantifies evidence against null
2. p-value is NOT probability of truth
3. Confidence intervals provide range estimates
4. A/B testing is gold standard for causal inference
5. Effect size matters as much as significance

### Slide 22: Lab Preview
**Lab 2: Statistical Testing in Python**
- t-tests on Philippine salary data
- Chi-square on demographic data
- Building an A/B test simulator

---

# WEEK 3: Data Wrangling & Cleaning

---

## Lecture 5: Data Collection & Acquisition

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 5: Data Collection & Acquisition
- Week 3, Session 1

### Slide 2: Learning Objectives
1. Identify various data sources and acquisition methods
2. Write SQL queries for data extraction
3. Use APIs to collect data programmatically
4. Understand data formats and conversions

### Slide 3: The Data Collection Landscape
**Data Sources**:
- Databases (relational, NoSQL)
- APIs (REST, GraphQL)
- Files (CSV, JSON, Excel, Parquet)
- Web scraping
- IoT devices and sensors
- Surveys and forms

### Slide 4: Philippine Data Sources
| Source | Type | Access |
|--------|------|--------|
| PSA OpenSTAT | Government statistics | Free API |
| BSP Statistics | Financial data | CSV downloads |
| PAGASA | Weather data | API/Files |
| SEC EDGE | Stock market | Paid API |
| Data.gov.ph | Open government | Various |

### Slide 5: SQL Fundamentals
**Why SQL matters**: Universal language for databases

**Basic structure**:
```sql
SELECT columns
FROM table
WHERE conditions
GROUP BY grouping
ORDER BY sorting
```

### Slide 6: SELECT and FROM
```sql
-- Select specific columns
SELECT customer_id, name, total_purchases
FROM customers;

-- Select all columns
SELECT * FROM orders;

-- Alias columns
SELECT customer_id AS id,
       total_purchases AS purchases
FROM customers;
```

### Slide 7: WHERE Clause
```sql
-- Filtering data
SELECT * FROM transactions
WHERE amount > 10000;

-- Multiple conditions
SELECT * FROM transactions
WHERE amount > 10000
  AND transaction_date >= '2024-01-01';

-- IN operator
SELECT * FROM customers
WHERE region IN ('NCR', 'Cebu', 'Davao');
```

### Slide 8: JOINs
**Visual**: Venn diagrams for each join type

```sql
-- INNER JOIN: matching rows only
SELECT o.order_id, c.name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;

-- LEFT JOIN: all from left + matches
SELECT c.name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;
```

### Slide 9: Aggregations
```sql
-- COUNT, SUM, AVG, MIN, MAX
SELECT
    region,
    COUNT(*) as num_customers,
    AVG(total_purchases) as avg_purchases,
    SUM(total_purchases) as total_revenue
FROM customers
GROUP BY region
HAVING AVG(total_purchases) > 5000;
```

### Slide 10: Subqueries
```sql
-- Find customers above average
SELECT name, total_purchases
FROM customers
WHERE total_purchases > (
    SELECT AVG(total_purchases) FROM customers
);

-- Find top 10% customers
SELECT * FROM customers
WHERE total_purchases >= (
    SELECT PERCENTILE_CONT(0.9)
    WITHIN GROUP (ORDER BY total_purchases)
    FROM customers
);
```

### Slide 11: APIs for Data Collection
**REST API basics**:
- GET: Retrieve data
- POST: Send data
- Response formats: JSON, XML

```python
import requests

url = "https://api.openstat.psa.gov.ph/data"
response = requests.get(url, params={'dataset': 'population'})
data = response.json()
```

### Slide 12: API Authentication
**Common methods**:
- API keys (query parameter or header)
- OAuth 2.0
- Basic authentication

```python
headers = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}
response = requests.get(url, headers=headers)
```

### Slide 13: Web Scraping Basics
**When to use**: No API available, public data

```python
from bs4 import BeautifulSoup
import requests

url = "https://example.com/data"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find elements
table = soup.find('table', {'class': 'data-table'})
rows = table.find_all('tr')
```

### Slide 14: Web Scraping Ethics
**Best practices**:
- Check robots.txt
- Respect rate limits
- Don't overload servers
- Check terms of service
- Cite your source

**Philippine legal note**: Data Privacy Act applies

### Slide 15: Data Formats
| Format | Pros | Cons |
|--------|------|------|
| CSV | Simple, universal | No schema, large files |
| JSON | Nested data, readable | Verbose |
| Parquet | Compressed, fast | Binary format |
| Excel | Familiar | Limited rows |

### Slide 16: Reading Different Formats
```python
import pandas as pd

# CSV
df_csv = pd.read_csv('data.csv')

# JSON
df_json = pd.read_json('data.json')

# Excel
df_excel = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# Parquet
df_parquet = pd.read_parquet('data.parquet')
```

### Slide 17: Connecting to Databases
```python
import pandas as pd
from sqlalchemy import create_engine

# Create connection
engine = create_engine('postgresql://user:pass@host:5432/db')

# Query directly to DataFrame
query = """
    SELECT * FROM customers
    WHERE region = 'NCR'
"""
df = pd.read_sql(query, engine)
```

### Slide 18: Data Quality Assessment
**First questions to ask**:
1. How many rows/columns?
2. What are the data types?
3. Are there missing values?
4. Are there duplicates?
5. What's the date range?

```python
df.shape
df.dtypes
df.isnull().sum()
df.duplicated().sum()
```

### Slide 19: In-Class Exercise
**Task**: Query PSA Data
1. Use PSA OpenSTAT API (or provided sample)
2. Extract Philippine population by region
3. Write SQL query equivalent
4. Save as CSV

### Slide 20: Key Takeaways
1. Multiple data sources require different acquisition methods
2. SQL is essential for database extraction
3. APIs provide structured programmatic access
4. Web scraping is last resort (respect ethics)
5. Always assess data quality immediately

### Slide 21: Next Lecture
**Lecture 6: Data Cleaning & Transformation**
- Handling missing data
- Outlier treatment
- Data type conversions
- pandas transformation techniques

---

## Lecture 6: Data Cleaning & Transformation

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 6: Data Cleaning & Transformation
- Week 3, Session 2

### Slide 2: Learning Objectives
1. Identify and handle missing data appropriately
2. Detect and treat outliers
3. Transform and reshape data
4. Apply pandas operations for data cleaning

### Slide 3: The 80/20 Rule of Data Science
**"80% of time is spent on data preparation"**

**Data cleaning involves**:
- Missing value handling
- Outlier treatment
- Data type corrections
- Duplicate removal
- Inconsistency resolution

### Slide 4: Types of Missing Data
| Type | Description | Example |
|------|-------------|---------|
| **MCAR** | Missing Completely at Random | Random survey non-response |
| **MAR** | Missing at Random | Income missing more for young |
| **MNAR** | Missing Not at Random | High earners hide income |

**Why it matters**: Different types need different treatment

### Slide 5: Detecting Missing Values
```python
# Count missing
df.isnull().sum()

# Percentage missing
(df.isnull().sum() / len(df) * 100).round(2)

# Visualize missing patterns
import seaborn as sns
sns.heatmap(df.isnull(), cbar=True)
```

### Slide 6: Missing Data Strategies
| Strategy | When to Use |
|----------|-------------|
| **Drop rows** | Few missing, MCAR |
| **Drop columns** | >50% missing |
| **Mean/Median imputation** | Numerical, MCAR |
| **Mode imputation** | Categorical |
| **Forward/Back fill** | Time series |
| **Model-based** | MAR, complex patterns |

### Slide 7: Imputation Examples
```python
# Drop rows with any missing
df_clean = df.dropna()

# Drop columns with >50% missing
threshold = len(df) * 0.5
df_clean = df.dropna(axis=1, thresh=threshold)

# Fill with mean
df['income'].fillna(df['income'].mean(), inplace=True)

# Fill with median (better for skewed)
df['income'].fillna(df['income'].median(), inplace=True)

# Forward fill for time series
df['price'].fillna(method='ffill', inplace=True)
```

### Slide 8: Outlier Detection
**Statistical methods**:
- Z-score: |z| > 3
- IQR: Below Q1-1.5×IQR or above Q3+1.5×IQR

```python
# Z-score method
from scipy import stats
z_scores = stats.zscore(df['amount'])
outliers = df[abs(z_scores) > 3]

# IQR method
Q1, Q3 = df['amount'].quantile([0.25, 0.75])
IQR = Q3 - Q1
outliers = df[(df['amount'] < Q1-1.5*IQR) |
              (df['amount'] > Q3+1.5*IQR)]
```

### Slide 9: Visualizing Outliers
```python
import matplotlib.pyplot as plt

# Box plot
df['amount'].plot(kind='box')

# Scatter plot
plt.scatter(df.index, df['amount'])

# Histogram with density
df['amount'].hist(bins=50, density=True)
```

### Slide 10: Outlier Treatment
| Strategy | When to Use |
|----------|-------------|
| **Remove** | Clear errors |
| **Cap (Winsorize)** | Preserve information |
| **Transform** | Log, sqrt for skewness |
| **Separate analysis** | Legitimate outliers |

```python
# Winsorize at 1st and 99th percentile
from scipy.stats.mstats import winsorize
df['amount_winsorized'] = winsorize(df['amount'], limits=[0.01, 0.01])

# Log transform
df['amount_log'] = np.log1p(df['amount'])
```

### Slide 11: Data Type Conversions
```python
# Check types
df.dtypes

# Convert to numeric
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

# Convert to datetime
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Convert to category
df['region'] = df['region'].astype('category')
```

### Slide 12: String Cleaning
```python
# Standardize text
df['name'] = df['name'].str.lower().str.strip()

# Remove special characters
df['phone'] = df['phone'].str.replace(r'[^\d]', '', regex=True)

# Extract patterns
df['year'] = df['date_str'].str.extract(r'(\d{4})')
```

### Slide 13: Handling Duplicates
```python
# Find duplicates
df.duplicated().sum()

# View duplicate rows
df[df.duplicated(keep=False)]

# Remove duplicates
df_clean = df.drop_duplicates()

# Remove based on subset
df_clean = df.drop_duplicates(subset=['customer_id', 'date'])
```

### Slide 14: Reshaping Data - Melt
**Wide to Long format**:

```python
# Wide format
#   Name  Jan  Feb  Mar
# 0 Alice 100  110  120

# Melt to long
df_long = pd.melt(df,
                  id_vars=['Name'],
                  value_vars=['Jan', 'Feb', 'Mar'],
                  var_name='Month',
                  value_name='Sales')
# Result:
#    Name Month  Sales
# 0 Alice   Jan    100
# 1 Alice   Feb    110
```

### Slide 15: Reshaping Data - Pivot
**Long to Wide format**:

```python
# Pivot
df_wide = df_long.pivot(index='Name',
                        columns='Month',
                        values='Sales')

# Pivot table with aggregation
df_summary = df.pivot_table(
    index='region',
    columns='year',
    values='sales',
    aggfunc='sum'
)
```

### Slide 16: GroupBy Operations
```python
# Basic groupby
df.groupby('region')['sales'].mean()

# Multiple aggregations
df.groupby('region').agg({
    'sales': ['sum', 'mean', 'count'],
    'profit': ['sum', 'mean']
})

# Transform (keeps original shape)
df['region_avg'] = df.groupby('region')['sales'].transform('mean')
```

### Slide 17: Merging DataFrames
```python
# Inner join
merged = pd.merge(df1, df2, on='customer_id', how='inner')

# Left join
merged = pd.merge(df1, df2, on='customer_id', how='left')

# Join on different column names
merged = pd.merge(df1, df2,
                  left_on='cust_id',
                  right_on='customer_id')
```

### Slide 18: Philippine Example
**Cleaning PSA Regional Data**:

```python
# Load data
psa = pd.read_csv('psa_regional_gdp.csv')

# Clean region names
psa['region'] = psa['region'].str.strip().str.upper()

# Handle missing GDP values
psa['gdp'] = pd.to_numeric(psa['gdp'], errors='coerce')
psa['gdp'].fillna(psa.groupby('year')['gdp'].transform('median'), inplace=True)

# Remove outliers
psa = psa[psa['gdp'] > 0]  # Remove negative/zero
```

### Slide 19: Data Cleaning Pipeline
**Best practice**: Create reproducible pipeline

```python
def clean_data(df):
    """Standard cleaning pipeline."""
    df = df.copy()

    # 1. Remove duplicates
    df = df.drop_duplicates()

    # 2. Handle missing values
    df['amount'].fillna(df['amount'].median(), inplace=True)

    # 3. Fix data types
    df['date'] = pd.to_datetime(df['date'])

    # 4. Standardize text
    df['category'] = df['category'].str.lower().str.strip()

    return df
```

### Slide 20: In-Class Exercise
**Task**: Clean Philippine Weather Data
1. Load PAGASA historical data
2. Handle missing temperature values
3. Remove outliers (physically impossible values)
4. Convert dates to datetime
5. Create summary by region

### Slide 21: Key Takeaways
1. Understand missing data type before imputing
2. Outliers require domain knowledge to handle
3. Consistent data types prevent errors
4. Reshaping enables different analyses
5. Build reproducible cleaning pipelines

### Slide 22: Lab Preview
**Lab 3: Data Wrangling Challenge**
- Clean a messy Philippine dataset
- Apply all techniques learned
- Document decisions made

---

# WEEK 4: Exploratory Data Analysis

---

## Lecture 7: Univariate & Bivariate Analysis

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 7: Univariate & Bivariate Analysis
- Week 4, Session 1

### Slide 2: Learning Objectives
1. Conduct comprehensive univariate analysis
2. Explore relationships between two variables
3. Understand correlation vs causation
4. Apply EDA techniques systematically

### Slide 3: What is EDA?
**Exploratory Data Analysis** (John Tukey, 1977):
- "Detective work" on data
- Understand patterns before modeling
- Generate hypotheses
- Check assumptions

**Goals**: Summarize, visualize, discover, understand

### Slide 4: EDA Process
1. **Understand structure**: shape, types, memory
2. **Univariate analysis**: Each variable alone
3. **Bivariate analysis**: Pairs of variables
4. **Multivariate analysis**: Multiple variables
5. **Document findings**: Key insights

### Slide 5: Univariate Analysis - Numerical
**Measures of Central Tendency**:
- Mean: Average (sensitive to outliers)
- Median: Middle value (robust)
- Mode: Most frequent

**Measures of Spread**:
- Range: Max - Min
- Variance: Average squared deviation
- Standard Deviation: √Variance
- IQR: Q3 - Q1

### Slide 6: Descriptive Statistics
```python
# Quick summary
df['sales'].describe()

# More detailed
print(f"Mean: {df['sales'].mean():.2f}")
print(f"Median: {df['sales'].median():.2f}")
print(f"Std: {df['sales'].std():.2f}")
print(f"Skewness: {df['sales'].skew():.2f}")
print(f"Kurtosis: {df['sales'].kurtosis():.2f}")
```

### Slide 7: Distribution Shape
**Skewness**:
- = 0: Symmetric
- > 0: Right-skewed (long right tail)
- < 0: Left-skewed (long left tail)

**Kurtosis**:
- = 3: Normal (mesokurtic)
- > 3: Heavy tails (leptokurtic)
- < 3: Light tails (platykurtic)

**Visual**: Examples of each distribution shape

### Slide 8: Visualizing Distributions
```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Histogram
axes[0].hist(df['sales'], bins=30, edgecolor='black')
axes[0].set_title('Histogram')

# Box plot
axes[1].boxplot(df['sales'])
axes[1].set_title('Box Plot')

# Density plot
sns.kdeplot(df['sales'], ax=axes[2])
axes[2].set_title('Density Plot')
```

### Slide 9: Univariate Analysis - Categorical
```python
# Frequency counts
df['region'].value_counts()

# Proportions
df['region'].value_counts(normalize=True)

# Bar plot
df['region'].value_counts().plot(kind='bar')
```

### Slide 10: Bivariate Analysis Overview
| Variable 1 | Variable 2 | Analysis |
|------------|------------|----------|
| Numerical | Numerical | Scatter, correlation |
| Categorical | Categorical | Cross-tab, chi-square |
| Categorical | Numerical | Box plots, t-test |

### Slide 11: Numerical vs Numerical
**Scatter plots reveal**:
- Direction (positive, negative)
- Strength (tight vs loose)
- Form (linear, curved)
- Outliers

```python
plt.scatter(df['advertising'], df['sales'])
plt.xlabel('Advertising Spend')
plt.ylabel('Sales')
```

### Slide 12: Correlation
**Pearson correlation** (r): Linear relationship, -1 to +1

```python
# Single correlation
df['advertising'].corr(df['sales'])

# Correlation matrix
df[['sales', 'advertising', 'price']].corr()

# Heatmap
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
```

### Slide 13: Correlation Interpretation
| r value | Interpretation |
|---------|----------------|
| 0.9 - 1.0 | Very strong positive |
| 0.7 - 0.9 | Strong positive |
| 0.4 - 0.7 | Moderate positive |
| 0.1 - 0.4 | Weak positive |
| -0.1 - 0.1 | No correlation |

**Remember**: Correlation ≠ Causation!

### Slide 14: Correlation vs Causation
**Famous examples**:
- Ice cream sales ↔ Drownings (both caused by hot weather)
- Shoe size ↔ Reading ability (both caused by age)

**Spurious correlations**: tylervigen.com

**Establishing causation requires**:
- Temporal precedence
- No confounding variables
- Experimental design (RCT)

### Slide 15: Simpson's Paradox
**A trend in groups reverses when combined**

**Example**: UC Berkeley admissions (1973)
- Overall: Men admitted at higher rate
- By department: Women admitted at higher rate in most!
- Explanation: Women applied to more competitive departments

**Lesson**: Always segment your analysis

### Slide 16: Categorical vs Categorical
```python
# Cross-tabulation
pd.crosstab(df['region'], df['product_category'])

# Normalized
pd.crosstab(df['region'], df['product_category'],
            normalize='index')  # Row percentages

# Heatmap
sns.heatmap(pd.crosstab(df['region'], df['product_category']),
            annot=True, fmt='d')
```

### Slide 17: Categorical vs Numerical
```python
# Box plot by category
sns.boxplot(x='region', y='sales', data=df)

# Violin plot (shows distribution)
sns.violinplot(x='region', y='sales', data=df)

# Summary statistics by group
df.groupby('region')['sales'].agg(['mean', 'median', 'std'])
```

### Slide 18: Philippine EDA Example
**Analyzing Regional GDP**:

```python
# Load PSA data
psa = pd.read_csv('ph_regional_gdp.csv')

# Univariate: GDP distribution
psa['gdp_billions'].hist(bins=20)

# Bivariate: GDP vs Population
plt.scatter(psa['population'], psa['gdp_billions'])

# By region type
sns.boxplot(x='island_group', y='gdp_billions', data=psa)
```

### Slide 19: EDA Checklist
- [ ] Data shape and types
- [ ] Missing values count and pattern
- [ ] Numerical: mean, median, std, distribution
- [ ] Categorical: frequencies, proportions
- [ ] Key correlations identified
- [ ] Outliers noted and understood
- [ ] Initial hypotheses formed
- [ ] Questions for stakeholders

### Slide 20: In-Class Exercise
**EDA on Philippine Tourism Data**:
1. Load tourism arrivals data
2. Describe arrivals distribution
3. Analyze seasonality (month)
4. Correlate with exchange rate
5. Compare by origin country

### Slide 21: Key Takeaways
1. EDA is detective work - explore before modeling
2. Univariate: Understand each variable alone
3. Bivariate: Explore relationships
4. Correlation ≠ Causation
5. Simpson's Paradox: Always segment

### Slide 22: Next Lecture
**Lecture 8: Multivariate EDA & Feature Engineering**
- PCA intuition
- Feature creation
- Handling categorical variables
- Feature scaling

---

## Lecture 8: Multivariate EDA & Feature Engineering

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 8: Multivariate EDA & Feature Engineering
- Week 4, Session 2

### Slide 2: Learning Objectives
1. Explore relationships among multiple variables
2. Apply dimensionality reduction concepts
3. Create new features from existing data
4. Properly encode and scale features

### Slide 3: Multivariate Analysis
**Why multivariate?**
- Variables interact in complex ways
- Patterns emerge only when viewing together
- Better predictions need multiple inputs

### Slide 4: Pairplot - Quick Multivariate View
```python
import seaborn as sns

# All numerical pairs
sns.pairplot(df[['sales', 'price', 'advertising', 'region']],
             hue='region')

# With regression lines
sns.pairplot(df, kind='reg', diag_kind='kde')
```

### Slide 5: Parallel Coordinates
```python
from pandas.plotting import parallel_coordinates

# Standardize first for comparability
df_scaled = (df - df.mean()) / df.std()
df_scaled['cluster'] = cluster_labels

parallel_coordinates(df_scaled, 'cluster')
```

### Slide 6: Dimensionality Reduction - Why?
**The curse of dimensionality**:
- Many features → sparse data
- Distance becomes meaningless
- Overfitting risk increases

**Solutions**: PCA, t-SNE, UMAP

### Slide 7: PCA Intuition
**Principal Component Analysis**:
- Finds directions of maximum variance
- Projects data onto fewer dimensions
- New dimensions are uncorrelated

**Visual**: 2D data cloud → PC1 and PC2 axes

### Slide 8: PCA Example
```python
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Always scale before PCA
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[numerical_cols])

# Fit PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Explained variance
print(pca.explained_variance_ratio_)
# e.g., [0.65, 0.20] → 85% variance in 2 components
```

### Slide 9: PCA Visualization
```python
# Scatter plot of first 2 components
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['cluster'])
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} var)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} var)')

# Scree plot
plt.plot(range(1, len(pca.explained_variance_ratio_)+1),
         np.cumsum(pca.explained_variance_ratio_))
plt.ylabel('Cumulative Explained Variance')
```

### Slide 10: Feature Engineering Overview
**Types**:
1. **Extraction**: Derive from existing (e.g., date → month)
2. **Transformation**: Modify (e.g., log, square)
3. **Aggregation**: Summarize (e.g., customer total)
4. **Encoding**: Convert categories to numbers

### Slide 11: Date/Time Features
```python
# Extract from datetime
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
df['quarter'] = df['date'].dt.quarter

# Time since event
df['days_since_signup'] = (pd.Timestamp.now() - df['signup_date']).dt.days
```

### Slide 12: Mathematical Transformations
```python
# Log transform (for right-skewed)
df['log_income'] = np.log1p(df['income'])

# Square root
df['sqrt_area'] = np.sqrt(df['area'])

# Polynomial features
df['price_squared'] = df['price'] ** 2

# Interactions
df['price_x_quantity'] = df['price'] * df['quantity']
```

### Slide 13: Aggregation Features
```python
# Customer-level aggregations
customer_features = df.groupby('customer_id').agg({
    'amount': ['sum', 'mean', 'count', 'max'],
    'date': ['min', 'max']  # First and last purchase
}).reset_index()

# Flatten column names
customer_features.columns = ['_'.join(col).strip()
                             for col in customer_features.columns]
```

### Slide 14: RFM Analysis
**Recency, Frequency, Monetary** - Customer segmentation

```python
# Calculate RFM
snapshot_date = df['date'].max() + timedelta(days=1)

rfm = df.groupby('customer_id').agg({
    'date': lambda x: (snapshot_date - x.max()).days,  # Recency
    'order_id': 'count',  # Frequency
    'amount': 'sum'  # Monetary
}).rename(columns={'date': 'recency',
                   'order_id': 'frequency',
                   'amount': 'monetary'})
```

### Slide 15: Categorical Encoding - One-Hot
```python
# One-hot encoding (nominal categories)
df_encoded = pd.get_dummies(df, columns=['region', 'product_type'])

# Result: region_NCR, region_Cebu, region_Davao, ...
```

**When to use**: No natural order (nominal)

### Slide 16: Categorical Encoding - Label/Ordinal
```python
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder

# Label encoding (binary/target)
le = LabelEncoder()
df['region_encoded'] = le.fit_transform(df['region'])

# Ordinal encoding (ordered categories)
size_order = ['small', 'medium', 'large']
oe = OrdinalEncoder(categories=[size_order])
df['size_encoded'] = oe.fit_transform(df[['size']])
```

### Slide 17: Target Encoding
```python
# Mean encoding (risky - can overfit)
target_means = df.groupby('region')['sales'].mean()
df['region_target_enc'] = df['region'].map(target_means)

# Better: Use cross-validation encoding
from category_encoders import TargetEncoder
te = TargetEncoder(cols=['region'])
df['region_target_enc'] = te.fit_transform(df['region'], df['sales'])
```

### Slide 18: Feature Scaling
| Method | Formula | When to Use |
|--------|---------|-------------|
| Standard | (x - μ) / σ | Most algorithms |
| Min-Max | (x - min) / (max - min) | Neural networks, images |
| Robust | (x - median) / IQR | Outliers present |

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

scaler = StandardScaler()
df[['sales_scaled', 'price_scaled']] = scaler.fit_transform(
    df[['sales', 'price']]
)
```

### Slide 19: Philippine Feature Engineering Example
**E-commerce Customer Analysis**:

```python
# Load Lazada-style transaction data
transactions = pd.read_csv('ph_ecommerce.csv')

# Create features
transactions['order_date'] = pd.to_datetime(transactions['order_date'])
transactions['month'] = transactions['order_date'].dt.month
transactions['is_sale_period'] = transactions['month'].isin([6, 11, 12]).astype(int)
# June (mid-year), Nov (11.11), Dec (Christmas)

# Region encoding
transactions = pd.get_dummies(transactions, columns=['region'])
```

### Slide 20: In-Class Exercise
**Feature Engineering Challenge**:
1. Load Philippine bank transaction data
2. Create time-based features (hour, day, weekend)
3. Create customer aggregations (RFM-style)
4. Encode categorical variables
5. Scale numerical features

### Slide 21: Key Takeaways
1. Multivariate analysis reveals complex patterns
2. PCA reduces dimensions while preserving variance
3. Feature engineering often more impactful than model choice
4. Match encoding method to category type
5. Scale features for distance-based algorithms

### Slide 22: Lab Preview
**Lab 4: EDA & Feature Engineering Project**
- Complete EDA on Philippine dataset
- Create at least 5 new features
- Document insights and decisions

---

# WEEK 5: Data Visualization Principles

---

## Lecture 9: Visual Perception & Design Principles

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 9: Visual Perception & Design Principles
- Week 5, Session 1

### Slide 2: Learning Objectives
1. Understand how humans perceive visual information
2. Apply Gestalt principles to visualization
3. Use pre-attentive attributes effectively
4. Design accessible, colorblind-friendly visualizations

### Slide 3: Why Visualization Matters
**"The greatest value of a picture is when it forces us to notice what we never expected to see."** - John Tukey

- Humans process visuals 60,000x faster than text
- Patterns invisible in tables become obvious in charts
- Communication is faster and more memorable

### Slide 4: The Visualization Pipeline
1. **Data** → What story to tell?
2. **Visual encoding** → How to represent?
3. **Perception** → How will viewers interpret?
4. **Cognition** → What will they understand?
5. **Action** → What will they do?

### Slide 5: Pre-attentive Attributes
**Processed in <200ms without conscious effort**:

| Attribute | Best For |
|-----------|----------|
| Position | Quantitative comparison |
| Length | Quantitative comparison |
| Color hue | Categories |
| Color intensity | Ordered categories |
| Size | Quantitative (use carefully) |
| Shape | Categories |
| Orientation | Categories |

### Slide 6: Pre-attentive Demo
**Visual**: Grid of circles
- "Find the blue circle" → Instant (color)
- "Find the large circle" → Instant (size)
- "Count the blue circles" → Slower (requires counting)

### Slide 7: Gestalt Principles
**How we perceive groups and patterns**:

1. **Proximity**: Close things belong together
2. **Similarity**: Similar things belong together
3. **Enclosure**: Enclosed things belong together
4. **Continuity**: We follow smooth paths
5. **Closure**: We complete incomplete shapes
6. **Connection**: Connected things belong together

### Slide 8: Gestalt - Proximity
**Visual examples**:
- Rows vs columns of dots (perceived based on spacing)
- Use spacing to group related data points

```python
# Good: Space groups clearly
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
# Leave more space between groups
```

### Slide 9: Gestalt - Similarity
**Visual examples**:
- Same color = same category
- Same shape = same type

```python
# Color groups similar items
colors = ['blue' if region == 'NCR' else 'orange' for region in df['region']]
plt.scatter(df['x'], df['y'], c=colors)
```

### Slide 10: Gestalt - Enclosure & Connection
**Enclosure**: Use boxes, shading to group
**Connection**: Lines link related items

```python
# Highlight a region
plt.axvspan(x1, x2, alpha=0.3, color='yellow', label='Event period')

# Connect related points
plt.plot(x, y, '-o')  # Line connects points
```

### Slide 11: Color Theory for Data
**Three uses of color**:
1. **Sequential**: Low → High (single hue, varying intensity)
2. **Diverging**: Below/Above midpoint (two hues)
3. **Categorical**: Different groups (distinct hues)

**Visual**: Examples of each color scheme

### Slide 12: Choosing Color Palettes
```python
import seaborn as sns

# Sequential (continuous data)
sns.color_palette("Blues", as_cmap=True)

# Diverging (centered data)
sns.color_palette("RdBu", as_cmap=True)

# Categorical (groups)
sns.color_palette("Set2")
```

### Slide 13: Colorblind Accessibility
**~8% of males are colorblind**

**Avoid**:
- Red-green combinations alone
- Relying solely on color

**Best practices**:
- Use colorblind-safe palettes
- Add patterns or shapes
- Include labels

```python
# Colorblind-friendly palettes
sns.color_palette("colorblind")
sns.color_palette("viridis")  # Perceptually uniform
```

### Slide 14: Colorblind Simulation
**Tools to check your work**:
- colorblindness.com/coblis
- Matplotlib: `plt.style.use('seaborn-colorblind')`

**Visual**: Same chart seen with different colorblindness types

### Slide 15: Visual Hierarchy
**Guide the viewer's eye**:
1. **Title**: What is this about?
2. **Main insight**: The key message
3. **Supporting detail**: Context and nuance
4. **Source/Notes**: Credibility

**Use size, position, color to create hierarchy**

### Slide 16: Data-Ink Ratio
**Edward Tufte's principle**:
> Maximize data-ink ratio = Data ink / Total ink

**Remove**:
- Grid lines (or make subtle)
- 3D effects
- Chart junk (decorations)
- Redundant labels

### Slide 17: Bad vs Good Examples
**Bad**: 3D pie chart with gradient fills
**Good**: Simple bar chart with clear labels

```python
# Bad
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')  # Avoid!

# Good
df.plot(kind='bar', color='steelblue', edgecolor='none')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
```

### Slide 18: Accessibility Checklist
- [ ] Color is not the only differentiator
- [ ] Sufficient contrast (WCAG 4.5:1)
- [ ] Text is legible (12pt minimum)
- [ ] Alt text provided for web/digital
- [ ] Labels are clear and visible
- [ ] Legend is near the data

### Slide 19: Philippine Design Example
**Regional GDP Visualization**:

```python
# Create accessible choropleth
import geopandas as gpd

ph_map = gpd.read_file('ph_regions.geojson')
ph_map = ph_map.merge(gdp_data, on='region')

fig, ax = plt.subplots(figsize=(10, 12))
ph_map.plot(column='gdp_billions',
            cmap='YlOrRd',  # Colorblind-safe
            legend=True,
            ax=ax)
ax.set_title('Philippine GDP by Region (2023)', fontsize=14)
ax.axis('off')
```

### Slide 20: In-Class Exercise
**Redesign Challenge**:
1. Review a "bad" visualization (provided)
2. Identify 5 problems
3. Sketch improved version
4. Present reasoning

### Slide 21: Key Takeaways
1. Pre-attentive attributes enable instant perception
2. Gestalt principles help group and organize
3. Color serves specific purposes (sequential, diverging, categorical)
4. Always design for accessibility
5. Remove chart junk, maximize data-ink

### Slide 22: Next Lecture
**Lecture 10: Choosing the Right Visualization**
- Chart taxonomy
- When to use what
- Matplotlib & Seaborn deep dive
- Interactive visualizations

---

## Lecture 10: Choosing the Right Visualization

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 10: Choosing the Right Visualization
- Week 5, Session 2

### Slide 2: Learning Objectives
1. Select appropriate chart types for different data
2. Identify and avoid common visualization mistakes
3. Create publication-quality plots with matplotlib/seaborn
4. Build interactive visualizations with Plotly

### Slide 3: Chart Selection Framework
**Ask**:
1. What's your message? (comparison, distribution, relationship, composition)
2. How many variables?
3. What data types? (numerical, categorical, temporal)
4. Who's the audience?

### Slide 4: Chart Taxonomy
| Purpose | Chart Types |
|---------|-------------|
| **Comparison** | Bar, grouped bar, bullet |
| **Distribution** | Histogram, box, violin, density |
| **Relationship** | Scatter, bubble, heatmap |
| **Composition** | Stacked bar, pie (use sparingly), treemap |
| **Trend** | Line, area, sparkline |

### Slide 5: Comparison Charts
```python
# Horizontal bar (for many categories)
df.sort_values('sales').plot(kind='barh', x='region', y='sales')

# Grouped bar (comparing groups)
df.pivot(index='region', columns='year', values='sales').plot(kind='bar')

# Lollipop (cleaner alternative)
plt.hlines(y=df['region'], xmin=0, xmax=df['sales'])
plt.plot(df['sales'], df['region'], 'o')
```

### Slide 6: Distribution Charts
```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Histogram
axes[0,0].hist(df['sales'], bins=30)
axes[0,0].set_title('Histogram')

# Box plot
axes[0,1].boxplot([df[df['region']==r]['sales'] for r in regions])
axes[0,1].set_title('Box Plot')

# Violin plot
sns.violinplot(data=df, x='region', y='sales', ax=axes[1,0])
axes[1,0].set_title('Violin Plot')

# KDE
for region in regions:
    sns.kdeplot(df[df['region']==region]['sales'], ax=axes[1,1], label=region)
axes[1,1].set_title('Density Plot')
```

### Slide 7: Relationship Charts
```python
# Scatter plot
plt.scatter(df['advertising'], df['sales'], alpha=0.6)

# Bubble chart (3 variables)
plt.scatter(df['advertising'], df['sales'],
            s=df['market_share']*100,  # Size
            c=df['region'].astype('category').cat.codes,  # Color
            alpha=0.6)

# Heatmap
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
```

### Slide 8: Composition Charts
```python
# Stacked bar
df.pivot(index='year', columns='region', values='sales').plot(kind='bar', stacked=True)

# Pie chart (use sparingly!)
df['sales'].plot(kind='pie', autopct='%1.1f%%')
# Better alternative: horizontal bar

# Treemap
import squarify
squarify.plot(sizes=df['sales'], label=df['region'], alpha=0.8)
```

### Slide 9: Trend Charts
```python
# Line chart
df.groupby('date')['sales'].sum().plot(kind='line')

# Area chart
df.pivot(index='date', columns='region', values='sales').plot(kind='area', stacked=True)

# Multiple lines
for region in regions:
    subset = df[df['region']==region]
    plt.plot(subset['date'], subset['sales'], label=region)
plt.legend()
```

### Slide 10: Common Mistakes to Avoid
1. **Truncated y-axis**: Exaggerates differences
2. **Dual y-axes**: Confuses correlations
3. **Pie charts with many slices**: Hard to compare
4. **3D charts**: Distorts perception
5. **Rainbow color schemes**: Not accessible
6. **Too much data**: Cluttered, unreadable

### Slide 11: Mistake Examples
**Visual**: Side-by-side bad vs good

```python
# BAD: Truncated axis
plt.ylim(98, 102)  # Makes 1% change look huge

# GOOD: Start from zero (for bar charts)
plt.ylim(0, df['value'].max() * 1.1)

# Or use explicit callout
plt.annotate('Note: y-axis does not start at 0', xy=(0.5, 0.02))
```

### Slide 12: Matplotlib Fundamentals
```python
import matplotlib.pyplot as plt

# Figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# Plot
ax.plot(x, y, color='steelblue', linewidth=2, label='Sales')

# Customize
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Sales (PHP millions)', fontsize=12)
ax.set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
ax.legend(loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('sales_trend.png', dpi=300)
```

### Slide 13: Seaborn for Statistical Plots
```python
import seaborn as sns

# Set style
sns.set_style('whitegrid')
sns.set_palette('colorblind')

# Statistical plots
sns.regplot(data=df, x='advertising', y='sales')  # With regression line
sns.jointplot(data=df, x='advertising', y='sales', kind='hex')  # With marginals
sns.catplot(data=df, x='region', y='sales', kind='box', col='year')  # Faceted
```

### Slide 14: Faceting (Small Multiples)
```python
# FacetGrid for multiple panels
g = sns.FacetGrid(df, col='region', col_wrap=3, height=4)
g.map(plt.hist, 'sales', bins=20)
g.set_titles('{col_name}')

# Relational plot with facets
sns.relplot(data=df, x='date', y='sales',
            hue='product', col='region', kind='line')
```

### Slide 15: Interactive Visualizations with Plotly
```python
import plotly.express as px

# Interactive scatter
fig = px.scatter(df, x='advertising', y='sales',
                 color='region', size='market_share',
                 hover_data=['company'],
                 title='Sales vs Advertising by Region')
fig.show()

# Interactive line
fig = px.line(df, x='date', y='sales', color='region',
              title='Sales Trend by Region')
fig.show()
```

### Slide 16: Plotly for Dashboards
```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Multiple plots
fig = make_subplots(rows=2, cols=2,
                    subplot_titles=['Trend', 'Distribution', 'By Region', 'Correlation'])

fig.add_trace(go.Scatter(x=df['date'], y=df['sales']), row=1, col=1)
fig.add_trace(go.Histogram(x=df['sales']), row=1, col=2)
fig.add_trace(go.Bar(x=df['region'], y=df['sales']), row=2, col=1)
fig.add_trace(go.Heatmap(z=df.corr()), row=2, col=2)

fig.update_layout(height=800, title_text="Sales Dashboard")
fig.show()
```

### Slide 17: Philippine Visualization Example
**Tourism Arrivals Dashboard**:

```python
import plotly.express as px

# Load tourism data
tourism = pd.read_csv('ph_tourism_arrivals.csv')

# Animated scatter
fig = px.scatter(tourism,
                 x='gdp_per_capita',
                 y='arrivals',
                 size='hotel_rooms',
                 color='island_group',
                 animation_frame='year',
                 hover_name='region',
                 title='Philippine Tourism Growth by Region')
fig.show()
```

### Slide 18: Annotation Best Practices
```python
# Add context to charts
ax.annotate('COVID-19 Impact',
            xy=('2020-03', low_point),
            xytext=('2020-01', low_point + 1000),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=10, color='red')

# Highlight key point
ax.axhline(y=threshold, color='gray', linestyle='--', label='Target')
ax.axvspan('2020-03', '2021-06', alpha=0.2, color='red', label='Lockdown')
```

### Slide 19: Chart Selection Quick Reference
| Question | Visualization |
|----------|---------------|
| How did X change over time? | Line chart |
| How is X distributed? | Histogram, box plot |
| How do categories compare? | Bar chart |
| What's the relationship between X and Y? | Scatter plot |
| What's the composition? | Stacked bar, treemap |
| How do groups differ in distribution? | Violin, ridge plot |

### Slide 20: In-Class Exercise
**Create a Mini Dashboard**:
1. Load Philippine economic data
2. Create 4 visualizations (one of each type)
3. Apply design principles learned
4. Add annotations and context

### Slide 21: Key Takeaways
1. Match chart type to your message and data
2. Avoid common pitfalls (truncation, 3D, too many slices)
3. matplotlib for control, seaborn for statistics, Plotly for interactivity
4. Annotations add context and insight
5. Always consider the audience

### Slide 22: Lab Preview
**Lab 5: Visualization Portfolio**
- Create 6 publication-quality visualizations
- Each addresses different question type
- Philippine data required for 3+

---

# WEEK 6: Data Storytelling & Communication

---

## Lecture 11: Narrative Structure in Data

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 11: Narrative Structure in Data
- Week 6, Session 1

### Slide 2: Learning Objectives
1. Structure data presentations for maximum impact
2. Apply storytelling frameworks to analytics
3. Avoid chartjunk and apply Tufte's principles
4. Learn from master data storytellers

### Slide 3: Why Data Storytelling?
**"Numbers have an important story to tell. They rely on you to give them a voice."** - Stephen Few

- Data alone doesn't drive decisions
- Stories are memorable (22x more than facts)
- Emotion + Logic = Action

### Slide 4: The Data Story Arc
**Classic narrative structure adapted**:

1. **Setup**: Context, background, why it matters
2. **Conflict**: The problem, the question, the gap
3. **Resolution**: The insight, the answer
4. **Call to Action**: What should happen next

### Slide 5: The Pyramid Principle (McKinsey)
**Start with the answer**:

1. **Lead with the insight** (so what?)
2. **Support with evidence** (why?)
3. **Detail as needed** (how?)

**Audience busy? They get the key message first.**

### Slide 6: Context-Action-Result (CAR)
**For action-oriented audiences**:

- **Context**: What's the situation?
- **Action**: What did we do/learn?
- **Result**: What's the impact?

**Example**: "Sales dropped 15% (C), we analyzed regional data (A), and found Visayas underperforming due to distribution issues (R)."

### Slide 7: The Three-Minute Story
**For executives**:

| Time | Content |
|------|---------|
| 0:00-0:30 | The headline (one sentence) |
| 0:30-1:30 | Three supporting points |
| 1:30-2:30 | Recommendation |
| 2:30-3:00 | Next steps |

**Rest is in the appendix**

### Slide 8: Building Tension
**Don't just present data - reveal it**:

1. "We expected X..."
2. "But we found Y..."
3. "This matters because..."
4. "Here's what we recommend..."

**Visual revelation**: Progressive disclosure

### Slide 9: Case Study - Hans Rosling
**Gapminder: "200 Countries, 200 Years, 4 Minutes"**

What makes it work:
- Animation reveals the story
- Commentary adds meaning
- Unexpected insights (Bangladesh vs Brazil)
- Emotion (countries as characters)

### Slide 10: Edward Tufte's Principles
**The Visual Display of Quantitative Information**:

1. **Show the data** - don't hide it
2. **Minimize non-data ink** - remove chartjunk
3. **Maximize data density** - small multiples
4. **Integrate words and graphics** - labels on data
5. **Ensure graphical integrity** - no distortion

### Slide 11: Chartjunk Examples
**Remove**:
- Decorative elements
- Heavy gridlines
- 3D effects
- Gradient fills
- Unnecessary legends
- Redundant labels

**Before/After visual demonstration**

### Slide 12: Data-Ink Ratio in Practice
```python
# Heavy chartjunk
plt.style.use('default')
ax.bar(x, y, color='blue', edgecolor='black', linewidth=2)
ax.grid(True, which='both', linestyle='-', linewidth=1)

# Clean, minimal
plt.style.use('seaborn-whitegrid')
ax.bar(x, y, color='steelblue', edgecolor='none')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.yaxis.grid(True, linestyle='--', alpha=0.3)
```

### Slide 13: Small Multiples
**Show many comparisons in same visual space**:

```python
# Instead of one cluttered chart
fig, axes = plt.subplots(4, 4, figsize=(12, 12), sharex=True, sharey=True)
for ax, region in zip(axes.flat, regions):
    subset = df[df['region'] == region]
    ax.plot(subset['date'], subset['sales'])
    ax.set_title(region, fontsize=10)
fig.suptitle('Sales Trend by Region', fontsize=14)
```

### Slide 14: Layering Information
**Build complexity gradually**:

1. **Layer 1**: The main point (large, prominent)
2. **Layer 2**: Supporting detail (medium, secondary color)
3. **Layer 3**: Context (small, gray, background)

**Example**: Headline number → Trend line → Reference lines

### Slide 15: Annotation Strategy
**Types of annotations**:
- **Explanatory**: What happened and why
- **Reference**: Benchmarks, targets, averages
- **Emphasis**: Highlighting key points
- **Context**: Events, policy changes

```python
# Annotate key event
ax.annotate('Launch date', xy=(launch_date, value),
            xytext=(launch_date, value*1.2),
            arrowprops=dict(arrowstyle='->'),
            fontsize=10, ha='center')
```

### Slide 16: The Slide-Doc
**Standalone documents that also present well**:

- Each slide conveys ONE idea
- Title IS the takeaway (not just topic)
- Visuals support, don't replace, text
- Works in presentation AND printed form

**Example**: "Sales grew 23% driven by Visayas expansion" vs "Sales Performance"

### Slide 17: Common Storytelling Mistakes
1. **Starting with methodology** (audience doesn't care)
2. **Too much detail** (can't see the forest)
3. **No clear takeaway** (so what?)
4. **Passive voice** ("it was found that...")
5. **Jargon overload** (speak their language)

### Slide 18: Philippine Storytelling Example
**Telling the GCash Growth Story**:

**Bad**: "GCash registered users increased from 20M in 2019 to 81M in 2023."

**Good**: "In just 4 years, GCash grew from a fintech startup to the financial backbone of the Philippines. With 81M users - more than the entire adult population - it's transformed how Filipinos handle money."

### Slide 19: Storyboarding Process
1. **Define audience**: Who? What do they care about?
2. **One sentence**: What's the key message?
3. **Sketch flow**: Beginning → Middle → End
4. **Choose visuals**: What shows, not tells?
5. **Write headlines**: Each slide's takeaway
6. **Refine**: Remove everything unnecessary

### Slide 20: In-Class Exercise
**Storyboard a Data Story**:
1. Given: Philippine tourism data
2. Audience: DOT Secretary
3. Task: Storyboard 5-slide presentation
4. Focus: Structure and headlines (no actual charts yet)

### Slide 21: Key Takeaways
1. Data needs narrative structure to drive action
2. Lead with insight, support with evidence
3. Tufte: Maximize data-ink, minimize chartjunk
4. Every slide needs ONE clear takeaway
5. Storyboard before creating visuals

### Slide 22: Next Lecture
**Lecture 12: Dashboard Design & BI Tools**
- Dashboard principles
- Tableau introduction
- Streamlit for Python
- KPI design

---

## Lecture 12: Dashboard Design & BI Tools

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 12: Dashboard Design & BI Tools
- Week 6, Session 2

### Slide 2: Learning Objectives
1. Design effective analytical dashboards
2. Apply dashboard best practices
3. Use Tableau for business intelligence
4. Build interactive dashboards with Streamlit

### Slide 3: What is a Dashboard?
**Definition**: Visual display of key information needed to achieve objectives, consolidated on a single screen

**Types**:
- **Strategic**: Executive-level, KPIs, long-term
- **Analytical**: Explore and analyze, interactive
- **Operational**: Real-time monitoring, alerts

### Slide 4: Dashboard vs Report
| Dashboard | Report |
|-----------|--------|
| At-a-glance | In-depth |
| Interactive | Static |
| Current state | Historical analysis |
| Monitoring | Explanation |
| KPIs | Detailed metrics |

### Slide 5: Dashboard Design Principles
1. **Know your audience**: What decisions will they make?
2. **Prioritize**: Most important = most prominent
3. **Group logically**: Related metrics together
4. **Minimize noise**: Only what's needed
5. **Enable action**: Not just inform, but drive behavior

### Slide 6: The 5-Second Rule
**A good dashboard answers key questions in <5 seconds**:

- What's our current status?
- Are we on track?
- What needs attention?

**Test**: Show for 5 seconds, then ask what they remember

### Slide 7: Dashboard Layout Patterns
**Z-Pattern**: Eye moves top-left → top-right → bottom-left → bottom-right
**F-Pattern**: Important items on left and top

```
┌─────────────────────────────────┐
│  KPI 1   │   KPI 2   │   KPI 3  │  ← Key metrics
├──────────┼───────────┴──────────┤
│          │                      │
│  Main    │   Secondary Chart    │
│  Chart   │                      │
├──────────┴──────────────────────┤
│         Detail Table            │
└─────────────────────────────────┘
```

### Slide 8: KPI Design
**Key Performance Indicator elements**:
- **Current value**: Big, prominent
- **Comparison**: vs target, vs last period
- **Trend**: Sparkline or arrow
- **Context**: What's good/bad?

```
┌─────────────────┐
│ Revenue         │
│ ₱12.5M    ▲15%  │
│ vs target: 98%  │
│ ~~~~~~~~        │ (sparkline)
└─────────────────┘
```

### Slide 9: Choosing Dashboard Charts
| Purpose | Best Chart |
|---------|------------|
| Current vs Target | Bullet chart, gauge |
| Trend | Line chart, sparkline |
| Composition | Stacked bar, donut |
| Comparison | Bar chart |
| Distribution | Histogram |
| Geographic | Map |

### Slide 10: Interactivity Guidelines
**Good interactivity**:
- Filters that affect multiple charts
- Drill-down to detail
- Hover for additional info
- Time range selection

**Bad interactivity**:
- Required clicks to see basic info
- Hidden important data
- Too many filter options

### Slide 11: Tableau Overview
**Strengths**:
- Drag-and-drop interface
- Powerful visualizations
- Easy sharing
- Industry standard

**Key concepts**:
- Dimensions vs Measures
- Worksheets → Dashboards → Stories
- Calculated fields, parameters, filters

### Slide 12: Tableau Workflow
1. **Connect** to data source
2. **Prepare** data (join, clean)
3. **Create** worksheets (individual charts)
4. **Assemble** dashboard
5. **Add** filters and actions
6. **Publish** to server or public

### Slide 13: Streamlit for Python Dashboards
```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Philippine Economic Dashboard')

# Sidebar filters
year = st.sidebar.slider('Year', 2015, 2024, 2023)
region = st.sidebar.multiselect('Region', regions, default=regions[:3])

# Filter data
filtered = df[(df['year'] == year) & (df['region'].isin(region))]

# KPI row
col1, col2, col3 = st.columns(3)
col1.metric("Total GDP", f"₱{filtered['gdp'].sum()/1e9:.1f}T", "+5.2%")
col2.metric("Employment", f"{filtered['employment'].sum()/1e6:.1f}M", "+2.1%")
col3.metric("Exports", f"${filtered['exports'].sum()/1e9:.1f}B", "-1.5%")

# Charts
st.plotly_chart(px.bar(filtered, x='region', y='gdp'))
```

### Slide 14: Streamlit Layout
```python
# Tabs
tab1, tab2 = st.tabs(["Overview", "Details"])
with tab1:
    st.plotly_chart(overview_fig)
with tab2:
    st.dataframe(detail_df)

# Expander for advanced options
with st.expander("Advanced Filters"):
    min_gdp = st.number_input("Minimum GDP", value=0)

# Columns for side-by-side
left, right = st.columns(2)
with left:
    st.plotly_chart(chart1)
with right:
    st.plotly_chart(chart2)
```

### Slide 15: Dashboard Color Strategy
**Semantic colors**:
- Green = Good / Above target
- Red = Bad / Below target
- Blue = Neutral / Informational
- Gray = Background / Supporting

**Limit palette**: 3-5 colors maximum

### Slide 16: Mobile Considerations
**Responsive design**:
- Stack vertically on mobile
- Larger touch targets
- Simplified navigation
- Critical KPIs first

```python
# Streamlit handles this automatically
# But design with mobile in mind
st.set_page_config(layout="wide")  # For desktop
```

### Slide 17: Dashboard Performance
**Best practices**:
- Pre-aggregate when possible
- Limit data points displayed
- Use efficient chart types
- Cache expensive computations

```python
@st.cache_data
def load_data():
    return pd.read_csv('large_file.csv')

@st.cache_data
def compute_aggregates(df):
    return df.groupby('region').agg(...)
```

### Slide 18: Philippine Dashboard Example
**GCash Business Analytics Dashboard**:

```python
import streamlit as st

st.title("📱 GCash Transaction Analytics")

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Daily Active Users", "45.2M", "+8%")
c2.metric("Transaction Volume", "₱2.3B", "+12%")
c3.metric("Avg Transaction", "₱520", "-3%")
c4.metric("Success Rate", "99.2%", "+0.1%")

# Main charts
st.subheader("Hourly Transaction Pattern")
st.plotly_chart(hourly_fig)

st.subheader("Regional Distribution")
col1, col2 = st.columns(2)
col1.plotly_chart(map_fig)
col2.plotly_chart(bar_fig)
```

### Slide 19: Dashboard Checklist
- [ ] Clear title and purpose
- [ ] Most important info is most prominent
- [ ] KPIs have context (trend, target, comparison)
- [ ] Filters are intuitive and responsive
- [ ] Color is meaningful and accessible
- [ ] Loads quickly (<3 seconds)
- [ ] Works on mobile
- [ ] Data source and update time shown

### Slide 20: In-Class Exercise
**Build a Mini Dashboard**:
1. Use provided Philippine data
2. Create in Streamlit (or sketch in Figma)
3. Include: 3 KPIs, 2 charts, 1 filter
4. Apply design principles learned
5. Present in 3 minutes

### Slide 21: Key Takeaways
1. Dashboards enable at-a-glance decision making
2. Design for your audience's questions
3. KPIs need context (target, trend, comparison)
4. Tableau for enterprise BI, Streamlit for Python
5. Test with the 5-second rule

### Slide 22: Midterm Exam Preview
**Coverage**: Weeks 1-6
- Data science lifecycle
- Probability and statistics
- Data wrangling and EDA
- Visualization principles
- Storytelling and dashboards

**Format**: Multiple choice + Short answer + Practical problem

---

# WEEK 7: ML Refresher & Regression Analytics

---

## Lecture 13: Linear Regression for Analytics

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 13: Linear Regression for Analytics
- Week 7, Session 1

### Slide 2: Learning Objectives
1. Review linear regression fundamentals
2. Interpret coefficients for business insights
3. Diagnose regression assumptions
4. Apply regularization techniques

### Slide 3: Why Regression in Analytics?
**Not just prediction - explanation**:

| ML Focus | Analytics Focus |
|----------|-----------------|
| What will happen? | Why did it happen? |
| Accuracy metrics | Coefficient interpretation |
| Complex models OK | Interpretability matters |
| Feature importance | Marginal effects |

### Slide 4: Simple Linear Regression Review
$$y = \beta_0 + \beta_1 x + \epsilon$$

- **β₀**: Intercept (y when x=0)
- **β₁**: Slope (change in y per unit x)
- **ε**: Error term (randomness)

**Goal**: Find β₀ and β₁ that minimize squared errors

### Slide 5: OLS Estimation
**Ordinary Least Squares**:

$$\hat{\beta}_1 = \frac{\sum(x_i - \bar{x})(y_i - \bar{y})}{\sum(x_i - \bar{x})^2}$$

$$\hat{\beta}_0 = \bar{y} - \hat{\beta}_1\bar{x}$$

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X, y)
print(f"Intercept: {model.intercept_}")
print(f"Coefficient: {model.coef_[0]}")
```

### Slide 6: Multiple Linear Regression
$$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + ... + \beta_p x_p + \epsilon$$

**Interpretation**: β₁ = change in y for 1-unit change in x₁, **holding all other variables constant**

### Slide 7: Coefficient Interpretation
**Example**: Sales = 100 + 2.5×Advertising + 15×Promotion

- **Intercept (100)**: Base sales with no advertising/promotion
- **Advertising (2.5)**: Each ₱1M in ads → ₱2.5M more sales
- **Promotion (15)**: Promotion present → ₱15M more sales

**Always consider**: Units, scale, ceteris paribus

### Slide 8: R² and Adjusted R²
**R² (Coefficient of Determination)**:
$$R^2 = 1 - \frac{SS_{res}}{SS_{tot}}$$

- Proportion of variance explained
- 0 to 1 (higher = better fit)
- **Problem**: Always increases with more variables

**Adjusted R²**: Penalizes extra variables
$$R^2_{adj} = 1 - (1-R^2)\frac{n-1}{n-p-1}$$

### Slide 9: Statistical Significance
```python
import statsmodels.api as sm

X = sm.add_constant(X)  # Add intercept
model = sm.OLS(y, X).fit()
print(model.summary())
```

**Key outputs**:
- Coefficients (coef)
- Standard errors (std err)
- t-statistics (t)
- p-values (P>|t|) - < 0.05 = significant
- Confidence intervals

### Slide 10: OLS Assumptions
**LINE**:
1. **L**inearity: Relationship is linear
2. **I**ndependence: Errors are independent
3. **N**ormality: Errors are normally distributed
4. **E**qual variance: Homoscedasticity

**Violations lead to**: Biased estimates, wrong p-values

### Slide 11: Diagnostic Plots
```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Residuals vs Fitted
axes[0,0].scatter(model.fittedvalues, model.resid)
axes[0,0].axhline(0, color='red', linestyle='--')
axes[0,0].set_title('Residuals vs Fitted')

# Q-Q plot
sm.qqplot(model.resid, line='45', ax=axes[0,1])
axes[0,1].set_title('Normal Q-Q')

# Scale-Location
axes[1,0].scatter(model.fittedvalues, np.sqrt(np.abs(model.resid)))
axes[1,0].set_title('Scale-Location')

# Residuals vs Leverage
sm.graphics.influence_plot(model, ax=axes[1,1])
```

### Slide 12: Multicollinearity
**Problem**: Predictors are highly correlated
**Consequence**: Unstable coefficients, inflated standard errors

**Detection**: Variance Inflation Factor (VIF)
- VIF > 5: Moderate collinearity
- VIF > 10: High collinearity

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
```

### Slide 13: Regularization - Ridge
**Problem**: Overfitting with many features
**Solution**: Add penalty for large coefficients

$$\min \sum(y_i - \hat{y}_i)^2 + \lambda\sum\beta_j^2$$

```python
from sklearn.linear_model import Ridge

ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
```

**Effect**: Shrinks coefficients toward zero (but not exactly zero)

### Slide 14: Regularization - Lasso
$$\min \sum(y_i - \hat{y}_i)^2 + \lambda\sum|\beta_j|$$

```python
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)

# Feature selection: some coefficients become exactly 0
print(f"Non-zero coefficients: {np.sum(lasso.coef_ != 0)}")
```

**Effect**: Can set coefficients exactly to zero (feature selection)

### Slide 15: Ridge vs Lasso
| Aspect | Ridge | Lasso |
|--------|-------|-------|
| Penalty | L2 (squared) | L1 (absolute) |
| Coefficients | Shrunk, not zero | Can be exactly zero |
| Feature selection | No | Yes |
| Correlated features | Keeps all | Picks one |
| Use when | Many useful features | Sparse model needed |

### Slide 16: Choosing λ with Cross-Validation
```python
from sklearn.linear_model import RidgeCV, LassoCV

# Cross-validation to find best alpha
ridge_cv = RidgeCV(alphas=[0.1, 1, 10, 100], cv=5)
ridge_cv.fit(X_train, y_train)
print(f"Best alpha: {ridge_cv.alpha_}")

lasso_cv = LassoCV(alphas=[0.001, 0.01, 0.1, 1], cv=5)
lasso_cv.fit(X_train, y_train)
print(f"Best alpha: {lasso_cv.alpha_}")
```

### Slide 17: Philippine Example
**Predicting Retail Sales**:

```python
# Load SM/Puregold-style data
retail = pd.read_csv('ph_retail_sales.csv')

X = retail[['advertising', 'promotion', 'store_size', 'competitors_nearby']]
y = retail['monthly_sales']

# Fit with statsmodels for interpretation
X_const = sm.add_constant(X)
model = sm.OLS(y, X_const).fit()
print(model.summary())

# Interpretation:
# - Each ₱1M advertising → ₱3.2M sales increase
# - Each additional competitor → ₱1.5M sales decrease
```

### Slide 18: Communicating Results
**For stakeholders**:

| Variable | Impact on Sales | Significance |
|----------|----------------|--------------|
| Advertising (₱M) | +₱3.2M per ₱1M spent | *** (p<0.001) |
| Promotion | +₱8.5M when active | ** (p<0.01) |
| Store size (sqm) | +₱50K per sqm | *** (p<0.001) |
| Competitors | -₱1.5M per competitor | * (p<0.05) |

"Model explains 72% of sales variation (Adj R² = 0.72)"

### Slide 19: In-Class Exercise
**Regression Analysis**:
1. Load Philippine housing price data
2. Fit regression: Price ~ Size + Bedrooms + Location
3. Check assumptions (diagnostic plots)
4. Interpret coefficients
5. Identify significant predictors

### Slide 20: Key Takeaways
1. Regression for analytics = interpretation, not just prediction
2. Coefficients = marginal effects (ceteris paribus)
3. Check assumptions with diagnostic plots
4. Watch for multicollinearity (VIF)
5. Regularization for many features (Ridge/Lasso)

### Slide 21: Next Lecture
**Lecture 14: Logistic Regression & Classification Metrics**
- Binary classification
- Odds ratios and interpretation
- ROC curves and AUC
- Business applications

---

## Lecture 14: Logistic Regression & Classification Metrics

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 14: Logistic Regression & Classification Metrics
- Week 7, Session 2

### Slide 2: Learning Objectives
1. Apply logistic regression for binary outcomes
2. Interpret odds ratios and log-odds
3. Evaluate classifiers with appropriate metrics
4. Understand the precision-recall tradeoff

### Slide 3: When Linear Regression Fails
**Problem**: Predicting probability of binary outcome (Yes/No)

Linear regression issues:
- Can predict values < 0 or > 1
- Assumes constant variance
- Relationship often S-shaped, not linear

**Solution**: Logistic regression

### Slide 4: The Logistic Function
$$P(Y=1) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 X)}}$$

**Properties**:
- Output bounded between 0 and 1
- S-shaped (sigmoid) curve
- Symmetric around 0.5

### Slide 5: Log-Odds (Logit)
$$\log\left(\frac{P}{1-P}\right) = \beta_0 + \beta_1 X$$

**Interpretation**:
- Left side: Log of odds ratio
- Right side: Linear combination (like linear regression)
- β₁ = change in log-odds for 1-unit increase in X

### Slide 6: Odds and Odds Ratios
**Odds**: P(event) / P(no event)
- If P = 0.8, Odds = 0.8/0.2 = 4 ("4 to 1")

**Odds Ratio**: How odds change with X
- OR = e^β
- OR = 2: Odds double with 1-unit increase in X

### Slide 7: Fitting Logistic Regression
```python
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm

# Scikit-learn (for prediction)
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

# Statsmodels (for interpretation)
X_const = sm.add_constant(X)
logit_model = sm.Logit(y, X_const).fit()
print(logit_model.summary())
```

### Slide 8: Interpreting Coefficients
**Credit Card Default Example**:

| Variable | Coefficient | Odds Ratio | Interpretation |
|----------|-------------|------------|----------------|
| Income (₱100K) | -0.35 | 0.70 | Each ₱100K income → 30% lower default odds |
| Balance (₱10K) | 0.52 | 1.68 | Each ₱10K balance → 68% higher default odds |
| Student (Yes=1) | 0.48 | 1.62 | Students 62% more likely to default |

### Slide 9: Predictions
```python
# Probability predictions
y_prob = log_reg.predict_proba(X_test)[:, 1]

# Class predictions (default threshold = 0.5)
y_pred = log_reg.predict(X_test)

# Custom threshold
threshold = 0.3  # More sensitive to positive class
y_pred_custom = (y_prob >= threshold).astype(int)
```

### Slide 10: Confusion Matrix
```
                  Predicted
              Negative  Positive
Actual  Negative   TN       FP    ← False Positive (Type I)
        Positive   FN       TP    ← False Negative (Type II)
```

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(cm).plot()
```

### Slide 11: Classification Metrics
$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

$$\text{Precision} = \frac{TP}{TP + FP}$$ (Of predicted positive, how many correct?)

$$\text{Recall} = \frac{TP}{TP + FN}$$ (Of actual positive, how many found?)

$$\text{F1} = 2 \times \frac{Precision \times Recall}{Precision + Recall}$$

### Slide 12: When Accuracy Fails
**Imbalanced data problem**:
- 99% non-fraud, 1% fraud
- Model predicting "no fraud" always: 99% accuracy!
- But: 0% recall for fraud (useless!)

**Use precision/recall for imbalanced data**

### Slide 13: Precision vs Recall Tradeoff
**High precision needed**: Spam filter (don't want false positives)
**High recall needed**: Disease screening (don't miss positive cases)

**Adjust threshold**:
- Lower threshold → Higher recall, lower precision
- Higher threshold → Lower recall, higher precision

### Slide 14: ROC Curve
**Receiver Operating Characteristic**:
- X-axis: False Positive Rate (1 - Specificity)
- Y-axis: True Positive Rate (Recall)
- Each point = different threshold

```python
from sklearn.metrics import roc_curve, auc

fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr, label=f'AUC = {roc_auc:.3f}')
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
```

### Slide 15: AUC Interpretation
**Area Under ROC Curve (AUC)**:
- 0.5 = Random guessing
- 0.7-0.8 = Acceptable
- 0.8-0.9 = Excellent
- 0.9+ = Outstanding

**Interpretation**: Probability that model ranks random positive higher than random negative

### Slide 16: Precision-Recall Curve
**Better for imbalanced data**:

```python
from sklearn.metrics import precision_recall_curve, average_precision_score

precision, recall, thresholds = precision_recall_curve(y_test, y_prob)
ap = average_precision_score(y_test, y_prob)

plt.plot(recall, precision, label=f'AP = {ap:.3f}')
plt.xlabel('Recall')
plt.ylabel('Precision')
```

### Slide 17: Classification Report
```python
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))

#               precision    recall  f1-score   support
#            0       0.95      0.98      0.96       500
#            1       0.82      0.68      0.74       100
#     accuracy                           0.93       600
#    macro avg       0.88      0.83      0.85       600
# weighted avg       0.93      0.93      0.93       600
```

### Slide 18: Philippine Case Study - Credit Scoring
**BPI/BDO Credit Default Prediction**:

```python
# Load credit data
credit = pd.read_csv('ph_credit_data.csv')

X = credit[['income', 'balance', 'age', 'employment_years', 'num_accounts']]
y = credit['default']

# Fit and evaluate
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y)
model = LogisticRegression()
model.fit(X_train, y_train)

# Results interpretation for risk team
odds_ratios = np.exp(model.coef_[0])
for var, odds in zip(X.columns, odds_ratios):
    print(f"{var}: OR = {odds:.2f}")
```

### Slide 19: Business Implications
**Credit scoring decisions**:

| Threshold | Precision | Recall | Business Impact |
|-----------|-----------|--------|-----------------|
| 0.3 | 0.45 | 0.85 | Many false alarms, but few defaults missed |
| 0.5 | 0.65 | 0.68 | Balanced |
| 0.7 | 0.82 | 0.42 | Fewer false alarms, but miss many defaults |

**Cost-benefit analysis needed**: Cost of false positive vs false negative

### Slide 20: In-Class Exercise
**Churn Prediction**:
1. Load Philippine telecom churn data
2. Fit logistic regression
3. Interpret top 3 predictors (odds ratios)
4. Plot ROC curve
5. Choose optimal threshold for business case

### Slide 21: Key Takeaways
1. Logistic regression predicts probabilities (0-1)
2. Coefficients → Odds ratios (eˆβ)
3. Accuracy misleading for imbalanced data
4. ROC/AUC for overall performance
5. Precision/Recall tradeoff depends on business cost

### Slide 22: Lab Preview
**Lab 6: Regression & Classification Analytics**
- Build credit scoring model
- Interpret coefficients for stakeholders
- Optimize threshold for business objective

---

# WEEK 8: Tree-Based Methods & Ensemble Analytics

---

## Lecture 15: Decision Trees for Interpretability

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 15: Decision Trees for Interpretability
- Week 8, Session 1

### Slide 2: Learning Objectives
1. Understand decision tree algorithms (CART)
2. Interpret tree structures for business insights
3. Apply pruning to prevent overfitting
4. Recognize when trees outperform other methods

### Slide 3: Why Decision Trees?
**The most interpretable ML model**:
- Visual, intuitive structure
- Mirrors human decision-making
- Handles non-linear relationships
- No feature scaling required
- Automatic feature selection

### Slide 4: Tree Structure
```
                    [Income > 50K?]
                    /            \
                 Yes              No
                  |                |
          [Age > 35?]      [Has Savings?]
          /        \        /         \
        Yes        No     Yes         No
         |          |       |           |
      Approve    Review  Review      Reject
```

**Components**: Root → Internal nodes → Leaf nodes (predictions)

### Slide 5: CART Algorithm
**Classification and Regression Trees**:

1. Start with all data at root
2. Find best split (feature + threshold)
3. Split into two child nodes
4. Repeat recursively
5. Stop when criteria met

**Splitting criteria**:
- Classification: Gini impurity, Entropy
- Regression: MSE, MAE

### Slide 6: Gini Impurity
$$Gini = 1 - \sum_{i=1}^{c} p_i^2$$

- Measures "impurity" of a node
- 0 = pure (all same class)
- 0.5 = maximum impurity (binary)

**Best split** = Largest reduction in weighted Gini

### Slide 7: Information Gain (Entropy)
$$Entropy = -\sum_{i=1}^{c} p_i \log_2(p_i)$$

$$Information\ Gain = Entropy_{parent} - \sum \frac{n_{child}}{n_{parent}} Entropy_{child}$$

**Best split** = Maximum information gain

### Slide 8: Building a Tree in Python
```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# Create and fit
tree = DecisionTreeClassifier(max_depth=4, random_state=42)
tree.fit(X_train, y_train)

# Visualize
plt.figure(figsize=(20, 10))
plot_tree(tree, feature_names=X.columns,
          class_names=['No', 'Yes'],
          filled=True, rounded=True)
plt.savefig('decision_tree.png', dpi=300, bbox_inches='tight')
```

### Slide 9: Reading a Decision Tree
**For each node**:
- **Condition**: Feature and threshold
- **Gini/Entropy**: Impurity measure
- **Samples**: Number of training examples
- **Value**: Class distribution [class0, class1]
- **Class**: Majority class prediction

### Slide 10: Overfitting in Trees
**Problem**: Deep trees memorize training data

**Symptoms**:
- Perfect training accuracy
- Poor test accuracy
- Complex, uninterpretable trees

**Visual**: Training vs test accuracy by tree depth

### Slide 11: Pruning Strategies
**Pre-pruning** (stop early):
- `max_depth`: Maximum tree depth
- `min_samples_split`: Minimum samples to split
- `min_samples_leaf`: Minimum samples in leaf
- `max_features`: Features to consider per split

```python
tree = DecisionTreeClassifier(
    max_depth=5,
    min_samples_split=20,
    min_samples_leaf=10
)
```

### Slide 12: Post-Pruning (Cost Complexity)
$$R_\alpha(T) = R(T) + \alpha|T|$$

- R(T): Misclassification rate
- |T|: Number of leaves
- α: Complexity parameter

```python
# Find optimal alpha with cross-validation
path = tree.cost_complexity_pruning_path(X_train, y_train)
alphas = path.ccp_alphas

# Test each alpha
scores = []
for alpha in alphas:
    clf = DecisionTreeClassifier(ccp_alpha=alpha)
    score = cross_val_score(clf, X_train, y_train, cv=5)
    scores.append(score.mean())
```

### Slide 13: Feature Importance
```python
# Get feature importance
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': tree.feature_importances_
}).sort_values('importance', ascending=False)

# Visualize
importance.plot(kind='barh', x='feature', y='importance')
plt.title('Feature Importance from Decision Tree')
```

**Interpretation**: Importance = total reduction in impurity

### Slide 14: When Trees Beat Neural Networks
**Trees are better when**:
- Interpretability required (regulated industries)
- Tabular data with mixed types
- Feature interactions matter
- Small to medium datasets
- Categorical features dominant

**Example**: Credit decisions require explainability

### Slide 15: Regression Trees
```python
from sklearn.tree import DecisionTreeRegressor

reg_tree = DecisionTreeRegressor(max_depth=5)
reg_tree.fit(X_train, y_train)

# Predictions are mean of leaf node
y_pred = reg_tree.predict(X_test)

# Same pruning applies
```

**Leaf value** = Mean of training samples in that leaf

### Slide 16: Philippine Example - Loan Approval
```python
# Load loan data
loans = pd.read_csv('ph_bank_loans.csv')

X = loans[['income', 'employment_years', 'loan_amount', 'credit_score']]
y = loans['approved']

# Fit interpretable tree
tree = DecisionTreeClassifier(max_depth=4)
tree.fit(X, y)

# Generate rules
from sklearn.tree import export_text
rules = export_text(tree, feature_names=list(X.columns))
print(rules)
```

### Slide 17: Extracting Business Rules
```
|--- credit_score <= 650
|   |--- income <= 25000
|   |   |--- class: Reject
|   |--- income > 25000
|   |   |--- employment_years <= 2
|   |   |   |--- class: Review
|   |   |--- employment_years > 2
|   |   |   |--- class: Approve
|--- credit_score > 650
|   |--- class: Approve
```

**Actionable insight**: Credit score > 650 = auto-approve

### Slide 18: Limitations of Single Trees
1. **High variance**: Small data changes → different tree
2. **Axis-aligned splits**: Can't capture diagonal boundaries
3. **Greedy**: May miss globally optimal splits
4. **Instability**: Not robust to outliers

**Solution**: Ensemble methods (next lecture)

### Slide 19: In-Class Exercise
**Build Interpretable Churn Predictor**:
1. Load Philippine telecom data
2. Fit decision tree (max_depth=5)
3. Visualize the tree
4. Extract top 3 business rules
5. Calculate feature importance

### Slide 20: Key Takeaways
1. Decision trees are the most interpretable ML model
2. CART uses Gini/Entropy to find best splits
3. Pruning prevents overfitting
4. Feature importance reveals drivers
5. Single trees have high variance → ensembles

### Slide 21: Next Lecture
**Lecture 16: Random Forests & Boosting**
- Ensemble methods overview
- Random Forest
- XGBoost/LightGBM
- SHAP for model explanation

---

## Lecture 16: Random Forests & Boosting

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 16: Random Forests & Boosting
- Week 8, Session 2

### Slide 2: Learning Objectives
1. Understand ensemble learning principles
2. Apply Random Forest for robust predictions
3. Use gradient boosting (XGBoost/LightGBM)
4. Explain model predictions with SHAP values

### Slide 3: Ensemble Learning
**"Wisdom of crowds"**: Combine multiple weak learners

**Types**:
- **Bagging**: Train in parallel, average results
- **Boosting**: Train sequentially, correct errors
- **Stacking**: Use predictions as features

### Slide 4: Bias-Variance Tradeoff
| Method | Bias | Variance | Strategy |
|--------|------|----------|----------|
| Single tree | Low | High | Overfit |
| Bagging | Low | Reduced | Average many trees |
| Boosting | Reduced | Low | Correct errors |

**Visual**: Bias-variance curves

### Slide 5: Random Forest Overview
**Bagging + Feature randomization**:

1. Create B bootstrap samples
2. For each sample, grow a tree
3. At each split, consider random subset of features
4. Aggregate predictions (vote or average)

### Slide 6: Why Random Subsets?
**Problem**: Correlated trees don't help
- If one feature dominates, all trees look similar

**Solution**: Random feature subset at each split
- `max_features='sqrt'` for classification
- `max_features='log2'` or `1/3` for regression
- Creates diverse, uncorrelated trees

### Slide 7: Random Forest in Python
```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=100,      # Number of trees
    max_depth=10,          # Depth of each tree
    max_features='sqrt',   # Features per split
    min_samples_leaf=5,    # Minimum leaf size
    n_jobs=-1,             # Parallel processing
    random_state=42
)

rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)[:, 1]
```

### Slide 8: Random Forest Feature Importance
```python
# Mean decrease in impurity
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

# Permutation importance (more reliable)
from sklearn.inspection import permutation_importance

perm_imp = permutation_importance(rf, X_test, y_test, n_repeats=10)
perm_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': perm_imp.importances_mean
}).sort_values('importance', ascending=False)
```

### Slide 9: Out-of-Bag (OOB) Error
**Free validation**: Each tree trained on ~63% of data

```python
rf = RandomForestClassifier(
    n_estimators=100,
    oob_score=True  # Enable OOB scoring
)
rf.fit(X_train, y_train)

print(f"OOB Score: {rf.oob_score_:.3f}")
# No need for separate validation set!
```

### Slide 10: Boosting Overview
**Sequential error correction**:

1. Train weak learner on data
2. Identify misclassified samples
3. Increase weight of misclassified
4. Train next learner on reweighted data
5. Combine all learners

### Slide 11: Gradient Boosting
$$F_m(x) = F_{m-1}(x) + \gamma_m h_m(x)$$

- Each tree fits the **residuals** of previous model
- Learning rate (γ) controls contribution
- Lower learning rate = more trees needed = better generalization

### Slide 12: XGBoost
**Extreme Gradient Boosting**: Fast, regularized, scalable

```python
import xgboost as xgb

xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,       # L1 regularization
    reg_lambda=1.0,      # L2 regularization
    random_state=42
)

xgb_model.fit(X_train, y_train,
              eval_set=[(X_val, y_val)],
              early_stopping_rounds=10)
```

### Slide 13: LightGBM
**Light Gradient Boosting Machine**: Even faster, handles large data

```python
import lightgbm as lgb

lgb_model = lgb.LGBMClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    num_leaves=31,       # Main complexity parameter
    feature_fraction=0.8,
    bagging_fraction=0.8,
    random_state=42
)

lgb_model.fit(X_train, y_train,
              eval_set=[(X_val, y_val)],
              callbacks=[lgb.early_stopping(10)])
```

### Slide 14: Random Forest vs Boosting
| Aspect | Random Forest | Boosting |
|--------|---------------|----------|
| Training | Parallel | Sequential |
| Speed | Faster | Slower |
| Overfitting | Less prone | More prone |
| Tuning | Easier | More hyperparams |
| Performance | Good | Often best |

**Rule of thumb**: Start with RF, try boosting for extra performance

### Slide 15: Hyperparameter Tuning
```python
from sklearn.model_selection import RandomizedSearchCV

param_dist = {
    'n_estimators': [100, 200, 500],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

rf_random = RandomizedSearchCV(
    RandomForestClassifier(),
    param_dist,
    n_iter=20,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1
)
rf_random.fit(X_train, y_train)
print(f"Best params: {rf_random.best_params_}")
```

### Slide 16: SHAP Values
**SHapley Additive exPlanations**: Explain individual predictions

```python
import shap

# Create explainer
explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_test)

# Summary plot (global importance)
shap.summary_plot(shap_values[1], X_test)

# Force plot (individual prediction)
shap.force_plot(explainer.expected_value[1],
                shap_values[1][0], X_test.iloc[0])
```

### Slide 17: SHAP Interpretation
**For each prediction**:
- Base value: Average prediction
- Each feature contributes + or -
- Sum of contributions = final prediction

**Visual**: Waterfall plot showing feature contributions

### Slide 18: Philippine Example - Credit Risk
```python
# Load credit data
credit = pd.read_csv('ph_credit_data.csv')

X = credit.drop('default', axis=1)
y = credit['default']

# Train XGBoost
xgb_model = xgb.XGBClassifier(n_estimators=100, max_depth=5)
xgb_model.fit(X_train, y_train)

# SHAP analysis
explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(X_test)

# Why was this customer rejected?
customer_idx = 42
shap.waterfall_plot(shap.Explanation(
    values=shap_values[customer_idx],
    base_values=explainer.expected_value,
    data=X_test.iloc[customer_idx]
))
```

### Slide 19: In-Class Exercise
**Ensemble Model Comparison**:
1. Load Philippine e-commerce churn data
2. Train: Decision Tree, Random Forest, XGBoost
3. Compare AUC scores
4. Plot feature importance from each
5. Explain one prediction with SHAP

### Slide 20: Key Takeaways
1. Ensembles combine multiple models for better performance
2. Random Forest: Bagging + feature randomization
3. Boosting: Sequential error correction
4. XGBoost/LightGBM are state-of-the-art for tabular data
5. SHAP explains individual predictions

### Slide 21: Lab Preview
**Lab 7: Ensemble Methods Competition**
- Build best model for Philippine dataset
- Compare multiple algorithms
- Document feature engineering
- Present findings

---

# WEEK 9: Clustering & Segmentation

---

## Lecture 17: Unsupervised Learning for Business

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 17: Unsupervised Learning for Business
- Week 9, Session 1

### Slide 2: Learning Objectives
1. Understand unsupervised learning applications
2. Apply K-means clustering algorithm
3. Determine optimal number of clusters
4. Interpret clusters for business segmentation

### Slide 3: Supervised vs Unsupervised
| Supervised | Unsupervised |
|------------|--------------|
| Has labels (y) | No labels |
| Predict outcome | Find structure |
| Classification, Regression | Clustering, Dimensionality reduction |
| "What will happen?" | "What patterns exist?" |

### Slide 4: Business Applications
**Customer Segmentation**:
- Group customers by behavior
- Tailor marketing strategies
- Personalize experiences

**Other uses**:
- Document clustering
- Anomaly detection
- Image compression
- Market research

### Slide 5: K-Means Algorithm
**Goal**: Partition n observations into k clusters

**Steps**:
1. Initialize k centroids randomly
2. Assign each point to nearest centroid
3. Recalculate centroids as cluster means
4. Repeat until convergence

**Objective**: Minimize within-cluster sum of squares

### Slide 6: K-Means Visualization
```
Iteration 1:     Iteration 2:     Iteration 3:
    *                *                *
   /|\              /|\              /|\
  . . .            . . .            . . .
  . * .    →       . * .    →       . * .
  . . .            . . .            . . .
    *                *                *
```

**Visual**: Animation of centroid movement

### Slide 7: K-Means in Python
```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Always scale first!
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit K-Means
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

# Add to dataframe
df['cluster'] = clusters
```

### Slide 8: Choosing K - Elbow Method
```python
inertias = []
K_range = range(1, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

plt.plot(K_range, inertias, 'bo-')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia (Within-cluster SS)')
plt.title('Elbow Method')
```

**Look for**: "Elbow" where improvement slows

### Slide 9: Choosing K - Silhouette Score
$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$

- a(i): Mean distance to points in same cluster
- b(i): Mean distance to nearest other cluster
- Range: -1 to 1 (higher = better)

```python
from sklearn.metrics import silhouette_score

for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    print(f"K={k}: Silhouette = {score:.3f}")
```

### Slide 10: Silhouette Plot
```python
from sklearn.metrics import silhouette_samples
import numpy as np

silhouette_vals = silhouette_samples(X_scaled, clusters)

y_lower = 10
for i in range(n_clusters):
    cluster_silhouette = silhouette_vals[clusters == i]
    cluster_silhouette.sort()

    y_upper = y_lower + len(cluster_silhouette)
    plt.fill_betweenx(np.arange(y_lower, y_upper),
                      0, cluster_silhouette)
    y_lower = y_upper + 10
```

### Slide 11: Interpreting Clusters
```python
# Cluster profiles
cluster_summary = df.groupby('cluster').agg({
    'revenue': 'mean',
    'frequency': 'mean',
    'recency': 'mean',
    'age': 'mean'
}).round(2)

# Visualize
cluster_summary.plot(kind='bar', subplots=True, layout=(2,2), figsize=(12,8))

# Name clusters based on characteristics
cluster_names = {
    0: 'High-Value Loyalists',
    1: 'New Customers',
    2: 'At-Risk',
    3: 'Lost Customers'
}
df['segment'] = df['cluster'].map(cluster_names)
```

### Slide 12: Visualizing Clusters
```python
# 2D visualization with PCA
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            marker='X', s=200, c='red', label='Centroids')
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
```

### Slide 13: K-Means Limitations
1. **Assumes spherical clusters**: Can't find elongated shapes
2. **Sensitive to initialization**: Run multiple times
3. **Requires specifying K**: Must choose beforehand
4. **Sensitive to outliers**: Pulls centroids
5. **Equal variance assumption**: May not fit real data

### Slide 14: Hierarchical Clustering
**Agglomerative (bottom-up)**:
1. Start with each point as cluster
2. Merge closest pair
3. Repeat until one cluster

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# Fit hierarchical clustering
hc = AgglomerativeClustering(n_clusters=4, linkage='ward')
hc_labels = hc.fit_predict(X_scaled)

# Dendrogram
Z = linkage(X_scaled, method='ward')
dendrogram(Z, truncate_mode='level', p=5)
```

### Slide 15: Dendrogram Interpretation
```
         _______|_______
        |               |
    ____|____       ____|____
   |         |     |         |
  _|_       _|_   _|_       _|_
 |   |     |   | |   |     |   |
 A   B     C   D E   F     G   H
```

**Cut at different heights** = Different number of clusters

### Slide 16: Linkage Methods
| Method | Description | Use When |
|--------|-------------|----------|
| Single | Min distance | Chain-like clusters |
| Complete | Max distance | Compact clusters |
| Average | Mean distance | Balanced |
| Ward | Minimize variance | Similar size clusters |

### Slide 17: Philippine Example - Customer Segmentation
```python
# Load GCash-style transaction data
customers = pd.read_csv('ph_gcash_customers.csv')

# RFM features
rfm = customers.groupby('customer_id').agg({
    'transaction_date': lambda x: (today - x.max()).days,  # Recency
    'transaction_id': 'count',  # Frequency
    'amount': 'sum'  # Monetary
}).rename(columns={
    'transaction_date': 'recency',
    'transaction_id': 'frequency',
    'amount': 'monetary'
})

# Scale and cluster
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)
kmeans = KMeans(n_clusters=4, random_state=42)
rfm['segment'] = kmeans.fit_predict(rfm_scaled)
```

### Slide 18: Segment Profiles
| Segment | Recency | Frequency | Monetary | Action |
|---------|---------|-----------|----------|--------|
| Champions | Low | High | High | Reward loyalty |
| Potential | Low | Medium | Medium | Upsell |
| At Risk | High | Low | Medium | Win back |
| Lost | High | Low | Low | Re-engage |

### Slide 19: In-Class Exercise
**Retail Customer Segmentation**:
1. Load Philippine retail data
2. Create RFM features
3. Determine optimal K (elbow + silhouette)
4. Profile each segment
5. Recommend marketing strategy per segment

### Slide 20: Key Takeaways
1. Clustering finds natural groups without labels
2. K-Means: Simple, fast, but assumes spherical clusters
3. Use elbow + silhouette to choose K
4. Hierarchical clustering shows relationships
5. Always interpret clusters with business context

### Slide 21: Next Lecture
**Lecture 18: Advanced Clustering & Applications**
- DBSCAN for anomaly detection
- Market basket analysis
- RFM deep dive

---

## Lecture 18: Advanced Clustering & Applications

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 18: Advanced Clustering & Applications
- Week 9, Session 2

### Slide 2: Learning Objectives
1. Apply DBSCAN for density-based clustering
2. Detect anomalies using clustering
3. Perform market basket analysis
4. Conduct comprehensive RFM analysis

### Slide 3: DBSCAN Overview
**Density-Based Spatial Clustering of Applications with Noise**

**Advantages**:
- No need to specify K
- Finds arbitrarily shaped clusters
- Identifies outliers (noise)

**Parameters**:
- `eps`: Maximum distance between neighbors
- `min_samples`: Minimum points to form cluster

### Slide 4: DBSCAN Concepts
**Point types**:
- **Core point**: Has ≥ min_samples within eps
- **Border point**: Within eps of core point
- **Noise point**: Neither core nor border

**Visual**: Diagram showing point types

### Slide 5: DBSCAN in Python
```python
from sklearn.cluster import DBSCAN

# Fit DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
labels = dbscan.fit_predict(X_scaled)

# Cluster labels: -1 = noise
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
n_noise = list(labels).count(-1)

print(f"Clusters: {n_clusters}, Noise points: {n_noise}")
```

### Slide 6: Choosing DBSCAN Parameters
```python
from sklearn.neighbors import NearestNeighbors

# K-distance plot to find eps
neighbors = NearestNeighbors(n_neighbors=5)
neighbors.fit(X_scaled)
distances, _ = neighbors.kneighbors(X_scaled)

# Sort and plot
distances = np.sort(distances[:, -1])
plt.plot(distances)
plt.xlabel('Points sorted by distance')
plt.ylabel('5th Nearest Neighbor Distance')
plt.title('K-Distance Plot')
# Look for "elbow" - that's your eps
```

### Slide 7: DBSCAN vs K-Means
| Aspect | K-Means | DBSCAN |
|--------|---------|--------|
| Cluster shape | Spherical | Any shape |
| Number of clusters | Must specify | Automatic |
| Outliers | Assigns to cluster | Labels as noise |
| Density | Assumes uniform | Handles varying |
| Scalability | Better | Slower |

### Slide 8: Anomaly Detection with Clustering
**Using clustering for fraud detection**:

```python
# Method 1: DBSCAN noise points
dbscan = DBSCAN(eps=0.5, min_samples=10)
labels = dbscan.fit_predict(X_scaled)
anomalies = X[labels == -1]

# Method 2: Distance from centroid
kmeans = KMeans(n_clusters=5)
kmeans.fit(X_scaled)
distances = kmeans.transform(X_scaled).min(axis=1)
threshold = np.percentile(distances, 95)
anomalies = X[distances > threshold]
```

### Slide 9: Isolation Forest
**Another anomaly detection method**:

```python
from sklearn.ensemble import IsolationForest

iso_forest = IsolationForest(
    contamination=0.05,  # Expected anomaly proportion
    random_state=42
)
anomaly_labels = iso_forest.fit_predict(X_scaled)
# 1 = normal, -1 = anomaly

anomalies = X[anomaly_labels == -1]
```

### Slide 10: Market Basket Analysis
**Goal**: Find products frequently bought together

**Applications**:
- Product recommendations
- Store layout optimization
- Cross-selling strategies
- Promotional bundles

### Slide 11: Association Rules Concepts
**Support**: How often items appear together
$$Support(A \rightarrow B) = \frac{\text{Transactions with A and B}}{\text{Total transactions}}$$

**Confidence**: How often rule is correct
$$Confidence(A \rightarrow B) = \frac{Support(A, B)}{Support(A)}$$

**Lift**: Strength of association
$$Lift(A \rightarrow B) = \frac{Confidence(A \rightarrow B)}{Support(B)}$$

### Slide 12: Apriori Algorithm
```python
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# Prepare transaction data
transactions = [
    ['milk', 'bread', 'eggs'],
    ['milk', 'bread'],
    ['bread', 'butter'],
    ['milk', 'eggs'],
    # ...
]

# Encode
te = TransactionEncoder()
te_array = te.fit_transform(transactions)
df_encoded = pd.DataFrame(te_array, columns=te.columns_)

# Find frequent itemsets
frequent_items = apriori(df_encoded, min_support=0.05, use_colnames=True)

# Generate rules
rules = association_rules(frequent_items, metric='lift', min_threshold=1.0)
```

### Slide 13: Interpreting Rules
```python
# Top rules by lift
top_rules = rules.sort_values('lift', ascending=False).head(10)

print(top_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# Example output:
# antecedents     consequents    support  confidence  lift
# {eggs}          {milk}         0.08     0.75        2.5
# {bread, butter} {milk}         0.05     0.80        2.7
```

**Interpretation**: Customers who buy eggs are 2.5x more likely to buy milk

### Slide 14: Philippine Example - Retail Basket
```python
# Load SM/Puregold transaction data
baskets = pd.read_csv('ph_retail_baskets.csv')

# One-hot encode
basket_encoded = baskets.groupby(['transaction_id', 'product'])['quantity'].sum().unstack().fillna(0)
basket_encoded = (basket_encoded > 0).astype(int)

# Find associations
frequent = apriori(basket_encoded, min_support=0.02, use_colnames=True)
rules = association_rules(frequent, metric='lift', min_threshold=1.5)

# Filter interesting rules
interesting = rules[(rules['confidence'] > 0.5) & (rules['lift'] > 2)]
```

### Slide 15: RFM Analysis Deep Dive
**Recency**: Days since last purchase
**Frequency**: Number of purchases
**Monetary**: Total spend

```python
# Calculate RFM
snapshot_date = df['order_date'].max() + timedelta(days=1)

rfm = df.groupby('customer_id').agg({
    'order_date': lambda x: (snapshot_date - x.max()).days,
    'order_id': 'nunique',
    'amount': 'sum'
}).rename(columns={
    'order_date': 'recency',
    'order_id': 'frequency',
    'amount': 'monetary'
})
```

### Slide 16: RFM Scoring
```python
# Create quintile scores (1-5)
rfm['R_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['M_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])

# Combined RFM score
rfm['RFM_score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

# Segment mapping
segment_map = {
    r'[4-5][4-5][4-5]': 'Champions',
    r'[3-5][3-5][3-5]': 'Loyal Customers',
    r'[4-5][0-2][0-2]': 'New Customers',
    r'[0-2][4-5][4-5]': 'At Risk',
    r'[0-2][0-2][0-2]': 'Lost',
}
```

### Slide 17: RFM Segment Actions
| Segment | Description | Action |
|---------|-------------|--------|
| Champions | Recent, frequent, high value | Reward, early access |
| Loyal | Consistent purchasers | Upsell, referral program |
| Potential | Recent, low frequency | Onboarding, education |
| At Risk | Lapsed high-value | Win-back campaign |
| Hibernating | Long inactive | Reactivation offer |
| Lost | Very long inactive | Survey, last attempt |

### Slide 18: Combining Clustering + RFM
```python
# Use clustering on RFM features
from sklearn.cluster import KMeans

rfm_features = rfm[['recency', 'frequency', 'monetary']]
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_features)

# Optimal clusters
kmeans = KMeans(n_clusters=5, random_state=42)
rfm['cluster'] = kmeans.fit_predict(rfm_scaled)

# Profile clusters
cluster_profile = rfm.groupby('cluster').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': ['mean', 'count']
}).round(2)
```

### Slide 19: In-Class Exercise
**Complete Customer Analytics**:
1. Load Philippine e-commerce data
2. Calculate RFM metrics
3. Cluster customers (K-Means + DBSCAN comparison)
4. Perform basket analysis
5. Create segment recommendations

### Slide 20: Key Takeaways
1. DBSCAN finds arbitrary shapes and identifies outliers
2. Anomaly detection uses distance from normal patterns
3. Market basket analysis finds product associations
4. RFM segments customers by value and behavior
5. Combine methods for comprehensive customer analytics

### Slide 21: Lab Preview
**Lab 8: Customer Segmentation Project**
- End-to-end customer analysis
- RFM + Clustering + Basket analysis
- Segment profiles and recommendations
- Presentation to "marketing team"

---

# WEEK 10: Time Series Analytics

---

## Lecture 19: Time Series Fundamentals

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 19: Time Series Fundamentals
- Week 10, Session 1

### Slide 2: Learning Objectives
1. Understand time series components
2. Test and achieve stationarity
3. Analyze autocorrelation patterns
4. Apply smoothing techniques

### Slide 3: What is Time Series Data?
**Definition**: Sequence of data points indexed in time order

**Characteristics**:
- Temporal dependence (today affects tomorrow)
- Trend (long-term direction)
- Seasonality (repeating patterns)
- Noise (random variation)

**Examples**: Stock prices, sales, weather, web traffic

### Slide 4: Time Series Components
$$Y_t = T_t + S_t + R_t$$ (Additive)
$$Y_t = T_t \times S_t \times R_t$$ (Multiplicative)

- **T**: Trend component
- **S**: Seasonal component
- **R**: Residual (noise)

**Visual**: Decomposition plot

### Slide 5: Time Series in Python
```python
import pandas as pd

# Load and set datetime index
df = pd.read_csv('sales.csv', parse_dates=['date'])
df.set_index('date', inplace=True)

# Ensure datetime index
df.index = pd.DatetimeIndex(df.index)

# Basic plot
df['sales'].plot(figsize=(12, 4))
plt.title('Daily Sales')
```

### Slide 6: Resampling
```python
# Aggregate to different frequencies
daily = df['sales']
weekly = df['sales'].resample('W').sum()
monthly = df['sales'].resample('M').sum()
quarterly = df['sales'].resample('Q').sum()

# Plot comparisons
fig, axes = plt.subplots(2, 2, figsize=(14, 8))
daily.plot(ax=axes[0,0], title='Daily')
weekly.plot(ax=axes[0,1], title='Weekly')
monthly.plot(ax=axes[1,0], title='Monthly')
quarterly.plot(ax=axes[1,1], title='Quarterly')
```

### Slide 7: Decomposition
```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Decompose (requires datetime index)
decomposition = seasonal_decompose(df['sales'], model='additive', period=7)

# Plot components
fig, axes = plt.subplots(4, 1, figsize=(12, 10))
decomposition.observed.plot(ax=axes[0], title='Observed')
decomposition.trend.plot(ax=axes[1], title='Trend')
decomposition.seasonal.plot(ax=axes[2], title='Seasonal')
decomposition.resid.plot(ax=axes[3], title='Residual')
```

### Slide 8: Stationarity
**A series is stationary if**:
- Constant mean over time
- Constant variance over time
- Covariance depends only on lag

**Why it matters**: Most forecasting methods assume stationarity

### Slide 9: Testing Stationarity
**Augmented Dickey-Fuller (ADF) Test**:
- H₀: Series has unit root (non-stationary)
- H₁: Series is stationary

```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(df['sales'])
print(f'ADF Statistic: {result[0]:.4f}')
print(f'p-value: {result[1]:.4f}')

# p < 0.05: Reject H0, series is stationary
if result[1] < 0.05:
    print("Series is stationary")
else:
    print("Series is non-stationary")
```

### Slide 10: Achieving Stationarity
**Differencing**: Remove trend
```python
# First difference
df['diff_1'] = df['sales'].diff()

# Second difference (if needed)
df['diff_2'] = df['sales'].diff().diff()

# Seasonal differencing
df['seasonal_diff'] = df['sales'].diff(7)  # Weekly seasonality
```

**Log transformation**: Stabilize variance
```python
df['log_sales'] = np.log(df['sales'])
```

### Slide 11: Autocorrelation
**ACF**: Correlation with lagged values
$$\rho_k = \frac{Cov(Y_t, Y_{t-k})}{Var(Y_t)}$$

```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, axes = plt.subplots(1, 2, figsize=(14, 4))
plot_acf(df['sales'], lags=30, ax=axes[0])
plot_pacf(df['sales'], lags=30, ax=axes[1])
```

### Slide 12: Interpreting ACF/PACF
| Pattern | ACF | PACF | Model Suggested |
|---------|-----|------|-----------------|
| Cut off lag q | Exponential decay | AR(p) |
| Exponential decay | Cut off lag p | MA(q) |
| Exponential decay | Exponential decay | ARMA(p,q) |
| Significant lag s | Significant lag s | Seasonal |

### Slide 13: Moving Average Smoothing
```python
# Simple moving average
df['SMA_7'] = df['sales'].rolling(window=7).mean()
df['SMA_30'] = df['sales'].rolling(window=30).mean()

# Centered moving average
df['CMA_7'] = df['sales'].rolling(window=7, center=True).mean()

# Plot
plt.figure(figsize=(12, 4))
plt.plot(df['sales'], alpha=0.5, label='Original')
plt.plot(df['SMA_7'], label='7-day MA')
plt.plot(df['SMA_30'], label='30-day MA')
plt.legend()
```

### Slide 14: Exponential Smoothing
**Weights recent observations more**:
$$S_t = \alpha Y_t + (1-\alpha) S_{t-1}$$

```python
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

# Fit exponential smoothing
ses = SimpleExpSmoothing(df['sales']).fit(smoothing_level=0.2)
df['SES'] = ses.fittedvalues

# Compare alphas
for alpha in [0.1, 0.3, 0.5]:
    ses = SimpleExpSmoothing(df['sales']).fit(smoothing_level=alpha)
    plt.plot(ses.fittedvalues, label=f'alpha={alpha}')
```

### Slide 15: Double Exponential (Holt's)
**Handles trend**:
$$L_t = \alpha Y_t + (1-\alpha)(L_{t-1} + T_{t-1})$$
$$T_t = \beta(L_t - L_{t-1}) + (1-\beta)T_{t-1}$$

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Holt's method (trend)
holt = ExponentialSmoothing(df['sales'], trend='add').fit()
df['Holt'] = holt.fittedvalues

# Forecast
forecast = holt.forecast(30)
```

### Slide 16: Triple Exponential (Holt-Winters)
**Handles trend + seasonality**:

```python
# Holt-Winters (trend + seasonality)
hw = ExponentialSmoothing(
    df['sales'],
    trend='add',
    seasonal='add',
    seasonal_periods=7
).fit()

df['HW'] = hw.fittedvalues
forecast = hw.forecast(30)
```

### Slide 17: Philippine Example - Remittances
```python
# Load BSP remittance data
remit = pd.read_csv('bsp_remittances_monthly.csv', parse_dates=['date'])
remit.set_index('date', inplace=True)

# Decompose (monthly data, annual seasonality)
decomp = seasonal_decompose(remit['remittances_usd'], period=12)
decomp.plot()

# Check stationarity
adf_result = adfuller(remit['remittances_usd'])
print(f"ADF p-value: {adf_result[1]:.4f}")

# Smooth
remit['SMA_12'] = remit['remittances_usd'].rolling(12).mean()
```

### Slide 18: Handling Missing Values
```python
# Forward fill
df['sales_ffill'] = df['sales'].fillna(method='ffill')

# Interpolation
df['sales_interp'] = df['sales'].interpolate(method='time')

# Seasonal interpolation (for periodic data)
df['sales_seasonal'] = df['sales'].interpolate(method='spline', order=3)
```

### Slide 19: In-Class Exercise
**Time Series EDA**:
1. Load Philippine stock (PSEi) data
2. Plot and decompose
3. Test stationarity
4. Apply differencing if needed
5. Plot ACF/PACF
6. Apply Holt-Winters smoothing

### Slide 20: Key Takeaways
1. Time series has trend, seasonality, and noise
2. Stationarity required for most forecasting
3. Differencing removes trend
4. ACF/PACF guide model selection
5. Exponential smoothing adapts to patterns

### Slide 21: Next Lecture
**Lecture 20: Forecasting Methods**
- ARIMA modeling
- Seasonal ARIMA
- Prophet for business
- Forecast evaluation

---

## Lecture 20: Forecasting Methods

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 20: Forecasting Methods
- Week 10, Session 2

### Slide 2: Learning Objectives
1. Build ARIMA models for forecasting
2. Apply seasonal ARIMA (SARIMA)
3. Use Facebook Prophet for business forecasting
4. Evaluate forecast accuracy

### Slide 3: ARIMA Overview
**AutoRegressive Integrated Moving Average**

- **AR(p)**: Past values predict future
- **I(d)**: Differencing for stationarity
- **MA(q)**: Past errors predict future

$$Y_t = c + \phi_1 Y_{t-1} + ... + \phi_p Y_{t-p} + \theta_1 \epsilon_{t-1} + ... + \theta_q \epsilon_{t-q} + \epsilon_t$$

### Slide 4: AR Component
**AutoRegressive**: Current value depends on past values

$$Y_t = c + \phi_1 Y_{t-1} + \phi_2 Y_{t-2} + ... + \epsilon_t$$

**Order p**: Number of lag terms
**Identified by**: PACF cut-off

### Slide 5: MA Component
**Moving Average**: Current value depends on past errors

$$Y_t = c + \theta_1 \epsilon_{t-1} + \theta_2 \epsilon_{t-2} + ... + \epsilon_t$$

**Order q**: Number of error terms
**Identified by**: ACF cut-off

### Slide 6: I Component (Integration)
**Differencing**: Makes series stationary

- d=0: Already stationary
- d=1: First difference
- d=2: Second difference (rare)

**Test**: ADF test after differencing

### Slide 7: ARIMA in Python
```python
from statsmodels.tsa.arima.model import ARIMA

# Fit ARIMA(p,d,q)
model = ARIMA(df['sales'], order=(2, 1, 1))
results = model.fit()

print(results.summary())

# Diagnostics
results.plot_diagnostics(figsize=(12, 8))
```

### Slide 8: Choosing p, d, q
**Manual (Box-Jenkins)**:
1. Test stationarity → determine d
2. Plot PACF → determine p
3. Plot ACF → determine q

**Automatic**:
```python
from pmdarima import auto_arima

auto_model = auto_arima(
    df['sales'],
    start_p=0, max_p=5,
    start_q=0, max_q=5,
    d=None,  # Auto-detect
    seasonal=False,
    trace=True
)
print(auto_model.summary())
```

### Slide 9: ARIMA Forecasting
```python
# In-sample fit
fitted = results.fittedvalues

# Out-of-sample forecast
forecast = results.forecast(steps=30)

# With confidence intervals
forecast_result = results.get_forecast(steps=30)
forecast_mean = forecast_result.predicted_mean
conf_int = forecast_result.conf_int()

# Plot
plt.figure(figsize=(12, 4))
plt.plot(df['sales'], label='Observed')
plt.plot(forecast_mean, label='Forecast', color='red')
plt.fill_between(conf_int.index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], alpha=0.2)
plt.legend()
```

### Slide 10: Seasonal ARIMA (SARIMA)
**ARIMA + Seasonal terms**: ARIMA(p,d,q)(P,D,Q)s

$$SARIMA(1,1,1)(1,1,1)_{12}$$

- (1,1,1): Non-seasonal parameters
- (1,1,1): Seasonal parameters
- 12: Seasonal period (monthly)

### Slide 11: SARIMA in Python
```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

# SARIMA with monthly seasonality
model = SARIMAX(
    df['sales'],
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12)
)
results = model.fit()

# Forecast
forecast = results.forecast(steps=12)
```

### Slide 12: Facebook Prophet
**Designed for business forecasting**:
- Handles missing data
- Robust to outliers
- Automatic changepoint detection
- Easy to add holidays/events

### Slide 13: Prophet Setup
```python
from prophet import Prophet

# Prophet requires specific column names
df_prophet = df.reset_index()
df_prophet.columns = ['ds', 'y']  # ds=date, y=value

# Create and fit model
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)
model.fit(df_prophet)
```

### Slide 14: Prophet Forecasting
```python
# Create future dataframe
future = model.make_future_dataframe(periods=30)

# Predict
forecast = model.predict(future)

# Plot
model.plot(forecast)

# Component plot
model.plot_components(forecast)
```

### Slide 15: Adding Holidays to Prophet
```python
# Philippine holidays
ph_holidays = pd.DataFrame({
    'holiday': 'philippine_holiday',
    'ds': pd.to_datetime([
        '2024-01-01',  # New Year
        '2024-04-09',  # Araw ng Kagitingan
        '2024-06-12',  # Independence Day
        '2024-11-01',  # All Saints
        '2024-12-25',  # Christmas
        '2024-12-30',  # Rizal Day
    ]),
    'lower_window': 0,
    'upper_window': 1
})

model = Prophet(holidays=ph_holidays)
model.fit(df_prophet)
```

### Slide 16: Forecast Evaluation Metrics
| Metric | Formula | Interpretation |
|--------|---------|----------------|
| MAE | mean(\|y - ŷ\|) | Average absolute error |
| RMSE | √mean((y - ŷ)²) | Penalizes large errors |
| MAPE | mean(\|y - ŷ\|/y) × 100 | Percentage error |
| MASE | MAE / naive_MAE | Compared to naive forecast |

### Slide 17: Train-Test Split for Time Series
```python
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Split (preserve time order!)
train = df['sales'][:-30]
test = df['sales'][-30:]

# Fit on train
model = ARIMA(train, order=(2,1,1))
results = model.fit()

# Forecast test period
forecast = results.forecast(steps=30)

# Evaluate
mae = mean_absolute_error(test, forecast)
rmse = np.sqrt(mean_squared_error(test, forecast))
mape = np.mean(np.abs((test - forecast) / test)) * 100

print(f"MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape:.2f}%")
```

### Slide 18: Cross-Validation for Time Series
```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)

scores = []
for train_idx, test_idx in tscv.split(df):
    train = df.iloc[train_idx]['sales']
    test = df.iloc[test_idx]['sales']

    model = ARIMA(train, order=(2,1,1))
    results = model.fit()
    forecast = results.forecast(steps=len(test))

    mape = np.mean(np.abs((test.values - forecast.values) / test.values)) * 100
    scores.append(mape)

print(f"Average MAPE: {np.mean(scores):.2f}%")
```

### Slide 19: Philippine Example - Stock Forecasting
```python
# Load PSEi data
psei = pd.read_csv('psei_daily.csv', parse_dates=['date'])
psei.set_index('date', inplace=True)

# Prophet model
df_prophet = psei.reset_index()[['date', 'close']]
df_prophet.columns = ['ds', 'y']

model = Prophet(changepoint_prior_scale=0.05)
model.fit(df_prophet)

# Forecast 30 trading days
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Plot with uncertainty
model.plot(forecast)
plt.title('PSEi 30-Day Forecast')
```

### Slide 20: In-Class Exercise
**Forecasting Challenge**:
1. Load Philippine exchange rate data (PHP/USD)
2. Split into train/test
3. Build ARIMA and Prophet models
4. Compare MAPE scores
5. Visualize forecasts with confidence intervals

### Slide 21: Key Takeaways
1. ARIMA combines AR, differencing, and MA
2. SARIMA handles seasonal patterns
3. Prophet is robust for business forecasting
4. Use time-aware train/test splits
5. MAPE is intuitive for business stakeholders

### Slide 22: Lab Preview
**Lab 9: Time Series Forecasting Project**
- Forecast Philippine economic indicator
- Compare multiple methods
- Document methodology
- Present to "management"

---

# WEEK 11: Text Analytics & Advanced Topics

---

## Lecture 21: Text Analytics Fundamentals

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 21: Text Analytics Fundamentals
- Week 11, Session 1

### Slide 2: Learning Objectives
1. Preprocess text data for analysis
2. Apply TF-IDF vectorization
3. Perform sentiment analysis
4. Conduct topic modeling with LDA

### Slide 3: Why Text Analytics?
**Unstructured data is everywhere**:
- Customer reviews
- Social media
- Support tickets
- Survey responses
- News articles

**Goal**: Extract insights from text

### Slide 4: Text Preprocessing Pipeline
1. **Lowercasing**: "Hello" → "hello"
2. **Tokenization**: "hello world" → ["hello", "world"]
3. **Stop word removal**: Remove "the", "is", "at"
4. **Punctuation removal**: Remove "!", "?", "."
5. **Stemming/Lemmatization**: "running" → "run"

### Slide 5: Preprocessing in Python
```python
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess(text):
    # Lowercase
    text = text.lower()
    # Tokenize
    tokens = word_tokenize(text)
    # Remove punctuation and stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop_words and t not in string.punctuation]
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return tokens
```

### Slide 6: Bag of Words
**Simplest representation**: Count word occurrences

```python
from sklearn.feature_extraction.text import CountVectorizer

corpus = [
    "The food was good",
    "The service was bad",
    "Good food but bad service"
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)

print(vectorizer.get_feature_names_out())
print(X.toarray())
```

### Slide 7: TF-IDF
**Term Frequency - Inverse Document Frequency**

$$TF\text{-}IDF = TF \times IDF$$
$$IDF = \log\frac{N}{df_t}$$

- **TF**: How often term appears in document
- **IDF**: How rare term is across documents
- **Result**: Important words get higher weight

### Slide 8: TF-IDF in Python
```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(
    max_features=1000,
    min_df=5,
    max_df=0.95,
    ngram_range=(1, 2)  # Unigrams and bigrams
)

X_tfidf = tfidf.fit_transform(documents)

# Most important terms per document
feature_names = tfidf.get_feature_names_out()
for i, doc in enumerate(X_tfidf):
    top_indices = doc.toarray().argsort()[0][-5:]
    top_terms = [feature_names[j] for j in top_indices]
    print(f"Doc {i}: {top_terms}")
```

### Slide 9: Sentiment Analysis
**Goal**: Classify text as positive, negative, or neutral

**Approaches**:
1. **Lexicon-based**: Use sentiment dictionaries
2. **ML-based**: Train classifier on labeled data
3. **Pre-trained**: Use existing models (VADER, TextBlob)

### Slide 10: VADER Sentiment
```python
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

texts = [
    "This product is amazing! I love it!",
    "Terrible experience, never buying again",
    "It's okay, nothing special"
]

for text in texts:
    scores = sia.polarity_scores(text)
    print(f"{text}")
    print(f"  Compound: {scores['compound']:.2f}")
    # Compound: -1 (negative) to +1 (positive)
```

### Slide 11: TextBlob Sentiment
```python
from textblob import TextBlob

text = "The food was delicious but the service was slow"
blob = TextBlob(text)

print(f"Polarity: {blob.sentiment.polarity:.2f}")   # -1 to 1
print(f"Subjectivity: {blob.sentiment.subjectivity:.2f}")  # 0 to 1

# Sentence-level analysis
for sentence in blob.sentences:
    print(f"'{sentence}' → {sentence.sentiment.polarity:.2f}")
```

### Slide 12: ML-based Sentiment
```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Labeled training data
X_train = ["great product", "terrible quality", ...]
y_train = [1, 0, ...]  # 1=positive, 0=negative

# Pipeline: TF-IDF + Naive Bayes
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

pipeline.fit(X_train, y_train)

# Predict new reviews
new_reviews = ["I love this!", "Worst purchase ever"]
predictions = pipeline.predict(new_reviews)
```

### Slide 13: Topic Modeling with LDA
**Latent Dirichlet Allocation**: Discover hidden topics

**Assumptions**:
- Documents are mixtures of topics
- Topics are distributions over words

```python
from sklearn.decomposition import LatentDirichletAllocation

# Fit LDA
lda = LatentDirichletAllocation(
    n_components=5,  # Number of topics
    random_state=42
)
lda.fit(X_tfidf)

# Print top words per topic
feature_names = tfidf.get_feature_names_out()
for i, topic in enumerate(lda.components_):
    top_words = [feature_names[j] for j in topic.argsort()[-10:]]
    print(f"Topic {i}: {', '.join(top_words)}")
```

### Slide 14: Visualizing Topics
```python
import pyLDAvis.sklearn

# Interactive visualization
vis = pyLDAvis.sklearn.prepare(lda, X_tfidf, tfidf)
pyLDAvis.display(vis)

# Or save to HTML
pyLDAvis.save_html(vis, 'lda_visualization.html')
```

### Slide 15: Word Clouds
```python
from wordcloud import WordCloud

# Combine all text
all_text = ' '.join(documents)

# Generate word cloud
wordcloud = WordCloud(
    width=800, height=400,
    background_color='white',
    max_words=100
).generate(all_text)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
```

### Slide 16: Philippine Example - Twitter Sentiment
```python
# Load Philippine Twitter data
tweets = pd.read_csv('ph_twitter_data.csv')

# Preprocess
tweets['clean_text'] = tweets['text'].apply(preprocess_text)

# Sentiment analysis
sia = SentimentIntensityAnalyzer()
tweets['sentiment'] = tweets['text'].apply(
    lambda x: sia.polarity_scores(x)['compound']
)

# Classify
tweets['sentiment_label'] = tweets['sentiment'].apply(
    lambda x: 'positive' if x > 0.05 else ('negative' if x < -0.05 else 'neutral')
)

# Visualize
tweets['sentiment_label'].value_counts().plot(kind='bar')
```

### Slide 17: Handling Filipino Text
```python
# Filipino stopwords
filipino_stopwords = ['ang', 'ng', 'sa', 'na', 'ay', 'mga', 'at', 'para', 'ko', 'mo']

# Combined stopwords
all_stopwords = set(stopwords.words('english') + filipino_stopwords)

# Preprocessing with Filipino
def preprocess_filipino(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in all_stopwords and t.isalpha()]
    return ' '.join(tokens)
```

### Slide 18: Named Entity Recognition
```python
import spacy

nlp = spacy.load('en_core_web_sm')

text = "SM Investments Corporation announced expansion plans in Cebu City."
doc = nlp(text)

for ent in doc.ents:
    print(f"{ent.text}: {ent.label_}")

# Output:
# SM Investments Corporation: ORG
# Cebu City: GPE
```

### Slide 19: In-Class Exercise
**Social Media Analysis**:
1. Load Philippine product reviews
2. Preprocess and create TF-IDF
3. Analyze sentiment distribution
4. Discover topics with LDA
5. Visualize findings

### Slide 20: Key Takeaways
1. Preprocessing is critical for text analysis
2. TF-IDF weights important terms
3. Sentiment analysis: lexicon or ML approaches
4. LDA discovers hidden topics
5. Consider Filipino language in Philippine context

### Slide 21: Next Lecture
**Lecture 22: Analytics at Scale & Ethics**
- Big data concepts
- Data privacy and GDPR
- Algorithmic bias
- Responsible AI

---

## Lecture 22: Analytics at Scale & Ethics

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 22: Analytics at Scale & Ethics
- Week 11, Session 2

### Slide 2: Learning Objectives
1. Understand big data concepts and tools
2. Apply data privacy principles (GDPR, DPA)
3. Identify and mitigate algorithmic bias
4. Practice responsible AI principles

### Slide 3: Big Data Characteristics (5 Vs)
| V | Description | Example |
|---|-------------|---------|
| **Volume** | Terabytes to petabytes | Facebook: 4PB/day |
| **Velocity** | Real-time streaming | Stock trades |
| **Variety** | Structured + unstructured | Text, images, sensors |
| **Veracity** | Data quality issues | Missing, inconsistent |
| **Value** | Extracting insights | Business decisions |

### Slide 4: When You Need Big Data Tools
**You DON'T need Spark/Hadoop if**:
- Data fits in memory (<16GB)
- Processing is one-time
- Simple aggregations

**You DO need them if**:
- Data exceeds single machine
- Distributed processing needed
- Real-time streaming

### Slide 5: Apache Spark Overview
**Distributed computing framework**:
- In-memory processing (100x faster than Hadoop)
- Supports Python (PySpark), SQL, R
- MLlib for machine learning at scale

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Analytics").getOrCreate()

# Read large dataset
df = spark.read.csv("large_data.csv", header=True, inferSchema=True)

# SQL-like operations
df.groupBy("region").agg({"sales": "sum"}).show()
```

### Slide 6: Cloud Analytics Platforms
| Platform | Service | Strength |
|----------|---------|----------|
| AWS | Redshift, Athena | Most comprehensive |
| GCP | BigQuery | Serverless SQL |
| Azure | Synapse | Enterprise integration |

```sql
-- BigQuery example
SELECT region, SUM(sales) as total_sales
FROM `project.dataset.table`
WHERE date >= '2024-01-01'
GROUP BY region
ORDER BY total_sales DESC
```

### Slide 7: Data Privacy Landscape
**Key regulations**:
- **GDPR** (EU): General Data Protection Regulation
- **CCPA** (California): Consumer Privacy Act
- **DPA** (Philippines): Data Privacy Act (RA 10173)

**Common principles**:
- Consent for data collection
- Right to access and delete
- Data minimization
- Security requirements

### Slide 8: Philippine Data Privacy Act
**Key provisions**:
1. **Consent**: Must be freely given, specific, informed
2. **Purpose limitation**: Use only for stated purpose
3. **Data minimization**: Collect only what's needed
4. **Accuracy**: Keep data up to date
5. **Storage limitation**: Delete when no longer needed
6. **Security**: Protect against unauthorized access

### Slide 9: Anonymization Techniques
| Technique | Description | Example |
|-----------|-------------|---------|
| Masking | Hide partial data | "Juan D." |
| Generalization | Broaden categories | Age 25 → "20-30" |
| Suppression | Remove identifiers | Remove SSN |
| Noise addition | Add random values | Salary ± 5% |
| K-anonymity | Ensure k similar records | 5+ with same quasi-identifiers |

```python
# Simple anonymization
df['name'] = df['name'].str[0] + '***'
df['age_group'] = pd.cut(df['age'], bins=[0,20,30,40,50,100],
                          labels=['<20','20-30','30-40','40-50','50+'])
```

### Slide 10: Algorithmic Bias
**Definition**: Systematic errors that create unfair outcomes

**Sources**:
- **Historical bias**: Data reflects past discrimination
- **Representation bias**: Undersampled groups
- **Measurement bias**: Features proxy for protected attributes
- **Aggregation bias**: One model for diverse groups

### Slide 11: Bias Case Studies
**COMPAS** (Criminal justice):
- Predicted recidivism
- Higher false positive for Black defendants
- Used in sentencing decisions

**Amazon Hiring** (HR):
- Trained on historical hires
- Penalized female applicants
- Scraped program

### Slide 12: Detecting Bias
```python
from sklearn.metrics import confusion_matrix

# Check metrics by group
for group in df['demographic'].unique():
    subset = df[df['demographic'] == group]
    cm = confusion_matrix(subset['actual'], subset['predicted'])

    # Calculate false positive rate
    fpr = cm[0, 1] / (cm[0, 0] + cm[0, 1])
    print(f"{group}: FPR = {fpr:.3f}")

# Compare rates across groups
# Significant differences indicate bias
```

### Slide 13: Fairness Metrics
| Metric | Definition | When to Use |
|--------|------------|-------------|
| Demographic parity | Equal positive rates | Loans, hiring |
| Equalized odds | Equal TPR and FPR | Criminal justice |
| Calibration | Equal precision | Medical diagnosis |

**Trade-offs**: Cannot satisfy all metrics simultaneously

### Slide 14: Mitigating Bias
**Pre-processing**:
- Rebalance training data
- Remove proxy features

**In-processing**:
- Add fairness constraints
- Use fair algorithms

**Post-processing**:
- Adjust thresholds by group
- Audit and correct predictions

### Slide 15: Explainability Requirements
**Why explainability matters**:
- GDPR "right to explanation"
- Build trust with users
- Debug model errors
- Regulatory compliance

**Tools**: SHAP, LIME, Counterfactual explanations

### Slide 16: Responsible AI Framework
1. **Fairness**: Equal treatment across groups
2. **Accountability**: Clear ownership
3. **Transparency**: Explainable decisions
4. **Ethics**: Consider societal impact
5. **Safety**: Prevent harm
6. **Privacy**: Protect personal data

### Slide 17: AI Ethics Checklist
Before deploying a model:
- [ ] Have we assessed potential bias?
- [ ] Is the model explainable to stakeholders?
- [ ] Have we considered unintended consequences?
- [ ] Is user consent properly obtained?
- [ ] Do we have monitoring in place?
- [ ] Is there a human override mechanism?
- [ ] Have we documented limitations?

### Slide 18: Philippine Context
**Ethics challenges in PH**:
- Credit scoring for informal economy
- Facial recognition in public spaces
- Social media monitoring
- Healthcare AI in resource-limited settings

**Opportunity**: Build AI that works for Filipinos, not just Western populations

### Slide 19: In-Class Discussion
**Case Study Analysis**:
1. GCash credit scoring for unbanked Filipinos
2. DOH disease prediction in rural areas
3. COMELEC voter fraud detection

**Questions**:
- What biases might exist?
- Who could be harmed?
- How to ensure fairness?

### Slide 20: Key Takeaways
1. Big data needs specialized tools when scale demands
2. Philippine DPA governs data privacy obligations
3. Algorithmic bias can cause real harm
4. Fairness metrics help quantify bias
5. Responsible AI requires continuous attention

### Slide 21: Lab Preview
**Lab 10: Bias Audit Project**
- Audit a model for bias
- Calculate fairness metrics
- Propose mitigations
- Document findings

---

# WEEK 12: Capstone & Professional Practice

---

## Lecture 23: Capstone Project Presentations I

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 23: Capstone Project Presentations
- Week 12, Session 1

### Slide 2: Presentation Guidelines
**Format**:
- 15 minutes presentation
- 5 minutes Q&A
- All team members participate

**Evaluation**:
- Problem definition (15%)
- Methodology (25%)
- Analysis quality (30%)
- Visualization (15%)
- Communication (15%)

### Slide 3: Presentation Structure
1. **Introduction** (2 min)
   - Problem statement
   - Why it matters

2. **Data & Methodology** (4 min)
   - Data sources
   - Preprocessing steps
   - Methods used

3. **Results** (5 min)
   - Key findings
   - Visualizations
   - Model performance

4. **Insights & Recommendations** (3 min)
   - Actionable insights
   - Limitations
   - Future work

5. **Q&A** (5 min)

### Slide 4: Evaluation Rubric

| Criterion | Excellent (4) | Good (3) | Satisfactory (2) | Needs Work (1) |
|-----------|---------------|----------|------------------|----------------|
| Problem | Clear, relevant, well-scoped | Clear but could be better scoped | Somewhat unclear | Poorly defined |
| Methods | Appropriate, well-executed | Appropriate with minor issues | Some issues | Inappropriate |
| Analysis | Deep insights, rigorous | Good insights | Surface-level | Missing insights |
| Visuals | Professional, clear | Good but minor issues | Basic | Poor/missing |
| Communication | Engaging, clear | Clear but could engage more | Some confusion | Hard to follow |

### Slides 5-20: Student Presentation Slots
[Reserved for 4-5 team presentations]

### Slide 21: Peer Feedback Form
- What was the strongest aspect?
- What could be improved?
- One question you still have
- Rating: 1-5 stars

### Slide 22: Next Session Preview
**Lecture 24: Remaining Presentations & Course Wrap-up**
- Final presentations
- Course summary
- Career guidance
- Q&A

---

## Lecture 24: Capstone Presentations II & Course Wrap-up

### Slide 1: Title
- **CMSC 178DA: Data Analytics**
- Lecture 24: Course Wrap-up & Future Directions
- Week 12, Session 2

### Slides 2-12: Remaining Presentations
[Reserved for remaining team presentations]

### Slide 13: Course Summary
**What We Covered**:

| Week | Topics |
|------|--------|
| 1-2 | Foundations, Probability, Statistics |
| 3-4 | Data Wrangling, EDA |
| 5-6 | Visualization, Storytelling, Dashboards |
| 7-8 | Regression, Classification, Ensembles |
| 9-10 | Clustering, Time Series |
| 11-12 | Text Analytics, Ethics, Capstone |

### Slide 14: Key Skills Acquired
**Technical**:
- Python for data analytics
- SQL for data extraction
- Statistical inference
- Machine learning fundamentals
- Data visualization

**Soft**:
- Data storytelling
- Business communication
- Problem framing
- Ethical reasoning

### Slide 15: Analytics Career Paths
```
Data Analyst → Senior Analyst → Lead Analyst → Analytics Manager
     ↓
Data Scientist → Senior DS → Principal DS → Chief Data Officer
     ↓
ML Engineer → Senior MLE → Staff MLE → VP of Engineering
     ↓
Analytics Consultant → Manager → Partner
```

### Slide 16: Philippine Job Market
**Growing sectors**:
- Fintech (GCash, Maya, banks)
- E-commerce (Lazada, Shopee)
- BPO (analytics services)
- Startups (various)

**Salary ranges** (entry-level):
- Data Analyst: ₱30,000-60,000/month
- Data Scientist: ₱50,000-100,000/month

### Slide 17: Building Your Portfolio
**Essential components**:
1. GitHub with clean code and documentation
2. 3-5 completed projects with write-ups
3. LinkedIn with skills and endorsements
4. Kaggle profile with competitions/notebooks
5. Personal website/blog (optional but helpful)

**Capstone project** is a great portfolio piece!

### Slide 18: Continuous Learning
**Free resources**:
- Kaggle Learn
- Google Data Analytics Certificate
- Harvard CS109 (online materials)

**Advanced topics to explore**:
- Deep learning (fast.ai, Coursera)
- MLOps and deployment
- Cloud certifications (AWS, GCP)
- Domain specialization (healthcare, finance)

### Slide 19: Emerging Trends
**What's next in analytics**:
- **GenAI for analytics**: Copilots, code generation
- **AutoML**: Automated model building
- **Real-time analytics**: Streaming data
- **Edge analytics**: IoT and mobile
- **Responsible AI**: Fairness, privacy by design

### Slide 20: Final Words
**To succeed in analytics**:
1. Stay curious - always ask "why?"
2. Practice constantly - do projects
3. Communicate clearly - insights must be shared
4. Think ethically - data affects real people
5. Never stop learning - field evolves rapidly

**Quote**: "The goal is to turn data into information, and information into insight." - Carly Fiorina

### Slide 21: Course Evaluation
Please complete the course evaluation:
- What worked well?
- What could be improved?
- Suggestions for future offerings

### Slide 22: Thank You!
**CMSC 178DA: Data Analytics**

University of the Philippines Cebu
Semester [X], AY 2025-2026

**Keep in touch**:
- Email: [instructor email]
- LinkedIn: [profile]

*Best wishes on your analytics journey!*

---

## Document Information

**Course**: CMSC 178DA - Data Analytics
**Institution**: University of the Philippines Cebu
**Total Lectures**: 24 (12 weeks × 2 sessions)
**Created**: January 2026
**Sources**: MIT 15.071, Harvard CS109, Stanford CS109, UC Berkeley Data 100
