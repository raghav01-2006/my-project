import os
from pyspark.sql import SparkSession

def main():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("ProductSalesProcessor") \
        .master("local[*]") \
        .getOrCreate()
    
    sc = spark.sparkContext
    sc.setLogLevel("WARN")
    
    csv_file = "sales.csv"
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        return

    # Read CSV file into Spark DataFrame
    print(f"Reading dataset: {csv_file}...")
    df = spark.read.csv(csv_file, header=True, inferSchema=True)
    
    # Display the schema
    print("\nDataFrame Schema:")
    df.printSchema()

    # -------------------------------------------------------------------------
    # Operation 1: Sort all products by sales in descending order and display
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("OPERATION 1: PRODUCTS SORTED BY SALES (DESCENDING)")
    print("=" * 80)
    sorted_df = df.orderBy(df["sales"].desc())
    sorted_df.show(truncate=False)
    print("=" * 80 + "\n")
    
    # -------------------------------------------------------------------------
    # Operation 2: Display the top 3 products with the highest sales values
    # -------------------------------------------------------------------------
    print("=" * 80)
    print("OPERATION 2: TOP 3 PRODUCTS WITH HIGHEST SALES")
    print("=" * 80)
    top_three_df = sorted_df.limit(3)
    top_three_df.show(truncate=False)
    print("=" * 80 + "\n")
    
    # -------------------------------------------------------------------------
    # Operation 3: Filter products with sales > 80,000 and save to CSV file
    # -------------------------------------------------------------------------
    print("=" * 80)
    print("OPERATION 3: FILTER PRODUCTS WITH SALES > 80,000")
    print("=" * 80)
    filtered_df = df.filter(df["sales"] > 80000)
    filtered_df.show(truncate=False)
    
    # Collect rows and write to a single CSV file on host
    high_sales = filtered_df.collect()
    output_filepath = "high_sales_products.csv"
    
    with open(output_filepath, "w") as f:
        # Write CSV Header
        f.write("product_id,product_name,category,sales\n")
        # Write CSV Rows
        for row in high_sales:
            f.write(f"{row['product_id']},{row['product_name']},{row['category']},{row['sales']}\n")
            
    print(f"Output successfully saved as a CSV file to: {output_filepath}")
    print("=" * 80 + "\n")
    
    # Stop Spark Session
    spark.stop()

if __name__ == "__main__":
    main()
