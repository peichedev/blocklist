import os
import json
import re

BLOCKLIST_FOLDER = "."  # current folder
OUTPUT_FILE = "adblock.custom.feeds"

# Find all files matching blockList_XX.txt
files = []
pattern = re.compile(r"blockList_(\d+)\.txt")
for f in os.listdir(BLOCKLIST_FOLDER):
    match = pattern.match(f)
    if match:
        files.append((int(match.group(1)), f))

# Sort by the number
files.sort()

feeds = {}

for i, (_, filename) in enumerate(files, start=1):
    key = f"source_{i}"
    feeds[key] = {
        "url": f"https://raw.githubusercontent.com/peichedev/blocklist/main/{filename}",
        "rule": r"/^0\.0\.0\.0[[:space:]]+(([[:alnum:]_-]{1,63}\.)+[[:alpha:]]+)$/ {print tolower($2)}",
        "size": "S",
        "descr": f"source {i}"
    }

# Write JSON to file
with open(OUTPUT_FILE, "w") as f:
    json.dump(feeds, f, indent=4)

print(f"{OUTPUT_FILE} created with {len(feeds)} sources!")
