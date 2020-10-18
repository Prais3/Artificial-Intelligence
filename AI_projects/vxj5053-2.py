############################################################
# CMPSC 442: Homework 3
############################################################

# student_name = "Varun Jani"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
from queue import PriorityQueue
import copy
import math


############################################################
# Section 1: Tile Puzzle
############################################################

# create tile puzzle function that returns a new puzzle with the specified dimensions
def create_tile_puzzle(rows, cols):
    puzzle = []
    new_puzzle = []
    x = 1
    for i in range(0, rows):
        for j in range(0, cols):
            new_puzzle.append(x)
            x += 1
        puzzle.append(new_puzzle)
        new_puzzle = []
    puzzle[rows - 1][cols - 1] = 0

    return TilePuzzle(puzzle)


class TilePuzzle(object):
    possible_moves = {"up": "down", "down": "up", "left": "right", "right": "left"}

    # Simple init function to initialize the variables required for the other function
    def __init__(self, board):
        self.puzzle = board
        self.temp_row = len(board)
        self.temp_col = len(board[0])
        self.tile = {}
        count = 1

        for i in range(self.temp_row):
            for j in range(self.temp_col):
                if board[i][j] == 0:
                    self.loc = (i, j)

        for i in range(self.temp_row):
            for j in range(self.temp_col):
                if count == self.temp_row * self.temp_col:
                    self.tile[0] = (i, j)
                else:
                    self.tile[count] = (i, j)
                count += 1

        self.solution = self.helper()
        self.moves = []

    # Helper function for the init function
    def helper(self):
        puzzle = []
        new_puzzle = []
        temp = 1

        for i in range(self.temp_row):
            for j in range(self.temp_col):
                new_puzzle.append(temp)
                temp += 1
            puzzle.append(new_puzzle)
            new_puzzle = []

        puzzle[self.temp_row - 1][self.temp_col - 1] = 0
        return puzzle

    # Simple function to return the internal representation of the puzzle
    def get_board(self):
        return self.puzzle

    # This function checks for which move to perform and swaps with its neighbor in the indicated direction
    def perform_move(self, direction):
        loc = self.loc

        # Direction up Case
        if direction == "up":
            if loc[0] == 0:
                return False
            else:
                self.puzzle[loc[0]][loc[1]] = self.puzzle[loc[0] - 1][loc[1]]
                self.puzzle[loc[0] - 1][loc[1]] = 0
                self.loc = (loc[0] - 1, loc[1])
                return True
        # Direction down Case
        elif direction == "down":
            if loc[0] == self.temp_row - 1:
                return False
            else:
                self.puzzle[loc[0]][loc[1]] = self.puzzle[loc[0] + 1][loc[1]]
                self.puzzle[loc[0] + 1][loc[1]] = 0
                self.loc = (loc[0] + 1, loc[1])
                return True
        # Direction left Case
        elif direction == "left":
            if loc[1] == 0:
                return False
            else:
                self.puzzle[loc[0]][loc[1]] = self.puzzle[loc[0]][loc[1] - 1]
                self.puzzle[loc[0]][loc[1] - 1] = 0
                self.loc = (loc[0], loc[1] - 1)
                return True
        # Direction right Case
        elif direction == "right":
            if loc[1] == self.temp_col - 1:
                return False
            else:
                self.puzzle[loc[0]][loc[1]] = self.puzzle[loc[0]][loc[1] + 1]
                self.puzzle[loc[0]][loc[1] + 1] = 0
                self.loc = (loc[0], loc[1] + 1)
                return True
        return False

    # Scrambles the function by calling perform_move function and the direction is random everytime when scrambling
    def scramble(self, num_moves):
        direction = ["up", "down", "left", "right"]
        for i in range(num_moves):
            self.perform_move(random.choice(direction))

    # This function checks whether the puzzle is solved or not and returns True or False accordingly
    def is_solved(self):
        sol = create_tile_puzzle(self.temp_row, self.temp_col)
        if sol.get_board() == self.puzzle:
            return True
        return False

    # Copy function for a new puzzle and this uses deepcopy
    def copy(self):
        new_puzzle = copy.deepcopy(self.puzzle)
        return TilePuzzle(new_puzzle)

    # This function simply yields the possible successor of the puzzle in the form of tuples
    def successors(self):
        puzzle_copy = self.copy()
        if puzzle_copy.perform_move("up"):
            yield ("up", puzzle_copy)
        puzzle_copy = self.copy()
        if puzzle_copy.perform_move("down"):
            yield ("down", puzzle_copy)
        puzzle_copy = self.copy()
        if puzzle_copy.perform_move("right"):
            yield ("right", puzzle_copy)
        puzzle_copy = self.copy()
        if puzzle_copy.perform_move("left"):
            yield ("left", puzzle_copy)

    # This function uses iddfs to yield all the optimal solutions of the current puzzle in the form of possible moves
    def find_solutions_iddfs(self):
        limit = 0
        sol = False
        while not sol:
            for pos in self.iddfs_helper(limit, []):
                yield pos
                sol = True
            limit += 1

    # Helper function for the iddfs function defined above
    def iddfs_helper(self, limit, moves):
        if self.puzzle == self.solution:
            yield moves
        elif len(moves) < limit:
            for move, pos in self.successors():
                for solution in pos.iddfs_helper(limit, moves + [move]):
                    yield solution

    # Helper function for the a_star solution function below and here the manhattan distance heuristic is implemented
    def manhattan(self, board):
        total = 0
        for i in range(self.temp_row):
            for j in range(self.temp_col):
                updated_puzzle = board.puzzle[i][j]
                sol = self.tile[updated_puzzle]
                total += abs(i - sol[0]) + abs(j - sol[1])
        return total

    # This function uses a_star solution to solve the tile puzzle problem using PriorityQueue
    def find_solution_a_star(self):
        q = PriorityQueue()

        # This steps allows to queue the initial successors
        for i, pos in self.successors():
            manhattan_dist = self.manhattan(pos)
            q.put((manhattan_dist, ([i], pos)))

        # Here we check in the queue for a successor until a solution is found
        while not q.empty():
            puzzle = q.get()
            pos = puzzle[1][1]

            # This checks if solved or not
            if pos.is_solved():
                return puzzle[1][0]

            # The determined successors are added into the priority queue
            for i, pos in pos.successors():
                if TilePuzzle.possible_moves[i] == puzzle[1][0][-1]:
                    continue
                copy_puz = copy.deepcopy(puzzle[1][0])
                copy_puz.append(i)
                updated_manhattan = self.manhattan(pos)
                q.put((puzzle[0] + updated_manhattan, (copy_puz, pos)))

        return None


