
from pathlib import Path

# Locate the project and its files
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = PROJECT_DIR / "data" / "raw" / "Listings.csv"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "Listings_utf8.csv"

# Check that the original file exists
if not RAW_FILE.exists():
    raise FileNotFoundError(f"Original file not found: {RAW_FILE}")

# Create the processed folder if necessary
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Avoid accidentally overwriting an existing output
if OUTPUT_FILE.exists():
    raise FileExistsError(
        f"Output already exists: {OUTPUT_FILE}\n"
        "Rename or remove it before running this script."
    )

line_count = 0
replacement_count = 0

# Read the original as bytes and write a UTF-8-compatible copy
with open(RAW_FILE, "rb") as source, open(OUTPUT_FILE, "wb") as target:
    for raw_line in source:
        line_count += 1

        decoded_line = raw_line.decode("utf-8", errors="replace")
        replacement_count += decoded_line.count("\uFFFD")

        target.write(decoded_line.encode("utf-8"))

# Validate that the new file can be decoded strictly as UTF-8
validation_lines = 0

with open(OUTPUT_FILE, "rb") as processed_file:
    for raw_line in processed_file:
        raw_line.decode("utf-8")
        validation_lines += 1

# Display results
print("UTF-8 COPY CREATED")
print("=" * 50)
print(f"Original file: {RAW_FILE}")
print(f"Processed file: {OUTPUT_FILE}")
print(f"Physical lines processed: {line_count:,}")
print(f"Replacement characters inserted: {replacement_count:,}")
print(f"Validation lines checked: {validation_lines:,}")
print(f"Processed file size: {OUTPUT_FILE.stat().st_size:,} bytes")
print("Strict UTF-8 validation: PASSED")
