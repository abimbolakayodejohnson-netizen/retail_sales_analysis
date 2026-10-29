
from pathlib import Path

import numpy as np
import pandas as pd

# Create the data folder if it does not exist
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

rng = np.random.default_rng(42)

# 1. Products dataset
products = pd.DataFrame({
    "product_id": [f"P{i:03d}" for i in range(1, 21)],
    "product_name": [
        "Laptop", "Mouse", "Keyboard", "Monitor", "Headphones",
        "USB Cable", "Printer", "Webcam", "Speaker", "Flash Drive",
        "Tablet", "Phone", "Power Bank", "Router", "Hard Drive",
        "SSD", "Microphone", "Projector", "Charger", "Smart Watch"
    ],
    "category": [
        "Computers", "Accessories", "Accessories", "Computers",
        "Audio", "Accessories", "Computers", "Accessories",
        "Audio", "Accessories", "Computers", "Phones", "Accessories",
        "Networking", "Storage", "Storage", "Audio", "Computers",
        "Accessories", "Wearables"
    ],
    "unit_cost": rng.integers(5_000, 250_000, size=20),
    "unit_price": rng.integers(10_000, 350_000, size=20)
})

# Ensure selling prices exceed costs
products["unit_price"] = (
    products["unit_price"].clip(lower=products["unit_cost"] + 1)
)

# 2. Customers dataset
cities = ["Lagos", "Abuja", "Ibadan", "Port Harcourt", "Kano"]

customers = pd.DataFrame({
    "customer_id": [f"C{i:04d}" for i in range(1, 301)],
    "customer_name": [
        f"Customer {i:03d}" for i in range(1, 301)
    ],
    "city": rng.choice(cities, size=300),
})

region_map = {
    "Lagos": "South West",
    "Ibadan": "South West",
    "Abuja": "North Central",
    "Kano": "North West",
    "Port Harcourt": "South South"
}

customers["region"] = customers["city"].map(region_map)

# 3. Orders dataset
n_orders = 3000

orders = pd.DataFrame({
    "order_id": [f"O{i:05d}" for i in range(1, n_orders + 1)],
    "order_date": pd.to_datetime(
        rng.choice(
            pd.date_range("2025-01-01", "2025-12-31"),
            size=n_orders
        )
    ),
    "customer_id": rng.choice(customers["customer_id"], size=n_orders),
    "product_id": rng.choice(products["product_id"], size=n_orders),
    "quantity": rng.integers(1, 6, size=n_orders),
})

# Add intentional data-quality problems
orders.loc[10, "quantity"] = -2
orders.loc[25, "customer_id"] = None
orders.loc[40, "product_id"] = "P999"
orders.loc[55, "order_date"] = pd.NaT

# Save the datasets
products.to_csv(DATA_DIR / "products.csv", index=False)
customers.to_csv(DATA_DIR / "customers.csv", index=False)
orders.to_csv(DATA_DIR / "orders.csv", index=False)

print("Retail datasets created successfully.")
print(f"Orders: {len(orders):,}")
print(f"Products: {len(products):,}")
print(f"Customers: {len(customers):,}")
print(f"Files saved in: {DATA_DIR.resolve()}")


# Load the saved datasets
orders_df = pd.read_csv("data/orders.csv")
products_df = pd.read_csv("data/products.csv")
customers_df = pd.read_csv("data/customers.csv")

# Display the structure of each dataset
print("ORDERS")
print(orders_df.shape)
print(orders_df.dtypes)

print("\nPRODUCTS")
print(products_df.shape)
print(products_df.dtypes)

print("\nCUSTOMERS")
print(customers_df.shape)
print(customers_df.dtypes)


# Merge orders with product information
sales_df = orders_df.merge(
    products_df,
    on="product_id",
    how="left",
    indicator=True
)

print(sales_df.head())
print("\nMerge status:")
print(sales_df["_merge"].value_counts())
print("\nMerged shape:", sales_df.shape)
unmatched_products = sales_df[
    sales_df["_merge"] == "left_only"
]

print(unmatched_products)
# renaming merging column
sales_df = sales_df.rename(columns={"_merge": "product_match"})
# merging customer with sales_df
sales_df = sales_df.merge(customers_df, on='customer_id', how='left', indicator="customer_match")
print(sales_df.head())

