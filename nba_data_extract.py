import pandas as pd
import time
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder

# 1. Get all NBA teams
nba_teams = teams.get_teams()

last_30_games_all_teams = []

for team in nba_teams:
    # 2. Search for games for a specific team
    # Specify the season and season type (Regular Season)
    gamefinder = leaguegamefinder.LeagueGameFinder(
        team_id_nullable=team['id'],
        season_nullable='2025-26',
        season_type_nullable='Regular Season'
    )

    # 3. Get as a DataFrame
    games = gamefinder.get_data_frames()[0]

    # 4. Sort by date amd take the last 30 games
    games['GAME_DATE'] = pd.to_datetime(games['GAME_DATE'])
    recent_30 = games.sort_values(by='GAME_DATE', ascending=False).head(30)

    last_30_games_all_teams.append(recent_30)

    # Sleep to avoid hitting API rate limits
    time.sleep(0.5)

# Combine into one master DataFrame
final_df = pd.concat(last_30_games_all_teams, ignore_index=True)
print(final_df.head())
final_df.to_csv('nba_last_30_games.csv', index=False)
