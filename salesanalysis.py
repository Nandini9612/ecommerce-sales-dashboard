import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# PART 1: DATA GENERATION - Realistic Myntra-style E-commerce Sales Data
# ============================================================================

def generate_myntra_sales_data(n_records=5000):
    """
    Generate realistic fashion e-commerce sales data similar to Myntra
    """
    np.random.seed(42)
    
    # Define product categories and subcategories (Myntra-style)
    categories = {
        'Men': ['T-Shirts', 'Shirts', 'Jeans', 'Trousers', 'Jackets', 'Shoes', 'Watches'],
        'Women': ['Dresses', 'Tops', 'Jeans', 'Sarees', 'Kurtis', 'Shoes', 'Handbags'],
        'Kids': ['T-Shirts', 'Dresses', 'Jeans', 'Shoes', 'Toys'],
        'Accessories': ['Sunglasses', 'Belts', 'Wallets', 'Bags', 'Jewelry']
    }
    
    # Brands (mix of premium and budget)
    brands = ['Roadster', 'H&M', 'Zara', 'Nike', 'Adidas', 'Puma', 'Levis', 
              'Allen Solly', 'Van Heusen', 'Mast & Harbour', 'HRX', 'Wrogn',
              'Biba', 'Libas', 'W', 'AND', 'Forever 21']
    
    # Cities
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 
              'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Chandigarh', 'Indore']
    
    # Payment methods
    payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'COD', 'Wallet']
    
    # Generate date range (last 12 months)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    data = []
    
    for i in range(n_records):
        # Random date with seasonal patterns
        random_days = np.random.randint(0, 365)
        order_date = start_date + timedelta(days=random_days)
        month = order_date.month
        
        # Category selection
        category = np.random.choice(list(categories.keys()))
        subcategory = np.random.choice(categories[category])
        
        # Brand selection
        brand = np.random.choice(brands)
        
        # Price based on category and brand (realistic pricing)
        base_prices = {
            'T-Shirts': (299, 1999), 'Shirts': (499, 2999), 'Jeans': (799, 3999),
            'Dresses': (599, 4999), 'Tops': (399, 2499), 'Sarees': (999, 9999),
            'Kurtis': (499, 2999), 'Shoes': (799, 5999), 'Watches': (999, 9999),
            'Handbags': (799, 6999), 'Jackets': (1299, 7999), 'Trousers': (699, 3499),
            'Sunglasses': (499, 2999), 'Belts': (299, 1499), 'Wallets': (399, 2499),
            'Bags': (599, 4999), 'Jewelry': (299, 4999), 'Toys': (199, 1999)
        }
        
        min_price, max_price = base_prices.get(subcategory, (500, 3000))
        
        # Premium brands have higher prices
        if brand in ['Zara', 'Nike', 'Adidas', 'Levis', 'Van Heusen']:
            price = np.random.randint(int(max_price*0.7), max_price)
        else:
            price = np.random.randint(min_price, int(max_price*0.7))
        
        # Discount (festive seasons have higher discounts)
        if month in [10, 11, 12, 1]:  # Festival season
            discount_pct = np.random.choice([10, 20, 30, 40, 50], p=[0.2, 0.3, 0.3, 0.15, 0.05])
        else:
            discount_pct = np.random.choice([0, 10, 20, 30], p=[0.3, 0.4, 0.2, 0.1])
        
        discount_amount = (price * discount_pct) / 100
        final_price = price - discount_amount
        
        # Quantity (mostly 1-2 items)
        quantity = np.random.choice([1, 2, 3], p=[0.7, 0.25, 0.05])
        
        # Total amount
        total_amount = final_price * quantity
        
        # Customer info
        customer_id = f'CUST{np.random.randint(10000, 99999)}'
        city = np.random.choice(cities)
        
        # Payment method
        payment_method = np.random.choice(payment_methods, p=[0.25, 0.20, 0.30, 0.10, 0.10, 0.05])
        
        # Order status (most are delivered)
        order_status = np.random.choice(['Delivered', 'Returned', 'Cancelled'], 
                                       p=[0.85, 0.10, 0.05])
        
        # Rating (only for delivered items)
        if order_status == 'Delivered':
            rating = np.random.choice([3, 4, 5], p=[0.15, 0.35, 0.50])
        else:
            rating = None
        
        # Customer segment
        if total_amount > 5000:
            customer_segment = 'Premium'
        elif total_amount > 2000:
            customer_segment = 'Mid-tier'
        else:
            customer_segment = 'Budget'
        
        data.append({
            'Order_ID': f'ORD{100000 + i}',
            'Order_Date': order_date.strftime('%Y-%m-%d'),
            'Customer_ID': customer_id,
            'Category': category,
            'Sub_Category': subcategory,
            'Brand': brand,
            'Product_Name': f'{brand} {subcategory}',
            'Original_Price': price,
            'Discount_Percent': discount_pct,
            'Discount_Amount': round(discount_amount, 2),
            'Final_Price': round(final_price, 2),
            'Quantity': quantity,
            'Total_Amount': round(total_amount, 2),
            'City': city,
            'Payment_Method': payment_method,
            'Order_Status': order_status,
            'Rating': rating,
            'Customer_Segment': customer_segment
        })
    
    return pd.DataFrame(data)

