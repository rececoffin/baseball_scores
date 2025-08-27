import statsapi
from datetime import date
import argparse

import statsapi
from datetime import date
import argparse

def print_detailed_game_info(game_data):
    game_info = game_data.get('gameData', {})
    live_data = game_data.get('liveData', {})

    # Game Info
    away_team = game_info.get('teams', {}).get('away', {}).get('name', 'N/A')
    home_team = game_info.get('teams', {}).get('home', {}).get('name', 'N/A')
    date_time = game_info.get('datetime', {}).get('dateTime', 'N/A')
    venue = game_info.get('venue', {}).get('name', 'N/A')
    weather = game_info.get('weather', {}).get('condition', 'N/A')

    print(f"""{away_team} vs. {home_team}"""
          f"Date: {date_time}"
          f"Venue: {venue}"
          f"Weather: {weather}")

    # Linescore
    linescore = live_data.get('linescore', {})
    innings = linescore.get('innings', [])
    away_runs = linescore.get('teams', {}).get('away', {}).get('runs', 0)
    home_runs = linescore.get('teams', {}).get('home', {}).get('runs', 0)

    print("\nLinescore:")
    header = "\t".join([str(i + 1) for i in range(len(innings))])
    print(f"Team\t{header}\tT")
    away_line = "\t".join([str(inning.get('away', {}).get('runs', '')) for inning in innings])
    print(f"{away_team[:3].upper()}\t{away_line}\t{away_runs}")
    home_line = "\t".join([str(inning.get('home', {}).get('runs', '')) for inning in innings])
    print(f"{home_team[:3].upper()}\t{home_line}\t{home_runs}")

    # Current Play
    current_play = live_data.get('plays', {}).get('currentPlay')
    if current_play:
        pitcher = current_play['matchup']['pitcher']['fullName']
        batter = current_play['matchup']['batter']['fullName']
        count = current_play['count']
        last_play = current_play.get('result', {}).get('description', 'N/A')

        print("\nCurrent Play:")
        print(f"\tPitcher: {pitcher}")
        print(f"\tBatter: {batter}")
        print(f"\tCount: {count['balls']} Balls, {count['strikes']} Strikes, {count['outs']} Outs")
        print(f"\tLast Play: {last_play}")

    # Box Score
    boxscore = live_data.get('boxscore', {})
    away_batters = boxscore.get('teams', {}).get('away', {}).get('batters', [])
    home_batters = boxscore.get('teams', {}).get('home', {}).get('batters', [])

    print("\nBox Score:")
    print(f"\n{away_team}")
    print("Player\t\tAB\tR\tH\tRBI\tK")
    for player_id in away_batters:
        player_data = boxscore.get('teams', {}).get('away', {}).get('players', {}).get(f'ID{player_id}', {})
        if player_data:
            stats = player_data.get('stats', {}).get('batting', {})
            name = player_data.get('person', {}).get('fullName', 'N/A')
            print(f"{name.ljust(15)}\t{stats.get('atBats', 0)}\t{stats.get('runs', 0)}\t{stats.get('hits', 0)}\t{stats.get('rbi', 0)}\t{stats.get('strikeOuts', 0)}")

    print(f"\n{home_team}")
    print("Player\t\tAB\tR\tH\tRBI\tK")
    for player_id in home_batters:
        player_data = boxscore.get('teams', {}).get('home', {}).get('players', {}).get(f'ID{player_id}', {})
        if player_data:
            stats = player_data.get('stats', {}).get('batting', {})
            name = player_data.get('person', {}).get('fullName', 'N/A')
            print(f"{name.ljust(15)}\t{stats.get('atBats', 0)}\t{stats.get('runs', 0)}\t{stats.get('hits', 0)}\t{stats.get('rbi', 0)}\t{stats.get('strikeOuts', 0)}")

def get_scores(team_name=None):
    if team_name:
        try:
            team_id = statsapi.lookup_team(team_name)[0]['id']
        except IndexError:
            print(f"Could not find team: {team_name}")
            return

    today = date.today().strftime("%m/%d/%Y")
    scores = statsapi.schedule(date=today)

    game_found = False
    for game in scores:
        if game['status'] in ['Final', 'Game Over', 'In Progress']:
            if team_name and not (team_name.lower() in game['away_name'].lower() or team_name.lower() in game['home_name'].lower()):
                continue
            
            game_found = True
            gamePk = game['game_id']
            game_data = statsapi.get('game', {'gamePk': gamePk})

            if team_name:
                print_detailed_game_info(game_data)
                return

            live_data = game_data.get('liveData', {})
            linescore = live_data.get('linescore', {})
            inning_info = ""
            if linescore.get('currentInning'):
                inning_half = linescore.get('inningHalf', '')
                inning_ordinal = linescore.get('currentInningOrdinal', '')
                inning_info = f"{inning_half.capitalize()} {inning_ordinal} inning"

            current_play = live_data.get('plays', {}).get('currentPlay')

            batter = "N/A"
            pitcher = "N/A"

            if current_play and 'matchup' in current_play:
                batter = current_play['matchup']['batter']['fullName']
                pitcher = current_play['matchup']['pitcher']['fullName']

            print(
                f"{game['away_name']} ({game['away_score']}) @ "
                f"{game['home_name']} ({game['home_score']}) - "
                f"{game['status']} {inning_info}"
                f"\n\tPitcher: {pitcher}"
                f"\n\tBatter: {batter}"
            )

    if team_name and not game_found:
        next_game_id = statsapi.next_game(team_id)
        if next_game_id:
            next_game_data = statsapi.get('game', {'gamePk': next_game_id})
            game_info = next_game_data.get('gameData', {})
            away_team = game_info.get('teams', {}).get('away', {}).get('name', 'N/A')
            home_team = game_info.get('teams', {}).get('home', {}).get('name', 'N/A')
            date_time = game_info.get('datetime', {}).get('dateTime', 'N/A')
            venue = game_info.get('venue', {}).get('name', 'N/A')
            print(f"No active game for {team_name}. Next game is on {date_time} at {venue} vs the {away_team if home_team == team_name else home_team}")
        else:
            print(f"No active or upcoming games found for {team_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get MLB scores.')
    parser.add_argument('--team', type=str, help='The name of the team to get the score for.')
    args = parser.parse_args()

    get_scores(args.team)
