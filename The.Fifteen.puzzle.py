"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) != 0:
            return False
        if target_row < self.get_height() - 1 and target_col <= self.get_width() - 1:
            row = target_row
            col = target_col
            number = target_row * self.get_width() + target_col
            max_number = (self.get_width() * self.get_height())
            #print row, col, number, max_number, self.get_number(row, col)
            while (self.get_number(row, col) == number or self.get_number(row, col) == 0) and number <= max_number:
                if row == self.get_height() - 1 and col == self.get_width() - 1:
                    return True
                number += 1
                col = (col + 1) % self.get_width()
                if col == 0:
                    row = (row + 1) % self.get_height()
                if row == self.get_width() - 1 and col == self.get_height() - 1:
                    return True
            return False
        return True
        
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        move_str = ""
        assert self.lower_row_invariant(target_row, target_col)
        target_position = self.current_position(target_row, target_col)
        if target_position[0] == target_row:
            temp_move_num = (target_col - target_position[1])
            for dummy_idx in range(target_col - target_position[1]):
                if temp_move_num == 1:
                    move_str += "l"
                    break
                move_str += "l" * temp_move_num + "u" + "r" * temp_move_num + "d"
                temp_move_num -= 1
            self.update_puzzle(move_str)
            assert self.lower_row_invariant(target_row, target_col - 1)
            return move_str
        elif target_position[1] == target_col:
            temp_move_num = (target_row - target_position[0])
            for dummy_idx in range(target_row - target_position[0]):
                if temp_move_num == 1:
                    move_str += "u" + "l" + "d"
                    break
                move_str += "u" * temp_move_num + "l" + "d" * temp_move_num + "r"
                temp_move_num -= 1
            self.update_puzzle(move_str)
            assert self.lower_row_invariant(target_row, target_col - 1)
            return move_str
        elif target_position[1] < target_col:
            temp_move_num_heigh = (target_row - target_position[0])
            temp_move_num_width = (target_col - target_position[1])
            move_str += "u" * temp_move_num_heigh + "l" * temp_move_num_width
            for dummy_idx in range(target_col - target_position[1] - 1):
                move_str += "d" + "r" * 2 + "u" + "l" * 1
            move_str += "d" * temp_move_num_heigh + "r"
            self.update_puzzle(move_str)
            temp_move = self.solve_interior_tile(target_row, target_col)
            move_str += temp_move
            assert self.lower_row_invariant(target_row, target_col - 1)
            return move_str
        elif target_position[1] > target_col:
            temp_move_num_heigh = (target_row - target_position[0])
            temp_move_num_width = (target_position[1] - target_col)
            move_str += "u" * temp_move_num_heigh + "r" * temp_move_num_width
            for dummy_idx in range(target_position[1] - target_col - 1):
                move_str += "u" + "l" * 2 + "d" + "r" * 1
            move_str += "u" + "l" * 2 + "d" + "d" * temp_move_num_heigh + "r"
            self.update_puzzle(move_str)
            temp_move = self.solve_interior_tile(target_row, target_col)
            move_str += temp_move
            assert self.lower_row_invariant(target_row, target_col - 1)
            return move_str

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        move_str = ""
        assert self.lower_row_invariant(target_row, 0)
        target_position = self.current_position(target_row, 0)
        if target_position[0] == target_row -1 and target_position[1] == 0:
            move_str += "u" + "r" * (self.get_width() - 1)
            self.update_puzzle(move_str)
            assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
            return move_str
        elif target_position[0] == target_row - 1 and target_position[1] == 1:
            move_str += "uurrdlldrurulldrdlu" + "r" * (self.get_width() - 1)
            self.update_puzzle(move_str)
            assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
            return move_str          
        elif target_position[1] == 0:
            temp_move_num_heigh = (target_row - target_position[0])
            move_str += "u" * temp_move_num_heigh
            for dummy_idx in range(temp_move_num_heigh - 2):
                move_str += "rddlu"
            move_str += "rdld"
            self.update_puzzle(move_str)
            temp_move = self.solve_col0_tile(target_row)
            move_str += temp_move
            assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
            return move_str
        elif target_position[0] == 0:
            temp_move_num_heigh = (target_row - target_position[0])
            temp_move_num_width = (target_position[1] - 0)
            move_str += "u" * temp_move_num_heigh + "r" * temp_move_num_width
            for dummy_idx in range(temp_move_num_width - 1):
                move_str += "dllur"
            move_str += "dl" + "d" * (temp_move_num_heigh - 1)
            self.update_puzzle(move_str)
            temp_move = self.solve_col0_tile(target_row)
            move_str += temp_move
            assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
            return move_str            
        else:
            temp_move_num_heigh = (target_row - target_position[0])
            temp_move_num_width = (target_position[1] - 0)
            move_str += "u" * temp_move_num_heigh + "r" * temp_move_num_width
            for dummy_index in range(temp_move_num_width - 2):
                move_str += "ulldr"
            for dummy_index in range(temp_move_num_heigh - 1):
                move_str += "dlurd"    
            move_str += "ulldd"
            self.update_puzzle(move_str)
            temp_move = self.solve_col0_tile(target_row)
            move_str += temp_move
            assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
            return move_str                     
                
    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        target_row = 0
        #print self.get_number(target_row, target_col) 
        if self.get_number(target_row, target_col) != 0:
            return False
        if target_row < self.get_height() - 1 and target_col <= self.get_width() - 1:
            row = target_row
            col = target_col
            number = target_row * self.get_width() + target_col
            max_number = (self.get_width() * self.get_height())
            #print row, col, number, max_number, self.get_number(row, col)
            while ((self.get_number(row, col) == number or self.get_number(row, col) == 0) and number <= max_number) \
                   or (row == target_row + 1 and col < target_col):
                #print row, col
                if row == target_row + 1 and col < target_col:
                    number += 1
                    col = (col + 1) % self.get_width()
                    #print number, col
                    continue                
                if row == self.get_height() - 1 and col == self.get_width() - 1:
                    return True
                number += 1
                col = (col + 1) % self.get_width()
                if col == 0:
                    row = (row + 1) % self.get_height()
                if row == self.get_width() - 1 and col == self.get_height() - 1:
                    return True
            return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        target_row = 1
        if target_row == 1:
            row = 0
            col = target_col + 1
            number = target_col + 1
            #print number
            while col <= self.get_width() - 1:
                if self.get_number(row, col) != number:
                    return False
                col += 1
                number += 1
        if self.get_number(target_row, target_col) != 0:
            return False
        if target_row < self.get_height() - 1 and target_col <= self.get_width() - 1:
            row = target_row
            col = target_col
            number = target_row * self.get_width() + target_col
            max_number = (self.get_width() * self.get_height())
            #print row, col, number, max_number, self.get_number(row, col)
            while (self.get_number(row, col) == number or self.get_number(row, col) == 0) and number <= max_number:
                if row == self.get_height() - 1 and col == self.get_width() - 1:
                    return True
                number += 1
                col = (col + 1) % self.get_width()
                if col == 0:
                    row = (row + 1) % self.get_height()
                if row == self.get_width() - 1 and col == self.get_height() - 1:
                    return True
            return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        move_str = ""
        target_row = 0
        assert self.row0_invariant(target_col)
        target_position = self.current_position(target_row, target_col)
        if target_position[0] == 0 and target_position[1] == target_col - 1:
            move_str += "ld"
            self.update_puzzle(move_str)
            assert self.row1_invariant(target_col - 1)
            return move_str
        elif target_position[0] == 0 and target_position[1] == target_col - 2:
            move_str += "dlurlldrruld"
            self.update_puzzle(move_str)
            assert self.row1_invariant(target_col - 1)
            return move_str
        elif target_position[0] == 0 and target_position[1] < target_col - 2:
            temp_move_num_width = (target_col - target_position[1])
            move_str += "l" * temp_move_num_width
            for dummy_idx in range(target_col - 2 - target_position[1] - 1):
                move_str += "drrul"
            move_str += "drrur"
            self.update_puzzle(move_str)
            temp_move = self.solve_row0_tile(target_col)
            move_str += temp_move
            assert self.row1_invariant(target_col - 1)
            return move_str
        elif target_position[0] == 1 and target_position[1] == target_col - 1:
            move_str += "ldlurr"
            self.update_puzzle(move_str)
            temp_move = self.solve_row0_tile(target_col)
            move_str += temp_move
            assert self.row1_invariant(target_col - 1)
            return move_str
        elif target_position[0] == 1:
            temp_move_num_width = (target_col - target_position[1])
            move_str += "l" * temp_move_num_width + "dru" + "r" * (temp_move_num_width - 1)
            self.update_puzzle(move_str)
            temp_move = self.solve_row0_tile(target_col)
            move_str += temp_move
            assert self.row1_invariant(target_col - 1)
            return move_str
        
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        move_str = ""
        target_row = 1
        assert self.row1_invariant(target_col)
        target_position = self.current_position(target_row, target_col)
        if target_position[0] == 1:
            temp_move_num_width = (target_col - target_position[1])
            move_str += "l" * temp_move_num_width
            for dummy_idx in range(temp_move_num_width - 1):
                move_str += "urrdl"
            move_str += "ur"
            self.update_puzzle(move_str)
            assert self.row0_invariant(target_col)
            return move_str
        elif target_position[0] == 0 and target_position[1] == target_col:
            move_str += "u"
            self.update_puzzle(move_str)
            assert self.row0_invariant(target_col)
            return move_str
        elif target_position[0] == 0:
            temp_move_num_width = (target_col - target_position[1])
            move_str += "l" * temp_move_num_width + "u" + "r" * temp_move_num_width + "d"
            self.update_puzzle(move_str)
            temp_move = self.solve_row1_tile(target_col)
            move_str += temp_move
            assert self.row0_invariant(target_col)
            return move_str

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)
        move_str = "ul"
        self.update_puzzle(move_str)
        if self.get_number(0, 1) == 1 and self.get_number(1, 0) == self.get_width():
            return move_str
        move_str = ""
        for dummy_idx in range(3):
            move_str += "drul"
            self.update_puzzle("drul")
            if self.get_number(0, 1) == 1 and self.get_number(1, 0) == self.get_width():
                return "ul" + move_str

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        #return "uuullldrrulldrrullddrruuldddruurddluurullddrullddrurullddruruurddluurddluulldrulddrurulldrrdllurdruurdllurrdlluldrul"
        move_str = ""
        row = self.get_height() - 1
        col = self.get_width() - 1
        solved = self.lower_row_invariant(0, 0)
        if solved == True:
            return move_str
        if self.get_number(row, col) != 0:
            zero_position = self.current_position(0, 0)
            move_str += "r" * (self.get_width() - 1 - zero_position[1]) 
            move_str += "d" * (self.get_height() - 1 - zero_position[0])
            self.update_puzzle(move_str)
        while solved == False:
            #print "inside",  row, col
            if row == 1 and col == 1:
                move_str += self.solve_2x2()
                return move_str
            if row == 1:
                move_str += self.solve_row1_tile(col)
                move_str += self.solve_row0_tile(col)
                col -= 1
                continue
            else:
                if col != 0:
                    move_str += self.solve_interior_tile(row, col)
                if col == 0:
                    move_str += self.solve_col0_tile(row)
                    col = self.get_width() - 1
                    row -= 1
                    continue
                col -= 1

