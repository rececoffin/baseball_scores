import statsapi
from datetime import date
import argparse

def get_scores(team_name=None):
    today = date.today().strftime("%m/%d/%Y")
    scores = statsapi.schedule(date=today)

    for game in scores:
        if game['status'] in ['Final', 'Game Over', 'In Progress']:
            if team_name and not (team_name.lower() in game['away_name'].lower() or team_name.lower() in game['home_name'].lower()):
                continue

            gamePk = game['game_id']
            game_data = statsapi.get('game', {'gamePk': gamePk})
            live_data = game_data.get('liveData', {})
            current_play = live_data.get('plays', {}).get('currentPlay')

            batter = "N/A"
            pitcher = "N/A"

            if current_play and 'matchup' in current_play:
                batter = current_play['matchup']['batter']['fullName']
                pitcher = current_play['matchup']['pitcher']['fullName']

            print(
                f"{game['away_name']} ({game['away_score']}) @ "
                f"{game['home_name']} ({game['home_score']}) - "
                f"{game['status']}"
                f"\n\tPitcher: {pitcher}"
                f"\n\tBatter: {batter}"
            )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get MLB scores.')
    parser.add_argument('--team', type=str, help='The name of the team to get the score for.')
    args = parser.parse_args()

    get_scores(args.team)
