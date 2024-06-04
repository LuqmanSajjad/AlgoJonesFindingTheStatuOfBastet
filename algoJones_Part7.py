import pygame
from random import choice, randrange

TILE = 50
cols, rows = 10,10
RES = WIDTH, HEIGHT = cols * TILE, rows * TILE
MARGIN = TILE // 4
CLOCK_SPEED = 15

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
text_font = pygame.font.SysFont('Arial', 20)
grid_cells = [] * rows

## image assets
algoJones = pygame.image.load('assets/algojones.png')
snake = pygame.image.load('assets/snake.png')
monster = pygame.image.load('assets/ghost.png')
coin = pygame.image.load('assets/coin.png')

## PERFORMANCE PARAMETER ## 
steps_count = 1
visited_count = 1
total_cell = cols * rows

#########################################
##       PYGAME DISPLAY MODULE         ##
#########################################

def drawWall(x, y, orientation):
    x1, y1, x2, y2 = x, y, x, y
    if orientation == 'N':
        x1, y1, x2, y2 = x, y, x + 1, y
    elif orientation == 'S':
        x1, y1, x2, y2 = x, y + 1, x + 1, y + 1
    elif orientation == 'W':
        x1, y1, x2, y2 = x, y, x, y + 1
    elif orientation == 'E':
        x1, y1, x2, y2 = x + 1, y, x + 1, y + 1

    pygame.draw.line(sc, pygame.Color('orange'), (x1 * TILE, y1 * TILE), (x2 * TILE, y2 * TILE), 4)

def drawSquare(x, y, color):
    pygame.draw.rect(sc, pygame.Color(color), (x * TILE, y * TILE, TILE, TILE))

