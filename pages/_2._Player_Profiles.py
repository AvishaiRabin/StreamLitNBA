import streamlit as st
import pandas as pd
import regex as re

from basketball_data.players import (
    get_players,
    get_player_career_stats,
    compare_season_stats,
    get_player_teams,
)

from basketball_data.teams import get_teams, get_team_roster

st.markdown("# Player Profiler")
st.sidebar.markdown("# Player Profiler")

st.write("Select a team and/or player")

# Retrieve teams and players
teams = get_teams()
all_players = get_players()

# Display team option
teams = ["All Teams"] + teams['full_name'].tolist()
team_name = st.selectbox("Select a team", teams)
# Display player option
if team_name != "All Teams":
    team_players = get_team_roster(team_name)
    players = ["Select a player..."] + team_players["PLAYER"].tolist()
    player_name = st.selectbox("Select a player", players)

else:
    players = ["Select a player..."] + all_players["full_name"].tolist()
    player_name = st.selectbox("Select a player", players)

if player_name != "Select a player...":
    player_id = all_players[all_players['full_name']==player_name]['id']
    player_teams = get_player_teams(player_id, '2024-25')['TEAM_ABBREVIATION'].unique()
    
    st.radio('Player Team:',player_teams)


