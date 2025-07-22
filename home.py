import streamlit as st

from basketball_data.scoreboard import get_today_scoreboard
from basketball_data.teams import get_team_stats

st.markdown("# Welcome to Backboard!")
st.sidebar.markdown("# Main page 🎈")

st.write("An interactive app to explore NBA data, player trends, and game insights by Avi Rabin")

st.write("Select below to view the top team and player averages by various metrics for the 2024-2025 NBA season")
year = st.select_slider('Choose year', options=[i for i in range(1996, 2025)], value=2024)
metrics = st.multiselect
season_type = st.radio('Pick one:', ['Regular Season','Playoffs'])

st.dataframe(get_team_stats(year, season_type))