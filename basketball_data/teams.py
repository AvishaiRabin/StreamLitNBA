import streamlit as st
import pandas as pd

from nba_api.stats.endpoints import (
    TeamGameLog,
    teamestimatedmetrics,
    leaguestandingsv3,
    teamestimatedmetrics,
    LeagueDashTeamStats,
    CommonTeamRoster

)
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.static import teams


@st.cache_data
def get_standings(year):
    """
    Query's a given season's standings (defaults to the current one)
    """
    standings = leaguestandingsv3.LeagueStandingsV3(season=year).get_data_frames()[0]

    standings = standings[
        [
            "TeamName",
            "Conference",
            "PlayoffRank",
            "Division",
            "Record",
            "L10",
            "ConferenceGamesBack",
        ]
    ]

    return standings


@st.cache_data
def get_teams():
    return pd.DataFrame(teams.get_teams())

@st.cache_data
def get_team_roster(team_name: str, season: str = '2024-25'):
    """ Takes as input a team name and returns all players who played for that team in a given season"""
    teams = get_teams()
    team_id = teams[teams['full_name'] == team_name]['id'].iloc[0]

    # Query the CommonTeamRoster endpoint
    ctro = CommonTeamRoster(
        team_id=team_id,
        league_id_nullable='00',
        season='2024-25'
    )

    roster = ctro.get_data_frames()[0]

    return roster



@st.cache_data
def get_team_stats(season, game_type):
    """
    Fetches team stat rankings by year.
    Includes:",PTS",REB",AST",STL",FG_PCT",FT_PCT",FG3_PCT",BLK

    Args:
        year
        game_type

    Returns:
        list[pd.DataFrame]: list of DataFrames for each metric
    """
    season = season[:5] + season[7:]

    team_stats = LeagueDashTeamStats(
        season=season,
        per_mode_detailed="PerGame",
        season_type_all_star=game_type,
    )

    df = team_stats.get_data_frames()[0]

    df = df[df['TEAM_ID'].isin(get_teams()['id'])]

    df = df[
        [
            "TEAM_NAME",
            "W",
            "L",
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
    ]


    return df


@st.cache_data
def get_team_logs_by_year(year=2024):
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

    for team_id in teams_df["id"]:
        team_log = TeamGameLog(team_id, season=year).get_data_frames()[0]
        # Merge team game log with teams DataFrame
        team_log = pd.merge(team_log, teams_df, left_on="Team_ID", right_on="id")
        final_teams_data = pd.concat([final_teams_data, team_log], ignore_index=True)

    final_teams_data["season"] = year

    final_teams_data = final_teams_data[final_teams_data["WL"].notnull()]

    return final_teams_data


@st.cache_data
def get_team_metrics(season):
    """
    Query's a given season's team ratings.  E.g. returns a list of teams and their OFFRTG, DEFTG, NETRTG, etc
    """
    season = season[:5] + season[7:]
    tbl = teamestimatedmetrics.TeamEstimatedMetrics(
        league_id="00", season=season
    ).get_data_frames()[0]

    tbl = tbl[
        [
            "TEAM_NAME",
            "E_OFF_RATING",
            "E_DEF_RATING",
            "E_NET_RATING",
            "E_PACE",
            "E_AST_RATIO",
            "E_OREB_PCT_RANK",
            "E_DREB_PCT_RANK",
            "E_REB_PCT_RANK",
            "E_TM_TOV_PCT_RANK",
        ]
    ]

    tbl.columns = [
        "Team",
        "Offensive Rating",
        "Defensive Rating",
        "Net Rating",
        "Pace Rating",
        "Assist to Turnover Ratio",
        "Offensive Rebound Ranking",
        "Defensive Rebound Ranking",
        "Rebound Ranking",
        "Turnovers Ranking",
    ]

    # tbl = pd.merge(tbl, teams, on='TEAM_ID')

    return tbl


@st.cache_data
def get_team_logos():
    """
    Get all team logos
    """
    team_logos = {
        "Atlanta Hawks": "https://cdn.nba.com/logos/nba/1610612737/primary/L/logo.svg",
        "Boston Celtics": "https://cdn.nba.com/logos/nba/1610612738/primary/L/logo.svg",
        "Brooklyn Nets": "https://cdn.nba.com/logos/nba/1610612751/primary/L/logo.svg",
        "Charlotte Hornets": "https://cdn.nba.com/logos/nba/1610612766/primary/L/logo.svg",
        "Chicago Bulls": "https://cdn.nba.com/logos/nba/1610612741/primary/L/logo.svg",
        "Cleveland Cavaliers": "https://cdn.nba.com/logos/nba/1610612739/primary/L/logo.svg",
        "Dallas Mavericks": "https://cdn.nba.com/logos/nba/1610612742/primary/L/logo.svg",
        "Denver Nuggets": "https://cdn.nba.com/logos/nba/1610612743/primary/L/logo.svg",
        "Detroit Pistons": "https://cdn.nba.com/logos/nba/1610612765/primary/L/logo.svg",
        "Golden State Warriors": "https://cdn.nba.com/logos/nba/1610612744/primary/L/logo.svg",
        "Houston Rockets": "https://cdn.nba.com/logos/nba/1610612745/primary/L/logo.svg",
        "Indiana Pacers": "https://cdn.nba.com/logos/nba/1610612754/primary/L/logo.svg",
        "Los Angeles Clippers": "https://cdn.nba.com/logos/nba/1610612746/primary/L/logo.svg",
        "Los Angeles Lakers": "https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg",
        "Memphis Grizzlies": "https://cdn.nba.com/logos/nba/1610612763/primary/L/logo.svg",
        "Miami Heat": "https://cdn.nba.com/logos/nba/1610612748/primary/L/logo.svg",
        "Milwaukee Bucks": "https://cdn.nba.com/logos/nba/1610612749/primary/L/logo.svg",
        "Minnesota Timberwolves": "https://cdn.nba.com/logos/nba/1610612750/primary/L/logo.svg",
        "New Orleans Pelicans": "https://cdn.nba.com/logos/nba/1610612740/primary/L/logo.svg",
        "New York Knicks": "https://cdn.nba.com/logos/nba/1610612752/primary/L/logo.svg",
        "Oklahoma City Thunder": "https://cdn.nba.com/logos/nba/1610612760/primary/L/logo.svg",
        "Orlando Magic": "https://cdn.nba.com/logos/nba/1610612753/primary/L/logo.svg",
        "Philadelphia 76ers": "https://cdn.nba.com/logos/nba/1610612755/primary/L/logo.svg",
        "Phoenix Suns": "https://cdn.nba.com/logos/nba/1610612756/primary/L/logo.svg",
        "Portland Trail Blazers": "https://cdn.nba.com/logos/nba/1610612757/primary/L/logo.svg",
        "Sacramento Kings": "https://cdn.nba.com/logos/nba/1610612758/primary/L/logo.svg",
        "San Antonio Spurs": "https://cdn.nba.com/logos/nba/1610612759/primary/L/logo.svg",
        "Toronto Raptors": "https://cdn.nba.com/logos/nba/1610612761/primary/L/logo.svg",
        "Utah Jazz": "https://cdn.nba.com/logos/nba/1610612762/primary/L/logo.svg",
        "Washington Wizards": "https://cdn.nba.com/logos/nba/1610612764/primary/L/logo.svg",
    }

    return team_logos
