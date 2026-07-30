import json
from pathlib import Path
from collections import Counter

DATA_PATH = Path("data/raw/lpl")

files = sorted(DATA_PATH.glob("*.json"))

print("=" * 70)
print("LPL DATASET PROFILE")
print("=" * 70)

print(f"Total JSON Files : {len(files)}")

seasons = Counter()
teams = set()
venues = set()
cities = set()
players = set()

matches_without_city = 0
matches_without_winner = 0
super_over_matches = 0

total_innings = 0
total_overs = 0
total_deliveries = 0
total_wickets = 0

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        match = json.load(f)

    info = match["info"]

    # -------------------------
    # Match level
    # -------------------------

    seasons[info.get("season")] += 1

    venues.add(info.get("venue"))

    if "city" in info:
        cities.add(info["city"])
    else:
        matches_without_city += 1

    for team in info.get("teams", []):
        teams.add(team)

    if "outcome" not in info:
        matches_without_winner += 1

    # Registry contains every player in the match
    registry = info.get("registry", {}).get("people", {})

    for player in registry.keys():
        players.add(player)

    # -------------------------
    # Innings level
    # -------------------------

    for innings in match.get("innings", []):

        total_innings += 1

        if innings.get("super_over", False):
            super_over_matches += 1

        for over in innings.get("overs", []):

            total_overs += 1

            deliveries = over.get("deliveries", [])

            total_deliveries += len(deliveries)

            for delivery in deliveries:

                if "wickets" in delivery:
                    total_wickets += len(delivery["wickets"])

            

print()
print("=" * 70)
print("MATCH STATISTICS")
print("=" * 70)

print(f"Matches              : {len(files)}")
print(f"Innings              : {total_innings}")
print(f"Overs                : {total_overs}")
print(f"Deliveries           : {total_deliveries}")
print(f"Wickets              : {total_wickets}")

print()
print("=" * 70)
print("UNIQUE VALUES")
print("=" * 70)

print(f"Seasons              : {len(seasons)}")
print(f"Teams                : {len(teams)}")
print(f"Players              : {len(players)}")
print(f"Venues               : {len(venues)}")
print(f"Cities               : {len(cities)}")

print()
print("=" * 70)
print("SEASONS")
print("=" * 70)

for season, count in sorted(seasons.items()):
    print(f"{season:<10} {count} matches")

print()
print("=" * 70)
print("DATA QUALITY")
print("=" * 70)

print(f"Matches without city     : {matches_without_city}")
print(f"Matches without outcome  : {matches_without_winner}")
print(f"Super Over innings       : {super_over_matches}")

print()
print("=" * 70)
print("TEAMS")
print("=" * 70)

for team in sorted(teams):
    print(team)

print()
print("=" * 70)
print("VENUES")
print("=" * 70)

for venue in sorted(venues):
    print(venue)