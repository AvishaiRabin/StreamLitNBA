from nba_api.stats.endpoints import ScoreboardV2
from nba_api.stats.static import teams
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

teams_tbl = pd.DataFrame(teams.get_teams())
teams_map = {teams_tbl['id'][i]: teams_tbl['nickname'][i] for i in range(len(teams_tbl))}

@st.cache_data
def get_today_date(date_diff=0):
    # Get today's date
    today = datetime.today()

    if date_diff:
        today = today + timedelta(days=date_diff)

    # Format the date as 'yyyy-mm-dd'
    formatted_date = today.strftime('%Y-%m-%d')

    return formatted_date


@st.cache_data
def get_game_status(game_date):
    scoreboard = ScoreboardV2(league_id='00', game_date=game_date)
    score_dict = scoreboard.get_dict()['resultSets'][0]

    tbl = pd.DataFrame(score_dict['rowSet'], columns=score_dict['headers'])
    tbl = tbl[['GAME_STATUS_TEXT', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'GAME_ID']]

    tbl['HOME_TEAM_ID'] = tbl['HOME_TEAM_ID'].map(teams_map)
    tbl['VISITOR_TEAM_ID'] = tbl['VISITOR_TEAM_ID'].map(teams_map)

    tbl.columns = ['Game Status', 'Home', 'Away', 'game_id']

    return tbl

from nba_api.live.nba.endpoints import scoreboard
from datetime import timezone
from dateutil import parser
def time_converter(time_str):
    # Get the time as standard
    dt_object = parser.parse(time_str).replace(tzinfo=timezone.utc).astimezone(tz=None)

    # Format datetime object in a more human-readable format
    human_readable_format = dt_object.strftime("%I:%M %p")

    return human_readable_format

@st.cache_data
def get_today_scoreboard():
    """
    Query's a selection of live games / upcoming games.
    """

    board = scoreboard.ScoreBoard()

    todays_scoreboard = pd.DataFrame()

    games = board.games.get_dict()

    for game in games:
        this_game = {
            'start_time': time_converter(game['gameTimeUTC']),
            'game_status_text': game['gameStatusText'],
            'home_team': game['homeTeam']['teamName'],
            'away_team': game['awayTeam']['teamName'],
            'score': f"{game['homeTeam']['score']}-{game['awayTeam']['score']}",
            'home_standings': f"{game['homeTeam']['wins']} - {game['homeTeam']['losses']}",
            'away_standings': f"{game['awayTeam']['wins']} - {game['homeTeam']['losses']}"
        }
        # Append this_game to todays_scoreboard using concat
        todays_scoreboard = pd.concat([todays_scoreboard, pd.DataFrame(this_game, index=[0])], ignore_index=True)

    return todays_scoreboard
