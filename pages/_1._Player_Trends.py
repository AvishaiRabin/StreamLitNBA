import streamlit as st
import altair as alt
import pandas as pd
import regex as re

from basketball_data.players import (
    get_players,
    get_player_career_stats,
    compare_season_stats,
    get_player_seasons,
)

st.markdown("# Player Trend Visualizer")
st.sidebar.markdown("# Player Trend Visualizer :chart:")

st.write("Select a player")

all_players = get_players()

players = ["Select a player..."] + all_players["full_name"].tolist()
player_name = st.selectbox("Select", players)

season_type = st.radio("Game Mode:", ["Regular Season", "Playoffs"])

per_mode = st.radio(
    "Per Mode",
    [
        "PerGame",
        "PerMinute",
        "Per36",
        "Per46",
        "Per100Plays",
        "Per100Possessions",
        "PerPlay",
        "PerPossession",
        "Totals",
    ],
)

stats = [
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
    "PF",
    "PTS",
]

if player_name != "Select a player...":
    player_id = all_players[all_players["full_name"] == player_name]["id"].iloc[0]
    # player_stats = get_player_career_stats(player_id)
    season_list = get_player_seasons(player_id)

    season_compare_tbl = compare_season_stats(
        player_name, season_list, "PTS", per_mode, season_type
    )

    hover = alt.selection_point(
        name="hover", fields=["Season"], nearest=True, on="mouseover", clear="mouseout"
    )

    stat_df_long = season_compare_tbl.melt(
        id_vars="Season", var_name="Percentile", value_name="Points"
    )

    # Add hover selection
    hover = alt.selection_single(
        fields=["Season"], nearest=True, on="mouseover", empty="none", clear="mouseout"
    )
    line = (
        alt.Chart(stat_df_long)
        .mark_line()
        .encode(
            x=alt.X("Season:O", title="Season"),
            y=alt.Y("Points:Q", title=f"Points {re.sub('Per', 'Per ', per_mode)}"),
            color=alt.Color("Percentile:N", title="Percentile"),
        )
    )

    selectors = (
        alt.Chart(stat_df_long)
        .mark_rule(opacity=0)
        .encode(
            x="Season:O",
        )
        .add_params(hover)
    )

    points = (
        alt.Chart(stat_df_long)
        .mark_circle()
        .encode(x="Season:O", y="Points:Q", color="Percentile:N")
        .transform_filter(hover)
    )

    text = (
        alt.Chart(stat_df_long)
        .mark_text(align="left", dx=5, dy=-5)
        .encode(
            x="Season:O",
            y="Points:Q",
            text=alt.Text("Points:Q", format=".1f"),
            color="Percentile:N",
        )
        .transform_filter(hover)
    )

    rule = (
        alt.Chart(stat_df_long)
        .mark_rule(color="gray")
        .encode(
            x="Season:O",
        )
        .transform_filter(hover)
    )

    chart = alt.layer(line, selectors, points, rule, text).properties(
        width=700, height=400, title="Percentiles of Points Per Game by Season"
    )

    st.altair_chart(chart, use_container_width=True)
