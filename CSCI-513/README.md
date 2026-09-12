# CSCI 513.01W — Python Programming for AI

**East Texas A&M University** · Fall 2026 · Web-based
**Instructor:** Dr. Omar El Ariss

An introduction to Python as the working language of artificial intelligence. The first
half covers the language itself — data types, control flow, functions, lists and
dictionaries, file I/O, and object-oriented programming. The second half turns to the AI
toolchain: NumPy, Pandas, data cleaning and preprocessing, basic machine learning
algorithms, web scraping, and applied AI problems.

Full details, grading breakdown, and the week-by-week outline are in the
[syllabus](Syllabus.pdf).

## Assignments

| # | Topic | What it does |
| --- | --- | --- |
| [2](AssignmentTwo) | Strings, conditionals, loops, files | A menu-driven bookmark manager that saves links to per-category text files |
| [3](AssignmentThree) | Dictionaries, file I/O | Reads a season of NBA box scores and writes each team's win count to a CSV |

### Assignment 2 — Bookmark Manager

[`assignment2.py`](AssignmentTwo/assignment2.py) loops on a four-option menu: add a
bookmark, show statistics, view bookmarks, or exit. Each bookmark is a title and a URL
filed under one of four categories — Wishlist, Work, Playlist, Miscellaneous — and
appended to that category's `.txt` file, so entries survive across runs. The statistics
view counts only what was added during the current session.

The folder also carries [`test_main.py`](AssignmentTwo/test_main.py), a black-box pytest
suite that drives the program as a user would — piping keystrokes to a subprocess in a
throwaway directory — rather than importing anything from it. It covers the menu, each
category's file, append-versus-overwrite behavior, session-scoped statistics, and
recovery from invalid input.

### Assignment 3 — NBA Wins

[`assignment3.py`](AssignmentThree/assignment3.py) reads
[`nba.txt`](AssignmentThree/nba.txt), a tab-separated file of 439 games listing both
teams, their scores, and attendance. It compares the scores to find each game's winner,
tallies wins into a dictionary, and writes `wins.csv` with one `team,wins` line per team.
