import pygame
from random import choice, randrange

TILE = 50
cols, rows = 5,5
RES = WIDTH, HEIGHT = cols * TILE, rows * TILE
MARGIN = TILE // 4
time = 5

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
text_font = pygame.font.SysFont('Arial', 20)
grid_cells = [] * rows

## PERFORMANCE PARAMETER ## 
steps_count = 1
visited_count = 1
total_cell = cols * rows

#########################################
##     PYGAME DISPLAY MODULE / GUI     ##
#########################################
def drawText(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    sc.blit(img, (x, y))

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

def drawCircle(x, y, color):
    pygame.draw.circle(sc, pygame.Color(color), (x * TILE + TILE // 2, y * TILE + TILE // 2), TILE // 3, width=3)

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
        self.id = (y * cols) + x + 1
        self.walls = {'N': False, 'S': False, 'W': False, 'E': False}
        self.flag = False
        self.visited = False

    def draw(self):
        # draw sqaure
        if self.visited:
            drawSquare(self.x, self.y, 'blue')
        else: 
            drawSquare(self.x, self.y, 'black')
        
        if self.flag:
            drawSmallerSquare(self.x, self.y, 'orange')
            
        number = self.y * cols + self.x + 1
        id = number.__str__()
        drawText(id, text_font, (255,255,255), self.x*TILE + MARGIN, self.y*TILE + MARGIN)
        
        for d in 'NSWE':
            if self.walls[d] == False:
                drawWall(self.x, self.y, d)

    def draw_current(self, color):
        drawSquare(self.x, self.y, color)

    def get_cell(self, x, y):
        if x < 0 or x > cols-1 or y < 0 or y > rows-1:
            return False
        return grid_cells[y][x]

    # direction is ENSW
    def get_neighbours(self):
        neighbours = []
        # retrieve all neighbour
        n = self.get_cell(self.x, self.y - 1)
        s = self.get_cell(self.x, self.y + 1)
        w = self.get_cell(self.x - 1, self.y)
        e = self.get_cell(self.x + 1, self.y)
        
        if e and not e.visited:
            if self.walls['E']:
                neighbours.append(e)
        if n and not n.visited:
            if self.walls['N']:
                neighbours.append(n)
        if w and not w.visited:
            if self.walls['W']:
                neighbours.append(w)
        if s and not s.visited:
            if self.walls['S']:
                neighbours.append(s)
        return neighbours
    
    # randomly pick a neighbour if not zero
    def pick_neighbour(self):
        neighbours = self.get_neighbours()
        if len(neighbours) > 0:
            return choice(neighbours)
        return False
        
    # return path to nearest unvisited cell !!!
    def bfs_unvisited(self, deadends):
        # this adjacent flag is intended to avoid prioritising adjacent deadends
        # !important note! this will create another loophole, on stub deadends. Where the adjancent itself is the true deadends
        adjacent = len(self.get_neighbours()) + 1
        start=(self.x, self.y)
        frontier = [start]
        explored = [start]
        bfsPath = {}    
        currCell = self
        while len(frontier) > 0:
            current=frontier.pop(0)
            
            # pause
            drawCircle(current[0], current[1], 'red')
            pygame.display.update()
            n = input()

            currCell = self.get_cell(current[0], current[1])
            adjacent -= 1
            # break if we find a deadend. else settle with nearest unvisited
            # if not currCell.visited:
            if deadends:
                if current in deadends and adjacent < 0:
                    deadends.remove(current)
                    break
            else:
                if not currCell.visited:
                    break
            
            # note, this loop can be terminated if we get the walls beforehand
            for d in 'WSNE':
                if currCell.walls[d] ==  True:
                    if d=='E':
                        child=(current[0]+1, current[1])
                    elif d=='W':
                        child=(current[0]-1, current[1])
                    elif d=='N':
                        child=(current[0], current[1]-1)
                    elif d=='S':
                        child=(current[0], current[1]+1)
                    if child in explored:
                        continue
                    frontier.append(child)
                    explored.append(child)
                    bfsPath[child]=current

        fwdPath=[]
        cell=(currCell.x, currCell.y)
        fwdPath.append(cell)
        while cell != start:
            fwdPath.append(bfsPath[cell])
            cell=bfsPath[cell]
        fwdPath.remove(start)
        return fwdPath

    # updates neighbouring cells flags in case of new deadends. this one specifically to tackle maze with loops
    # need to supply with deadends list to update also
    def update_neighbour_flags(self, deadends):
        # retrieve all neighbour
        neighbours = self.get_neighbours() 
        if len(neighbours) == 0:
            return
        
        # if total walls + visited neighbour = 3, then it is a deadend
        for nei in neighbours:
            if nei.visited or nei.flag:
                continue
            count = 0
            count += len(nei.get_neighbours())
            for d in 'WSNE':
                if nei.walls[d] == False:
                    count += 1
            if count > 2:
                nei.flag = True
                deadends.append((nei.x, nei.y))  


##########################################
##               MAZE MAPS              ##
##########################################
# 4 by 3 maze
# mazemap = {(1, 1): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (2, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (3, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (4, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 0}, (1, 2): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (3, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (4, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 3): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (3, 3): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (4, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}}
# 5 by 5 maze
# mazemap = {(1, 1): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (2, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (3, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (4, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 2): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (3, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (4, 2): {'E': 0, 'W': 0, 'N': 1, 'S': 0}, (5, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (2, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (3, 3): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (4, 3): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (1, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (2, 4): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (3, 4): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (4, 4): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 4): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 5): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 5): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (3, 5): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (4, 5): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0}}
# assignment maze
mazemap = {(1, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (2, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (3, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (4, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (5, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 0},(1, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (2, 2): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (3, 2): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (4, 2): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (5, 2): {'E': 0, 'W': 0, 'N': 1, 'S': 0}, (1, 3): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 3): {'E': 1, 'W': 1, 'N': 1, 'S': 1}, (3, 3): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (4, 3): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 3): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 4): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (3, 4): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (4, 4): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (5, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 5): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (3, 5): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (4, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (5, 5): {'E': 0, 'W': 1, 'N': 0, 'S': 0}}

# 10 by 10 maze with loop
# mazemap = {(1, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 1): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (3, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (4, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (5, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (6, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (7, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (8, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (9, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (10, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (3, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (4, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (5, 2): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (6, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (7, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 0}, (8, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (9, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (10, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 3): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (2, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (3, 3): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (4, 3): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (5, 3): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (6, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (7, 3): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (8, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (9, 3): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (10, 3): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (1, 4): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 4): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (3, 4): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (4, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (5, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (6, 4): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (7, 4): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (8, 4): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (9, 4): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (10, 4): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (1, 5): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (2, 5): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (3, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (4, 5): {'E': 0, 'W': 1, 'N': 0, 'S': 0}, (5, 5): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (6, 5): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (7, 5): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (8, 5): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (9, 5): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (10, 5): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 6): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 6): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (3, 6): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (4, 6): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (5, 6): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (6, 6): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (7, 6): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (8, 6): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (9, 6): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (10, 6): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 7): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 7): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (3, 7): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (4, 7): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (5, 7): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (6, 7): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (7, 7): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (8, 7): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (9, 7): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (10, 7): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (1, 8): {'E': 1, 'W': 1, 'N': 0, 'S': 1}, (2, 8): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (3, 8): {'E': 1, 'W': 0, 'N': 1, 'S': 1}, (4, 8): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 8): {'E': 0, 'W': 0, 'N': 1, 'S': 0}, (6, 8): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (7, 8): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (8, 8): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (9, 8): {'E': 0, 'W': 1, 'N': 0, 'S': 0}, (10, 8): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 9): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 9): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (3, 9): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (4, 9): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (5, 9): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (6, 9): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (7, 9): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (8, 9): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (9, 9): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (10, 9): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (1, 10): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (2, 10): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (3, 10): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (4, 10): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (5, 10): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (6, 10): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (7, 10): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (8, 10): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (9, 10): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (10, 10): {'E': 0, 'W': 1, 'N': 1, 'S': 0}}



## mapping generated mazemap into wall, also listing all deadends
grid_cells = [[Cell(x, y) for x in range(cols)] for y in range(rows)]
deadends = []
for y in range(rows):
    for x in range(cols):
        newCell = Cell(x, y)
        walls = mazemap[(y+1, x+1)]
        walls_count=0
        for d in 'EWNS':
            if walls[d] == 1:
                newCell.walls[d] = True
            else:
                newCell.walls[d] = False
                walls_count+=1
        grid_cells[y][x] = newCell 

        # deadend found
        if walls_count == 3:
            grid_cells[y][x].flag = True
            deadends.append((x,y))


x, y = 0,0

current = grid_cells[y][x]
current.flag = False
counter = 0

#############################################
##           MAZE EXTRA MODULES            ##
#############################################

def tranverse_bwd(current, path, deadends):
    for i in range(len(path)-1, -1, -1):
        current = change_position(current, grid_cells[path[i][1]][path[i][0]], deadends)
    return current

# function specifcally to render cells in case of any changes

def change_position(cell, next_cell, deadends):

    # remove current cell form deadend list
    if (cell.x, cell.y) in deadends:
        deadends.remove((cell.x, cell.y))
    
    # update the neighbours before moving to next cell
    cell.update_neighbour_flags(deadends)
    cell = next_cell

    # remove current cell from deadend list
    if (cell.x, cell.y) in deadends:
        deadends.remove((cell.x, cell.y))
    

    draw_all()
    cell.draw_current('red')  
    global visited_count 
    if cell.visited == False:
        cell.visited = True
        visited_count += 1
    cell.flag = False

    pygame.display.flip()
    # pause
    n = input()
    clock.tick(time)

    ### check for finish
    global steps_count
    global total_cell
    if (visited_count==total_cell):
        print('Greedy BFS finished with', steps_count, 'steps.')
        steps_count = 1
        visited_count = 1
        return None
    else:
        steps_count += 1

    return cell


# set a copy list of deadend cells
current_deadends = deadends.copy()
current.visited = True

def run(current, current_deadends):      
    while True:
        sc.fill(pygame.Color('darkslategray'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        draw_all()
        current.draw_current('red')
        pygame.display.flip()   

        
        # if only possible way to go is that one cell
        while len(current.get_neighbours()) == 1:
            nei = current.get_neighbours()
            # the cell also must be unvisited
            if nei[0].visited == False:
                current = change_position(current, nei[0], current_deadends)
                if current == None:
                    return
            else:
                break
        

        # pick nearest deadend, else unvisited cell
        current = tranverse_bwd(current, current.bfs_unvisited(current_deadends), current_deadends)
        if current == None:
            return  

while True:
    run(current, current_deadends)
    for row in grid_cells:
        for cell in row:
            if (cell.x, cell.y) in deadends:
                cell.flag = True
            cell.visited = False
    current = grid_cells[0][0]
    current.visited = True
    current_deadends = deadends.copy()
    steps_count = 1
    visited_count = 1