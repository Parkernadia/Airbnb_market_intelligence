
from pathlib import Path
import duckdb

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = PROJECT_DIR / "data" / "processed" / "airbnb.duckdb"

con = duckdb.connect(str(DATABASE_FILE), read_only=True)

# Identify listing pairs that share repeated review IDs
pairs_query = """
WITH repeated_pairs AS (
    SELECT
        LEAST(a.listing_id, b.listing_id) AS listing_id_1,
        GREATEST(a.listing_id, b.listing_id) AS listing_id_2,
        COUNT(*) AS shared_review_ids
    FROM reviews a
    JOIN reviews b
        ON a.review_id = b.review_id
       AND a.listing_id < b.listing_id
    GROUP BY 1, 2
)
SELECT
    p.listing_id_1,
    p.listing_id_2,
    p.shared_review_ids,

    l1.host_id AS host_1,
    l2.host_id AS host_2,

    l1.name AS name_1,
    l2.name AS name_2,

    l1.city AS city_1,
    l2.city AS city_2,

    l1.neighbourhood AS neighbourhood_1,
    l2.neighbourhood AS neighbourhood_2,

    l1.property_type AS property_type_1,
    l2.property_type AS property_type_2,

    l1.room_type AS room_type_1,
    l2.room_type AS room_type_2,

    l1.latitude AS latitude_1,
    l2.latitude AS latitude_2,
    l1.longitude AS longitude_1,
    l2.longitude AS longitude_2,

    l1.accommodates AS accommodates_1,
    l2.accommodates AS accommodates_2,

    l1.price AS price_1,
    l2.price AS price_2

FROM repeated_pairs p
LEFT JOIN listings l1
    ON p.listing_id_1 = l1.listing_id
LEFT JOIN listings l2
    ON p.listing_id_2 = l2.listing_id
ORDER BY p.shared_review_ids DESC
"""

results = con.execute(pairs_query).fetchall()
columns = [description[0] for description in con.description]

print("REPEATED REVIEW LISTING COMPARISON")
print("=" * 75)
print(f"Listing pairs identified: {len(results)}")

# Summarise similarities across all pairs
summary_query = """
WITH repeated_pairs AS (
    SELECT
        LEAST(a.listing_id, b.listing_id) AS id_1,
        GREATEST(a.listing_id, b.listing_id) AS id_2
    FROM reviews a
    JOIN reviews b
        ON a.review_id = b.review_id
       AND a.listing_id < b.listing_id
    GROUP BY 1, 2
),
comparisons AS (
    SELECT
        l1.host_id IS NOT DISTINCT FROM l2.host_id
            AND l1.host_id IS NOT NULL AS same_host,

        l1.city IS NOT DISTINCT FROM l2.city
            AND l1.city IS NOT NULL AS same_city,

        l1.neighbourhood IS NOT DISTINCT FROM l2.neighbourhood
            AND l1.neighbourhood IS NOT NULL AS same_neighbourhood,

        l1.property_type IS NOT DISTINCT FROM l2.property_type
            AND l1.property_type IS NOT NULL AS same_property_type,

        l1.room_type IS NOT DISTINCT FROM l2.room_type
            AND l1.room_type IS NOT NULL AS same_room_type,

        l1.latitude = l2.latitude
            AND l1.longitude = l2.longitude
            AND l1.latitude IS NOT NULL
            AND l1.longitude IS NOT NULL AS same_coordinates

    FROM repeated_pairs p
    JOIN listings l1 ON p.id_1 = l1.listing_id
    JOIN listings l2 ON p.id_2 = l2.listing_id
)
SELECT
    COUNT(*) AS total_pairs,
    COUNT(*) FILTER (WHERE same_host) AS same_host,
    COUNT(*) FILTER (WHERE same_city) AS same_city,
    COUNT(*) FILTER (WHERE same_neighbourhood) AS same_neighbourhood,
    COUNT(*) FILTER (WHERE same_property_type) AS same_property_type,
    COUNT(*) FILTER (WHERE same_room_type) AS same_room_type,
    COUNT(*) FILTER (WHERE same_coordinates) AS same_coordinates
FROM comparisons
"""

summary = con.execute(summary_query).fetchone()

print("\nPAIR SIMILARITY SUMMARY")
print("-" * 75)

labels = [
    "Total listing pairs",
    "Pairs with the same host",
    "Pairs with the same city",
    "Pairs with the same neighbourhood",
    "Pairs with the same property type",
    "Pairs with the same room type",
    "Pairs with identical coordinates",
]

for label, value in zip(labels, summary):
    print(f"{label}: {value:,}")

# Display detailed comparison
print("\nDETAILED LISTING COMPARISON")
print("-" * 75)

for row in results:
    record = dict(zip(columns, row))

    print(f"\nListing pair: {record['listing_id_1']:,} / "
          f"{record['listing_id_2']:,}")
    print(f"Shared review IDs: {record['shared_review_ids']}")
    print(f"Host IDs: {record['host_1']} / {record['host_2']}")
    print(f"Names: {record['name_1']} / {record['name_2']}")
    print(f"Cities: {record['city_1']} / {record['city_2']}")
    print(f"Neighbourhoods: {record['neighbourhood_1']} / "
          f"{record['neighbourhood_2']}")
    print(f"Property types: {record['property_type_1']} / "
          f"{record['property_type_2']}")
    print(f"Room types: {record['room_type_1']} / "
          f"{record['room_type_2']}")
    print(f"Coordinates: ({record['latitude_1']}, "
          f"{record['longitude_1']}) / "
          f"({record['latitude_2']}, {record['longitude_2']})")
    print(f"Accommodates: {record['accommodates_1']} / "
          f"{record['accommodates_2']}")
    print(f"Prices: {record['price_1']} / {record['price_2']}")

print("\nCOMPARISON COMPLETED")

con.close()