# Start interactive simulation
#test = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]]))
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]]))
#poc_fifteen_gui.FifteenGUI( Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]]))

########################################################
#             choice one bellow to play                #
#                   by Jr-Han Tai                      #
#     Uncomment the # sign at begining to start        # 
########################################################

poc_fifteen_gui.FifteenGUI(puzzle=Puzzle(4, 4, [[15, 11, 8, 12], [14, 10, 9, 13], [2, 6, 1, 4], [3, 7, 5, 0]]))
#poc_fifteen_gui.FifteenGUI(Puzzle(9,9))



#############################################
#self test

#test = Puzzle(8, 6, [[41,21, 3, 9, 5, 42],
#                     [8,7, 6, 1, 37, 36],
#                     [12,10, 17, 19, 15, 2],
#                     [13,14, 16, 18, 20, 22],
#                     [23,26, 28, 30, 32, 34],
#                     [11,25, 35, 29, 31, 33], 
#                     [4,37, 38, 39, 40,24], 
#                     [0,43,44,45,46,47]])

#test = Puzzle(4, 5, [[6, 5, 1, 2, 0], 
#                     [4, 3, 8, 7, 9], 
#                     [10, 11, 12, 13, 14], 
#                     [15, 16, 17, 18, 19]])
#test = Puzzle(3, 3, [[5, 2, 6],
#                     [4, 3, 1],
#                     [0, 7, 8]])

#print test
#print test.row0_invariant(2)

#print test
#print test.solve_row0_tile(7)
#test = Puzzle(3,3)
 
#print test.lower_row_invariant(2,3)
#print test.get_width(), test.get_height()
#print test.solve_interior_tile(7,5)
#print test.solve_col0_tile(7)
#print test

#############################################
# challenge
#puzzle=Puzzle(4, 4, [[15, 11, 8, 12], [14, 10, 9, 13], [2, 6, 1, 4], [3, 7, 5, 0]])
#sol=puzzle.solve_puzzle()
#print sol
#print len(sol)
