# Philippine Datasets for CMSC 178DA
## Curated Data Sources for Data Analytics Course

---

## 1. Government Official Sources

### Philippine Statistics Authority (PSA)
**URL**: https://openstat.psa.gov.ph/

| Dataset | Description | Format | Use Case |
|---------|-------------|--------|----------|
| Population Census | Regional/provincial population, demographics | CSV, API | EDA, clustering |
| Labor Force Survey | Employment, unemployment, underemployment | CSV | Regression, trends |
| Consumer Price Index | Inflation rates by region and commodity | CSV | Time series |
| GDP by Region | Gross Regional Domestic Product | CSV | Regression, comparison |
| Poverty Statistics | Poverty incidence by region | CSV | Classification, clustering |
| Vital Statistics | Births, deaths, marriages | CSV | EDA, visualization |

**Access**: Free, some require registration
**Update Frequency**: Quarterly to annually

```python
# Example: Loading PSA population data
import pandas as pd

# Direct download from OpenSTAT
pop_url = "https://openstat.psa.gov.ph/dataset/regional-population"
# Or use local cached copy
pop_df = pd.read_csv('data/psa_population_2020.csv')
```

---

### Bangko Sentral ng Pilipinas (BSP)
**URL**: https://www.bsp.gov.ph/statistics

| Dataset | Description | Format | Use Case |
|---------|-------------|--------|----------|
| Exchange Rates | Daily PHP vs major currencies | Excel, CSV | Time series, forecasting |
| Interest Rates | Policy rates, lending rates | Excel | Regression |
| Banking Statistics | Deposits, loans by bank type | Excel | EDA, clustering |
| Balance of Payments | Imports, exports, remittances | Excel | Time series |
| OFW Remittances | Monthly remittance inflows | Excel | Forecasting |
| Inflation Report | Monthly CPI components | PDF, Excel | Time series |

**Access**: Free download
**Update Frequency**: Daily to quarterly

```python
# Example: Loading BSP exchange rate data
exchange_df = pd.read_excel('bsp_exchange_rates_2024.xlsx', sheet_name='Daily')
exchange_df['date'] = pd.to_datetime(exchange_df['date'])
exchange_df.set_index('date', inplace=True)
```

---

### PAGASA (Weather Bureau)
**URL**: https://bagong.pagasa.dost.gov.ph/climate/climate-data

| Dataset | Description | Format | Use Case |
|---------|-------------|--------|----------|
| Daily Weather | Temperature, rainfall, humidity | CSV | Time series, regression |
| Tropical Cyclones | Typhoon tracks, intensity | GeoJSON, CSV | Visualization, prediction |
| Climate Normals | 30-year averages by station | CSV | Baseline comparison |
| Extreme Events | Record temperatures, rainfall | CSV | Outlier analysis |
| Seasonal Forecasts | El Niño/La Niña predictions | PDF | Feature engineering |

**Access**: Some free, historical data may require request
**Update Frequency**: Daily to seasonal

```python
# Example: Loading PAGASA weather data
weather_df = pd.read_csv('pagasa_manila_2024.csv')
weather_df['date'] = pd.to_datetime(weather_df['date'])

# Feature engineering
weather_df['month'] = weather_df['date'].dt.month
weather_df['is_wet_season'] = weather_df['month'].isin([6,7,8,9,10,11]).astype(int)
```

---

### Department of Health (DOH)
**URL**: https://doh.gov.ph/statistics

| Dataset | Description | Format | Use Case |
|---------|-------------|--------|----------|
| COVID-19 Data Drop | Daily cases, deaths, recoveries | CSV, Google Sheets | Time series, EDA |
| Disease Surveillance | Dengue, measles, TB cases | Excel | Forecasting, mapping |
| Hospital Statistics | Bed capacity, utilization | Excel | Capacity planning |
| Health Facilities | Hospitals, clinics locations | CSV | Geospatial analysis |
| Vaccination Data | Coverage by region, age group | CSV | Classification |

**Access**: Free, COVID data widely available
**Update Frequency**: Daily to monthly

```python
# Example: COVID-19 analysis
covid_df = pd.read_csv('doh_covid_data.csv')
covid_df['date_reported'] = pd.to_datetime(covid_df['date_reported'])

# Weekly aggregation
weekly = covid_df.groupby(pd.Grouper(key='date_reported', freq='W'))['cases'].sum()
```

---

### Commission on Elections (COMELEC)
**URL**: https://comelec.gov.ph/

| Dataset | Description | Format | Use Case |
|---------|-------------|--------|----------|
| Election Results | Presidential, local votes | CSV, Excel | EDA, clustering |
| Voter Registration | Registered voters by region | Excel | Demographic analysis |
| Political Parties | Party list votes | CSV | Classification |

**Access**: Free, historical data on website
**Update Frequency**: Election cycles

---

### Department of Tourism (DOT)
**URL**: https://dot.gov.ph/statistics

| Dataset | Description | Format | Use Case |
|---------|-------------|--------|----------|
| Tourist Arrivals | Monthly arrivals by country | Excel | Time series, forecasting |
| Accommodation Stats | Hotel occupancy rates | Excel | Regression |
| Tourism Revenue | Receipts by region | Excel | EDA |
| Destination Rankings | Visitor counts by site | Excel | Comparison |