print("PRODUCT MATCHING")
print(sales_df["product_match"].value_counts())

print("\nCUSTOMER MATCHING")
print(sales_df["customer_match"].value_counts())

print("\nDATASET SHAPE")
print(sales_df.shape)


# Convert order_date from string to datetime
sales_df["order_date"] = pd.to_datetime(
    sales_df["order_date"],
    errors="coerce"
)

# Check missing dates and invalid quantities
print("Missing order dates:")
print(sales_df["order_date"].isna().sum())

print("\nInvalid quantities:")
print(sales_df[sales_df["quantity"] <= 0][
    ["order_id", "quantity"]
])

print("\nMissing customer IDs:")
print(sales_df["customer_id"].isna().sum())

print("\nUnmatched product IDs:")
print(
    sales_df.loc[
        sales_df["product_match"] == "left_only",
        ["order_id", "product_id"]
    ]
)


# Calculate sales metrics
sales_df["revenue"] = (
    sales_df["quantity"] * sales_df["unit_price"]
)

sales_df["total_cost"] = (
    sales_df["quantity"] * sales_df["unit_cost"]
)

sales_df["profit"] = (
    sales_df["revenue"] - sales_df["total_cost"]
)

# Display sample results
print(
    sales_df[
        [
            "order_id",
            "quantity",
            "unit_price",
            "unit_cost",
            "revenue",
            "total_cost",
            "profit",
        ]
    ].head(10)
)

print("\nOverall metrics:")
print(
    sales_df[["revenue", "total_cost", "profit"]].sum()
)
print(sales_df.columns)
columns = ['order_id', 'order_date', 'customer_id', 'product_id', 'quantity',
       'product_name', 'category', 'unit_cost', 'unit_price', 'product_match',
       'customer_name', 'city', 'region', 'customer_match', 'revenue',
       'total_cost', 'profit']
# sales metric
category_sales = sales_df.groupby('category').agg(total_revenue=('revenue', 'sum'),
                                                  total_cost=('total_cost', 'sum'),
                                                  total_profit=('profit', 'sum'),
                                                  total_quantity=('quantity', 'sum'),
                                                  number_of_orders=('order_id', 'count')).sort_values('total_profit', ascending=False)
print('Category Sales')
print(category_sales.to_string())
# calculating profit margin
category_sales['profit_margin_pct'] = category_sales['total_profit'] / category_sales['total_revenue'] * 100
# revenue share per item category
category_sales['revenue_share_pct'] = category_sales['total_revenue'] / category_sales['total_revenue'].sum() * 100
category_sales[['profit_margin_pct', 'revenue_share_pct']] = category_sales[['profit_margin_pct', 'revenue_share_pct']].round(2)
print(category_sales[['profit_margin_pct', 'revenue_share_pct']].sort_values('profit_margin_pct', ascending=False))
#extracting month from order column
sales_df['month'] = sales_df['order_date'].dt.to_period('M')
# monthly sales
monthly_sales = sales_df.groupby('month').agg(total_revenue=('revenue', 'sum'),
                                    total_cost=('total_cost', 'sum'),
                                    total_profit=('profit', 'sum'),
                                    total_quantity=('quantity', 'sum'),
                                    total_order=('order_id', 'count')).sort_index()


print("Highest revenue months:")
print(
    monthly_sales.nlargest(3, "total_revenue")
)

print("\nLowest revenue months:")
print(
    monthly_sales.nsmallest(3, "total_revenue")
)

print("\nHighest profit month:")
print(
    monthly_sales.loc[
        monthly_sales["total_profit"].idxmax()
    ]
)

print("\nLowest profit month:")
print(
    monthly_sales.loc[
        monthly_sales["total_profit"].idxmin()
    ]
)

# Visualizing the data

import matplotlib.pyplot as plt

# Create a monthly revenue line chart
plt.figure(figsize=(10, 5))

plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales["total_revenue"],
    marker="o"
)

plt.title("Monthly Revenue — 2025")
plt.xlabel("Month")
plt.ylabel("Revenue (₦)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save the chart in the project folder
plt.savefig("charts/monthly_revenue.png", dpi=300)

#plt.show()
# showing profit by month
plt.figure(figsize=(10,5))
plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales["total_profit"],
    marker="o"
)
plt.title("Monthly Profit")
plt.xlabel("Month")
plt.ylabel("Profit")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("charts/monthly_profits.png", dpi=300)
#plt.show()

