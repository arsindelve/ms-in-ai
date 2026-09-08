# CSCI 513.01W – Python Programming for AI
# Student: Michael Lane
# Assignment 3


def read_file():
    try:
        with open('nba.txt', 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print("Error: The file 'nba.txt' was not found.")
    return None


def get_winning_team(data):
    winning_team = []
    # Skip the first line which is a header
    for next_line in data[1:]:
        line = next_line.strip().split('\t')
        team_one, team_one_score = line[0], int(line[1])
        team_two, team_two_score = line[2], int(line[3])
        if team_one_score > team_two_score:
            winning_team.append(team_one)
        else:
            winning_team.append(team_two)
    return winning_team


def count_winning_team(winning_teams):
    team_wins = {}
    for team in winning_teams:
        if team in team_wins:
            team_wins[team] += 1
        else:
            team_wins[team] = 1
    return team_wins


def export_csv(winning_team_counts):
    with open('wins.csv', 'w') as file:
        for team, wins in winning_team_counts.items():
            file.write(f"{team},{wins}\n")


def go():
    data = read_file()
    if data is not None:
        winning_teams = get_winning_team(data)
        winning_team_counts = count_winning_team(winning_teams)
        export_csv(winning_team_counts)
        print("Done")


if __name__ == '__main__':
    go()
