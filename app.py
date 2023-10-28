import json
import streamlit as st
import pandas as pd


def provide_raw_data(path):
    with open(file=path, mode="r") as raw_file:
        raw_data = json.load(raw_file)

    raw_data_df = pd.DataFrame(raw_data["games"])

    home_team = st.selectbox(label="Home Team", options=raw_data["teams"], index=0)
    away_team = st.selectbox(label="Away Team", options=raw_data["teams"], index=1)

    with st.expander(label="Raw Data"):
        st.json(raw_data)

    return raw_data_df, home_team, away_team


def provide_derived_data(raw_data_df):
    with st.expander(label="Insights"):
        st.subheader("Home Insights")
        home_stats = raw_data_df.groupby("team")[["points_scored", "points_allowed"]].mean()
        home_stats["team"] = home_stats.index
        home_stats.sort_values("points_scored", ascending=False, inplace=True)
        home_stats.reset_index(drop=True, inplace=True)
        home_stats.index += 1
        st.write(home_stats)

        st.subheader("Away Insights")
        away_stats = raw_data_df.groupby("opponent")[
            ["points_scored", "points_allowed"]
        ].mean()
        away_stats["team"] = away_stats.index
        away_stats.sort_values("points_scored", ascending=False, inplace=True)
        away_stats.reset_index(drop=True, inplace=True)
        away_stats.index += 1
        st.write(away_stats)

    return home_stats, away_stats


def main():
    st.title("NFL-Predictor")

    path = "data/nfl_data.json"

    # Level 1
    raw_data_df, home_team, away_team = provide_raw_data(path=path)

    # Level 2
    home_stats, away_stats = provide_derived_data(raw_data_df=raw_data_df)

    return


if __name__ == "__main__":
    main()