import json
from io import StringIO
import requests
import streamlit as st
import pandas as pd

URL = "http://127.0.0.1:8000"
#URL = "http://172.17.0.1:8000"
ENDPOINT_DATA = URL+"/level-1/data"
ENDPOINT_TEAMS = URL+"/level-1/teams"
ENDPOINT_STATS = URL+"/level-2/stats"
ENDPOINT_ALGORITHM = URL+"/level-3/algorithm"
ENDPOINT_DECISION_SUPPORT = URL+"/level-4/decision_support" 
ENDPOINT_AUTOMATED_DECISION = URL+"/level-5/automated_decision"

def provide_raw_data():
    response = requests.get(url=ENDPOINT_DATA)        
    raw_data = response.json()
 
    with st.expander(label="Raw Data"):
        st.json(raw_data)

    return


def provide_derived_data():
    with st.expander(label="Insights"):
        team_types = ["team", "opponent"]

        for team_type in team_types:
            if team_type == "team":
                label = "Home"
            else:
                label = "Away"

            st.subheader(f"{label} Insights")
            
            response = requests.get(url=ENDPOINT_STATS, params={"team_type": team_type})        
            raw_data = response.json()
            df = pd.read_json(StringIO(raw_data), orient = "index")
            st.write(df)

    return


def provide_algorithm():
    with st.expander("Algorithm for Home Advantage"):
        st.markdown(
            """
                    **Heimvorteil sind +3 Punkte im Handicap**  
                    *(Modellierte Annahme)*
                    
                    ---

                    Erklärung:
            
                    Die Schätzung des Heimvorteils in der NFL auf ungefähr 2,5 bis 3 Punkte pro Spiel basiert auf einer Kombination von historischen Daten, Studien und Erfahrungen von Sportanalysten. Es ist wichtig zu beachten, dass dies eine allgemeine Schätzung ist und keine exakte wissenschaftliche Berechnung darstellt. Hier sind einige der Quellen und Grundlagen, auf denen diese Schätzung basiert:

                    - **Historische Daten:** Durch die Analyse von jahrzehntelangen NFL-Spielprotokollen können Sportanalysten Muster erkennen, die darauf hinweisen, dass Teams, die zu Hause spielen, tendenziell bessere Ergebnisse erzielen als bei Auswärtsspielen. Dies kann als Ausgangspunkt für die Schätzung des Heimvorteils dienen.

                    - **Akademische Studien:** Es gibt einige akademische Studien und wissenschaftliche Arbeiten, die den Heimvorteil im Sport, einschließlich der NFL, untersuchen. Diese Studien nutzen statistische Methoden, um den Heimvorteil zu quantifizieren. Obwohl die Ergebnisse variieren können, zeigen viele dieser Studien einen Heimvorteil von etwa 2,5 bis 3 Punkten pro Spiel.

                    - **Erfahrung von Sportanalysten:** Sportexperten und Analysten, die die NFL und andere Sportligen abdecken, bringen ihre Erfahrung und Einsichten in die Schätzung des Heimvorteils ein. Dies kann auf beobachteten Mustern und ihrer Kenntnis der Dynamik von Heim- und Auswärtsspielen basieren.
                    """
        )

        response = requests.get(url=ENDPOINT_ALGORITHM)        
        prepared_data = response.json()
        prepared_data_df = pd.read_json(StringIO(prepared_data), orient = "index")
        st.write(prepared_data_df)

    return


def provide_decision_support(home_team, away_team):
    response = requests.get(ENDPOINT_DECISION_SUPPORT, params=({"home_team": home_team, "away_team": away_team}))
    mean_scores = response.json()

    with st.expander("Metrics for Decision"):
        first_col, second_col = st.columns(2)

        first_col.metric("Home Scoring Mean", mean_scores["home_scoring_mean"])
        second_col.metric("Away Scoring Mean", mean_scores["away_scoring_mean"])

        first_col.metric("Home Allowed Mean", mean_scores["home_allowed_mean"])
        second_col.metric("Away Allowed Mean", mean_scores["away_allowed_mean"])

    return
  

def provide_automated_decision(home_team, away_team): 
    response = requests.get(ENDPOINT_AUTOMATED_DECISION, params=({"home_team": home_team, "away_team": away_team}))
    prediction = response.json()
    
    winner = prediction["winner"]
    spread_pred = prediction["spread_pred"]
    
    with st.expander("Prediction"):
        st.success(f"{winner} wins with a handicap of {spread_pred} points.")
        
    return


def main():
    st.title("NFL-Predictor")

    response = requests.get(url=ENDPOINT_TEAMS)
    teams = response.json()

    home_team = st.selectbox(label = "Home", options = teams, index = 0)
    away_team = st.selectbox(label = "Away", options = teams, index = 1)

    # Level 1
    provide_raw_data()

    # # Level 2
    provide_derived_data()

    # # Level 3
    provide_algorithm()

    # # Level 4
    provide_decision_support(home_team, away_team)

    # # Level 5
    provide_automated_decision(home_team, away_team)
    return


if __name__ == "__main__":
    main()