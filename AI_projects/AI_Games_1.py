############################################################
# CMPSC 442: Homework 2
############################################################

# student_name = "Varun Jani"

############################################################
# Imports
############################################################

# All the imports I have used for this homework
import random
from collections import deque
import copy


############################################################
# Section 1: N-Queens
############################################################

# Simple factorial function I implemented to use here
def factorial(n):
    return factorial(n - 1) * n if n > 1 else 1


# Since the logic for solving this is nCr(n^2, n)
def num_placements_all(n):
    return factorial(n ** 2) / factorial(n ** 2 - n) / factorial(n)


# Returns no. of possible placements of n queens on an n by n board without additional restriction
def num_placements_one_per_row(n):
    return n ** n


# Check if the queen positioning is valid or not by returning True or False using nested for loops
def n_queens_valid(board):
    for i, j in enumerate(board):
        if j in board[:i] or j in board[i + 1:]:
            return False
        for var in range(-len(board), len(board)):
            final = var + i
            if var == 0 or final < 0 or final >= len(board):
                continue
            if board[final] in [j + var, j - var]:
                return False
    return True


# A helper function to yield all valid possible placements to extend the partial solution
def n_queens_helper(n, board):
    if len(board) == n:
        yield board
    else:
        for i in [element for element in range(n) if n_queens_valid(board + [element])]:
            for j in n_queens_helper(n, board + [i]):
                yield j


# yields all the possible valid solutions using the above helper function
def n_queens_solutions(n):
    for sol in n_queens_helper(n, []):
        yield sol


############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    # Simple __init__ function
    def __init__(self, board):
        self.board = board
        self.temp_row = len(self.board)
        self.temp_col = len(self.board[0])

    # Simple get_board function
    def get_board(self):
        return self.board

    # This function toggles the lights located up, down, left and right from the current position
    def perform_move(self, row, col):
        up = row - 1
        down = row + 1
        right = col + 1
        left = col - 1

        # To check for the center light (Center)
        self.board[row][col] = not self.board[row][col]

        # To check for the right light (right)
        if col < self.temp_col - 1:
            self.board[row][right] = not self.board[row][right]

        # # To check for the left light (left)
        if col > 0:
            self.board[row][left] = not self.board[row][left]

        # # To check for the upper light (up)
        if row > 0:
            self.board[up][col] = not self.board[up][col]

        # # To check for the light below (down)
        if row < self.temp_row - 1:
            self.board[down][col] = not self.board[down][col]

        return self

    # Scrambles the puzzle using random function
    def scramble(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    # To check if all the lights  on the board are turned off
    def is_solved(self):
        for row in self.board:
            for x in row:
                if x:
                    return False
        return True

    # Function to create a deep copy of the current board using copy.deepcopy()
    def copy(self):
        new_board = copy.deepcopy(self.board)
        return LightsOutPuzzle(new_board)

    # Function to yield all the successors of the puzzle as tuples
    def successors(self):
        for row in range(self.temp_row):
            for col in range(self.temp_col):
                new_board = self.copy()
                new_board.perform_move(row, col)
                yield (row, col), new_board

    # To find an optimal solution to the current board using breadth first graph search
    def find_solution(self):
        temp = deque([([], self)])  # Used deque from collections since more efficient
        x = set()
        while temp:
            pos, arr = temp.popleft()
            if arr.is_solved():
                return pos

            current_state = tuple(map(tuple, arr.get_board()))

            if current_state in x:
                continue
            else:
                x.add(current_state)

            for i, j in arr.successors():
                move = copy.deepcopy(pos)
                move.append(i)
                temp.append((move, j))
        return None


def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for col in range(cols)] for row in range(rows)])


############################################################
# Section 3: Linear Disk Movement
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
        for i, j in identical(arr, length):
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
        if x + 1 < length and p[x + 1] and x + 2 < length and not puzzle[x + 2]:
            puzzle[x], puzzle[x + 2] = puzzle[x + 2], puzzle[x]
            yield ((x, x + 2), puzzle)
            puzzle = p[:]

        if x + 1 < length and not puzzle[x + 1]:
            puzzle[x], puzzle[x + 1] = puzzle[x + 1], puzzle[x]
            yield ((x, x + 1), puzzle)
            puzzle = p[:]

        if x - 1 >= 0 and puzzle[x - 1] and x - 2 >= 0 and not puzzle[x - 2]:
            puzzle[x - 2], puzzle[x] = puzzle[x], puzzle[x - 2]
            yield ((x, x - 2), puzzle)
            puzzle = p[:]

        if x - 1 >= 0 and not puzzle[x - 1]:
            puzzle[x - 1], puzzle[x] = puzzle[x], puzzle[x - 1]
            yield ((x, x - 1), puzzle)
            puzzle = p[:]


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
        for i, j in distinct(arr, length):
            sol = pos + [i]
            if j == des:
                return sol
            con = (sol, j)
            if tuple(j) not in x and tuple(j) not in t:
                temp.append(con)
    return 0


############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
Somewhere around 8 hours
"""

feedback_question_2 = """
Section 3 of the assignment was the hardest in my opinion. I had to spend a lot more time there.
It was tough to pass some test cases but I eventually figured them out.
"""

feedback_question_3 = """
I liked the lights out puzzle, as it was challenging but I had the idea so I could figure it out.
As for changing, the linear disk movement problem could have been explained in the class
so its easier to solve the programming problem.
"""
