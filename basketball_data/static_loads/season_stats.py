import os
import time
from nba_api.stats.endpoints import leaguedashplayerstats


def store_season_stats(
    season: str, per_mode: str = "PerGame", season_type: str = "Regular Season"
):
    """
    Collects season stats and stores it in a parquet file.

    Args:
        season:  E.g. '2023-24', '2024-25'
        per_mode: E.g. PerGame, Per36, Totals
        season_type: E.g. Regular Season or Playoffs

    """
    print(f"Storing {per_mode} stats for season {season} - {season_type}")

    season_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed=per_mode,  # or 'Totals', 'Per36', etc.
        season_type_all_star=season_type,
    ).get_data_frames()[0]

    season_stats["SEASON"] = season
    season_stats["PER_MODE"] = per_mode
    season_stats["SEASON_TYPE"] = season_type

    file_path = (
        f"../../static/data/seasons/players/{season}/{season_type}/{per_mode}.parquet"
    )

    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # create if it doesn't exist
    season_stats.to_parquet(file_path, index=False)

    return True


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

for season in all_seasons:
    for per_mode in per_modes:
        for season_type in season_types:
            store_season_stats(season, per_mode, season_type)
