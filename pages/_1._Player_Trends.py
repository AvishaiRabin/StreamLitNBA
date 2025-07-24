import streamlit as st

from basketball_data.players import get_players

st.markdown("# Player Trend Visualizer")
st.sidebar.markdown("# Player Trend Visualizer :chart:")

st.write("Select a player")
st.selectbox('Select', get_players()['full_name'].tolist())
