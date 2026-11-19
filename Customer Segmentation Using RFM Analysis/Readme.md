# Customer Segmentation Using RFM Analysis

**Tech Stack:** Python | Pandas

## Overview

This project analyses customer purchasing behaviour using the Online Retail dataset and Recency, Frequency and Monetary (RFM) analysis.

The workflow includes data exploration, cleaning, customer-level aggregation, RFM scoring and rule-based customer segmentation.


## Business Questions

1. **Customer Activity:** How does purchase recency determine customer segment classification?

2. **Purchase Frequency:** How does the number of distinct purchase invoices contribute to customer segmentation?

3. **Customer Spending:** How does total customer spending vary across customers, and how is it reflected in monetary scores?

4. **Customer Segmentation:** How can recency and purchase frequency be combined to identify highly active and potentially at-risk customers?


## Data Exploration & Cleaning

- Examined missing values, duplicates, data types and descriptive statistics.
- Removed records with missing customer IDs.
- Removed duplicate rows and cancelled invoices.
- Excluded transactions with non-positive quantities or unit prices.

## RFM Analysis

Calculated customer-level metrics:

- **Recency:** Days since the customer's last purchase.
- **Frequency:** Number of distinct invoices per customer.
- **Monetary:** Total customer spending (Quantity × UnitPrice).

Assigned RFM scores using predefined thresholds.

## Customer Segmentation

Classified customers into four groups using recency and frequency scores:

- **Champions:** Recent and frequent purchasers.
- **At Risk:** Previously frequent purchasers with low recency scores.
- **Loyal Customers:** Relatively frequent purchasers who do not meet the earlier segment conditions.
- **Other Customers:** Customers who do not meet the above criteria.

Monetary scores are calculated but are not used in the current segmentation rules.

## Technical Implementation

Organised the analysis into a Python class with methods for:

- Data exploration and quality checks.
- Data cleaning and filtering.
- Customer-level RFM calculations.
- RFM scoring and rule-based segmentation.

## How to Run

### 1. Install Dependencies

```bash
pip install pandas openpyxl matplotlib seaborn
```

### 2. Download Dataset

Download the Online Retail dataset and save it as:

`../data/Online Retail.xlsx`

The path is relative to the working directory.

### 3. Run the Script

Execute the Python script to display data quality checks, RFM metrics, scores and customer segments.