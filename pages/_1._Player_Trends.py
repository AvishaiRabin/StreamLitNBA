import streamlit as st
import altair as alt
import pandas as pd
import regex as re

from basketball_data.players import (
    get_players,
    get_player_career_stats,
    compare_season_stats,
    get_player_seasons,
    get_player_teams
)

st.markdown("# Player Trend Visualizer")
st.sidebar.markdown("# Player Trend Visualizer :chart:")

st.write("Select a player")

all_players = get_players()

col1, col2 = st.columns(2)


with col1:

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
with col2:
    stats_map = {
        "PTS": "Points",
        "REB": "Rebounds",
        "OREB": "Offensive Rebounds",
        "DREB": "Defensive Rebounds",
        "AST": "Assists",
        "STL": "Steals",
        "BLK": "Blocks",
        "PF": "Personal Fouls",
        "TOV": "Turnovers",
        "FGM": "Field Goals Made",
        "FGA": "Field Goals Attempted",
        "FG_PCT": "Field Goal Percent",
        "FG3M": "3 Pointers Made",
        "FG3A": "3 Pointers Attempted",
        "FG3_PCT": "3 Point Shooting Percent",
        "FTM": "Free Throws Made",
        "FTA": "Free Throws Attempted",
        "FT_PCT": "Free Throw Percent",
    }

    stat = st.radio("Stat to Analyze:", stats_map.keys())


if player_name != "Select a player...":
    player_id = all_players[all_players["full_name"] == player_name]["id"].iloc[0]
    # player_stats = get_player_career_stats(player_id)
    season_list = get_player_seasons(player_id)

    season_compare_tbl = compare_season_stats(
        player_name, season_list, stat, per_mode, season_type
    )

    hover = alt.selection_point(
        name="hover", fields=["Season"], nearest=True, on="mouseover", clear="mouseout"
    )


    stat_df_long = season_compare_tbl.melt(
        id_vars="Season", var_name="Percentile", value_name=stats_map[stat]
    )
    stat_df_long["Player"] = player_name

    legend_order = season_compare_tbl.columns.tolist()[::-1]

    # Add hover selection
    hover = alt.selection_single(
        fields=["Season"], nearest=True, on="mouseover", empty="none", clear="mouseout"
    )

    tooltip = [
        alt.Tooltip("Player:N", title="Player"),
        alt.Tooltip("Season:O", title="Season"),
        alt.Tooltip("Percentile:N", title="Percentile"),
        alt.Tooltip(f"{stats_map[stat]}:Q", title=stats_map[stat], format=".1f"),
    ]

    color_scale = alt.Scale(domain=legend_order)  # explicitly set domain

    color = alt.Color(
        "Percentile:N",
        title="Percentile",
        scale=color_scale,
        sort=legend_order,  # sort here helps too, but domain is key
    )

    line = (
        alt.Chart(stat_df_long)
        .mark_line()
        .encode(
            x=alt.X("Season:O", title="Season"),
            y=alt.Y(
                f"{stats_map[stat]}:Q",
                title=f"{stats_map[stat]} {re.sub('Per', 'Per ', per_mode)}",
            ),
            color=color,
            tooltip=tooltip,
        )
    )

    selectors = (
        alt.Chart(stat_df_long)
        .mark_rule(opacity=0)
        .encode(
            x="Season:O",
            tooltip=tooltip,  # ✅ full tooltip here

        )
        .add_params(hover)
    )

    chart = (
        alt.Chart(stat_df_long)
        .mark_circle(size=70)
        .encode(
            x="Season:O",
            y=f"{stats_map[stat]}:Q",
            color=color,
            tooltip=tooltip,  # this now shows everything
        )
    )

    shape = alt.Shape(
        "Percentile:N",
        scale=alt.Scale(domain=["Best in the League"], range=["diamond"]),
        legend=None,  # hide extra legend if desired
    )

    chart = chart.encode(shape=shape)

    text = (
        alt.Chart(stat_df_long)
        .mark_text(align="left", dx=5, dy=-5)
        .encode(
            x="Season:O",
            y=f"{stats_map[stat]}:Q",
            text=alt.Text(f"{stats_map[stat]}:Q", format=".1f"),
            color=color,
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

    chart = alt.layer(line, selectors, chart, rule, text).properties(
        width=1000,
        height=500,
        title=f"Percentiles of {stats_map[stat]} {re.sub('Per', 'Per ', per_mode)} by Season",
    )

    st.altair_chart(chart, use_container_width=True)