############################################################
# Section 2: Grid Navigation
############################################################

# Function that returns the shortest path from start to goal points using A* search algorithm and euclidean heuristic
def find_path(start, goal, scene):
    temp_row = len(scene)
    temp_col = len(scene[0])

    # Function which checks for the possible successors or the possible paths in the possible directions
    def successor(var):
        i, j = var
        final = []

        # Below are the possible cases which can be successors:
        # Left Case
        if j + 1 >= 0 and not scene[i][j - 1]:
            final.append((i, j - 1))
        # Right Case
        if j + 1 < temp_col and not scene[i][j + 1]:
            final.append((i, j + 1))
        # Up Case
        if i - 1 >= 0 and not scene[i - 1][j]:
            final.append((i - 1, j))
        # Down Case
        if i + 1 < temp_row and not scene[i + 1][j]:
            final.append((i + 1, j))
        # Up-right Case
        if i - 1 >= 0 and j + 1 < temp_col and not scene[i - 1][j + 1]:
            final.append((i - 1, j + 1))
        # Up-left Case
        if i - 1 >= 0 and j - 1 >= 0 and not scene[i - 1][j - 1]:
            final.append((i - 1, j - 1))
        # Down-left Case
        if i + 1 < temp_row and j - 1 >= 0 and not scene[i + 1][j - 1]:
            final.append((i + 1, j - 1))
        # Down-right Case
        if i + 1 < temp_row and j + 1 < temp_col and not scene[i + 1][j + 1]:
            final.append((i + 1, j + 1))

        return final

    # This function simply implements the euclidean distance heuristic
    def euclid_distance(begin, end):
        return math.sqrt((begin[0] - end[0]) ** 2 + (begin[1] - end[1]) ** 2)

    if scene[start[0]][start[1]] or scene[goal[0]][goal[1]]:
        return None

    # Using priority queue since it uses A* search algorithm
    q = PriorityQueue()

    for u in successor(start):
        q.put((euclid_distance(u, goal), [start, u]))

    while not q.empty():
        t, cost = q.get()
        loc = cost[-1]

        if loc == goal:
            return cost

        for k in successor(loc):
            if k == cost[-2]:
                continue
            new_t = euclid_distance(k, goal)
            copy_cost = copy.deepcopy(cost)
            copy_cost.append(k)
            q.put((t + new_t, copy_cost))

    return None


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