# ============================================================================
# PART 2: DATA LOADING AND BASIC EXPLORATION
# ============================================================================

print("=" * 80)
print("MYNTRA SALES PERFORMANCE ANALYSIS")
print("=" * 80)
print("\nGenerating realistic Myntra-style sales data...")

# Generate the dataset
df = generate_myntra_sales_data(5000)

# Convert date to datetime
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# Extract additional date features
df['Year'] = df['Order_Date'].dt.year
df['Month'] = df['Order_Date'].dt.month
df['Month_Name'] = df['Order_Date'].dt.strftime('%B')
df['Quarter'] = df['Order_Date'].dt.quarter
df['Day_of_Week'] = df['Order_Date'].dt.day_name()
df['Week'] = df['Order_Date'].dt.isocalendar().week

print(f"\n✓ Dataset Generated: {len(df)} records")
print(f"✓ Date Range: {df['Order_Date'].min().date()} to {df['Order_Date'].max().date()}")

# Display basic information
print("\n" + "=" * 80)
print("DATASET OVERVIEW")
print("=" * 80)
print(f"\nDataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\nColumn Names and Types:")
print(df.dtypes)

print("\n" + "-" * 80)
print("First 5 Records:")
print("-" * 80)
print(df.head())

print("\n" + "-" * 80)
print("Dataset Statistics:")
print("-" * 80)
print(df.describe())

# Check for missing values
print("\n" + "-" * 80)
print("Missing Values:")
print("-" * 80)
print(df.isnull().sum())

# ============================================================================
# PART 3: KEY PERFORMANCE INDICATORS (KPIs)
# ============================================================================

print("\n" + "=" * 80)
print("KEY PERFORMANCE INDICATORS")
print("=" * 80)

# Overall metrics
total_revenue = df['Total_Amount'].sum()
total_orders = len(df)
avg_order_value = df['Total_Amount'].mean()
total_customers = df['Customer_ID'].nunique()
avg_discount = df['Discount_Percent'].mean()

delivered_orders = df[df['Order_Status'] == 'Delivered']
return_rate = (len(df[df['Order_Status'] == 'Returned']) / total_orders) * 100
cancellation_rate = (len(df[df['Order_Status'] == 'Cancelled']) / total_orders) * 100

print(f"\n📊 OVERALL BUSINESS METRICS:")
print(f"   • Total Revenue: ₹{total_revenue:,.2f}")
print(f"   • Total Orders: {total_orders:,}")
print(f"   • Average Order Value (AOV): ₹{avg_order_value:,.2f}")
print(f"   • Total Customers: {total_customers:,}")
print(f"   • Average Discount: {avg_discount:.1f}%")
print(f"   • Return Rate: {return_rate:.2f}%")
print(f"   • Cancellation Rate: {cancellation_rate:.2f}%")

if len(delivered_orders) > 0 and delivered_orders['Rating'].notna().sum() > 0:
    avg_rating = delivered_orders['Rating'].mean()
    print(f"   • Average Rating: {avg_rating:.2f}/5.0")

# ============================================================================
# PART 4: SALES TREND ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("SALES TREND ANALYSIS")
print("=" * 80)

# Monthly sales trend
monthly_sales = df.groupby(df['Order_Date'].dt.to_period('M')).agg({
    'Total_Amount': 'sum',
    'Order_ID': 'count'
}).reset_index()
monthly_sales.columns = ['Month', 'Revenue', 'Orders']
monthly_sales['Month'] = monthly_sales['Month'].astype(str)

print("\nMonthly Sales Performance:")
print(monthly_sales.to_string(index=False))

# Best and worst performing months
best_month = monthly_sales.loc[monthly_sales['Revenue'].idxmax()]
worst_month = monthly_sales.loc[monthly_sales['Revenue'].idxmin()]

print(f"\n✓ Best Month: {best_month['Month']} (₹{best_month['Revenue']:,.2f})")
print(f"✓ Worst Month: {worst_month['Month']} (₹{worst_month['Revenue']:,.2f})")

