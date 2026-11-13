
from pathlib import Path
import duckdb

# Locate the project folders
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATABASE_PATH = PROJECT_DIR / "data" / "processed" / "airbnb.duckdb"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed" / "powerbi_exports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Output files
LISTINGS_OUTPUT = OUTPUT_DIR / "listings_analysis.csv"
CITY_OUTPUT = OUTPUT_DIR / "city_summary.csv"
TRENDS_OUTPUT = OUTPUT_DIR / "monthly_review_trends.csv"

# Connect to the existing database without modifying it
con = duckdb.connect(str(DATABASE_PATH), read_only=True)

# 1. Listing-level analysis table
listings_query = """
SELECT
    l.*,
    COALESCE(r.review_count, 0) AS review_count,
    r.last_review_date,
    h.host_listing_count
FROM listings AS l
LEFT JOIN (
    SELECT
        listing_id,
        COUNT(*) AS review_count,
        MAX(date) AS last_review_date
    FROM reviews
    GROUP BY listing_id
) AS r
    ON l.listing_id = r.listing_id
LEFT JOIN (
    SELECT
        host_id,
        COUNT(*) AS host_listing_count
    FROM listings
    GROUP BY host_id
) AS h
    ON l.host_id = h.host_id
"""

# 2. City-level market summary
city_query = """
SELECT
    city,
    COUNT(*) AS listing_count,
    ROUND(AVG(price), 2) AS average_price,
    MEDIAN(price) AS median_price,
    ROUND(AVG(accommodates), 2) AS average_capacity,
    ROUND(AVG(review_scores_rating), 2) AS average_review_score,
    COUNT(*) FILTER (WHERE review_count > 0) AS listings_with_reviews,
    COUNT(*) FILTER (WHERE host_is_superhost = TRUE) AS superhost_listings
FROM (
    SELECT
        l.city,
        l.price,
        l.accommodates,
        l.review_scores_rating,
        l.host_is_superhost,
        COUNT(r.review_id) AS review_count
    FROM listings AS l
    LEFT JOIN reviews AS r
        ON l.listing_id = r.listing_id
    GROUP BY
        l.listing_id,
        l.city,
        l.price,
        l.accommodates,
        l.review_scores_rating,
        l.host_is_superhost
) AS listing_data
WHERE city IS NOT NULL
GROUP BY city
ORDER BY listing_count DESC
"""

# 3. Monthly review trends
trends_query = """
SELECT
    DATE_TRUNC('month', date)::DATE AS review_month,
    COUNT(*) AS review_count
FROM reviews
GROUP BY review_month
ORDER BY review_month
"""

# Export each query as a CSV file
con.execute(
    f"COPY ({listings_query}) TO '{LISTINGS_OUTPUT.as_posix()}' "
    "(HEADER, DELIMITER ',')"
)

con.execute(
    f"COPY ({city_query}) TO '{CITY_OUTPUT.as_posix()}' "
    "(HEADER, DELIMITER ',')"
)

con.execute(
    f"COPY ({trends_query}) TO '{TRENDS_OUTPUT.as_posix()}' "
    "(HEADER, DELIMITER ',')"
)

# Confirm the exported row counts
for output_file in [LISTINGS_OUTPUT, CITY_OUTPUT, TRENDS_OUTPUT]:
    print(f"{output_file.name}: {output_file.stat().st_size:,} bytes")

print("\nPOWER BI DATA EXPORTS COMPLETED")

con.close()
