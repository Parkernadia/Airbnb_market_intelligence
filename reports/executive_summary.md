# Airbnb Market Intelligence

## Executive Summary

### Project Overview

This project looks at Airbnb listing and review data to understand patterns in the short-term rental market across the cities in the dataset. It covers how listings are distributed, how prices vary, which accommodation types dominate, how active hosts are and how guests review properties. I used Python and DuckDB to inspect, validate and prepare the data, and Power BI to build an interactive dashboard.

### Business Questions

1. How are listings distributed across cities?
2. Which accommodation types make up the largest share of listings?
3. How do prices vary by room type and capacity?
4. How does host activity vary with the number of listings a host manages?
5. What share of listings are managed by superhosts?
6. How many listings have reviews, and how does review activity change over time?
7. How do average guest ratings differ across cities?

### Key Findings

**1. The market is large.**

The Listings dataset has 279,712 records, which gives a broad base for looking at how short-term rentals are spread across cities.

**2. Prices only make sense within a city.**

There is no currency field, so comparing prices across cities could be misleading. Price analysis should stay within each city.

**3. Almost a third of listings have no reviews.**

Of the 279,712 listings, 193,556 have reviews and 86,156 don't. That is about 30.8% with no recorded reviews.

**4. Rating data is patchy.**

The review score fields have a lot of gaps. For example, 91,405 listings have no overall rating, which limits how many can be used in rating comparisons.

**5. Repeated review IDs need caution.**

160 review IDs appear twice. Each pair belongs to two different listings but has the same reviewer and date. The combination of listing ID and review ID is still unique, but I couldn't work out the cause from the available fields.

### Recommendations

**1. Compare prices city by city.**

Local currencies differ, so city-level analysis gives a fairer picture of prices and accommodation options.

**2. Fill in the missing listing and host information.**

The gaps in district, host response and review scores limit how deep the analysis can go. More complete data would make market and host performance assessments more reliable.

**3. Check the repeated review IDs against the source.**

Until the cause is clear, use listing ID plus review ID, not review ID alone, to identify a record.

### Methodology and Tools

- **Python:** data inspection, encoding checks, validation and preparation scripts.
- **DuckDB:** processing the large datasets, checking data quality, investigating IDs and exporting analysis-ready tables.
- **SQL:** querying and aggregating listing and review data.
- **Power BI:** building the interactive dashboard.

Listings has 279,712 records and 33 columns. Reviews has 5,373,143 records and 4 columns.

### Limitations

- No booking or occupancy data, so prices are not revenue.
- No currency information for each city's prices.
- No review text or individual review ratings.
- Missing values in some host and listing fields.
- The cause of the repeated review IDs is unresolved.

### Conclusion

The analysis gives an overview of listings, pricing, host activity and guest reviews across the cities in the dataset. It also shows why data quality checks matter before drawing conclusions. Validating the data, investigating the inconsistencies and documenting the limits make the results easier to trust. The Power BI dashboard pulls it all together so the market can be explored and the areas needing a closer look are easier to spot
