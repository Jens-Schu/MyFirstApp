import json
from io import StringIO
import pandas as pd
from fastapi import FastAPI

PATH = "data/nfl_data.json"

app= FastAPI()

def FileHandler():
    with open(file=PATH, mode="r") as raw_file:
        data = json.load(raw_file)
    return data


@app.get("/level-1/data")
async def get_data():
    return FileHandler()


@app.get("/level-1/teams")
async def get_data():
    data = FileHandler()
    return data["teams"]


@app.get("/level-2/stats")
async def get_stats(team_type:str = "team"):
    raw_data = FileHandler()
    raw_data_df = pd.DataFrame(raw_data["games"])

    stats = raw_data_df.groupby(team_type)[["points_scored", "points_allowed"]].mean()
    stats[team_type] = stats.index
    stats.sort_values("points_scored", ascending=False, inplace=True)
    stats.reset_index(drop=True, inplace=True)
    stats.index += 1  
    return stats.to_json(orient = "index")


@app.get("/level-3/algorithm")
async def algorithm():
    raw_data = FileHandler()
    raw_data_df = pd.DataFrame(raw_data["games"])

    condition_1 = raw_data_df["points_scored"] - raw_data_df["points_allowed"] > 3
    condition_2 = raw_data_df["points_scored"] - raw_data_df["points_allowed"] < 0

    raw_data_df["true wins"] = condition_1 | condition_2
    return raw_data_df.to_json(orient = "index")


@app.get("/level-4/decision_support")
async def get_decision_support(home_team, away_team):
    home_stats = await get_stats(team_type="team")
    away_stats = await get_stats(team_type="opponent")

    home_stats_df = pd.read_json(StringIO(home_stats), orient="index")
    away_stats_df = pd.read_json(StringIO(away_stats), orient="index")

    mean_scores = {
        "home_scoring_mean": home_stats_df[home_stats_df["team"] == home_team]["points_scored"].values[0],
        "away_scoring_mean": away_stats_df[away_stats_df["opponent"] == away_team]["points_scored"].values[0],
        "home_allowed_mean": home_stats_df[home_stats_df["team"] == home_team]["points_allowed"].values[0],
        "away_allowed_mean": away_stats_df[away_stats_df["opponent"] == away_team]["points_allowed"].values[0],
    }

    return mean_scores