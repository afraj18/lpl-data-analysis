from pathlib import Path

files = list(Path("data/raw/lpl").glob("*.json"))

print(f"Total Matches : {len(files)}")