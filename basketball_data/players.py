from nba_api.stats.static import players

import pandas as pd

import streamlit as st


@st.cache_data
def get_players(active=True):
    """ Retrieves all players (active or inactive) """
    if active:
        return pd.DataFrame(players.get_active_players())
    return pd.DataFrame(players.get_inactive_players())