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
    operation_map[int(choice)]()
    prompt_for_action_and_execute()

def add_bookmark():
    title = input("Enter the title of the bookmark: ")
    url = input("Enter the URL of the bookmark: ")
    category = input("Enter the category of the bookmark: ")
    bookmark = Bookmark(title, url, category)
    print(f"Bookmark '{title}' added successfully!")

def view_bookmarks():
    print("Viewing bookmarks...")

def statistics():
    print("Statistics...")

operation_map = {
    1: add_bookmark,
    2: statistics,
    3: view_bookmarks,
    4: exit
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


