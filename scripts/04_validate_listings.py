
from pathlib import Path
import duckdb

PROJECT_DIR = Path(__file__).resolve().parent.parent
LISTINGS_FILE = PROJECT_DIR / "data" / "processed" / "Listings_utf8.csv"

if not LISTINGS_FILE.exists():
    raise FileNotFoundError(f"Processed file not found: {LISTINGS_FILE}")

con = duckdb.connect()

file_path = LISTINGS_FILE.as_posix()

print("LISTINGS FILE VALIDATION")
print("=" * 50)

# Read the complete CSV and count its records
row_count = con.execute(
    f"""
    SELECT COUNT(*)
    FROM read_csv_auto('{file_path}', sample_size=10000)
    """
).fetchone()[0]

# Count the detected columns
column_count = len(
    con.execute(
        f"""
        DESCRIBE
        SELECT *
        FROM read_csv_auto('{file_path}', sample_size=10000)
        """
    ).fetchall()
)

print(f"File: {LISTINGS_FILE.name}")
print(f"Records: {row_count:,}")
print(f"Columns: {column_count}")
print("DuckDB full-file read: PASSED")

con.close()
