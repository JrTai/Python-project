"""
Clone of 2048 game.
"""

import poc_2048_gui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code from the previous mini-project
    result_list = []
    zero_list = []
    count = 0
    for index in range(len(line)):
        if line[index] != 0:
            result_list.append(line[index])
        else:
            zero_list.append(0)
    for index in range(len(result_list)):
        if result_list[index] == result_list[index - 1] and index != 0:
            result_list[index - 1] += result_list[index]
            result_list[index] = 0
            count += 1
            zero_list.append(0)
    for index in range(count):
        result_list.remove(0)
    for index in range(len(zero_list)):
        result_list.append(0)
    return result_list

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._height = grid_height
        self._width = grid_width
        self.reset()
        self._upp = [(0, col) for col in range(self._width)]
        self._down = [(self._height - 1, col) for col in range(self._width)]
        self._left = [(row, 0) for row in range(self._height)]
        self._right = [(row, self._width - 1) for row in range(self._height)]
        self._start = {"UP": self._upp, "DOWN": self._down, "LEFT": self._left, "RIGHT": self._right}
        
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self._cells = [[0 for dummy_col in range(self._width)] 
                          for dummy_row in range(self._height)]
        self.new_tile()
        self.new_tile()
        
                
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return str(self._cells)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        if direction == UP:
            self.upp()
                   
        elif direction == DOWN:
            self.down()
                    
        elif direction == LEFT:
            self.left()
            
        elif direction == RIGHT:
            self.right()

        #if min(min(self._cells)) == 0:
        self.new_tile()    

    def upp(self):
        """
        Up merging process, the sub-process under move method
        """ 
        for col in range(self._width):
            self._temp = []
            row_x = self._start["UP"][col][0]
            row_y = self._start["UP"][col][1]
            for row in range(self._height):
                self._temp.append(self._cells[row_x][row_y])
                row_x += OFFSETS[1][0]
                #row_y += OFFSETS[1][1]
            self._temp = merge(self._temp)
            row_x = self._start["UP"][col][0]
            row_y = self._start["UP"][col][1]
            for row in range(self._height):
                self._cells[row_x][row_y] = self._temp[row]
                row_x += OFFSETS[1][0]
                #row_y += OFFSETS[1][1]

    def down(self):
        """
        Down merging process, the sub-process under move method
        """ 
        for col in range(self._width):
            self._temp = []
            row_x = self._start["DOWN"][col][0]
            row_y = self._start["DOWN"][col][1]
            for row in range(self._height):
                self._temp.append(self._cells[row_x][row_y])
                row_x += OFFSETS[2][0]
                #row_y += OFFSETS[2][1]
            self._temp = merge(self._temp)
            row_x = self._start["DOWN"][col][0]
            row_y = self._start["DOWN"][col][1]
            for row in range(self._height):
                self._cells[row_x][row_y] = self._temp[row]
                row_x += OFFSETS[2][0]
                #row_y += OFFSETS[2][1]
        
    def left(self):
        """
        Left merging process, the sub-process under move method
        """ 
        for col in range(self._height):
            self._temp = []
            row_x = self._start["LEFT"][col][0]
            row_y = self._start["LEFT"][col][1]
            for row in range(self._width):
                self._temp.append(self._cells[row_x][row_y])
                #row_x += OFFSETS[3][0]
                row_y += OFFSETS[3][1]
            self._temp = merge(self._temp)
            row_x = self._start["LEFT"][col][0]
            row_y = self._start["LEFT"][col][1]
            for row in range(self._width):
                self._cells[row_x][row_y] = self._temp[row]
                #row_x += OFFSETS[3][0]
                row_y += OFFSETS[3][1]
                    
    def right(self):
        """
        Up merging process, the sub-process under move method
        """
        for col in range(self._height):
            self._temp = []
            row_x = self._start["RIGHT"][col][0]
            row_y = self._start["RIGHT"][col][1]
            for row in range(self._width):
                self._temp.append(self._cells[row_x][row_y])
                #row_x += OFFSETS[4][0]
                row_y += OFFSETS[4][1]
            self._temp = merge(self._temp)
            row_x = self._start["RIGHT"][col][0]
            row_y = self._start["RIGHT"][col][1]
            for row in range(self._width):
                self._cells[row_x][row_y] = self._temp[row]
                #row_x += OFFSETS[4][0]
                row_y += OFFSETS[4][1]
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        import random
        self._tile = random.choice([2,2,2,2,2,2,2,2,2,4])
        self._row = random.choice(range(self._height))
        self._col = random.choice(range(self._width))
        if min(min(self._cells)) == 0:
            while self._cells[self._row][self._col] != 0:
                self._row = random.choice(range(self._height))
                self._col = random.choice(range(self._width))
            self.set_tile(self._row, self._col, self._tile)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._cells[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._cells[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