# Creating a class called LinearDiskMovement since is allows to implement A* search clearly
class LinearDiskMovement(object):

    # Simple init function to initialize the variables required for the problem
    def __init__(self, length, n, disk):
        self.length = length
        self.x = n
        self.k = 0
        self.disk = disk
        self.move = []
        if len(disk) == 0:
            self.disk = [0 for i in range(self.length)]
            for i in range(n):
                self.disk[i] = i + 1

    # Simply returns the disk
    def get_disk(self):
        return self.disk

    # This function performs the move and determines from where (current) to where(step)
    def perform_move(self, current, step):
        distance = current - step
        if abs(distance) > 2 or abs(distance) == 0 or current < 0 or step < 0 or step > (self.length - 1):
            return False
        else:
            if self.disk[step] == 0 and self.disk[current] > 0:
                if abs(-distance) == 1:
                    self.disk[step] = self.disk[current]
                    self.disk[current] = 0
                    return True
                elif distance == -2 and not self.disk[current + 1] == 0:
                    self.disk[step] = self.disk[current]
                    self.disk[current] = 0
                    return True
                elif distance == 2 and not self.disk[current - 1] == 0:
                    self.disk[step] = self.disk[current]
                    self.disk[current] = 0
                    return True
        return False

    # Simple function to check if the problem is solved or not
    def is_solved(self):
        count = 0
        for i in range(self.length - self.x, self.length):
            if not self.disk[i] == self.x - count:
                return False
            count += 1
        return True

    # Simple copy function that uses deepcopy to copy the length, x and the disk
    def copy(self):
        length_copy = copy.deepcopy(self.length)
        x_copy = copy.deepcopy(self.x)
        disk_copy = copy.deepcopy(self.disk)
        return LinearDiskMovement(length_copy, x_copy, disk_copy)

    # Successor function which checks for the possible successors and returns them in the form of tuples
    def successor(self):
        successor_val = []

        for i in range(self.length):
            if i < self.length:
                disk_copy = self.copy()
                if disk_copy.perform_move(i, i + 1):
                    successor_val.append([(i, i + 1), disk_copy])
                disk_copy = self.copy()
                if disk_copy.perform_move(i, i - 1):
                    successor_val.append([(i, i - 1), disk_copy])
                disk_copy = self.copy()
                if disk_copy.perform_move(i, i + 2):
                    successor_val.append([(i, i + 2), disk_copy])
                disk_copy = self.copy()
                if disk_copy.perform_move(i, i - 2):
                    successor_val.append([(i, i - 2), disk_copy])

        return (j for j in successor_val)

    # heuristic function implemented for the A* search algorithm to solve the problem
    def heuristic(self):
        heuristic = {}
        y1, y2, j = 0, 0, 0

        for i in range(self.length - self.x, self.length):
            heuristic[self.x - y1] = i
            y1 += 1
        while self.disk[j] > 0:
            y2 += abs(j - heuristic[self.disk[j]])
            j += 1

        return y2


# Function that uses A* search algorithm using the above class to solve the distinct disk problem
def solve_distinct_disks(length, n):
    if length == n:
        return []

    # Initializing the variables and the priority queue
    new_disk = LinearDiskMovement(length, n, [])
    visited = set()
    q = PriorityQueue()
    limit = 0
    q.put((new_disk.heuristic(), limit, new_disk))

    # Until all the successors are found from the priority queue
    while not q.empty():
        current = q.get()
        pos = current[2]

        # Checks if solved or not
        if pos.is_solved():
            return pos.move

        for i, node in pos.successor():
            if node not in visited:
                limit += 1
                node.k = pos.k + node.heuristic()
                node.move = pos.move + [i]
                visited.add(node)
                q.put((node.k, limit, node))

    return None


############################################################
# Section 4: Dominoes Game
############################################################

# Simple function to return a new DominoesGame with all squares initialized to 0
def create_dominoes_game(rows, cols):
    return DominoesGame([[False for j in range(cols)] for i in range(rows)])


