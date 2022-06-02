import pygame
import os

x_img = pygame.image.load(os.path.join('files','X.png'))
o_img = pygame.image.load(os.path.join('files','O.png'))

class Grid:
    def __init__(self):
        self.grid_lines = [((30, 200), (570, 200)),  # 1st horizontal
                           ((30, 400), (570, 400)),  # 2nd horizontal
                           ((200, 30), (200, 570)),  # 1st vert
                           ((400, 30), (400, 570))]  # 2nd vert
        self.grid = [[0 for x in range(3)] for y in range(3)] # create matrix 3x
        self.switch_player = True
        # search direction  N NW W WN
        self.search_directions = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1),(1, 0), (1, -1)]
        self.game_over = False


    def draw(self, window):
        for line in self.grid_lines:
            pygame.draw.line(window, (137,101,173), line[0], line[1], 2)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x,y) == 'X':
                    window.blit(x_img, (x*200, y*200))
                elif self.get_cell_value(x,y) == 'O':
                    window.blit(o_img, (x*200, y*200))


    def get_cell_value(self, x, y):
        return self.grid[y][x]

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    def get_mouse(self, x, y, player):
        if self.get_cell_value(x,y) == 0: # change X O onle if the cell is empty
            self.set_cell_value(x,y,player)
            self.check_grid(x,y,player)

    def within_bounds(self, x,y):
        return x >=0 and x < 3 and y >= 0 and y <3

    def check_grid(self, x, y, player):
        count = 1
        for index, (dirx, diry) in enumerate(self.search_directions):
            if self.within_bounds(x+dirx, y+diry) and self.get_cell_value(x+dirx, y+diry) == player:
                count += 1
                xx = x + dirx
                yy = y + diry
                if self.within_bounds(xx+dirx, yy+diry) and self.get_cell_value(xx+dirx, yy+diry) == player:
                    count += 1
                    if count == 3:
                        break
                if count < 3:
                    new_dir = 0
                    # mapping the indices to opposite direction: 0-4 1-5 2-6 3-7 4-0 5-1 6-2 7-3
                    if index == 0:
                        new_dir = self.search_directions[4] # N to S
                    elif index == 1:
                        new_dir = self.search_directions[5] # NW to SE
                    elif index == 2:
                        new_dir = self.search_directions[6] # W to E
                    elif index == 3:
                        new_dir = self.search_directions[7] # SW to NE
                    elif index == 4:
                        new_dir = self.search_directions[0] # S to N
                    elif index == 5:
                        new_dir = self.search_directions[1] # SE to NW
                    elif index == 6:
                        new_dir = self.search_directions[2] # E to W
                    elif index == 7:
                        new_dir = self.search_directions[3] # NE to SW

                    if self.within_bounds(x + new_dir[0], y + new_dir[1]) and self.get_cell_value(x + new_dir[0], y + new_dir[1]) == player:
                        count += 1
                        if count == 3:
                            break
                    else:
                        count = 1

        if count == 3:
            print(player, 'wins!')
            self.game_over = True
        else:
            self.game_over = self.grid_full()

    def clear_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.set_cell_value(x, y, 0)

    def grid_full(self):
        for row in self.grid:
            for value in row:
                if value == 0:
                    return False
        return True

    def print_grid(self):
        for row in self.grid:
            print(row)