
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
REVIEWS_FILE = PROJECT_DIR / "data" / "raw" / "Reviews.csv"

if not REVIEWS_FILE.exists():
    raise FileNotFoundError(f"Reviews file not found: {REVIEWS_FILE}")

total_lines = 0
invalid_lines = 0
replacement_count = 0
examples = []

with open(REVIEWS_FILE, "rb") as file:
    for line_number, raw_line in enumerate(file, start=1):
        total_lines += 1

        try:
            raw_line.decode("utf-8")
        except UnicodeDecodeError:
            invalid_lines += 1

            decoded_line = raw_line.decode("utf-8", errors="replace")
            replacements = decoded_line.count("\uFFFD")
            replacement_count += replacements

            if len(examples) < 10:
                examples.append((line_number, replacements))

print("REVIEWS ENCODING DIAGNOSTIC")
print("=" * 50)
print(f"File: {REVIEWS_FILE.name}")
print(f"Physical lines scanned: {total_lines:,}")
print(f"Lines with invalid UTF-8: {invalid_lines:,}")
print(f"Replacement characters needed: {replacement_count:,}")

if examples:
    print("\nFirst affected lines:")
    for line_number, replacements in examples:
        print(f"Line {line_number:,}: {replacements} replacement(s)")

if invalid_lines == 0:
    print("\nRESULT: UTF-8 validation PASSED")
else:
    print("\nRESULT: Encoding issues detected; further investigation required.")
