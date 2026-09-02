"""Black-box tests for the Assignment 2 bookmark manager.

Put this file beside ``main.py`` and run:

    python -m pytest -q

The tests execute the program exactly as a user would. They do not import or
depend on any functions, classes, or variables inside main.py.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest


PROGRAM = Path(__file__).with_name("assignment2.py")
CATEGORY_FILES = {
    1: "wishlist.txt",
    2: "work.txt",
    3: "playlist.txt",
    4: "miscellaneous.txt",
}


def run_program(tmp_path: Path, *answers: object) -> subprocess.CompletedProcess[str]:
    """Run main.py with simulated keyboard input in an isolated directory."""
    assert PROGRAM.exists(), f"Place main.py beside this test file: {PROGRAM}"
    keyboard_input = "\n".join(str(answer) for answer in answers) + "\n"
    return subprocess.run(
        [sys.executable, str(PROGRAM)],
        input=keyboard_input,
        text=True,
        capture_output=True,
        cwd=tmp_path,
        timeout=5,
        check=False,
    )


def normalize(text: str) -> str:
    """Ignore capitalization and insignificant whitespace in displayed text."""
    return " ".join(text.lower().split())

def saved_lines(path: Path) -> list[str]:
    """Return nonblank bookmark records without their newline characters."""
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def assert_all_category_files_empty(tmp_path: Path) -> None:
    """Allow category files to be absent or pre-created, but require no records."""
    for filename in CATEGORY_FILES.values():
        path = tmp_path / filename
        if path.exists():
            assert saved_lines(path) == []


def assert_finished_normally(result: subprocess.CompletedProcess[str]) -> None:
    assert result.returncode == 0, (
        f"Program exited with status {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )


def assert_stat(output: str, count: int, category: str) -> None:
    assert re.search(rf"\b{count}\s+{category.lower()}\b", normalize(output)), output


def menu_count(output: str) -> int:
    return normalize(output).count("welcome to the bookmark manager")


# Required behavior ---------------------------------------------------------


def test_complete_menu_is_displayed(tmp_path: Path) -> None:
    result = run_program(tmp_path, 4)

    assert_finished_normally(result)
    output = normalize(result.stdout)
    assert "welcome to the bookmark manager" in output
    assert re.search(r"\(1\)\s+add a bookmark", output)
    assert re.search(r"\(2\)\s+statistics", output)
    assert re.search(r"\(3\)\s+view bookmarks", output)
    assert re.search(r"\(4\)\s+exit program", output)


def test_add_operation_displays_all_required_prompts(tmp_path: Path) -> None:
    result = run_program(
        tmp_path,
        1,
        "PromptTitle",
        "https://example.com/prompt",
        1,
        4,
    )

    assert_finished_normally(result)
    output = normalize(result.stdout)
    assert re.search(r"enter[^:]*title", output)
    assert re.search(r"enter[^:]*(?:link|url)", output)
    assert "enter category" in output
    for category in ("wishlist", "work", "playlist", "miscellaneous"):
        assert category in output


def test_exit_option_stops_program_without_saving_bookmarks(tmp_path: Path) -> None:
    result = run_program(tmp_path, 4)

    assert_finished_normally(result)
    assert_all_category_files_empty(tmp_path)


@pytest.mark.parametrize(
    ("category", "expected_filename"), CATEGORY_FILES.items()
)
def test_add_bookmark_saves_to_the_correct_category_file(
    tmp_path: Path, category: int, expected_filename: str
) -> None:
    title = f"Category {category} Bookmark"
    link = f"https://example.com/category-{category}"

    result = run_program(tmp_path, 1, title, link, category, 4)

    assert_finished_normally(result)
    assert saved_lines(tmp_path / expected_filename) == [f"{title} {link}"]
    for other_filename in set(CATEGORY_FILES.values()) - {expected_filename}:
        other_path = tmp_path / other_filename
        if other_path.exists():
            assert saved_lines(other_path) == []


def test_second_bookmark_is_appended_instead_of_replacing_first(
    tmp_path: Path,
) -> None:
    result = run_program(
        tmp_path,
        1,
        "First Bookmark",
        "https://example.com/first",
        2,
        1,
        "Second Bookmark",
        "https://example.com/second",
        2,
        4,
    )

    assert_finished_normally(result)
    assert saved_lines(tmp_path / "work.txt") == [
        "First Bookmark https://example.com/first",
        "Second Bookmark https://example.com/second",
    ]


def test_category_files_remain_separate(tmp_path: Path) -> None:
    result = run_program(
        tmp_path,
        1,
        "Wish Bookmark",
        "https://example.com/wish",
        1,
        1,
        "Playlist Bookmark",
        "https://example.com/song",
        3,
        4,
    )

    assert_finished_normally(result)
    assert saved_lines(tmp_path / "wishlist.txt") == [
        "Wish Bookmark https://example.com/wish"
    ]
    assert saved_lines(tmp_path / "playlist.txt") == [
        "Playlist Bookmark https://example.com/song"
    ]


def test_statistics_count_only_bookmarks_added_during_current_run(
    tmp_path: Path,
) -> None:
    result = run_program(
        tmp_path,
        1,
        "Wish",
        "https://example.com/wish",
        1,
        1,
        "Work One",
        "https://example.com/work-1",
        2,
        1,
        "Work Two",
        "https://example.com/work-2",
        2,
        1,
        "Music",
        "https://example.com/music",
        3,
        2,
        4,
    )

    assert_finished_normally(result)
    assert_stat(result.stdout, 1, "wishlist")
    assert_stat(result.stdout, 2, "work")
    assert_stat(result.stdout, 1, "playlist")
    assert_stat(result.stdout, 0, "miscellaneous")


def test_initial_statistics_are_all_zero(tmp_path: Path) -> None:
    result = run_program(tmp_path, 2, 4)

    assert_finished_normally(result)
    for category in ("wishlist", "work", "playlist", "miscellaneous"):
        assert_stat(result.stdout, 0, category)


def test_view_displays_every_bookmark_in_selected_category(tmp_path: Path) -> None:
    result = run_program(
        tmp_path,
        1,
        "FirstWork",
        "https://example.com/first",
        2,
        1,
        "SecondWork",
        "https://example.com/second",
        2,
        3,
        2,
        4,
    )

    assert_finished_normally(result)
    output = normalize(result.stdout)
    assert "firstwork" in output
    assert "https://example.com/first" in output
    assert "secondwork" in output
    assert "https://example.com/second" in output


@pytest.mark.parametrize(
    ("category", "title"),
    [(1, "WishItem"), (2, "WorkItem"), (3, "SongItem"), (4, "MiscItem")],
)
def test_each_category_can_be_viewed(
    tmp_path: Path, category: int, title: str
) -> None:
    link = f"https://example.com/view-{category}"
    result = run_program(tmp_path, 1, title, link, category, 3, category, 4)

    assert_finished_normally(result)
    assert f"{title.lower()} {link}" in normalize(result.stdout)


def test_bookmark_persists_after_program_restarts(tmp_path: Path) -> None:
    # Bookmark files are persistent: a later execution must still be able to
    # view records saved by an earlier execution.
    first_run = run_program(
        tmp_path,
        1,
        "Persistent",
        "https://example.com/persistent",
        3,
        4,
    )
    second_run = run_program(tmp_path, 3, 3, 4)

    assert_finished_normally(first_run)
    assert_finished_normally(second_run)
    output = normalize(second_run.stdout)
    assert "persistent" in output
    assert "https://example.com/persistent" in output


def test_restart_keeps_bookmarks_but_resets_statistics(tmp_path: Path) -> None:
    first_run = run_program(
        tmp_path,
        1,
        "FirstWork",
        "https://example.com/first-work",
        2,
        4,
    )
    second_run = run_program(
        tmp_path,
        1,
        "SecondWork",
        "https://example.com/second-work",
        2,
        2,
        3,
        2,
        4,
    )

    assert_finished_normally(first_run)
    assert_finished_normally(second_run)
    assert_stat(second_run.stdout, 1, "work")
    output = normalize(second_run.stdout)
    assert "firstwork https://example.com/first-work" in output
    assert "secondwork https://example.com/second-work" in output
    assert saved_lines(tmp_path / "work.txt") == [
        "FirstWork https://example.com/first-work",
        "SecondWork https://example.com/second-work",
    ]


def test_statistics_reset_after_program_restarts(tmp_path: Path) -> None:
    # Statistics are session-only even though the bookmark files persist.
    first_run = run_program(
        tmp_path,
        1,
        "Old Work Bookmark",
        "https://example.com/old",
        2,
        4,
    )
    second_run = run_program(tmp_path, 2, 4)

    assert_finished_normally(first_run)
    assert_finished_normally(second_run)
    for category in ("wishlist", "work", "playlist", "miscellaneous"):
        assert_stat(second_run.stdout, 0, category)


def test_menu_reappears_after_add(tmp_path: Path) -> None:
    result = run_program(
        tmp_path,
        1,
        "MenuAdd",
        "https://example.com/menu-add",
        1,
        4,
    )

    assert_finished_normally(result)
    assert menu_count(result.stdout) >= 2


def test_menu_reappears_after_statistics(tmp_path: Path) -> None:
    result = run_program(tmp_path, 2, 4)

    assert_finished_normally(result)
    assert menu_count(result.stdout) >= 2


def test_menu_reappears_after_view(tmp_path: Path) -> None:
    result = run_program(
        tmp_path,
        1,
        "MenuView",
        "https://example.com/menu-view",
        1,
        3,
        1,
        4,
    )

    assert_finished_normally(result)
    assert menu_count(result.stdout) >= 3


# Negative behavior ---------------------------------------------------------
# The PDF does not specify invalid-input messages. These tests therefore check
# recovery and state, not exact error wording.


@pytest.mark.parametrize("invalid_choice", [0, 5, -1, "abc"])
def test_invalid_menu_choice_is_rejected_without_creating_bookmarks(
    tmp_path: Path, invalid_choice: object
) -> None:
    result = run_program(tmp_path, invalid_choice, 4)

    assert_finished_normally(result)
    assert_all_category_files_empty(tmp_path)


@pytest.mark.parametrize("invalid_category", [0, 5, -1, "abc"])
def test_invalid_category_does_not_save_a_bookmark(
    tmp_path: Path, invalid_category: object
) -> None:
    # Stop supplying input after the invalid category. The PDF does not say
    # whether the program should retry the category or return to the main menu,
    # so either subsequent control flow is acceptable.
    result = run_program(
        tmp_path,
        1,
        "Recovered Bookmark",
        "https://example.com/recovered",
        invalid_category,
    )

    assert_all_category_files_empty(tmp_path)


def test_viewing_empty_category_never_displays_another_category(
    tmp_path: Path,
) -> None:
    add_result = run_program(
        tmp_path,
        1,
        "Work Only Bookmark",
        "https://example.com/private-work",
        2,
        4,
    )
    view_result = run_program(tmp_path, 3, 1, 4)

    assert_finished_normally(add_result)
    # The assignment explicitly permits a missing-file error here, so this
    # test does not require a zero exit status for the view operation.
    assert "work only bookmark" not in normalize(view_result.stdout)
    assert "https://example.com/private-work" not in normalize(view_result.stdout)
