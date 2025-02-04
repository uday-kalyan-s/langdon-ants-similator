import pygame
from models import Grid, Ant

height = 80
width = 150
speed = 150
cell_size = 10
ant_count = 1

pygame.init()
screen = pygame.display.set_mode((width*cell_size, height*cell_size))
clock = pygame.time.Clock()
running = True

grid = Grid(width, height)
grid.populate()

ants = [Ant(id, width, height, grid) for id in range(ant_count)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for row_num, row in enumerate(grid.cells):
        for col_num, cell in enumerate(row):
            color = cell.color
            for ant in ants:
                if ant.row == row_num and ant.col == col_num:
                   color = "red" 
            pygame.draw.rect(screen, color, pygame.Rect(cell_size*col_num, cell_size*row_num, cell_size, cell_size))

    for ant in ants:
        ant.make_move()
    grid.deprecate_pheromones()

    pygame.display.flip()
    
    #clock.tick(speed)

pygame.quit()