class DominoesGame(object):

    # Required init function that defines the input board
    def __init__(self, board):
        self.board = board
        self.temp_row = len(board)
        self.temp_col = len(board[0])

    # Function that returns the internal representation of the board
    def get_board(self):
        return self.board

    # Reset function which resets all the states inside the board to 0
    def reset(self):
        for i in range(self.temp_row):
            for j in range(self.temp_col):
                self.board[i][j] = False

    # Checks if the move can be played on the current situation of the board or not
    def is_legal_move(self, row, col, vertical):
        if self.board[row][col]:
            return False
        if vertical:
            row += 1
        else:
            col += 1
        if row >= self.temp_row or col >= self.temp_col or self.board[row][col]:
            return False
        return True

    # Function that yields all the possible legal moves in the form of tuples
    def legal_moves(self, vertical):
        for i in range(self.temp_row):
            for j in range(self.temp_col):
                if self.is_legal_move(i, j, vertical):
                    yield i, j

    # Function that fills the squares based on the domino location in the specified orientation
    def perform_move(self, row, col, vertical):
        self.board[row][col] = True
        if not vertical:
            self.board[row][col + 1] = True
        else:
            self.board[row + 1][col] = True

    # Returns True or False depending on whether the current player can place aby more dominoes or not
    def game_over(self, vertical):
        if not list(self.legal_moves(vertical)):
            return True
        return False

    # Simple copy function that creates a copy using the deepcopy function
    def copy(self):
        new_board = copy.deepcopy(self.board)
        return DominoesGame(new_board)

    # Successor function that yields all the successors of the puzzle for the player in the form of tuples
    def successors(self, vertical):
        for i in self.legal_moves(vertical):
            new_board = self.copy()
            new_board.perform_move(i[0], i[1], vertical)
            yield i, new_board

    # Gives a random legal move for the current player
    def get_random_move(self, vertical):
        return random.choice(list(self.legal_moves(vertical)))

    # Returns the best possible move for the current player based on alpha-beta search
    def get_best_move(self, vertical, limit):

        # evaluates the possible legal moves
        def evaluate(current):
            x1 = len(list(current.legal_moves(vertical)))
            x2 = len(list(current.legal_moves(not vertical)))
            return x1 - x2

        # returns the alpha-beta search solution in the form of tuples
        def alpha_beta(current):
            return tuple(max_value(current, float("-inf"), float("inf"), limit, vertical, 0))

        # Max function for the alpha-beta search with the negative infinity condition
        def max_value(state, alpha, beta, limit, vertical, counter):
            val_1 = state[0]
            val_2 = state[1]

            if limit == 0 or val_2.game_over(vertical):
                return val_1, evaluate(val_2), counter + 1

            # Since in the form a 3 value tuple
            u = [None, float("-inf"), None]

            for val_2 in val_2.successors(vertical):
                move, temp, counter = min_value(val_2, alpha, beta, limit - 1, not vertical, counter)

                if temp > u[1]:
                    u = [val_2[0], temp, counter]
                else:
                    u[2] = counter

                if u[1] >= beta:
                    return u

                alpha = max([alpha, u[1]])
            return u

        # Min function for the alpha-beta search with the positive infinity condition
        def min_value(state, alpha, beta, limit, vertical, counter):
            val_1 = state[0]
            val_2 = state[1]

            if limit == 0 or val_2.game_over(vertical):
                return val_1, evaluate(val_2), counter + 1

            # Since in the form a 3 value tuple
            u = [None, float("inf"), None]

            for val_2 in val_2.successors(vertical):
                move, temp, counter = max_value(val_2, alpha, beta, limit - 1, not vertical, counter)

                if temp < u[1]:
                    u = [val_2[0], temp, counter]
                else:
                    u[2] = counter

                if u[1] <= alpha:
                    return u

                beta = min([beta, u[1]])
            return u

        return alpha_beta((None, self))


############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
Around 10-12 hours
"""

feedback_question_2 = """
The Linear Disk Movement was the most challenging one in my opinion. I was stuck on whether
I had to create a class or not, and after understanding the problem, I realized I needed a
class for this problem. Since test cases were not given, I had to use hw2 test cases.
"""

feedback_question_3 = """
I liked the Tile Puzzle one and the dominoes game. Yes, I did not like the linear disk problem
and I hope it is not there in the future homeworks.
"""
