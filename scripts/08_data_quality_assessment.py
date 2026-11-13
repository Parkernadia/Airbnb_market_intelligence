
from pathlib import Path
import duckdb

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = PROJECT_DIR / "data" / "processed" / "airbnb.duckdb"

if not DATABASE_FILE.exists():
    raise FileNotFoundError(f"Database not found: {DATABASE_FILE}")

con = duckdb.connect(str(DATABASE_FILE), read_only=True)


def profile_missing_values(table_name):
    print(f"\nMISSING VALUES — {table_name.upper()}")
    print("-" * 65)

    schema = con.execute(f"DESCRIBE {table_name}").fetchall()
    expressions = []

    for column in schema:
        name = column[0]
        data_type = column[1]
        safe_name = '"' + name.replace('"', '""') + '"'

        expressions.append(
            f"COUNT(*) FILTER (WHERE {safe_name} IS NULL)"
        )

        if data_type.upper() == "VARCHAR":
            expressions.append(
                f"COUNT(*) FILTER "
                f"(WHERE TRIM({safe_name}) = '')"
            )

    results = con.execute(
        f"SELECT {', '.join(expressions)} FROM {table_name}"
    ).fetchone()

    index = 0
    for column in schema:
        name = column[0]
        null_count = results[index]
        index += 1

        blank_count = None
        if column[1].upper() == "VARCHAR":
            blank_count = results[index]
            index += 1

        if null_count > 0 or (blank_count is not None and blank_count > 0):
            print(f"{name}: NULL = {null_count:,}", end="")
            if blank_count is not None:
                print(f" | Blank = {blank_count:,}")
            else:
                print()


def count_duplicate_groups(query):
    return con.execute(query).fetchone()[0]


print("AIRBNB DATA QUALITY ASSESSMENT")
print("=" * 65)

# 1. Missing values
profile_missing_values("listings")
profile_missing_values("reviews")

# 2. Listing identifier uniqueness
duplicate_listing_ids = count_duplicate_groups("""
    SELECT COUNT(*)
    FROM (
        SELECT listing_id
        FROM listings
        GROUP BY listing_id
        HAVING COUNT(*) > 1
    )
""")

print("\nIDENTIFIER DUPLICATES")
print("-" * 65)
print(f"Duplicate listing_id groups: {duplicate_listing_ids:,}")

# 3. Review identifier duplication
duplicate_review_ids = count_duplicate_groups("""
    SELECT COUNT(*)
    FROM (
        SELECT review_id
        FROM reviews
        GROUP BY review_id
        HAVING COUNT(*) > 1
    )
""")

duplicate_review_rows = con.execute("""
    SELECT COALESCE(SUM(review_count), 0)
    FROM (
        SELECT COUNT(*) AS review_count
        FROM reviews
        GROUP BY review_id
        HAVING COUNT(*) > 1
    )
""").fetchone()[0]

print(f"Duplicate review_id groups: {duplicate_review_ids:,}")
print(f"Rows belonging to duplicate review_id groups: {duplicate_review_rows:,}")

# 4. Composite review key uniqueness
duplicate_composite_keys = count_duplicate_groups("""
    SELECT COUNT(*)
    FROM (
        SELECT listing_id, review_id
        FROM reviews
        GROUP BY listing_id, review_id
        HAVING COUNT(*) > 1
    )
""")

print(f"Duplicate (listing_id, review_id) groups: {duplicate_composite_keys:,}")

# 5. Referential integrity
orphan_reviews = con.execute("""
    SELECT COUNT(*)
    FROM reviews r
    LEFT JOIN listings l
        ON r.listing_id = l.listing_id
    WHERE l.listing_id IS NULL
""").fetchone()[0]

listings_without_reviews = con.execute("""
    SELECT COUNT(*)
    FROM listings l
    LEFT JOIN (
        SELECT DISTINCT listing_id
        FROM reviews
    ) r
        ON l.listing_id = r.listing_id
    WHERE r.listing_id IS NULL
""").fetchone()[0]

listings_with_reviews = con.execute("""
    SELECT COUNT(DISTINCT listing_id)
    FROM reviews
""").fetchone()[0]

print("\nLISTINGS AND REVIEWS RELATIONSHIP")
print("-" * 65)
print(f"Distinct listings with reviews: {listings_with_reviews:,}")
print(f"Listings without reviews: {listings_without_reviews:,}")
print(f"Review records with unmatched listing IDs: {orphan_reviews:,}")

print("\nASSESSMENT COMPLETED")
con.close()
