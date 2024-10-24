import csv

RESULT_FILE = "results/news-elpais-e2e-8b/locations.csv"

location_types = set()
with open(RESULT_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        location_types.add(row["location_type"])
        other= eval(row["location_other"])
        location_types.add(other.get("type_suggestion"))

for loc in location_types:
    print(loc)