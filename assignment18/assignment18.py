from pyspark.sql import SparkSession

def main():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("DataFramePartitioning") \
        .master("local[*]") \
        .getOrCreate()
    
    sc = spark.sparkContext
    sc.setLogLevel("WARN")
    
    print("\n" + "=" * 80)
    print("PySpark DataFrame Partitioning Application (Assignment 18)")
    print("=" * 80)
    
    # 1. Generate DataFrame with 5 million records using spark.range()
    print("Generating DataFrame containing 5,000,000 records using spark.range()...")
    df = spark.range(0, 5000000)
    
    # 2. Display the initial number of partitions
    initial_partitions = df.rdd.getNumPartitions()
    print("\n[Initial State]")
    print(f"Number of partitions: {initial_partitions}")
    
    # 3. Increase partitions to 12 using repartition()
    print("\nIncreasing partition count to 12 using repartition(12)...")
    repartitioned_df = df.repartition(12)
    repartitioned_count = repartitioned_df.rdd.getNumPartitions()
    print("[After Repartition]")
    print(f"Number of partitions: {repartitioned_count}")
    
    # 4. Reduce partitions to 3 using coalesce()
    print("\nReducing partition count to 3 using coalesce(3)...")
    coalesced_df = repartitioned_df.coalesce(3)
    coalesced_count = coalesced_df.rdd.getNumPartitions()
    print("[After Coalesce]")
    print(f"Number of partitions: {coalesced_count}")
    
    # 5. Verify the record count
    print("\n[Validation]")
    print("Verifying record count in final coalesced DataFrame...")
    record_count = coalesced_df.count()
    print(f"Total records in coalesced DataFrame: {record_count:,}")
    
    if record_count == 5000000:
        print("SUCCESS: Record count matches target of 5,000,000!")
    else:
        print(f"WARNING: Record count mismatch! Found {record_count}")
        
    print("=" * 80 + "\n")
    
    # Stop Spark Session
    spark.stop()

if __name__ == "__main__":
    main()
