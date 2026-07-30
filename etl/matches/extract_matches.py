from pathlib import Path
import json
import pandas as pd

DATA_PATH = Path("data/raw/lpl")
OUTPUT_PATH = Path("data/processed/matches.csv")

def get_match_files(path:Path):
    return sorted(path.glob("*.json"))

def loadJson(file):
    with open(file,"r") as f:
        return json.load(f)

def extract_match_data(match):
    info = match["info"]
    meta = match["meta"]
    innings = match["innings"]

    teams = info["teams"]
    outcome = info.get("outcome")
    winner = outcome.get("winner")

    return {
        "date" : info.get("dates"),
        "season": info.get("season"),
        "venue": info.get("venue"),
        "team1": teams[0],
        "team2": teams[1],
        "winner": winner,
        "toss_winner": info.get("toss").get("winner"),
        "toss_decision": info.get("toss").get("decision")
    }


def create_match_data():

    matches = []

    files = get_match_files(DATA_PATH)

    for file in files:
        match = loadJson(file)
        match_data = extract_match_data(match)

        matches.append(match_data);

    return pd.DataFrame(matches)

def main():
    df = create_match_data()
    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    df.head()


if __name__ == "__main__":
    main()