#comparing revenue and profit by month
monthly_summary = monthly_sales[['total_revenue', 'total_profit']]
print(monthly_summary)

monthly_summary['profit_margin_pct'] = (monthly_summary['total_profit'] / monthly_summary['total_revenue']) * 100
print('Monthly Profit Margin')
print(monthly_summary['profit_margin_pct'])
# locating months with maximum and minimum profit margin
best_month = monthly_summary.loc[
    monthly_summary['profit_margin_pct'].idxmax()
]

worst_month = monthly_summary.loc[
    monthly_summary['profit_margin_pct'].idxmin()
]
print("Best month:")
print(best_month)
print("\nWorst month:")
print(worst_month)
# ranking months by profit margin
monthly_margin_ranking = monthly_summary.sort_values('profit_margin_pct', ascending=False)

print("\nMonthly Margin Ranking")
print(monthly_margin_ranking[["total_revenue", "total_profit", "profit_margin_pct"]])
# finding highest revenue, profit and margin
highest_revenue = monthly_summary.loc[monthly_summary['total_revenue'].idxmax(), 'total_revenue']
highest_profit = monthly_summary.loc[monthly_summary['total_profit'].idxmax(), 'total_profit']
highest_margin_pct = monthly_summary.loc[monthly_summary['profit_margin_pct'].idxmax(), 'profit_margin_pct']
print("Highest revenue:")
print(highest_revenue)
print("Highest profit:")
print(highest_profit)
print("Highest margin:")
print(highest_margin_pct)
# Find the month with the highest values
highest_revenue_month = monthly_summary['total_revenue'].idxmax()
highest_profit_month = monthly_summary['total_profit'].idxmax()
highest_margin_month = monthly_summary['profit_margin_pct'].idxmax()

print("Highest revenue month:", highest_revenue_month)
print("Highest profit month:", highest_profit_month)
print("Highest profit margin month:", highest_margin_month)
# calculating percentage change in revenue
monthly_summary['revenue_change_pct'] = monthly_summary['total_revenue'].pct_change() * 100
print("\nMonthly Revenue Change PCT")
print(monthly_summary[['total_revenue', 'revenue_change_pct']])
# months with largest positive and largest changes
largest_revenue_change_month = monthly_summary['revenue_change_pct'].idxmax()
lowest_revenue_change_month = monthly_summary['revenue_change_pct'].idxmin()
print("Largest revenue change month:", largest_revenue_change_month)
print("\nBest Revenue Change:", monthly_summary.loc[largest_revenue_change_month, 'revenue_change_pct'])
print("\nLowest revenue change month:", lowest_revenue_change_month)
print("\nWorst Revenue Change:", monthly_summary.loc[lowest_revenue_change_month, 'revenue_change_pct'])
# calculating profit change percentage
monthly_summary['profit_change_pct'] = monthly_summary['total_profit'].pct_change() * 100
print("\nMonthly Profit Change PCT")
print(monthly_summary[['total_profit', 'profit_change_pct']])
# indexing the month with the highest and lowest profits
highest_profit_change_month = monthly_summary['profit_change_pct'].idxmax()
lowest_profit_change_month = monthly_summary['profit_change_pct'].idxmin()
print("Best month profit:", highest_profit_change_month)
print(monthly_summary.loc[highest_profit_change_month, 'profit_change_pct'])
print("\nLowest month profit:", lowest_profit_change_month)
print(monthly_summary.loc[lowest_profit_change_month, 'profit_change_pct'])

