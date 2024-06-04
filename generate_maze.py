from pyamaze import maze, agent
import pygame


RES = WIDTH, HEIGHT = 502, 502
TILE = 100
cols, rows = WIDTH // TILE, HEIGHT // TILE

cols, rows = 3,3
# class Cell
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False


grid = [{}]  * 4


m=maze(10,10)

'''
{(1, 1): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, 
(2, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, 
(3, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, 
(4, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 0}, (1, 2): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (3, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (4, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 3): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (3, 3): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (4, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}}
'''

# m.CreateMaze(loadMaze='maze--2024-05-08--21-42-16.csv') # 2 by 2 maze
# m.CreateMaze(loadMaze='maze--2024-05-13--23-00-08.csv')  # 3 by 3 maze
# m.CreateMaze(loadMaze='sample4by3.csv')  # 4 by 3 maze
# m.CreateMaze(loadMaze='s1_5by5.csv')  # 5 by 5 maze

m.CreateMaze(loopPercent = 5)
# print(m.maze_map)
print(m.maze_map)
# 5 by 5 still fail
# m.mazemap = {(1, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (3, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (4, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (2, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 0}, (3, 2): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (4, 2): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 2): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (1, 3): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 3): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (3, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (4, 3): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (5, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (1, 4): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 4): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (3, 4): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (4, 4): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (5, 4): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 5): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0}, (3, 5): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (4, 5): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (5, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0}}

# mazemap = {
    # (1, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, 
    # (2, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, 
    # (1, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, 
    # (2, 2): {'E': 0, 'W': 1, 'N': 1, 'S': 0}
# }


'''
1,1 2,1 
1,2 2,2 

0,0 0,1
'''

m.run()

# for i in range(cols):
#     for j in range(rows):
#         walls = mazemap[(i+1,j+1)]
#         cell = Cell(i,j)
#         for d in 'ENSW':
#             cell.walls[d] = walls[d]
#         grid[cols * i + j] = cell
#         print(grid[cols * i + j].walls)


# print(mazemap)
# print(mazemap[(1,1)])


