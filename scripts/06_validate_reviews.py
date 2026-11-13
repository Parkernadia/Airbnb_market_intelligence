
from pathlib import Path
import duckdb

PROJECT_DIR = Path(__file__).resolve().parent.parent
REVIEWS_FILE = PROJECT_DIR / "data" / "raw" / "Reviews.csv"

if not REVIEWS_FILE.exists():
    raise FileNotFoundError(f"Reviews file not found: {REVIEWS_FILE}")

con = duckdb.connect()

file_path = REVIEWS_FILE.as_posix()

print("REVIEWS FILE VALIDATION")
print("=" * 50)

row_count = con.execute(
    f"""
    SELECT COUNT(*)
    FROM read_csv_auto('{file_path}', sample_size=10000)
    """
).fetchone()[0]

column_count = len(
    con.execute(
        f"""
        DESCRIBE
        SELECT *
        FROM read_csv_auto('{file_path}', sample_size=10000)
        """
    ).fetchall()
)

print(f"File: {REVIEWS_FILE.name}")
print(f"Records: {row_count:,}")
print(f"Columns: {column_count}")
print("DuckDB full-file read: PASSED")

con.close()
