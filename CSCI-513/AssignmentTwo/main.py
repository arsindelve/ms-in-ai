# CSCI 513.01W – Python Programming for AI**
# Student: Michael Lane
# Assignment 2
from pygments.unistring import xid_continue


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
    if category in {member for member in category_map}:
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

    with open(filename_map[category], "a") as file:
        # Write text to the file (this adds it to the end)
        file.write(f"{title} {url}\n")


def view_bookmarks():
    category = get_category_from_user()
    if category is None:
        return
    with open(filename_map[category], "r") as file:
        lines = file.readlines()
        for line in lines:
            title, url = line.strip().split(" ")
            print(f"{title} {url}")
    print()


def statistics():
    print("We have:\n")
    for category in category_map:
        with open(filename_map[category], "r") as file:
            lines = len(file.readlines())
            print(f"{lines} {category_map[category]}")
    print()

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

category_map = {
    1: "Wishlist",
    2: "Work",
    3: "Playlist",
    4: "Miscellaneous"
}

def initialize():
    # Clean up and reset after any recent runs.
    for filename in filename_map.values():
        try:
            with open(filename, "w"):
                pass  # No content written — file is created empty
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


