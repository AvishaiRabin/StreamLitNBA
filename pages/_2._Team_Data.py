import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import TeamGameLog
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import leaguestandingsv3, teamestimatedmetrics
from nba_api.stats.static import teams

st.markdown("# Team Data")
st.sidebar.markdown("# Team Data ❄️")

@st.cache_data
def get_teams():
    return pd.DataFrame(teams.get_teams())

@st.cache_data
def get_team_logs_by_year(year=2023):
    """
    Fetches team game logs for the specified year (or all available years) and returns a DataFrame.

    Args:
        year (int, optional): The year for which to fetch game logs. Defaults to None (all available years).

    Returns:
        pd.DataFrame: DataFrame containing team game logs.
    """
    # Call the function to fetch all teams
    teams_df = get_teams()
    final_teams_data = pd.DataFrame()

    for team_id in teams_df['id']:

        team_log = TeamGameLog(team_id, season=year).get_data_frames()[0]
        # Merge team game log with teams DataFrame
        team_log = pd.merge(team_log, teams_df, left_on='Team_ID', right_on='id')
        final_teams_data = pd.concat([final_teams_data, team_log], ignore_index=True)

    final_teams_data['season'] = year

    final_teams_data = final_teams_data[final_teams_data['WL'].notnull()]

    return final_teams_data

@st.cache_data
def get_standings(year):
    """
    Query's a given season's standings (defaults to the current one)
    """
    standings = leaguestandingsv3.LeagueStandingsV3(season=year).get_data_frames()[0]

    standings = standings[['TeamName', 'Conference', 'PlayoffRank', 'Division', 'Record', 'L10', 'ConferenceGamesBack']]

    return standings

# Function to highlight the first row
def highlight_first_row(row):
    return ['background-color: yellow' if row.name == 1 else '' for _ in row]


year_range = list(range(1970, 2025))
str_year_range = [f'{i}-{i+1}' for i in year_range]
team_log_year = st.selectbox('View team data by year', str_year_range, index=str_year_range.index(max(str_year_range[:-1])))
team_log_year = int(team_log_year[:4])

standings = get_standings(team_log_year)

col1, col2 = st.columns(2)
col1.write('West')
col2.write('East')

with col1:
    west_standings = standings[standings['Conference']=='West'].reset_index(drop=True)
    west_standings.index = range(1, 16)
    st.dataframe(west_standings[['TeamName', 'Record']].style.apply(highlight_first_row, axis=1))

with col2:
    east_standings = standings[standings['Conference']=='East'].reset_index(drop=True)
    east_standings.index = range(1, 16)
    st.dataframe(east_standings[['TeamName', 'Record']])
# def get_team_logs_by_year(year=2023):
#     """
#     Fetches team game logs for the specified year (or all available years) and returns a DataFrame.
#
#     Args:
#         year (int, optional): The year for which to fetch game logs. Defaults to None (all available years).
#
#     Returns:
#         pd.DataFrame: DataFrame containing team game logs.
#     """
#     # Call the function to fetch all teams
#     teams_df = get_all_teams()
#     final_teams_data = pd.DataFrame()
#
#     for team_id in teams_df['id']:
#
#         team_log = TeamGameLog(team_id, season=year).get_data_frames()[0]
#         # Merge team game log with teams DataFrame
#         team_log = pd.merge(team_log, teams_df, left_on='Team_ID', right_on='id')
#         final_teams_data = pd.concat([final_teams_data, team_log], ignore_index=True)
#
#     final_teams_data['season'] = year
#
#     final_teams_data = final_teams_data[final_teams_data['WL'].notnull()]
#
#     return final_teams_data
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
