# Retail Sales Analysis

## Project Overview

This project analyzes retail sales data using Python to evaluate business performance, identify profitable products and categories, investigate pricing issues, and generate actionable business recommendations.

The analysis covers sales transactions across 2025 and produces reports and visualizations to support data-driven decision-making.

## Business Objectives

The project aims to:

- Evaluate monthly revenue, costs, profit and profit margins.
- Identify the most and least profitable product categories.
- Compare product performance using revenue, quantity sold and profit.
- Investigate products with unusually low profit margins.
- Develop recommendations based on the findings.

## Tools and Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- OpenPyXL
- PyCharm
- Git and GitHub

## Dataset Overview

The analysis covers:

- 3,000 unique orders.
- 8,961 units sold.
- 20 products.
- Multiple product categories and customer locations.

## Analysis and Methodology

### 1. Monthly Performance Analysis

Evaluated monthly revenue, profit and profit margins, including changes in performance between consecutive months.

### 2. Category Performance Analysis

Compared product categories using revenue contribution, profit contribution and profit margins.

### 3. Product Performance Analysis

Identified top-performing and low-performing products based on revenue, quantity sold, profit and profit margins.

### 4. Pricing Investigation

Investigated products with extremely low unit profit margins and evaluated their contribution to overall business revenue and profit.

### 5. Executive Reporting

Created an Excel workbook containing an executive summary, key business findings and recommendations.

## Key Business Findings

- **Overall revenue:** ₦2,003,295,236.
- **Overall cost:** ₦1,202,324,889.
- **Overall profit:** ₦800,970,347.
- **Overall gross profit margin:** 39.98%.
- **Best monthly profit margin:** November 2025 at 43.16%.
- **Highest-revenue month:** December 2025.
- **Most profitable category:** Computers, contributing 45.23% of total profit.
- **Highest-margin product:** Projector, with an 87.51% profit margin.

### Pricing Investigation

Six products generated 25.71% of total revenue but contributed only approximately 0.000322% of total profit.

This finding highlights a potential pricing or cost-data issue requiring further investigation.

## Business Recommendations

1. Investigate the factors behind November's high profit margin and December's higher revenue.
2. Maintain adequate stock of profitable computer products while monitoring their margins.
3. Monitor projector sales and profitability to sustain its strong performance.
4. Investigate the cost and selling-price records of the six extremely low-margin products before making pricing decisions.

## Project Structure

```text
retail-sales-analysis/
│
├── data/
│   ├── customers.csv
│   ├── orders.csv
│   └── products.csv
│
├── outputs/
│   ├── category_performance_report.csv
│   ├── monthly_performance_report.csv
│   ├── product_performance_report.csv
│   └── retail_business_report.xlsx
│
├── charts/
│   ├── monthly_profits.png
│   ├── monthly_revenue.png
│   └── top_five_products_profit.png
│
├── main.py
├── .gitignore
└── README.md

## How to Run the Project

1. Clone or download this repository.
2. Install Python and the required libraries.
3. Install the dependencies:

```bash
pip install pandas numpy matplotlib openpyxl
```

4. Open the project in PyCharm or another Python IDE.
5. Run `main.py`.

## Project Outputs

The project generates:

- Monthly performance CSV report.
- Category performance CSV report.
- Product performance CSV report.
- Monthly revenue chart.
- Monthly profit chart.
- Top five products by profit chart.
- Consolidated Excel business report.

## Conclusion

This project demonstrates the application of Python and data analysis techniques to transform raw retail sales data into meaningful business insights.

It showcases data aggregation, financial performance analysis, product and category comparisons, visualization, Excel reporting and evidence-based business recommendations.

---

**Dataset source and license:

The retail sales dataset used in this project was generated with assistance from OpenAI's ChatGPT for educational and portfolio development purposes.

The dataset contains synthetic retail transaction, customer, and product records. It does not represent actual transactions from a real business.