def drawSmallerSquare(x, y, color):
    margin = TILE // 4
    pygame.draw.rect(sc, pygame.Color(color), (x * TILE + margin, y * TILE + margin, TILE//2, TILE//2))

def draw_all():
    for i in range(rows):
        for j in range(cols):
            grid_cells[i][j].draw()


##########################################
##               CELL CLASS             ##
##########################################
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'N': False, 'S': False, 'W': False, 'E': False}
        self.flag = False

    def draw(self):
        # draw sqaure
        drawSquare(self.x, self.y, 'black')
        if self.flag:
            sc.blit(coin, (self.x * TILE, self.y * TILE))
            
        number = self.y * cols + self.x + 1
        id = number.__str__()
        
        for d in 'NSWE':
            if self.walls[d] == False:
                drawWall(self.x, self.y, d)

    def draw_current(self, color):
        drawSquare(self.x, self.y, color)

    def get_cell(self, x, y):
        if x < 0 or x > cols-1 or y < 0 or y > rows-1:
            return None
        return grid_cells[y][x]

    # direction is ENSW
    def get_neighbours(self):
        neighbours = []
        # retrieve all neighbour
        n = self.get_cell(self.x, self.y - 1)
        s = self.get_cell(self.x, self.y + 1)
        w = self.get_cell(self.x - 1, self.y)
        e = self.get_cell(self.x + 1, self.y)
        
        if self.walls['E']:
            neighbours.append(e)
        if self.walls['N']:
            neighbours.append(n)
        if self.walls['W']:
            neighbours.append(w)
        if self.walls['S']:
            neighbours.append(s)
        return neighbours
    
    # randomly pick a neighbour if not zero
    def pick_neighbour(self):
        neighbours = self.get_neighbours()
        if len(neighbours) > 0:
            return choice(neighbours)
        return False

    def get_neighbour_in_direction(self, direction):
        if direction == 'N':
            if self.walls['N']:
                return self.get_cell(self.x, self.y - 1)
        elif direction == 'S':
            if self.walls['S']:
                return self.get_cell(self.x, self.y + 1)
        elif direction == 'W':
            if self.walls['W']:
                return self.get_cell(self.x - 1, self.y)
        elif direction == 'E':
            if self.walls['E']:
                return self.get_cell(self.x + 1, self.y)
        return False


##########################################
##               MAZE MAPS              ##
##########################################
# 4 by 3 maze
# mazemap = {(1, 1): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (2, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (3, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (4, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 0}, (1, 2): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (3, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (4, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 3): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (3, 3): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (4, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}}
# 5 by 5 maze
# mazemap = {(1, 1): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (2, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (3, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (4, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 2): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (3, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (4, 2): {'E': 0, 'W': 0, 'N': 1, 'S': 0}, (5, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (2, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (3, 3): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (4, 3): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (1, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (2, 4): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (3, 4): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (4, 4): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 4): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 5): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 5): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (3, 5): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (4, 5): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0}}
# assignment maze
mazemap = {(1, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, 
            (2, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, 
            (3, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, 
            (4, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, 
            (5, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 0},

            (1, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, 
            (2, 2): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, 
            (3, 2): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, 
            (4, 2): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, 
            (5, 2): {'E': 0, 'W': 0, 'N': 1, 'S': 0}, 

            (1, 3): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, 
            (2, 3): {'E': 1, 'W': 1, 'N': 1, 'S': 1}, 
            (3, 3): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, 
            (4, 3): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, 
            (5, 3): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, 

            (1, 4): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, 
            (2, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, 
            (3, 4): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, 
            (4, 4): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, 
            (5, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, 

            (1, 5): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, 
            (2, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, 
            (3, 5): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, 
            (4, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, 
            (5, 5): {'E': 0, 'W': 1, 'N': 0, 'S': 0}}

# 10 by 10 maze with loop
mazemap = {(1, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 1): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (3, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (4, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (5, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (6, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (7, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (8, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (9, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (10, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (3, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (4, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (5, 2): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (6, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (7, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 0}, (8, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (9, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (10, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 3): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (2, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (3, 3): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (4, 3): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (5, 3): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (6, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (7, 3): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (8, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (9, 3): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (10, 3): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (1, 4): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 4): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (3, 4): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (4, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (5, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (6, 4): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (7, 4): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (8, 4): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (9, 4): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (10, 4): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (1, 5): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (2, 5): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (3, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (4, 5): {'E': 0, 'W': 1, 'N': 0, 'S': 0}, (5, 5): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (6, 5): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (7, 5): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (8, 5): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (9, 5): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (10, 5): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 6): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 6): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (3, 6): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (4, 6): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (5, 6): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (6, 6): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (7, 6): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (8, 6): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (9, 6): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (10, 6): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 7): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 7): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (3, 7): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (4, 7): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (5, 7): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (6, 7): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (7, 7): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (8, 7): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (9, 7): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (10, 7): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (1, 8): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (2, 8): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (3, 8): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (4, 8): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 8): {'E': 0, 'W': 0, 'N': 1, 'S': 0}, (6, 8): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (7, 8): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (8, 8): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (9, 8): {'E': 0, 'W': 1, 'N': 0, 'S': 0}, (10, 8): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 9): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 9): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (3, 9): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (4, 9): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (5, 9): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (6, 9): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (7, 9): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (8, 9): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (9, 9): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (10, 9): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (1, 10): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (2, 10): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (3, 10): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (4, 10): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (5, 10): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (6, 10): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (7, 10): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (8, 10): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (9, 10): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (10, 10): {'E': 0, 'W': 1, 'N': 1, 'S': 0}}

# pacman maze
mazemap = {(1, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (2, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (3, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (4, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (5, 1): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (6, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (7, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (8, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (9, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (10, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 0}, (1, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (2, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (3, 2): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (4, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (5, 2): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (6, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (7, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (8, 2): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (9, 2): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (10, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 3): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 3): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (3, 3): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (4, 3): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (5, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (6, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (7, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (8, 3): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (9, 3): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (10, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (1, 4): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (2, 4): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (3, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (4, 4): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 4): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (6, 4): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (7, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (8, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (9, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (10, 4): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 5): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (2, 5): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (3, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (4, 5): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (5, 5): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (6, 5): {'E': 1, 'W': 1, 'N': 1, 'S': 1}, (7, 5): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (8, 5): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (9, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (10, 5): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 6): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (2, 6): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (3, 6): {'E': 0, 'W': 0, 'N': 1, 'S': 0}, (4, 6): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (5, 6): {'E': 0, 'W': 0, 'N': 1, 'S': 0}, (6, 6): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (7, 6): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (8, 6): {'E': 0, 'W': 1, 'N': 0, 'S': 0}, (9, 6): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (10, 6): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (1, 7): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (2, 7): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (3, 7): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (4, 7): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (5, 7): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (6, 7): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (7, 7): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (8, 7): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (9, 7): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (10, 7): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 8): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (2, 8): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (3, 8): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (4, 8): {'E': 0, 'W': 0, 'N': 1, 'S': 0}, (5, 8): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (6, 8): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (7, 8): {'E': 1, 'W': 1, 'N': 1, 'S': 1}, (8, 8): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (9, 8): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (10, 8): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (1, 9): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (2, 9): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (3, 9): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (4, 9): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (5, 9): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (6, 9): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (7, 9): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (8, 9): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (9, 9): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (10, 9): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (1, 10): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 10): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (3, 10): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (4, 10): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (5, 10): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (6, 10): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (7, 10): {'E': 0, 'W': 0, 'N': 1, 'S': 0}, (8, 10): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (9, 10): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (10, 10): {'E': 0, 'W': 1, 'N': 1, 'S': 0}}
## mapping generated mazemap into wall, also listing all deadends
grid_cells = [[Cell(x, y) for x in range(cols)] for y in range(rows)]
deadends = []
for y in range(rows):
    for x in range(cols):
        newCell = Cell(x, y)
        walls = mazemap[(y+1, x+1)]
        for d in 'EWNS':
            if walls[d] == 1:
                newCell.walls[d] = True
            else:
                newCell.walls[d] = False
        if (y * cols + x) % 3 == 0:
            newCell.flag = True
        grid_cells[y][x] = newCell 

current = grid_cells[0][0]
ghost = grid_cells[rows-1][cols-1]
ghost2 = grid_cells[0][cols-1]
counter = 0

#############################################
##           MAZE EXTRA MODULES            ##
#############################################

def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)
    
from queue import PriorityQueue
def aStar(xs, ys, xd, yd):
    grid = [(x, y) for y in range(cols) for x in range(rows)]
    start=(xs,ys)
    g_score={cell:float('inf') for cell in grid}
    g_score[start]=0
    f_score={cell:float('inf') for cell in grid}
    f_score[start]=h(start,(xd,yd))

    open=PriorityQueue()
    # is fscore and gscore is the same
    open.put((h(start,(xd,yd)), h(start,(xd,yd)), start))
    aPath={}
    while not open.empty():

        currCell = open.get()[2]
        if currCell == (xd,yd):
            break
        
        # get list of neighbours
        neighbours = grid_cells[currCell[1]][currCell[0]].get_neighbours()  
        for nei in neighbours:
            childCell =(nei.x, nei.y)
            # update g score for the neighbours, steps from startd
            temp_g_score = g_score[currCell] + 1 
            # update f score for the neighbours, overall score
            temp_f_score = temp_g_score + h(childCell,(xd,yd))
            # assign the new score
            if temp_f_score < f_score[childCell]:
                g_score[childCell] = temp_g_score
                f_score[childCell] = temp_f_score
                open.put((temp_f_score, h(childCell,(1,1)), childCell)) 
                aPath[childCell]=currCell
        
    fwdPath=[]
    cell=(xd,yd)
    while cell!=start:
        fwdPath.append(aPath[cell])
        cell = aPath[cell]
    return fwdPath

def tranverse_bwd(cell, path):
    for coordinate in path:
        cell = grid_cells[coordinate[1]][coordinate[0]]
        draw_all()
        cell.draw_current('red')
        current.draw_current('green')
        clock.tick(1)    
        pygame.display.flip()
    return cell

moved = False 
steps, steps2 = [], []
ghostpath = []
ghostpath2 = []
cycle = 0
speed = CLOCK_SPEED/3.5
pause_time = 0

while True:
    # print('new clock tick')
    sc.fill(pygame.Color('darkslategray'))

    ## lose condition
    # if ghost == current or ghost2 == current:
    if ghost == current or ghost2 == current:
        print('You lose')
        break

    moved = False
    ## todo: make sure each clock cycle only one movement. use flag
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit()

        if moved: break

        current.flag = False

        if event.type == pygame.KEYDOWN:
            current.flag = False
            moved = True
            if event.key == pygame.K_s:
                down = current.get_neighbour_in_direction('S')
                if down: current = down
            if event.key == pygame.K_w:
                up = current.get_neighbour_in_direction('N')
                if up: current = up
            if event.key == pygame.K_a:
                left = current.get_neighbour_in_direction('W')
                if left: current = left
            if event.key == pygame.K_d:
                right = current.get_neighbour_in_direction('E')
                if right: current = right

    # pacman movement
    if steps == []:
        ghostpath = aStar(current.x, current.y, ghost.x, ghost.y)
        c =  len(ghostpath)

        if c == 0:
            print('You lose')
            break
        if c > 15: 
            c = 15

        for i in range(c):
            steps.append(ghostpath.pop(0))
    
    if steps2 == []:
        ghostpath2 = aStar(current.x, current.y, ghost2.x, ghost2.y)
        d = len(ghostpath2)
        if d == 0:
            print('You lose')
            break
        if d > 3: 
            d = 3
        for i in range(d):
            steps2.append(ghostpath2.pop(0))

    # need to break if break
            
    if cycle >= CLOCK_SPEED:
        cycle = 0
        # make ghosts move one step
        coordinate = steps.pop(0)
        ghost = grid_cells[coordinate[1]][coordinate[0]]
        coordinate = steps2.pop(0)
        ghost2 = grid_cells[coordinate[1]][coordinate[0]]
    
    cycle += speed
    draw_all()
    sc.blit(algoJones, (current.x * TILE, current.y * TILE))
    sc.blit(snake, (ghost.x * TILE, ghost.y * TILE))
    sc.blit(monster, (ghost2.x * TILE, ghost2.y * TILE))
    pygame.display.flip()
    clock.tick(CLOCK_SPEED)
## neighbour flags update should only be called when tranversing on new node