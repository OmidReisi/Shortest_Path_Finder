import curses
from curses import wrapper
from collections import deque
import numpy as np
import time

#  "#" is used for obstacles " " is the open way "O" is the starting point and "X" is the ending point.
main_maze: np.ndarray = np.array(
    [
        ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
        ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
        ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
        ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
        ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "X", "#"],
    ]
)


def print_maze(maze, stdscr, path=None):
    if not path:
        path = []
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 2, "X", BLUE)
            else:
                stdscr.addstr(i, j * 2, value, RED)


def find_start(maze, start_value):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start_value:
                return i, j
    return None


def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    q = deque([[start_pos]])

    visited = set()

    while q:

        current_path = q.pop()
        current_pos = current_path[-1]
        row, col = current_pos

        stdscr.clear()
        print_maze(main_maze, stdscr, current_path)
        stdscr.refresh()
        time.sleep(0.5)

        if maze[row, col] == end:
            return current_path

        neighbors = find_neighbors(maze, current_pos)
        for neighbor in neighbors:
            if neighbor in visited or maze[neighbor[0], neighbor[1]] == "#":
                continue
            new_path = current_path.copy()
            new_path.append(neighbor)
            q.appendleft(new_path)
            visited.add(neighbor)


def find_neighbors(maze, position):
    neighbors = []
    row, col = position
    if row > 0:
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):
        neighbors.append((row, col + 1))

    return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    find_path(main_maze, stdscr)
    stdscr.getch()


wrapper(main)
