
# Author: Varun Jani

############################################################
# Import Statements
############################################################

import math
import random
import copy
from collections import deque

############################################################
# Section 1: To implement the N-Queen problem in python
############################################################

# Possible number of combinations of queens in every row and every column
def num_placements_all(n):
    res = 1
    for i in range(n):
        res *= (n ** 2 - i)  # nPr (Permutation with n^2 and n as inputs) (Ex: 16P4 = 43680)
    return res


# Possible number of placements if we do not include any restriction of where the queen is placed
def num_placements_one_per_row(n):
    res = 1
    for i in range(n):
        res *= n * (n - i)  # Similar idea as num_placements_all except for one per row
    return res


# Function to check the validity of the board and return true or false accordingly
def n_queens_valid(board):
    if len(board) == 1:
        return True
    for (i, j) in enumerate(board):
        if j in board[i + 1:]:
            return False
        for x in range(i + 1, len(board)):
            if abs(i - x) == abs(j - board[x]):
                return False
    return True


# Function of solution to solve the N Queen problem
def n_queens_solutions(n):
    x = n_queens_helper(n, [])
    while x:
        board = x.pop()
        if n_queens_valid(board):
            if len(board) == n:
                yield board
            else:
                x.extend(n_queens_helper(n, board))


# A helper function for n_queen_solutions
def n_queens_helper(n, board):
    return [board + [i] for i in range(n - 1, -1, -1)]


############################################################
# Section 2: To solve the lights out puzzle 
############################################################

class LightsOutPuzzle(object):

    # Simple __init__ function to initialize the board
    def __init__(self, board):
        self.board = board
        self.row = len(board)
        if self.row != 0:
            self.col = len(board[0])
        else:
            self.col = 0

    def get_board(self):
        return self.board

    # Function to perform the move and toggle the light at the right locations
    def perform_move(self, row, col):
        up = row - 1
        down = row + 1
        right = col + 1
        left = col - 1

        # Case where the rows and columns exist between 0 and the original rows and columns
        if 0 <= row < self.row and 0 <= col < self.col:
            self.board[row][col] = not self.board[row][col]

        # To toggle the left, right, up and down lights
        if left >= 0:
            self.board[row][left] = not self.board[row][left]
        if right >= 0:
            self.board[row][right] = not self.board[row][right]
        if up >= 0:
            self.board[up][col] = not self.board[up][col]
        if down >= 0:
            self.board[down][col] = not self.board[down][col]

    # Function to scramble the board using random module
    def scramble(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    # Function to check if all the lights on the board are turned off
    def is_solved(self):
        for row in self.board:
            for x in row:
                if x:
                    return False
        return True

    # Function to copy the board using copy module
    def copy(self):
        new_board = copy.deepcopy(self.board)
        return LightsOutPuzzle(new_board)

    # Function to yield all the successors of the puzzle as tuples
    def successors(self):
        for row in range(self.row):
            for col in range(self.col):
                res = (row, col)
                new_board = self.copy()
                new_board.perform_move(row, col)
                yield (res, new_board)

    # Function to return an optimum solution of the board represented as tuples
    def find_solution(self):
        if self.is_solved():
            return []
        temp = deque([([], self)])  # Used deque from collections since more efficient
        x = set()
        temp_board = []
        new_board = ()
        while temp:
            pos, arr = temp.popleft()
            for row in arr.get_board():
                x.add(tuple(tuple(row)))
            for (i, j) in arr.successors():
                sol = pos + [i]
                if j.is_solved():
                    return sol
                con = (sol, j)
                for row in j.get_board():
                    new_board = tuple(tuple(row))
                if new_board not in x and j.get_board() not in temp_board:
                    temp.append(con)
        return 0


# Function to return a new LightsOutPuzzle every instance when called
def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for col in range(cols)] for row in range(rows)])


############################################################
# Section 3: To solve the Linear Disk Movement
############################################################


# Helper function for solve_identical-disks function
def identical(puzzle, length):
    for x in range(length):
        if not puzzle[x]:
            continue
        p = puzzle[:]

        # If statements to check the possibility of the disk movements when identical
        if x + 1 < length and puzzle[x + 1] and x + 2 < length and not puzzle[x + 2]:
            puzzle[x], puzzle[x + 2] = puzzle[x + 2], puzzle[x]
            yield ((x, x + 2), puzzle)
            puzzle = p[:]

        if x + 1 < length and not puzzle[x + 1]:
            puzzle[x], puzzle[x + 1] = puzzle[x + 1], puzzle[x]
            yield ((x, x + 1), puzzle)
            puzzle = p[:]


# Function that solves the Linear Disk Movement for identical disks
def solve_identical_disks(length, n):
    puz = [True if a < n else False for a in range(length)]
    des = [False if a < length - n else True for a in range(length)]
    if length == 0 or puz == des:
        return []
    t = set()
    x = set()
    temp = deque([([], puz)])
    while temp:
        pos, arr = temp.popleft()  # Can also use list.pop(0) but deque.popleft() is faster
        x.add(tuple(arr))
        for (i, j) in identical(arr, length):
            sol = pos + [i]
            if puz == des:
                return sol
            con = (sol, j)

            if tuple(j) not in t and tuple(j) not in x:
                temp.append(con)
    return 0


# Helper function for solve_distinct_disks function
def distinct(puzzle, length):
    for x in range(length):
        if not puzzle[x]:
            continue
        p = puzzle[:]

        # If statements to check the possibility of the disk movement when distinct
        if x + 1 < length and p[x + 1] and x + 2 < length and not p[x + 2]:
            p[x], p[x + 2] = p[x + 2], p[x]
            yield ((x, x + 2), p)

        if x + 1 < length and not p[x + 1]:
            p[x], p[x + 1] = p[x + 1], p[x]
            yield ((x, x + 1), p)

        if x - 1 >= 0 and p[x - 1] and x - 2 >= 0 and not p[x - 2]:
            p[x - 2], p[x] = p[x], p[x - 2]
            yield ((x, x - 2), p)

        if x - 1 >= 0 and not p[x - 1]:
            p[x - 1], p[x] = p[x], p[x - 1]
            yield ((x, x - 1), p)


# Function that solves the Linear Disk problem for distinct disks
def solve_distinct_disks(length, n):
    puz = [a + 1 if a < n else False for a in range(length)]
    des = [False if a < length - n else length - a for a in range(length)]
    if length == 0 or puz == des:
        return []
    t = set()
    x = set()
    temp = deque([([], puz)])
    while temp:
        pos, arr = temp.popleft()  # Can also use list.pop(0) but deque.popleft() is faster
        for (i, j) in distinct(arr, length):
            sol = pos + [i]
            if j == des:
                return sol
            con = (sol, j)

            if tuple(j) not in x and tuple(j) not in t:
                temp.append(con)
    return 0
