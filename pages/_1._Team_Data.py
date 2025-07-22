import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import TeamGameLog
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import teamestimatedmetrics
from nba_api.stats.static import teams

from basketball_data.teams import *

st.markdown("# Team Data")
st.sidebar.markdown("# Team Data ❄️")


# Function to highlight the first row
def highlight_first_row(row):
    return ['background-color: yellow' if row.name == 1 else '' for _ in row]

year_range = list(range(1970, 2025))
str_year_range = [f'{i}-{i+1}' for i in year_range]
season = st.selectbox('View team data by year', str_year_range, index=str_year_range.index(max(str_year_range[:-1])))
year = int(season[:4])
# Team log logic
metric = st.radio('Pick one:', ['None', 'Standings','Metrics'])

if metric == 'Standings':

    standings = get_standings(year)

    col1, col2 = st.columns(2)
    col1.write('West')
    col2.write('East')

    with col1:
        west_standings = standings[standings['Conference']=='West'].reset_index(drop=True)
        west_standings.index = range(1, len(west_standings)+1)
        st.dataframe(west_standings[['TeamName', 'Record']].style.apply(highlight_first_row, axis=1))

    with col2:
        east_standings = standings[standings['Conference']=='East'].reset_index(drop=True)
        east_standings.index = range(1, len(east_standings)+1)
        st.dataframe(east_standings[['TeamName', 'Record']])

elif metric == 'Metrics':
    df = get_team_metrics(season)
    st.dataframe(df)

#
# @st.cache_data
# def get_league_stats():
#     conn = get_db_connection('team_logs')
#     league_stats = conn.execute('SELECT W, W + L as Games_Played, nickname FROM team_logs',
#                                ).fetchall()
#     league_data = []
#     for row in league_stats:
#         league_data.append({
#             'Wins': row[0],
#             'Games': row[1],
#             'Team': row[2]
#             # Add more columns as needed
#         })
#     conn.close()
#     return league_data

