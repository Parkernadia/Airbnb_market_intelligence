
from pathlib import Path
import duckdb

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = PROJECT_DIR / "data" / "processed" / "airbnb.duckdb"

con = duckdb.connect(str(DATABASE_FILE), read_only=True)

print("REPEATED REVIEW ID INVESTIGATION")
print("=" * 65)

# 1. Distribution of repeated review IDs
print("\n1. FREQUENCY DISTRIBUTION")
print("-" * 65)

distribution = con.execute("""
    SELECT occurrence_count, COUNT(*) AS review_id_groups
    FROM (
        SELECT review_id, COUNT(*) AS occurrence_count
        FROM reviews
        GROUP BY review_id
    )
    WHERE occurrence_count > 1
    GROUP BY occurrence_count
    ORDER BY occurrence_count
""").fetchall()

for occurrences, groups in distribution:
    print(f"Review IDs appearing {occurrences} times: {groups:,}")

# 2. Check whether reviewer and date are consistent
print("\n2. REVIEWER AND DATE CONSISTENCY")
print("-" * 65)

consistency = con.execute("""
    SELECT
        COUNT(*) AS repeated_groups,
        COUNT(*) FILTER (WHERE occurrence_count = 2) AS groups_exactly_twice,
        COUNT(*) FILTER (WHERE distinct_reviewers = 1) AS same_reviewer,
        COUNT(*) FILTER (WHERE distinct_dates = 1) AS same_date,
        COUNT(*) FILTER (
            WHERE distinct_reviewers = 1 AND distinct_dates = 1
        ) AS same_reviewer_and_date,
        MAX(occurrence_count) AS maximum_occurrences
    FROM (
        SELECT
            review_id,
            COUNT(*) AS occurrence_count,
            COUNT(DISTINCT reviewer_id) AS distinct_reviewers,
            COUNT(DISTINCT date) AS distinct_dates
        FROM reviews
        GROUP BY review_id
        HAVING COUNT(*) > 1
    )
""").fetchone()

print(f"Repeated review ID groups: {consistency[0]:,}")
print(f"Groups appearing exactly twice: {consistency[1]:,}")
print(f"Groups with one reviewer: {consistency[2]:,}")
print(f"Groups with one review date: {consistency[3]:,}")
print(f"Groups matching on reviewer and date: {consistency[4]:,}")
print(f"Maximum occurrences of one review ID: {consistency[5]:,}")

# 3. Identify listing pairs most frequently sharing review IDs
print("\n3. MOST FREQUENTLY ASSOCIATED LISTING PAIRS")
print("-" * 65)

pairs = con.execute("""
    SELECT
        LEAST(a.listing_id, b.listing_id) AS listing_id_1,
        GREATEST(a.listing_id, b.listing_id) AS listing_id_2,
        COUNT(*) AS shared_review_ids
    FROM reviews a
    JOIN reviews b
        ON a.review_id = b.review_id
       AND a.listing_id < b.listing_id
    GROUP BY listing_id_1, listing_id_2
    ORDER BY shared_review_ids DESC
    LIMIT 15
""").fetchall()

for listing_1, listing_2, shared_count in pairs:
    print(
        f"Listings {listing_1:,} and {listing_2:,}: "
        f"{shared_count:,} shared review IDs"
    )

# 4. Check whether any repeated IDs have different listing counts
print("\n4. REPEATED REVIEW ID EXAMPLES")
print("-" * 65)

examples = con.execute("""
    SELECT
        review_id,
        COUNT(*) AS occurrences,
        COUNT(DISTINCT listing_id) AS distinct_listings,
        COUNT(DISTINCT reviewer_id) AS distinct_reviewers,
        COUNT(DISTINCT date) AS distinct_dates
    FROM reviews
    GROUP BY review_id
    HAVING COUNT(*) > 1
    ORDER BY review_id
    LIMIT 10
""").fetchall()

for row in examples:
    print(row)

print("\nINVESTIGATION COMPLETED")

con.close()
