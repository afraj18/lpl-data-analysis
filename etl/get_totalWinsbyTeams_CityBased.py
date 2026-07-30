from pathlib import Path
import json
import pandas as pd
from collections import defaultdict


DATA_PATH = Path("data/raw/lpl")
MAPPING_PATH = Path("data/reference/team_mapping.csv")


def load_team_mapping(mapping_path: Path) -> dict:
    """
    Load team name mapping from CSV file.
    """
    team_mapping = pd.read_csv(mapping_path)

    return dict(
        zip(
            team_mapping["original_name"],
            team_mapping["city_name"]
        )
    )


def get_match_files(data_path: Path):
    """
    Get all JSON match files.
    """
    return sorted(data_path.glob("*.json"))


def load_match(file_path: Path) -> dict:
    """
    Load a single JSON match file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_winner(match: dict):
    """
    Extract winner team from match JSON.
    """
    return (
        match
        .get("info", {})
        .get("outcome", {})
        .get("winner")
    )


def normalize_team_name(team_name: str, team_map: dict) -> str:
    """
    Convert historical team names into common franchise names.
    """
    return team_map.get(team_name, team_name)


def calculate_team_wins(files, team_map):
    """
    Calculate total wins per team.
    """
    wins_by_team = defaultdict(int)

    for file in files:

        match = load_match(file)

        winner = extract_winner(match)

        if winner:
            normalized_team = normalize_team_name(
                winner,
                team_map
            )

            wins_by_team[normalized_team] += 1

    return wins_by_team


def create_wins_dataframe(wins_by_team):
    """
    Convert dictionary into sorted dataframe.
    """
    return (
        pd.DataFrame(
            wins_by_team.items(),
            columns=["Team", "Wins"]
        )
        .sort_values(
            "Wins",
            ascending=False
        )
        .reset_index(drop=True)
    )


def main():

    team_map = load_team_mapping(MAPPING_PATH)

    match_files = get_match_files(DATA_PATH)

    wins = calculate_team_wins(
        match_files,
        team_map
    )

    df = create_wins_dataframe(wins)

    print(df)


if __name__ == "__main__":
    main()