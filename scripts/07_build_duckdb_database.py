
from pathlib import Path
import duckdb

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

LISTINGS_FILE = PROCESSED_DIR / "Listings_utf8.csv"
REVIEWS_FILE = PROJECT_DIR / "data" / "raw" / "Reviews.csv"

DATABASE_FILE = PROCESSED_DIR / "airbnb.duckdb"
TEMP_DIR = PROCESSED_DIR / "duckdb_temp"

# Check input files
for file in [LISTINGS_FILE, REVIEWS_FILE]:
    if not file.exists():
        raise FileNotFoundError(f"Required file not found: {file}")

# Avoid overwriting an existing database
if DATABASE_FILE.exists():
    raise FileExistsError(
        f"Database already exists: {DATABASE_FILE}\n"
        "Rename or remove it before running this script again."
    )

# Create temporary storage directory
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Connect to a persistent DuckDB database
con = duckdb.connect(str(DATABASE_FILE))

# Configure DuckDB for the available laptop resources
con.execute("SET memory_limit = '2GB'")
con.execute("SET threads = 4")
con.execute(f"SET temp_directory = '{TEMP_DIR.as_posix()}'")
con.execute("SET preserve_insertion_order = false")

listings_path = LISTINGS_FILE.as_posix()
reviews_path = REVIEWS_FILE.as_posix()

print("BUILDING AIRBNB DUCKDB DATABASE")
print("=" * 50)

# Import Listings
print("\nImporting Listings...")
con.execute(
    f"""
    CREATE TABLE listings AS
    SELECT *
    FROM read_csv_auto('{listings_path}', sample_size=10000)
    """
)
print("Listings table created.")

# Import Reviews
print("\nImporting Reviews...")
con.execute(
    f"""
    CREATE TABLE reviews AS
    SELECT *
    FROM read_csv_auto('{reviews_path}', sample_size=10000)
    """
)
print("Reviews table created.")

# Verify imported records
listings_count = con.execute(
    "SELECT COUNT(*) FROM listings"
).fetchone()[0]

reviews_count = con.execute(
    "SELECT COUNT(*) FROM reviews"
).fetchone()[0]

print("\nDATABASE VALIDATION")
print("=" * 50)
print(f"Listings records: {listings_count:,}")
print(f"Reviews records: {reviews_count:,}")

print(f"\nDatabase location: {DATABASE_FILE}")
print(f"Database size: {DATABASE_FILE.stat().st_size:,} bytes")

con.close()

print("\nRESULT: DATABASE CREATED AND VALIDATED")
