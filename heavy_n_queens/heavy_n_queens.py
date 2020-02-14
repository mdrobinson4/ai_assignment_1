import argparse
import csv

# determine position and weight of each queen
def set_queens(input_file):
    queens = []
    with open(input_file) as board_data:
        csv_reader = csv.reader(board_data, delimiter=',')
        row_count = 1
        # iterate through each row of the board
        for row in csv_reader:
            # for each row, locate the queens in that row
            find_queens_in_row(row, row_count, queens)
            row_count += 1
    return queens


# find every queen in a given row
def find_queens_in_row(row, row_count, queens):
    # iterate the columns of a given row
    for col in range(len(row)):
        weight = row[col]   # get the weight
        if weight.isdigit() == True:
            # create a new queen tuple if a queen exists in this position
            new_queen = ((row_count, col+1), int(weight))
            # add the queen to the "queens" list
            queens.append(new_queen)



def move_cost(num_tiles, weight):
    return num_tiles * weight**2


def num_attacking_queens(position):
    #find the lightest queen

    #Compute the cost of each move for that queen
    pass

def heuristic_one(queens):
    weight = 10
    lowest_queen = None
    for q in queens:
        if not q.is_attacking(board):
            continue
        if q.weight < weight:
            weight = q.weight
            lowest_queen = q
    return lowest_queen.weight


def create_queens(data, board):
    queens = []
    for q in data:
        queen = Queen(position=q[0], weight=q[1])
        board = queen.determine_initial_attacks(board)
        queens.append(queen)
    return queens, board


class Queen:
    def __init__(self, position, weight):
        self.position = position
        self.weight = weight
        self.attacking_positions = set()

    def is_attacking(self, board):
        for pos in self.attacking_positions:
            if board.check_position(pos):
                return True
        return False

    def move(self, spaces):
        self.position[1] = self.position[1] + spaces

    def determine_initial_attacks(self, board):
        for i in range(1, board.size + 1):
            if i != self.position[0]:
                horizontal = (i, self.position[1])
                self.attacking_positions.add(horizontal)

            # Forward Horizontal Diaganol up
            for_diaganol_up = self.position[1] + (i - self.position[0])
            if for_diaganol_up <= 5 and i > self.position[0]:
                self.attacking_positions.add((i, for_diaganol_up))
            # Forward Horizontal Diaganol down
            for_diaganol_down = self.position[1] - (i - self.position[0])
            if for_diaganol_down > 0 and i > self.position[0] and i < 5:
                self.attacking_positions.add((i, for_diaganol_down))

            # Reverse Horizontal Diaganol up
            rev_diaganol_up = self.position[1] + (self.position[0] - i)
            if rev_diaganol_up <= 5 and i < self.position[0]:
                self.attacking_positions.add((i, rev_diaganol_up))
            # Reverse Horizontal Diaganol down
            rev_diaganol_down = self.position[1] - (self.position[0] - i)
            if rev_diaganol_down > 0 and i < self.position[0] and i < 5:
                self.attacking_positions.add((i, rev_diaganol_down))

        board.add_attacks(self)

        return board

class Board:
    def __init__(self, n):
        self.size = n
        self._board = self.make_board()

    def make_board(self):
        board = {}
        for x in range(1, self.size + 1):
            for y in range(1, self.size + 1):
                board[(x, y)] = set()
        return board

    def add_attacks(self, queen):
        for pos in queen.attacking_positions:
            self._board[pos].add(queen)

    def show_board(self):
        print(self._board)

    def check_position(self, pos):
        return self._board[pos]

    def get_queens_attacking(self, queen):
        attackers = self.check_position(queen.position)
        return attackers


def a_star(board, queens, heuristic):
    attacking_pairs = set()
    for q in queens:
        attackers = board.get_queens_attacking(q)
        for a in attackers:
            lq = a if a.position[0] < q.position[0] else q
            gq = a if a.position[0] > q.position[0] else q
            attacking_pairs.add((lq, gq))
    print(attacking_pairs)


def get_input():
    my_parser = argparse.ArgumentParser(description='Please add some command line inputs... if you do not, I won"t know how to behave')
    my_parser.add_argument('input_file', help='Name of the file containing the n-queens board')
    my_parser.add_argument('strategy', help='Specifies the search technique')
    my_parser.add_argument('heuristic', help='Specifies the heuristic (H1 or H2)')
    args = my_parser.parse_args()
    return args.input_file, args.strategy, args.heuristic




if __name__ == '__main__':
    # get command line input
    input_file, strategy, heuristic = get_input()
    # get the locations and weights of the queens
    queens = set_queens(input_file)
    SIZE = len(queens)
    #queens = [((1, 1), 3), ((2, 3), 2), ((3, 2), 1), ((4, 4), 8), ((5, 3), 9)]
    board = Board(n=SIZE)
    queens, board = create_queens(queens, board)
    h1 = heuristic_one(queens)
    print("heuristsic weight: ", h1)
    for q in queens:
        print(q.weight)
        print(q.attacking_positions)
        print()
    a_star(board=board, queens=queens, heuristic=h1)
