# Airbnb Market Intelligence

## Data Quality Assessment

### Overview

Before analyzing anything, I checked how reliable and complete the two datasets were: Listings (279,712 rows, 33 columns) and Reviews (5,373,143 rows, 4 columns). I loaded both into DuckDB, and all expected columns were present with no records lost.

### Missing Values

Listings has gaps in several important fields:

| Field | Missing |
| --- | ---: |
| District | 242,700 |
| Host response time / rate | 128,782 |
| Host acceptance rate | 113,087 |
| Review scores (rating and sub-scores) | About 91,400–91,800 each |
| Bedrooms | 29,435 |
| Host location | 832 |
| Listing name | 171 |
| Host registration date | 165 |

Reviews had no missing values in the four fields.

District is missing for most listings, so I can't rely on it for neighborhood-level analysis. I left missing review scores blank rather than setting them to zero, since "no rating" is not the same as a score of zero. I didn't impute anything, to avoid adding assumptions that could skew the results.

### Duplicate IDs

Every listing ID is unique. In Reviews, 160 review IDs appear twice (320 rows). Each pair is tied to two different listings, with the same reviewer and the same date. The combination of `listing_id` and `review_id` is unique, so I used that as the key. I kept these rows because the data doesn't explain the cause, and deleting them could remove valid reviews.

### Listings and Reviews

All reviews match an existing listing. 193,556 listings have reviews and 86,156 don't. That isn't necessarily an error, since some properties may be new or never reviewed, so I treated "no reviews" as a real characteristic of the data.

### Encoding

The Listings CSV failed to load in DuckDB because of invalid UTF-8 bytes (for example, `0x81`), mostly in multilingual names and location text. I converted it to a clean UTF-8 copy and kept the original untouched. The conversion went through all 279,713 lines, including the header, and replaced 984 characters that couldn't be decoded. The file now loads, but those characters are lost, so some multilingual listing names are slightly off. Reviews needed no conversion.

### Limitations

1. There is no currency field, so prices should only be compared within a city, not across cities.
2. There is no booking, occupancy or revenue data, so prices are not earnings.
3. Reviews have no text or individual ratings, only IDs and dates.
4. Missing district and host response data limit neighborhood and responsiveness analysis.
5. The cause of the repeated review IDs is unresolved.
6. The encoding fix left replacement characters in some listing text.

### Conclusion

Both datasets are usable. The main issues are the missing values, the repeated review IDs and the encoding problem. I've documented these limits so the dashboard findings can be read with them in mind.
