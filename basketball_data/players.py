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
def get_season_stats(
    season_list: list,
    stat: str,
    per_mode: str = "PerGame",
    season_type: str = "Regular Season",
):
    """
    Collects ntile values of season stats.

    Args:
        season_list: A list of seasons (e.g. ['2023-24', '2024-25'])
        stat: The stat we are examining (e.g. 'PTS')
        per_mode: E.g. PerGame, Per36, Totals
        season_type: E.g. Regular Season or Playoffs

    Returns a DataFrame of season and 0.1, 0.25, 0.5, 0.75, 0.9, max
    """
    ppg_df = pd.DataFrame(
        columns=[
            "Season",
            "10th Percentile",
            "25th Percentile",
            "50th Percentile",
            "75th percentile",
            "90th percentile",
            "Best in the League",
        ]
    )

    for season in season_list:
        # Fetch league-wide player stats for the season
        league_stats = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season,
            per_mode_detailed=per_mode,  # or 'Totals', 'Per36', etc.
            season_type_all_star=season_type,
        ).get_data_frames()[0]

        ppg = league_stats[stat]

        # Get quantiles
        ppgq = ppg.quantile([0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
        ppg_df.loc[len(ppg_df)] = [season] + [i for i in ppgq]

    return ppg_df
