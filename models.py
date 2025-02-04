from enum import Enum
import random

class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3

    @classmethod
    def rotate_clockwise(cls, direction):
        return cls

    @classmethod
    def rotate_anticlockwise(cls, direction):
        pass

    @classmethod
    def get_movement_vector(cls, direction):
        pass

directions = [(-1,0), (0,1), (1,0), (0,-1)]
def get_clock(direc):
    return directions[(directions.index(direc)+1)%4]

def get_anticlock(direc):
    return directions[(directions.index(direc)-1)%4]

class Cell:
    def __init__(self) -> None:
        #self.color = random.choice(["black","white"])
        self.color = "white"
        self.pheromone_id = None
        self.pheromone_life = 0
    
    def get_descision(self, ant_id, direction):
        if ant_id == self.pheromone_id:
            straight_weight = self.pheromone_life * 0.8
            straight_choice = random.choices([True, False], weights=[straight_weight, 1-straight_weight], k=1)
            if straight_choice:
                return direction
        elif self.pheromone_id is not None: # check logic impl if low life does turn prob inc or dec
            straight_weight = self.pheromone_life * 0.2
            straight_choice = random.choices([True, False], weights=[straight_weight, 1-straight_weight], k=1)
            if straight_choice:
                return direction
        # ant doesnt detect pheromone or choice was denied (literally 1984)
        if self.color == "white":
            return get_clock(direction)
        else:
            return get_anticlock(direction)

    def flip(self):
        self.color = "black" if self.color == "white" else "white"

    def add_pheromone(self, ant_id):
        self.pheromone_id = ant_id
        self.pheromone_life = 5

    def reduce_pheromone_life(self):
        if self.pheromone_id is not None:
            self.pheromone_life -= 1
        if self.pheromone_life == 0:
            self.pheromone_id = None


class Grid:
    def __init__(self, width, height) -> None:
        self.cells = [[Cell() for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height

    def deprecate_pheromones(self):
        for row in self.cells:
            for cell in row:
                cell.reduce_pheromone_life()

class Ant:
    def __init__(self, id, width, height, grid) -> None:
        self.id = id
        self.row = random.randint(0, height)
        self.col = random.randint(0, width)
        self.direction = random.choice(directions)
        self.grid = grid

    def make_move(self):
        cur_cell = self.grid.cells[self.row][self.col]
        move_dir = cur_cell.get_descision(self.id, self.direction)
        self.direction = move_dir
        self.row += move_dir[0] # :P space wrapping plane
        self.col += move_dir[1]
        
        self.row = self.row%self.grid.height
        self.col = self.col%self.grid.width

        cur_cell.flip()
        cur_cell.add_pheromone(self.id)
