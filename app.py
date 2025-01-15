import streamlit as st

from basketball_data.scoreboard import get_today_scoreboard

st.markdown("# Welcome to Backboard!")
st.sidebar.markdown("# Main page 🎈")

st.text("A basketball project by Avi Rabin")

st.dataframe(get_today_scoreboard())