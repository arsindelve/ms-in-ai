# CSCI 513.01W – Python Programming for AI**
# Student: Michael Lane
# Assignment 2

from enum import Enum

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

def add_bookmark():
    title = input("Enter the title of the bookmark: ")
    url = input("Enter the URL of the bookmark: ")
    category_raw = input("Enter category, 1 for Wishlist, 2 for Work, 3 for Playlist, 4 for Miscellaneous: ")

    try:
        category = int(category_raw)
    except ValueError:
        print("Invalid input: Please enter a valid number.")
        return

    if category in {member.value for member in Category}:
        bookmark = Bookmark(title, url, category)
        bookmarks[Category(category).value].append(bookmark)
        return
    else:
        print("No such category.")

    bookmark = Bookmark(title, url, category)
    bookmarks[Category(category).value].append(bookmark)
    print(f"Bookmark '{title}' added successfully!")

def view_bookmarks():
    print("Viewing bookmarks...")

def statistics():
    print("We have:\n")
    for category in bookmarks:
        print(f"{Category(category).name}: {len(bookmarks[category])}")
    print("\n")

operation_map = {
    1: add_bookmark,
    2: statistics,
    3: view_bookmarks,
    4: exit
}

bookmarks = {
    1: [],
    2: [],
    3: [],
    4: []
}

def print_menu():
        print(f'''Welcome to the Bookmark Manager:
    (1) Add a bookmark
    (2) Statistics
    (3) View bookmarks
    (4) Exit Program
    ''')

if __name__ == '__main__':
    prompt_for_action_and_execute()


