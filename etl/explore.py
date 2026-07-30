import json
from pathlib import Path

DATA_PATH = Path("data/raw/lpl")

# Get the first JSON file
json_file = next(DATA_PATH.glob("*.json"))

with open(json_file, "r", encoding="utf-8") as f:
    match = json.load(f)

print("=" * 60)
print("Top Level Keys")
print("=" * 60)

print(match.keys())

print("\n")

print("=" * 60)
print("Info Keys")
print("=" * 60)

print(match["info"].keys())

print("\n")

print("=" * 60)
print("First Innings Keys")
print("=" * 60)

print(match["innings"][0].keys())

print("\n")

print("=" * 60)
print("First Over Keys")
print("=" * 60)

print(match["innings"][0]["overs"][0].keys())

print("\n")

print("=" * 60)
print("First Delivery")
print("=" * 60)

print(match["innings"][0]["overs"][0]["deliveries"][0])