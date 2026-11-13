
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = PROJECT_DIR / "data" / "raw" / "Listings.csv"

print("TARGETED ENCODING VERIFICATION")
print("=" * 55)

target = b"A\x81lvaro Obregon"

total_invalid_bytes = 0
target_occurrences = 0
other_occurrences = 0
affected_lines = 0

with open(FILE_PATH, "rb") as file:
    for line_number, raw_line in enumerate(file, start=1):

        byte_count = raw_line.count(b"\x81")

        if byte_count:
            affected_lines += 1
            total_invalid_bytes += byte_count

            target_count = raw_line.count(target)
            target_occurrences += target_count

            if target_count != byte_count:
                other_occurrences += byte_count - target_count
                print(f"\nOther occurrence on line {line_number}:")
                print(raw_line[:250])

print("\n" + "=" * 55)
print(f"Lines affected: {affected_lines}")
print(f"Total 0x81 bytes: {total_invalid_bytes}")
print(f"Occurrences in target text: {target_occurrences}")
print(f"Other occurrences: {other_occurrences}")

if total_invalid_bytes == target_occurrences:
    print("\nRESULT: All invalid bytes belong to the same target text.")
else:
    print("\nRESULT: Additional investigation is required.")
