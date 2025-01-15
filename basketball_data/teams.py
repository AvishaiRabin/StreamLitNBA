import streamlit as st
import pandas as pd

from nba_api.stats.endpoints import TeamGameLog, teamestimatedmetrics, leaguestandingsv3, teamestimatedmetrics
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.static import teams

@st.cache_data
def get_standings(year):
    """
    Query's a given season's standings (defaults to the current one)
    """
    standings = leaguestandingsv3.LeagueStandingsV3(season=year).get_data_frames()[0]

    standings = standings[['TeamName', 'Conference', 'PlayoffRank', 'Division', 'Record', 'L10', 'ConferenceGamesBack']]

    return standings

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
def get_team_metrics(season):
    """
    Query's a given season's team ratings.  E.g. returns a list of teams and their OFFRTG, DEFTG, NETRTG, etc
    """
    season = season[:5] + season[7:]
    tbl = teamestimatedmetrics.TeamEstimatedMetrics(league_id='00', season=season).get_data_frames()[0]

    tbl = tbl[['TEAM_NAME', 'E_OFF_RATING', 'E_DEF_RATING', 'E_NET_RATING', 'E_PACE', 'E_AST_RATIO', 'E_OREB_PCT_RANK',
         'E_DREB_PCT_RANK', 'E_REB_PCT_RANK', 'E_TM_TOV_PCT_RANK']]

    tbl.columns = [
        'Team', 'Offensive Rating', 'Defensive Rating', 'Net Rating', 'Pace Rating', 'Assist to Turnover Ratio',
        'Offensive Rebound Ranking', 'Defensive Rebound Ranking', 'Rebound Ranking', 'Turnovers Ranking'
    ]

    # tbl = pd.merge(tbl, teams, on='TEAM_ID')

    return tbl