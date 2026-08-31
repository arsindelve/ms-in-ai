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

def start():
    print_menu()

def print_menu():
        print(f'''Welcome to the Bookmark Manager:
    (1) Add a bookmark
    (2) Statistics
    (3) View bookmarks
    (4) Exit Program
    ''')

if __name__ == '__main__':
    start()