**Access**: Free download
**Update Frequency**: Monthly to annually

---

## 2. Financial & Economic Data

### Philippine Stock Exchange (PSE)
**URL**: https://edge.pse.com.ph/

| Dataset | Description | Format | Use Case |
|---------|-------------|--------|----------|
| Stock Prices | Daily OHLCV for all stocks | CSV, API | Time series, prediction |
| PSEi Components | Index composition | CSV | Portfolio analysis |
| Company Disclosures | Financial reports | PDF | Text analytics |
| IPO Data | New listings | CSV | Event analysis |

**Access**: Basic free, detailed requires subscription
**Update Frequency**: Daily

```python
# Example: Using yfinance for PSE data
import yfinance as yf

# Philippine stocks have .PS suffix
sm = yf.download('SM.PS', start='2020-01-01', end='2024-12-31')
jfc = yf.download('JFC.PS', start='2020-01-01', end='2024-12-31')

# Combine
stocks = pd.DataFrame({
    'SM': sm['Close'],
    'JFC': jfc['Close']
})
```

---

### Securities and Exchange Commission (SEC)
**URL**: https://www.sec.gov.ph/

| Dataset | Description | Format | Use Case |
|---------|-------------|--------|----------|
| Company Registry | Registered corporations | CSV | EDA, classification |
| Financial Statements | Quarterly reports | PDF, Excel | Financial analysis |
| Corporate Actions | Dividends, stock splits | CSV | Event study |

---

## 3. Transportation & Mobility

### Land Transportation Office (LTO)
**URL**: https://lto.gov.ph/

| Dataset | Description | Format | Use Case |
|---------|-------------|--------|----------|
| Vehicle Registration | New registrations by type | Excel | Time series, regression |
| Driver's License | Licensed drivers by region | Excel | Demographic analysis |
| Road Accidents | Accident statistics | Excel | Classification, prediction |

---

### Department of Transportation (DOTr)
**URL**: https://dotr.gov.ph/

| Dataset | Description | Format | Use Case |
|---------|-------------|--------|----------|
| Airport Statistics | Passenger counts | Excel | Time series |
| Port Statistics | Cargo volumes | Excel | Forecasting |
| Rail Ridership | MRT/LRT passengers | Excel | Demand analysis |

---

## 4. Open Data Portals

### Data.gov.ph
**URL**: https://data.gov.ph/

**Categories**:
- Agriculture and Fisheries
- Budget and Finance
- Education
- Environment
- Health
- Infrastructure
- Trade and Industry

**Format**: Various (CSV, JSON, Excel)
**Access**: Free, open data policy

---

### Humanitarian Data Exchange (Philippines)
**URL**: https://data.humdata.org/group/phl

| Dataset | Description | Format | Use Case |
|---------|-------------|--------|----------|
| Admin Boundaries | Province/city/barangay shapes | GeoJSON, SHP | Mapping |
| Population Estimates | Gridded population | GeoTIFF | Spatial analysis |
| Poverty Maps | Poverty by admin level | CSV | Choropleth maps |
| Disaster Data | Typhoon impacts | CSV | Risk analysis |

---

## 5. Recommended Datasets by Week

### Week 1-2: Foundations & Statistics
| Dataset | Source | Purpose |
|---------|--------|---------|
| Regional GDP | PSA | Introduction to Philippine economy |
| Population by Age/Sex | PSA | Probability distributions |
| COVID-19 Daily Cases | DOH | A/B testing, hypothesis examples |

### Week 3-4: Data Wrangling & EDA
| Dataset | Source | Purpose |
|---------|--------|---------|
| Labor Force Survey | PSA | Data cleaning practice (messy) |
| Exchange Rates | BSP | Time series wrangling |
| Weather Data | PAGASA | Missing value handling |

### Week 5-6: Visualization & Storytelling
| Dataset | Source | Purpose |
|---------|--------|---------|
| Tourism Arrivals | DOT | Time series visualization |
| Regional GDP Map | PSA + Admin Boundaries | Choropleth creation |
| Election Results | COMELEC | Dashboard design |

### Week 7-8: Regression & Classification
| Dataset | Source | Purpose |
|---------|--------|---------|
| Housing Prices | Property websites (scraped) | Linear regression |
| Bank Default Data | Simulated based on BSP patterns | Logistic regression |
| Customer Churn | Simulated telecom data | Classification metrics |

### Week 9-10: Clustering & Time Series
| Dataset | Source | Purpose |
|---------|--------|---------|
| Consumer Spending | PSA FIES | Customer segmentation |
| Remittances | BSP | Time series forecasting |
| Stock Prices | PSE | ARIMA modeling |

### Week 11: Text Analytics
| Dataset | Source | Purpose |
|---------|--------|---------|
| News Headlines | News websites | Sentiment analysis |
| Twitter/X PH | Twitter API | Topic modeling |
| Product Reviews | E-commerce sites | NLP basics |

---

## 6. Data Collection Guide

### API Access Examples

