# CSCI 513.01W – Python Programming for AI
# Student: Michael Lane
# Assignment 3


def initialize():
    try:
        with open('nba.txt', 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print("Error: The file 'nba.txt' was not found.")
    return None


def get_winning_team(data):
    winning_team = []
    # Skip the first line which is a header
    for lines in data[1:2]:
        line = lines.strip().split('\t')
        team_one = line[0]
        team_one_score = int(line[1])
        team_two = line[2]
        team_two_score = int(line[3])
        if team_one_score > team_two_score:
            winning_team.append(team_one)
        else:
            winning_team.append(team_two)

def go():
    data = initialize()
    if data is not None:
        get_winning_team(data)


if __name__ == '__main__':
    go()
