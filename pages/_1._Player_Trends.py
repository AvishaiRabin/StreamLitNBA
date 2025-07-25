import streamlit as st
import altair as alt
import pandas as pd

from basketball_data.players import get_players, get_player_career_stats, get_season_stats

st.markdown("# Player Trend Visualizer")
st.sidebar.markdown("# Player Trend Visualizer :chart:")

st.write("Select a player")

all_players = get_players()

players = ['Select a player...'] + all_players['full_name'].tolist()
player_name = st.selectbox('Select', players)

if player_name != 'Select a player...':
    player_id = all_players[all_players['full_name'] == player_name]['id'].iloc[0]
    player_stats = get_player_career_stats(player_id)

    # Prepare data
    player_stats = player_stats.rename(columns={'SEASON_ID': 'Season', 'PTS': 'Points'})

    ppg_df = get_season_stats(player_stats['Season'].unique(), 'PTS')

    ppg_df[player_name] = round(player_stats['Points'] / player_stats['GP'], 2)

    hover = alt.selection_point(
        name="hover",
        fields=["Season"],
        nearest=True,
        on="mouseover",
        clear="mouseout"
    )

    ppg_df_long = ppg_df.melt(
        id_vars='Season',
        var_name='Percentile',
        value_name='Points'
    )

    # Add hover selection
    hover = alt.selection_single(
        fields=["Season"],
        nearest=True,
        on="mouseover",
        empty="none",
        clear="mouseout"
    )

    line = alt.Chart(ppg_df_long).mark_line().encode(
        x=alt.X('Season:O', title='Season'),
        y=alt.Y('Points:Q', title='Points Per Game'),
        color=alt.Color('Percentile:N', title='Percentile')
    )

    selectors = alt.Chart(ppg_df_long).mark_rule(opacity=0).encode(
        x='Season:O',
    ).add_params(hover)

    points = alt.Chart(ppg_df_long).mark_circle().encode(
        x='Season:O',
        y='Points:Q',
        color='Percentile:N'
    ).transform_filter(hover)

    text = alt.Chart(ppg_df_long).mark_text(align='left', dx=5, dy=-5).encode(
        x='Season:O',
        y='Points:Q',
        text=alt.Text('Points:Q', format=".1f"),
        color='Percentile:N'
    ).transform_filter(hover)

    rule = alt.Chart(ppg_df_long).mark_rule(color='gray').encode(
        x='Season:O',
    ).transform_filter(hover)

    chart = alt.layer(line, selectors, points, rule, text).properties(
        width=700,
        height=400,
        title="Percentiles of Points Per Game by Season"
    )

    st.altair_chart(chart, use_container_width=True)
