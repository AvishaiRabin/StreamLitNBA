from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, leaguedashplayerstats

import pandas as pd

import streamlit as st


@st.cache_data
def get_players(active: bool = True):
    """Retrieves all players (active or inactive)"""
    if active:
        return pd.DataFrame(players.get_active_players())
    return pd.DataFrame(players.get_inactive_players())


@st.cache_data
def get_player_seasons(player_id: int):
    """Takes a player ID and returns the seasons they've played"""
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)

    # Get the data as a pandas DataFrame
    career_stats_df = career_stats.get_data_frames()[0]

    season_list = [i for i in career_stats_df["SEASON_ID"].unique()]

    return season_list


@st.cache_data
def get_player_teams(player_id: int, season: str):
    """ Takes a player ID and returns the teams they played on each year """
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0].reset_index()
    career_stats = career_stats[['TEAM_ID', 'TEAM_ABBREVIATION', 'SEASON_ID']]
    career_stats = career_stats[(career_stats['SEASON_ID']==season)&(career_stats['TEAM_ABBREVIATION']!='TOT')]
    return career_stats

@st.cache_data
def get_player_career_stats(player_id: int):
    """Takes a player ID and returns their career states"""
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)

    # Get the data as a pandas DataFrame
    career_stats_df = career_stats.get_data_frames()[0]

    career_stats_df = career_stats_df.reset_index()

    # Remove traded player totals
    career_stats_df = career_stats_df[career_stats_df["TEAM_ABBREVIATION"] != "TOT"]

    agg_dict = {
        "PLAYER_ID": "last",
        "TEAM_ID": "last",
        "TEAM_ABBREVIATION": "last",
        "PLAYER_AGE": "last",
        "GP": "sum",
        "MIN": "sum",
        "FGM": "sum",
        "FGA": "sum",
        "FG_PCT": "mean",
        "FG3M": "sum",
        "FG3A": "sum",
        "FG3_PCT": "mean",
        "FTM": "sum",
        "FTA": "sum",
        "FT_PCT": "mean",
        "OREB": "sum",
        "DREB": "sum",
        "REB": "sum",
        "AST": "sum",
        "STL": "sum",
        "BLK": "sum",
        "TOV": "sum",
        "PF": "sum",
        "PTS": "sum",
    }

    career_stats_df = (
        career_stats_df.drop(["LEAGUE_ID", "GS"], axis=1)
        .groupby("SEASON_ID")
        .agg(agg_dict)
    )

    career_stats_df = career_stats_df.reset_index()

    return career_stats_df


@st.cache_data
def compare_season_stats(
    player_name: str, season_list: list, stat: str, per_mode: str, season_type: str
):
    """
    Collects ntile values of season stats.

    Args:
        player_name: Player name to compare against
        season_list: A list of seasons (e.g. ['2023-24', '2024-25'])
        stat: The stat we are examining (e.g. 'PTS')
        per_mode: E.g. PerGame, Per36, Totals
        season_type: E.g. Regular Season or Playoffs

    Returns a DataFrame of season and 0.1, 0.25, 0.5, 0.75, 0.9, max
    """
    ntile_df = pd.DataFrame(
        columns=[
            "Season",
            "10th Percentile",
            "25th Percentile",
            "50th Percentile",
            "75th percentile",
            "90th percentile",
            "Best in the League",
            player_name,
        ]
    )

    for season in season_list:
        # Fetch league-wide player stats for the season
        league_stats = pd.read_parquet(
            f"static/data/seasons/players/{season}/{season_type}/{per_mode}.parquet"
        )

        # Get player-specific stat first
        player_stat = league_stats[league_stats["PLAYER_NAME"] == player_name][
            stat
        ].iloc[0]

        stat_df = league_stats[stat]

        # Get quantiles
        stat_df_q = stat_df.quantile([0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
        ntile_df.loc[len(ntile_df)] = [season] + [i for i in stat_df_q] + [player_stat]

    return ntile_df
