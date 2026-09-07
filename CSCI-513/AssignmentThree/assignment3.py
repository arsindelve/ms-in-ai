# CSCI 513.01W – Python Programming for AI
# Student: Michael Lane
# Assignment 3


def initialize():
    try:
        with open('nba.txt', 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print("Error: The file 'nba.txt' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def go():
    data = initialize()
    if data is not None:
        print(data)


if __name__ == '__main__':
    go()

