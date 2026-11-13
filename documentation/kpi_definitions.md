# Airbnb Market Intelligence

## KPI Definitions and Calculations

### Overview

This document explains how each KPI in the Airbnb Market Intelligence dashboard is defined and calculated, and how to read the results. All figures come from the Listings and Reviews datasets, which I prepared in DuckDB before loading into Power BI.

### 1. Market Overview

| KPI | Definition | Calculation |
| --- | --- | --- |
| Total Listings | Number of unique listings | Distinct count of `listing_id` |
| Average Price | Average listing price in the selected data | Average of `price` |
| Average Rating | Average overall guest rating | Average of `review_scores_rating`, excluding missing values |
| Total Reviews | Number of review records across listings | Sum of `review_count` |

**Note:** There is no currency field, so compare prices within a city, not across cities. Ratings are listing-level scores, not ratings for individual reviews.

### 2. Pricing and Accommodation

| KPI | Definition | Calculation |
| --- | --- | --- |
| Average Price by Room Type | Average price for each accommodation type | Average `price` grouped by `room_type` |
| Average Price by Capacity | Average price by number of guests accommodated | Average `price` grouped by `accommodates` |
| Median Listing Price | Middle price when listings are sorted by price | Median of `price`, where available |
| Average Capacity | Average number of guests a listing sleeps | Average of `accommodates` |

**Note:** As above, compare prices within the selected city.

### 3. Host Performance

| KPI | Definition | Calculation |
| --- | --- | --- |
| Total Hosts | Number of unique hosts | Distinct count of `host_id` |
| Superhost Listings | Listings managed by superhosts | Distinct count of `listing_id` where `host_is_superhost` is True |
| Average Host Listing Count | Average number of listings per host, across listing records | Average of `host_listing_count` |
| Instant Bookable Listings | Listings that allow instant booking | Distinct count of `listing_id` where `instant_bookable` is True |
| Listings by Host Portfolio Size | Listings grouped by how many listings their host manages | Distinct count of `listing_id` grouped by `host_listing_count` |

**Note:** Average host listing count is calculated across listing records, so hosts with bigger portfolios count for more. It is not an equal-weighted average across unique hosts.

### 4. Guest Experience

| KPI | Definition | Calculation |
| --- | --- | --- |
| Total Reviews | Number of review records | Sum of listing-level `review_count` |
| Average Guest Rating | Average overall listing rating | Average of `review_scores_rating`, excluding missing values |
| Listings with Reviews | Listings with at least one review | Distinct count of `listing_id` where `review_count` > 0 |
| Listings without Reviews | Listings with no reviews | Distinct count of `listing_id` where `review_count` = 0 |
| Monthly Review Volume | Reviews recorded each month | Count of review records grouped by month of `date` |
| Average Rating by City | Average listing rating per city | Average of `review_scores_rating` grouped by city, excluding missing values |

### 5. Validation Reference

Use these figures to check the dashboard against the source data.

| Metric | Expected Value |
| --- | ---: |
| Total Listings | 279,712 |
| Total Review Records | 5,373,143 |
| Listings with Reviews | 193,556 |
| Listings without Reviews | 86,156 |
| Duplicate Listing IDs | 0 |
| Unmatched Review Listing IDs | 0 |

Listings with and without reviews should add up to the total: 193,556 + 86,156 = 279,712

### 6. Notes and Limitations

- Missing review scores are excluded from average ratings, not treated as zero.
- Without currency data, cross-city price comparisons can mislead.
- Total reviews come from review records, not the number of listings.
- A listing with no reviews is not necessarily a weak one.
- Superhost listings count listings, not unique superhosts.
- Average host listing count is weighted by listings, not by hosts.
- There is no booking, occupancy or revenue data, so the dashboard can't measure actual earnings.

### Conclusion

These definitions give a consistent way to read the dashboard. They also make the calculations transparent and easy to check, which helps avoid misleading conclusions about listings, prices, hosts and guest reviews.
