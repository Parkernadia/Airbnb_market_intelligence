# Airbnb Market Intelligence

An exploratory data analytics project looking at Airbnb listings, pricing, host activity and guest reviews across the cities in the dataset.

## Overview

This project analyzes Airbnb listing and review data to understand the short-term rental market: how listings are spread across cities, how prices vary by room type and capacity, how hosts manage their listings and how guests review properties.

I used Python and DuckDB to inspect, validate and prepare the data, SQL for querying and aggregation, and Power BI for the interactive dashboard.

## Business Questions

1. How are listings distributed across cities?
2. Which accommodation types make up the largest share of listings?
3. How do prices vary by room type and capacity?
4. How does host activity vary with the number of listings a host manages?
5. What share of listings are managed by superhosts?
6. How many listings have reviews, and how does review activity change over time?
7. How do average guest ratings differ across cities?

## Tools

| Tool | Purpose |
| --- | --- |
| Python, Pandas | Data inspection, validation, preparation and analysis |
| DuckDB | Processing large datasets and running analytical queries |
| SQL | Querying and aggregation |
| Power BI, Power Query, DAX | Dashboard, data import and calculations |
| Git, GitHub, VS Code | Version control and development |

## Data

| Dataset | Records | Columns |
| --- | ---: | ---: |
| Listings | 279,712 | 33 |
| Reviews | 5,373,143 | 4 |

Listings covers properties, hosts, prices, accommodation types and guest ratings. Reviews holds review IDs, listing IDs, reviewer IDs and review dates. The two are linked by `listing_id`.

## Workflow

1. **Inspect:** Checked the structure, columns, record counts and data types.
2. **Assess quality:** Looked at missing values, duplicate IDs, links between datasets and encoding.
3. **Prepare:** Made a UTF-8 copy of Listings and kept the original raw file.
4. **Load:** Put both datasets into DuckDB for validation and analysis.
5. **Explore:** Used SQL to look at listing distribution, pricing, hosts and reviews.
6. **Export:** Produced analysis-ready tables for Power BI.
7. **Build:** Created a four-page interactive dashboard.
8. **Document:** Wrote up the data quality findings, KPI definitions and limitations.

## Dashboard

| Page | Focus |
| --- | --- |
| Market Overview | Listing distribution, average price, average rating, review volume |
| Pricing & Accommodation | Prices by room type and capacity |
| Host Performance | Host portfolios, superhost listings, instant booking |
| Guest Experience | Review activity, ratings, listings with and without reviews |

## Key Findings

- Listings has 279,712 records across the cities represented.
- With no currency field, prices should only be compared within a city.
- 193,556 listings have reviews and 86,156 have none.
- 91,405 listings have no overall rating.
- 160 review IDs appear twice, each tied to two different listings but the same reviewer and date.

Read these alongside the data quality notes below.

## Repository Structure

```text
Airbnb_market_intelligence/
│
├── data/
│   ├── raw/
│   │   ├── Listings.csv
│   │   ├── Listings_data_dictionary.csv
│   │   ├── Reviews.csv
│   │   └── Reviews_data_dictionary.csv
│   └── processed/
│       ├── Listings_utf8.csv
│       ├── airbnb.duckdb
│       └── powerbi_exports/
│           ├── city_summary.csv
│           ├── listings_analysis.csv
│           └── monthly_review_trends.csv
│
├── documentation/
│   └── kpi_definitions.md
│
├── notebooks/
│   └── 01_data_inspection.ipynb
│
├── powerbi/
│   ├── dashboard/
│   │   └── Airbnb_Market_Intelligence.pbix
│   └── screenshots/
│       ├── 01_market_overview.png
│       ├── 02_pricing_accommodation.png
│       ├── 03_host_performance.png
│       └── 04_guest_experience.png
│
├── reports/
│   ├── data_quality_report.md
│   └── executive_summary.md
│
├── scripts/
│   ├── 01_inspect_data.py
│   ├── 02_check_encoding.py
│   ├── 03_create_utf8_copy.py
│   ├── 04_validate_listings.py
│   ├── 05_check_reviews_encoding.py
│   ├── 06_validate_reviews.py
│   ├── 07_build_duckdb_database.py
│   ├── 08_data_quality_assessment.py
│   ├── 09_investigate_repeated_reviews.py
│   ├── 09_investigate_review_ids.py
│   ├── 10_compare_repeated_review_listings.py
│   └── 11_prepare_powerbi_data.py
│
├── sql/
│
├── .gitignore
├── README.md
├── requirements.txt
└── .venv/
```

## Data Quality and Limitations

- District is missing for most listings.
- Host response information and review scores have many missing values.
- 160 review IDs are repeated.
- The original Listings CSV had invalid UTF-8 characters. I made a UTF-8 copy, and 984 characters that couldn't be decoded were replaced.
- There is no booking, occupancy or revenue data.
- Prices have no currency.
- Reviews have no comments or individual ratings.

I documented these and kept them in mind throughout to avoid unsupported conclusions.

## Documentation

- [`reports/data_quality_report.md`](reports/data_quality_report.md): data quality checks, findings and preparation decisions
- [`reports/executive_summary.md`](reports/executive_summary.md): overview, questions, findings and recommendations
- [`documentation/kpi_definitions.md`](documentation/kpi_definitions.md): KPI definitions and calculations

## Reproducing the Analysis

Create the environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Then run the scripts from the project root in numbered order.

**Note:** Large source and processed data files may need to be generated or restored locally before running the pipeline. If you are starting from a fresh checkout, place the raw CSV files in `data/raw/` and the processed outputs in `data/processed/` before executing the scripts.

## Conclusion

This project walks through a practical analytics workflow: inspecting and validating large datasets, preparing analysis-ready tables and building an interactive Power BI dashboard. It combines data quality checks, SQL analysis and business-focused visuals to explore the Airbnb short-term rental market.