```python
# PSA OpenSTAT API (if available)
import requests

url = "https://openstat.psa.gov.ph/api/v1/data"
params = {
    'dataset': 'population',
    'region': 'NCR',
    'year': 2020
}
response = requests.get(url, params=params)
data = response.json()

# For most Philippine sources, manual download is required
# Store in: static/data/courses/cmsc178da/datasets/
```

### Web Scraping Guidelines

```python
# Property prices from Lamudi/PropertyGuru
from bs4 import BeautifulSoup
import requests
import time

# ALWAYS check robots.txt first
# Add delays between requests
# Respect rate limits

def scrape_property_prices(url):
    time.sleep(2)  # Be respectful
    response = requests.get(url, headers={'User-Agent': 'Educational Research'})
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract data...
    return data

# Better: Use provided datasets or official APIs
```

---

## 7. Sample Dataset Files

### Directory Structure
```
static/data/courses/cmsc178da/datasets/
├── economic/
│   ├── psa_regional_gdp_2015_2023.csv
│   ├── bsp_exchange_rates_2020_2024.csv
│   └── bsp_remittances_monthly.csv
├── demographics/
│   ├── psa_population_2020.csv
│   ├── psa_labor_force_2023.csv
│   └── psa_poverty_incidence.csv
├── health/
│   ├── doh_covid_cases.csv
│   ├── doh_vaccination_coverage.csv
│   └── doh_hospital_statistics.csv
├── tourism/
│   ├── dot_arrivals_2015_2023.csv
│   └── dot_receipts_by_region.csv
├── financial/
│   ├── pse_daily_prices_2024.csv
│   └── psei_components.csv
├── weather/
│   ├── pagasa_manila_daily_2020_2024.csv
│   └── pagasa_typhoons_2010_2024.csv
├── geospatial/
│   ├── ph_regions.geojson
│   ├── ph_provinces.geojson
│   └── ph_cities.geojson
└── simulated/
    ├── ph_ecommerce_transactions.csv
    ├── ph_telecom_churn.csv
    └── ph_credit_scoring.csv
```

---

## 8. Dataset Preparation Checklist

Before using a dataset in class:

- [ ] Downloaded and stored locally (don't rely on live URLs)
- [ ] Verified data quality (no critical issues)
- [ ] Created data dictionary (column descriptions)
- [ ] Tested loading in Python
- [ ] Prepared backup/alternative if needed
- [ ] Credited source appropriately
- [ ] Checked for PII/sensitive data (anonymize if needed)
- [ ] Validated Philippine context relevance

---

## 9. Creating Simulated Datasets

When real data unavailable:

```python
import numpy as np
import pandas as pd
from faker import Faker

fake = Faker('en_PH')  # Philippine locale

def generate_ph_ecommerce_data(n=10000):
    """Generate realistic Philippine e-commerce data."""
    np.random.seed(42)

    regions = ['NCR', 'Region III', 'Region IV-A', 'Region VII', 'Region XI']
    categories = ['Electronics', 'Fashion', 'Home', 'Beauty', 'Food']
    payment_methods = ['GCash', 'Maya', 'COD', 'Credit Card', 'Bank Transfer']

    data = {
        'order_id': range(1, n+1),
        'customer_id': np.random.randint(1, n//5, n),
        'order_date': pd.date_range('2023-01-01', periods=n, freq='H'),
        'region': np.random.choice(regions, n, p=[0.35, 0.20, 0.20, 0.15, 0.10]),
        'category': np.random.choice(categories, n),
        'amount': np.random.lognormal(mean=6, sigma=1.2, size=n).round(2),
        'payment_method': np.random.choice(payment_methods, n, p=[0.40, 0.25, 0.20, 0.10, 0.05]),
        'is_returned': np.random.binomial(1, 0.05, n)
    }

    return pd.DataFrame(data)

# Generate and save
ecommerce_df = generate_ph_ecommerce_data()
ecommerce_df.to_csv('ph_ecommerce_transactions.csv', index=False)
```

---

## 10. Data Source Citation Format

```markdown
**Source**: Philippine Statistics Authority (PSA)
**Dataset**: Regional Gross Domestic Product
**URL**: https://openstat.psa.gov.ph/
**Accessed**: January 2026
**License**: Open Data Philippines
```

---

## Quick Reference: Top 10 Datasets for Course

| # | Dataset | Source | Primary Use |
|---|---------|--------|-------------|
| 1 | Regional GDP | PSA | EDA, regression |
| 2 | COVID-19 Cases | DOH | Time series |
| 3 | Exchange Rates | BSP | Forecasting |
| 4 | Tourist Arrivals | DOT | Visualization |
| 5 | Weather Data | PAGASA | Data cleaning |
| 6 | Stock Prices | PSE | Time series |
| 7 | Population Census | PSA | Clustering |
| 8 | OFW Remittances | BSP | Forecasting |
| 9 | Election Results | COMELEC | Classification |
| 10 | Admin Boundaries | HDX | Mapping |

---

**Document Information**
- Course: CMSC 178DA - Data Analytics
- Institution: University of the Philippines Cebu
- Created: January 2026
- Last Updated: January 2026
