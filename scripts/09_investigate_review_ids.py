
from pathlib import Path
import duckdb

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = PROJECT_DIR / "data" / "processed" / "airbnb.duckdb"

con = duckdb.connect(str(DATABASE_FILE), read_only=True)

print("REPEATED REVIEW ID INVESTIGATION")
print("=" * 65)

# Display examples of repeated review IDs
results = con.execute("""
    SELECT
        listing_id,
        review_id,
        date,
        reviewer_id
    FROM reviews
    WHERE review_id IN (
        SELECT review_id
        FROM reviews
        GROUP BY review_id
        HAVING COUNT(*) > 1
    )
    ORDER BY review_id, listing_id
    LIMIT 20
""").fetchall()

print("\nFIRST 20 RECORDS WITH REPEATED REVIEW IDs")
print("-" * 65)

for row in results:
    print(row)

# Check the review date range
date_range = con.execute("""
    SELECT
        MIN(date),
        MAX(date),
        COUNT(DISTINCT date)
    FROM reviews
""").fetchone()

print("\nREVIEW DATE PROFILE")
print("-" * 65)
print(f"Earliest review date: {date_range[0]}")
print(f"Latest review date: {date_range[1]}")
print(f"Distinct review dates: {date_range[2]:,}")

con.close()
