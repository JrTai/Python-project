"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import user39_dCvjpgvQ3O_0 as poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)      
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for item in self._zombie_list:
            yield item

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for item in self._human_list:
            yield item
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = poc_grid.Grid(poc_grid.Grid.get_grid_height(self), poc_grid.Grid.get_grid_width(self))
        distance_field = [[poc_grid.Grid.get_grid_width(self) * poc_grid.Grid.get_grid_height(self) 
                             for dummy_col in range(poc_grid.Grid.get_grid_width(self))]
                             for dummy_row in range(poc_grid.Grid.get_grid_height(self))]
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            item_list = self.zombies()
        else:
            item_list = self.humans()
        for item in item_list:
            boundary.enqueue(item)
            visited.set_full(item[0], item[1])
            distance_field[item[0]][item[1]] = 0
        while boundary.__len__() != 0:
            current_cell = boundary.dequeue()
            neighbor_cells = visited.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbor_cells:
                if visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
        return distance_field
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        #visited = poc_grid.Grid(poc_grid.Grid.get_grid_height(self), poc_grid.Grid.get_grid_width(self))
        final_moves = []
        for item in self._human_list:
            neighbor_cells = self.eight_neighbors(item[0], item[1])
            max_list = [zombie_distance[neighbor[0]][neighbor[1]] for neighbor in neighbor_cells]
            move = []
            for index in range(len(max_list)):
                if max_list[index] == poc_grid.Grid.get_grid_width(self) * poc_grid.Grid.get_grid_height(self):
                    max_list[index] = float("-inf")
            for index in range(len(max_list)):    
                if max_list[index] == max(max_list) and self.is_empty(neighbor_cells[index][0], neighbor_cells[index][1]):
                    move.append(neighbor_cells[index])
            if len(move) != 0:
                final_moves.append(random.choice(move))
            else:
                final_moves.append(item)
        self._human_list = [item for item in final_moves]    
            
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        #visited = poc_grid.Grid(poc_grid.Grid.get_grid_height(self), poc_grid.Grid.get_grid_width(self))
        final_moves = []
        for item in self._zombie_list:
            neighbor_cells = self.four_neighbors(item[0], item[1])
            min_list = [human_distance[neighbor[0]][neighbor[1]] for neighbor in neighbor_cells]
            move = []
            for index in range(len(min_list)):
                if min_list[index] == poc_grid.Grid.get_grid_width(self) * poc_grid.Grid.get_grid_height(self):
                    min_list[index] = float("inf")
            for index in range(len(min_list)):    
                if min_list[index] == min(min_list) and self.is_empty(neighbor_cells[index][0], neighbor_cells[index][1]):
                    move.append(neighbor_cells[index])
            if len(move) != 0 and item not in self._human_list:
                final_moves.append(random.choice(move))
            else:
                final_moves.append(item)
        self._zombie_list = [item for item in final_moves] 

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))
