
# ============================================================
# PROJECT: Airbnb Market Intelligence
# PHASE 1: Data Understanding and Inspection
# SCRIPT: 01_inspect_data.py
# PURPOSE: Verify source files and prepare for data inspection
# ============================================================

from pathlib import Path
import duckdb

# 1. Identify the project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# 2. Define the raw dataset directory
DATA_DIR = PROJECT_DIR / "data" / "raw"

# 3. Define source dataset paths
LISTINGS_FILE = DATA_DIR / "Listings.csv"
REVIEWS_FILE = DATA_DIR / "Reviews.csv"

# 4. Connect to DuckDB (in-memory database)
con = duckdb.connect(database=":memory:")

# 5. Display project information
print("=" * 60)
print("AIRBNB MARKET INTELLIGENCE")
print("PHASE 1: DATA UNDERSTANDING AND INSPECTION")
print("=" * 60)

print(f"\nProject directory: {PROJECT_DIR}")
print(f"Data directory: {DATA_DIR}")
print(f"DuckDB version: {duckdb.__version__}")

# 6. Verify source datasets
print("\nSOURCE DATASET VERIFICATION")
print("-" * 60)

for file_path in [LISTINGS_FILE, REVIEWS_FILE]:

    if file_path.exists():
        size_mb = file_path.stat().st_size / (1024 * 1024)

        print(f"File: {file_path.name}")
        print(f"Status: Found")
        print(f"Size: {size_mb:.2f} MB\n")

    else:
        print(f"ERROR: {file_path.name} not found!\n")


# 7. Inspect dataset structures
print("\nDATASET STRUCTURE INSPECTION")
print("=" * 60)

datasets = {
    "LISTINGS": LISTINGS_FILE,
    "REVIEWS": REVIEWS_FILE
}

for dataset_name, file_path in datasets.items():

    print(f"\n{dataset_name} DATASET")
    print("-" * 60)

    # Prepare a safe file path for DuckDB
    sql_path = str(file_path).replace("\\", "/").replace("'", "''")

    # Detect column names and data types
    schema = con.execute(
        f"""
        DESCRIBE
        SELECT *
        FROM read_csv_auto('{sql_path}', sample_size=10000)
        """
    ).fetchall()

    print(f"Number of columns: {len(schema)}")
    print("\nColumn names and detected data types:")

    for column in schema:
        column_name = column[0]
        data_type = column[1]

        print(f"{column_name:<35} {data_type}")

# 8. Count records in each dataset
print("\nDATASET RECORD COUNTS")
print("=" * 60)

for dataset_name, file_path in datasets.items():

    sql_path = str(file_path).replace("\\", "/").replace("'", "''")
    record_count = con.execute(
    f"""
    SELECT COUNT(*)
    FROM read_csv_auto(
        '{sql_path}',
        encoding='latin-1'
    )
    """
).fetchone()[0]


    print(f"{dataset_name}: {record_count:,} records")

con.close()


