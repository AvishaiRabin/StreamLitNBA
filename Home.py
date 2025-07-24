import streamlit as st
import math
import matplotlib
from basketball_data.scoreboard import get_today_scoreboard
from basketball_data.teams import get_team_stats, get_team_logos

st.markdown("# Welcome to Backboard!")
st.sidebar.markdown("# Main page :basketball:")

st.write(
    ":basketball: An interactive app to explore NBA data, player trends, and game insights by Avi Rabin :basketball:"
)

st.write(
    "Select below to view the top team and player averages by various metrics for the 2024-2025 NBA season"
)
year_range = list(range(1997, 2026))
str_year_range = [f"{i}-{i+1}" for i in year_range]
season = st.selectbox(
    "View team data by year",
    str_year_range,
    index=str_year_range.index(max(str_year_range[:-1])),
)
metrics = st.multiselect
season_type = st.radio("Game Type:", ["Regular Season", "Playoffs"])

team_stats = get_team_stats(season, season_type)
statistics = [
    "FGM",
    "FGA",
    "FG_PCT",
    "FG3M",
    "FG3A",
    "FG3_PCT",
    "FTM",
    "FTA",
    "FT_PCT",
    "OREB",
    "DREB",
    "REB",
    "AST",
    "TOV",
    "STL",
    "BLK",
    "BLKA",
    "PF",
    "PFD",
    "PTS",
    "PLUS_MINUS",
]

# Store selected options
selected = ["TEAM_NAME", "W", "L"]

# Loop through each option and place it in a column
cols_per_row = 6  # show only 4 columns per row
cols = st.columns(cols_per_row)
rows = math.ceil(len(statistics) / cols_per_row)  # determine the number of rows

for i in range(rows):  # for every row
    for j in range(cols_per_row):  # for each column in each row
        idx = (
            i * cols_per_row + j
        )  # grab the ID of the row * number of columns per row + column
        if idx < len(
            statistics
        ):  # as long as we haven't exceeded the number of statistics available
            with cols[j]:
                if st.checkbox(
                    statistics[idx],
                    key=statistics[idx],
                    value=True if i == 0 else False,
                ):
                    selected.append(statistics[idx])

# Collect selected items
team_stats = team_stats[selected]


team_stats = team_stats.rename(columns={"TEAM_NAME": "Team Name"})

team_stats.sort_values(by="W", ascending=False, inplace=True)
team_stats.reset_index(inplace=True, drop=True)
numeric_cols = [i for i in selected if i != "TEAM_NAME"]
team_stats_styled = (
    team_stats.style.background_gradient(
        subset=[i for i in numeric_cols if i != "L"], cmap="YlGn"
    )
    .background_gradient(
        subset=["L"], cmap="YlOrRd"  # Only apply red-yellow to 'L' column
    )
    .format({col: "{:.1f}" for col in numeric_cols})
    .set_table_styles(
        [
            {"selector": "th", "props": [("text-align", "center")]},
            {"selector": "td", "props": [("text-align", "center")]},
        ]
    )
)


st.dataframe(team_stats_styled)

