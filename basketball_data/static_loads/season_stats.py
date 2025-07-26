import pandas as pd

from nba_api.stats.endpoints import leaguedashplayerstats

season_stats_df = pd.DataFrame(
    columns=[
        "PLAYER_ID",
        "PLAYER_NAME",
        "NICKNAME",
        "TEAM_ID",
        "TEAM_ABBREVIATION",
        "AGE",
        "GP",
        "W",
        "L",
        "W_PCT",
        "MIN",
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
        "NBA_FANTASY_PTS",
        "DD2",
        "TD3",
        "WNBA_FANTASY_PTS",
        "GP_RANK",
        "W_RANK",
        "L_RANK",
        "W_PCT_RANK",
        "MIN_RANK",
        "FGM_RANK",
        "FGA_RANK",
        "FG_PCT_RANK",
        "FG3M_RANK",
        "FG3A_RANK",
        "FG3_PCT_RANK",
        "FTM_RANK",
        "FTA_RANK",
        "FT_PCT_RANK",
        "OREB_RANK",
        "DREB_RANK",
        "REB_RANK",
        "AST_RANK",
        "TOV_RANK",
        "STL_RANK",
        "BLK_RANK",
        "BLKA_RANK",
        "PF_RANK",
        "PFD_RANK",
        "PTS_RANK",
        "PLUS_MINUS_RANK",
        "NBA_FANTASY_PTS_RANK",
        "DD2_RANK",
        "TD3_RANK",
        "WNBA_FANTASY_PTS_RANK",
        "SEASON",
        "PER_MODE",
        "SEASON_TYPE",
    ]
)


def store_season_stats(
    season_stats_df, season: str, per_mode: str = "PerGame", season_type: str = "Regular Season"
):
    """
    Collects season stats and stores it in a parquet file.

    Args:
        season:  E.g. '2023-24', '2024-25'
        per_mode: E.g. PerGame, Per36, Totals
        season_type: E.g. Regular Season or Playoffs

    """

    league_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed=per_mode,  # or 'Totals', 'Per36', etc.
        season_type_all_star=season_type,
    ).get_data_frames()[0]

    league_stats["SEASON"] = season
    league_stats["PER_MODE"] = per_mode
    league_stats["SEASON_TYPE"] = season_type

    # Get quantiles
    # ppgq = ppg.quantile([0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
    # ppg_df.loc[len(ppg_df)] = [season] + [i for i in ppgq]

    return pd.concat([season_stats_df, league_stats], ignore_index=True)

    # return ppg_df


all_seasons = [f"{year}-{str(year + 1)[2:]}" for year in range(1996, 2025)]
per_modes = [
    "Totals",
    "PerGame",
    "Per36",
    "Per48",
    "PerMinute",
    "PerPossession",
    "PerPlay",
    "Per100Possessions",
    "Per100Plays",
]
season_types = ["Regular Season", "Playoffs"]
store_season_stats(season_stats_df, all_seasons[0], per_modes[0], season_types[0])