#investigating months where revenue and profits move in opposite directions
revenue_up_profit_down = monthly_summary[(monthly_summary['revenue_change_pct'] > 0) & (monthly_summary['profit_change_pct'] < 0)]
revenue_down_profit_up = monthly_summary[(monthly_summary['revenue_change_pct'] < 0) & (monthly_summary['profit_change_pct'] > 0)]
print("\nRevenue Up Profit Down")
print(revenue_up_profit_down[['revenue_change_pct', 'profit_change_pct']])
print("\nRevenue Down Profit Up")
print(revenue_down_profit_up[['revenue_change_pct', 'profit_change_pct']])
# Calculating margin change points
monthly_summary['margin_change_pp'] = monthly_summary['profit_margin_pct'].diff()
print("\nMonthly Margin Change PCT")
print(monthly_summary[['profit_margin_pct', 'margin_change_pp']])
#month with largest margin change point
best_margin_change_month = monthly_summary['margin_change_pp'].idxmax()
#month with lowest margin change change point
worst_margin_change_month = monthly_summary['margin_change_pp'].idxmin()
print("\nBest margin month:", best_margin_change_month)
print("Best Month:", monthly_summary.loc[best_margin_change_month, 'margin_change_pp'])
print("\nWorst margin month:", worst_margin_change_month)
print("Worst Margin Month:", monthly_summary.loc[worst_margin_change_month, 'margin_change_pp'])
# creating monthly report dataframe
monthly_report = monthly_summary[['total_revenue', 'total_profit', 'profit_margin_pct',
                                  'revenue_change_pct', 'profit_change_pct', 'margin_change_pp']]
monthly_report_rounded = monthly_report.round(2)
monthly_report_rounded.to_csv("outputs/monthly_performance_report.csv", index_label='month')
print(monthly_report_rounded.head())
print(monthly_report_rounded.shape)

# product category performance
print(sales_df.columns.to_list())
sales_df_columns = ['order_id', 'order_date', 'customer_id', 'product_id', 'quantity',
                    'product_name', 'category', 'unit_cost', 'unit_price',
                    'product_match', 'customer_name', 'city', 'region',
                    'customer_match', 'revenue', 'total_cost', 'profit', 'month']
category_summary = sales_df.groupby('category').agg(total_revenue=('revenue', 'sum'),
                   total_profit=('profit', 'sum'))
category_summary['profit_margin_pct'] = category_summary['total_profit'] / category_summary['total_revenue'] * 100
print(category_summary['profit_margin_pct'])
profit_margin_sorted= category_summary.sort_values('profit_margin_pct', ascending=False)
print(profit_margin_sorted)

# filtering phone category
phone_category_filtered = sales_df[sales_df['category'] == 'Phones']
print(phone_category_filtered[['product_name', 'quantity', 'unit_cost', 'unit_price',
                               'revenue', 'total_cost', 'profit']])
print(
    phone_category_filtered[
        ['product_name', 'unit_cost', 'unit_price']
    ].drop_duplicates()
)
print(products_df.columns.tolist())
print(products_df[products_df['product_name'] == 'Phone'])
products_columns = ['product_id', 'product_name', 'category', 'unit_cost', 'unit_price']

# filtering networking category
networking_category_filtered = sales_df[sales_df['category'] == 'Networking']
print(networking_category_filtered[['product_name', 'quantity', 'unit_cost', 'unit_price',
                               'revenue', 'total_cost', 'profit']])

# investigating the number of products in Networking
print(
    networking_category_filtered[
        ['product_name', 'unit_cost', 'unit_price']
    ].drop_duplicates()
)
#Note: the low margin of Networking is consistent with the cost and price
#Finding Revenue Contribution by Category
category_summary['revenue_contribution_pct'] = (category_summary['total_revenue'] /
                                                category_summary['total_revenue'].sum() * 100)
print(category_summary['revenue_contribution_pct'])
#profit contribution by category
category_summary['profit_contribution_pct'] = (category_summary['total_profit'] /
                                               category_summary['total_profit'].sum() * 100)
print(category_summary['profit_contribution_pct'])
#Contribution gap
category_summary['contribution_gap_pp'] = (category_summary['profit_contribution_pct'] -
                                           category_summary['revenue_contribution_pct'])
print(category_summary['contribution_gap_pp'])
category_summary = category_summary.sort_values('contribution_gap_pp', ascending=False)
print(category_summary[['revenue_contribution_pct', 'profit_contribution_pct',
                        'contribution_gap_pp', 'profit_margin_pct']])
# category report
category_report = category_summary[['total_revenue', 'total_profit',
                                    'revenue_contribution_pct', 'profit_contribution_pct',
                                    'contribution_gap_pp', 'profit_margin_pct',
                                    ]]
category_report_rounded = category_report.round(2)
category_report_rounded.to_csv("outputs/category_performance_report.csv", index_label="category")
import os

print(os.path.exists("outputs/category_performance_report.csv"))