import os
from pyspark.sql import SparkSession

def main():
    # Initialize Spark Session and Context
    spark = SparkSession.builder \
        .appName("EmployeeSalaryProcessor") \
        .master("local[*]") \
        .getOrCreate()
    
    sc = spark.sparkContext
    
    # Set log level to WARN to avoid verbose logs
    sc.setLogLevel("WARN")
    
    csv_file = "employee.csv"
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        return

    # Read CSV file into RDD
    print(f"Reading dataset: {csv_file}...")
    rdd = sc.textFile(csv_file)
    
    # Filter out header line
    header = rdd.first()
    data_rdd = rdd.filter(lambda line: line != header)
    
    # Parse lines to (id, name, department, salary)
    # Fields: 1,Amit,IT,55000
    def parse_line(line):
        parts = line.split(',')
        emp_id = int(parts[0])
        name = parts[1]
        department = parts[2]
        salary = float(parts[3])
        return (emp_id, name, department, salary)
    
    parsed_rdd = data_rdd.map(parse_line)
    
    # -------------------------------------------------------------------------
    # Operation 1: Sort all employees by salary in descending order and display
    # -------------------------------------------------------------------------
    sorted_rdd = parsed_rdd.sortBy(lambda emp: emp[3], ascending=False)
    sorted_employees = sorted_rdd.collect()
    
    print("\n" + "=" * 60)
    print("OPERATION 1: EMPLOYEES SORTED BY SALARY (DESCENDING)")
    print("=" * 60)
    for emp in sorted_employees:
        print(f"ID: {emp[0]:<2} | Name: {emp[1]:<10} | Dept: {emp[2]:<10} | Salary: {emp[3]:.2f}")
    print("=" * 60 + "\n")
    
    # -------------------------------------------------------------------------
    # Operation 2: Calculate total salary paid in each department and print
    # -------------------------------------------------------------------------
    dept_salary_rdd = parsed_rdd.map(lambda emp: (emp[2], emp[3])).reduceByKey(lambda a, b: a + b)
    dept_salaries = dept_salary_rdd.collect()
    
    print("=" * 60)
    print("OPERATION 2: DEPARTMENT-WISE TOTAL SALARIES")
    print("=" * 60)
    for dept, total_sal in dept_salaries:
        print(f"Department: {dept:<10} | Total Salary Paid: {total_sal:.2f}")
    print("=" * 60 + "\n")
    
    # -------------------------------------------------------------------------
    # Operation 3: Identify top three highest-paid employees and save to file
    # -------------------------------------------------------------------------
    top_three = sorted_rdd.take(3)
    output_filepath = "top_three_employees.txt"
    
    with open(output_filepath, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("OPERATION 3: TOP 3 HIGHEST-PAID EMPLOYEES\n")
        f.write("=" * 60 + "\n")
        for emp in top_three:
            f.write(f"ID: {emp[0]:<2} | Name: {emp[1]:<10} | Dept: {emp[2]:<10} | Salary: {emp[3]:.2f}\n")
        f.write("=" * 60 + "\n")
        
    print("=" * 60)
    print("OPERATION 3: TOP 3 HIGHEST-PAID EMPLOYEES")
    print("=" * 60)
    for emp in top_three:
        print(f"ID: {emp[0]:<2} | Name: {emp[1]:<10} | Dept: {emp[2]:<10} | Salary: {emp[3]:.2f}")
    print("=" * 60)
    print(f"Output successfully saved to: {output_filepath}\n")
    
    # Stop Spark context
    spark.stop()

if __name__ == "__main__":
    main()
