from pathlib import Path
import json
import pandas as pd


DATA_PATH = Path("data/raw/lpl")
OUTPUT_PATH = Path("data/processed/innings.csv")

def load_json(file):

    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_innings_score(innings,match_id):
    total_runs = 0
    wicket = 0
    balls = 0

    for over in innings["overs"]:
        for delivery in over["deliveries"]:    

            # count total runs 
            total_runs += delivery["runs"].get("total")
            extras = delivery.get("extras",{})
            # count balls 
            if "wides" not in extras and "noballs" not in extras:
                balls += 1
                

            # count wickets 
            if "wickets" in delivery:
                wicket +=1
    overs = f"{balls // 6}.{balls % 6}"
    return total_runs,wicket,overs

def extract_innings(match,match_id):
    info = match["info"]
    teams = info["teams"]
    date = info["dates"][0]
    season = info.get("season")

    result = []

    for index, innings in enumerate(match["innings"]):
        batting_team = innings["team"]
        bowling_team = (
            teams[1] if teams[0] == batting_team else teams[0]
        )

        runs,wickets,overs = calculate_innings_score(innings,match_id)

        result.append({
            "match_id" : match_id,
            "date" : date,
            "season" : season,
            "innings_number": index + 1,
            "batting_team" : batting_team,
            "bowling_team" : bowling_team,
            "runs" : runs,
            "wickets" : wickets,
            "overs" : overs
        })
    return result

def main():
    files = DATA_PATH.glob("*.json")
    all_innings = []

    for file in files:
        match = load_json(file)
        match_id = file.stem

        innings = extract_innings(match,match_id)
        all_innings.extend(innings)

    df = pd.DataFrame(all_innings)
    df.to_csv(OUTPUT_PATH,index=False)

    print(df.head(10))





if __name__ == "__main__":
    main()


                    