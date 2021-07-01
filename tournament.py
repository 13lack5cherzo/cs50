# Simulate a sports tournament

import os
import csv
import sys
import pandas as pd
import random

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    # Read teams into memory from file
    teams_df = pd.read_csv(os.getcwd() + "/" + sys.argv[1])
    # create dict
    teams_d = dict(zip(teams_df["team"].values, teams_df["rating"].values))
    # list of dict
    teams = [{"team":key1, "rating":teams_d[key1]} for key1 in teams_d.keys()]

    counts = {key1:0 for key1 in teams_d.keys()}
    # Simulate N tournaments and keep track of win counts
    for tournament1 in range(0, N):
        tournament_winner = simulate_tournament(teams)[0]["team"] # get winner
        counts[tournament_winner] = counts[tournament_winner] + 1 # add win

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    win_team = teams.copy()
    # simulate till only 1 winner is left
    while len(win_team) != 1:
        win_team = simulate_round(win_team)
    return win_team


if __name__ == "__main__":
    main()
