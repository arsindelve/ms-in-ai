# CSCI 513.01W – Python Programming for AI**
# Student: Michael Lane
# Assignment 2

from enum import Enum
import os

class Category(Enum):
    Wishlist = 1
    Work = 2
    Playlist = 3
    Miscellaneous = 4

class Bookmark:
    def __init__(self, title, url, category):
        self.title = title
        self.url = url
        self.category = category

def prompt_for_action_and_execute():
    print_menu()
    choice = input()

    try:
        operation_map[int(choice)]()
    except ValueError:
        print("Invalid input: Please enter a valid number.")
    except KeyError:
        print("No such operation available.")

    prompt_for_action_and_execute()

def get_category_from_user():
    category_raw = input("Enter category, 1 for Wishlist, 2 for Work, 3 for Playlist, 4 for Miscellaneous: ")

    try:
        category = int(category_raw)
    except ValueError:
        print("Invalid input: Please enter a valid number.")
        return None

    if category in {member.value for member in Category}:
        return category
    else:
        print("No such category.")
        return None


def add_bookmark():
    title = input("Enter the title of the bookmark: ")
    url = input("Enter the URL of the bookmark: ")
    category = get_category_from_user()

    if category is None:
        return

    #bookmark = Bookmark(title, url, category)
    #bookmarks[Category(category).value].append(bookmark)
    print(f"Bookmark '{title}' added successfully!")


def view_bookmarks():
    category = get_category_from_user()

    if category is None:
        return

    #for bookmark in bookmarks[category]:
    #    print(f"{bookmark.title} {bookmark.url}")

    print()


def statistics():
    print("We have:\n")
    for filename in filename_map:
        with open(filename_map[filename], "r") as file:
            lines = file.readlines()
            line_count = len(lines)
            category = {member.value: member.name for member in Category}
            print(f"{line_count} {category}")

operation_map = {
    1: add_bookmark,
    2: statistics,
    3: view_bookmarks,
    4: exit
}

filename_map = {
    1: "wishlist.txt",
    2: "work.txt",
    3: "playlist.txt",
    4: "miscellaneous.txt"
}

def initialize():
    # Clean up and reset after any recent runs.
    for filename in filename_map.values():
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass


def print_menu():
        print(f'''Welcome to the Bookmark Manager:
    (1) Add a bookmark
    (2) Statistics
    (3) View bookmarks
    (4) Exit Program
    ''')

if __name__ == '__main__':
    initialize()
    prompt_for_action_and_execute()