# ============================================================================
# PART 5: CATEGORY PERFORMANCE ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("CATEGORY PERFORMANCE ANALYSIS")
print("=" * 80)

category_analysis = df.groupby('Category').agg({
    'Total_Amount': 'sum',
    'Order_ID': 'count',
    'Quantity': 'sum'
}).reset_index()
category_analysis.columns = ['Category', 'Revenue', 'Orders', 'Units_Sold']
category_analysis['Avg_Order_Value'] = category_analysis['Revenue'] / category_analysis['Orders']
category_analysis = category_analysis.sort_values('Revenue', ascending=False)

print("\nCategory-wise Performance:")
print(category_analysis.to_string(index=False))

# Top subcategories
print("\n" + "-" * 80)
print("Top 10 Sub-Categories by Revenue:")
print("-" * 80)
top_subcategories = df.groupby('Sub_Category')['Total_Amount'].sum().sort_values(ascending=False).head(10)
print(top_subcategories)

# ============================================================================
# PART 6: BRAND ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("BRAND PERFORMANCE ANALYSIS")
print("=" * 80)

brand_analysis = df.groupby('Brand').agg({
    'Total_Amount': 'sum',
    'Order_ID': 'count'
}).reset_index()
brand_analysis.columns = ['Brand', 'Revenue', 'Orders']
brand_analysis = brand_analysis.sort_values('Revenue', ascending=False).head(10)

print("\nTop 10 Brands by Revenue:")
print(brand_analysis.to_string(index=False))

# ============================================================================
# PART 7: GEOGRAPHICAL ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("GEOGRAPHICAL ANALYSIS")
print("=" * 80)

city_analysis = df.groupby('City').agg({
    'Total_Amount': 'sum',
    'Order_ID': 'count',
    'Customer_ID': 'nunique'
}).reset_index()
city_analysis.columns = ['City', 'Revenue', 'Orders', 'Customers']
city_analysis = city_analysis.sort_values('Revenue', ascending=False)

print("\nCity-wise Performance:")
print(city_analysis.to_string(index=False))

# ============================================================================
# PART 8: CUSTOMER SEGMENTATION ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("CUSTOMER SEGMENTATION ANALYSIS")
print("=" * 80)

segment_analysis = df.groupby('Customer_Segment').agg({
    'Total_Amount': 'sum',
    'Order_ID': 'count',
    'Customer_ID': 'nunique'
}).reset_index()
segment_analysis.columns = ['Segment', 'Revenue', 'Orders', 'Customers']
segment_analysis['Revenue_per_Customer'] = segment_analysis['Revenue'] / segment_analysis['Customers']

print("\nCustomer Segment Performance:")
print(segment_analysis.to_string(index=False))

# ============================================================================
# PART 9: PAYMENT METHOD ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("PAYMENT METHOD ANALYSIS")
print("=" * 80)

payment_analysis = df.groupby('Payment_Method').agg({
    'Total_Amount': 'sum',
    'Order_ID': 'count'
}).reset_index()
payment_analysis.columns = ['Payment_Method', 'Revenue', 'Orders']
payment_analysis['Revenue_Share_%'] = (payment_analysis['Revenue'] / payment_analysis['Revenue'].sum()) * 100
payment_analysis = payment_analysis.sort_values('Revenue', ascending=False)

print("\nPayment Method Distribution:")
print(payment_analysis.to_string(index=False))

# ============================================================================
# PART 10: EXPORT DATA FOR POWER BI
# ============================================================================

print("\n" + "=" * 80)
print("EXPORTING DATA FOR POWER BI")
print("=" * 80)

# Main sales data
df.to_csv('myntra_sales_data.csv', index=False)
print("✓ Main dataset exported: myntra_sales_data.csv")

# Monthly summary
monthly_sales.to_csv('monthly_sales_summary.csv', index=False)
print("✓ Monthly summary exported: monthly_sales_summary.csv")

# Category summary
category_analysis.to_csv('category_performance.csv', index=False)
print("✓ Category performance exported: category_performance.csv")

# City summary
city_analysis.to_csv('city_performance.csv', index=False)
print("✓ City performance exported: city_performance.csv")

# Brand summary
brand_analysis.to_csv('brand_performance.csv', index=False)
print("✓ Brand performance exported: brand_performance.csv")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print("\n📁 Files Generated:")
print("   1. myntra_sales_data.csv (Main dataset)")
print("   2. monthly_sales_summary.csv")
print("   3. category_performance.csv")
print("   4. city_performance.csv")
print("   5. brand_performance.csv")
print("\n✨ You can now import these CSV files into Power BI to create your dashboard!")
print("=" * 80)