# MLB Scores

This project is a Python script that scrapes mlb.com for MLB scores and outputs them to the command line.

## Installation

1.  Clone the repository.
2.  Create a virtual environment:
    ```
    python3 -m venv venv
    ```
3.  Activate the virtual environment:
    ```
    source venv/bin/activate
    ```
4.  Install the dependencies:
    ```
    pip3 install -r requirements.txt
    ```

## Usage

To get all the scores for the current day, run the script without any arguments:

```
python3 get_scores.py
```

To get the score for a specific team, use the `--team` flag:

```
python3 get_scores.py --team "Team Name"
```

For example:

```
python3 get_scores.py --team "Yankees"
```

This will provide a detailed box score for the specified team's game, including game info, linescore, current play, and box score.
