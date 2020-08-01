# Xander Houdek
# 07/28/20
# minesweeper.py - a clone of the game Minesweeper, used for my
# CS325 Algorithms portfolio project

import sys
import random
import time
import pygame
from pygame.locals import *


ICON = pygame.image.load("./Portfolio/ms_icon.png")

# CONSTANTS
BG = (211, 211, 211)
GRAY = (127, 127, 127)
MED_GRAY = (100, 100, 100)
DARK_GRAY = (75, 75, 75)
WHITE = (250, 250, 250)
YELLOW = (242, 242, 109)
BLUE = (51, 51, 255)
GREEN = (0, 125, 0)
RED = (225, 0, 0)
NAVY = (0, 0, 102)
MAROON = (170, 1, 20)
TURQUOISE = (0, 153, 153) 
BLACK = (0, 0, 0)

DIFFICULTY = [  # (grid size, # of mines)
    (8, 10),    # easy
    (16, 40),   # medium
    (24, 99)    # hard
]
TEXT_COLOR = [
    BLUE, GREEN, RED, NAVY, MAROON, TURQUOISE, BLACK, MED_GRAY
]


class Button:
    """A class to represent a menu button"""

    def __init__(self, x, y, width, height, text='', color=GRAY):
        """Set dimensions and properties of button"""

        self.x = x
        self.y = y
        self.width, self.height =width, height
        self.color = color
        self.text_color = WHITE
        self.text = text
        self.font = pygame.font.SysFont(None, 48)

    def draw(self, win):
        """Draws button onto screen"""
        
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont(None, 48)
            text = font.render(self.text, 1, self.text_color)
            win.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 - text.get_height()//2)))

    def is_over(self, pos):
        """Determines if mouse position is over the button"""
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


class Cell:
    """A class to represent each cell on the board"""

    def __init__(self, x, y, level, cells):
        self.x = x 
        self.y = y
        self.width = 750//level[0] - 5
        self.height = 750//level[0] - 5
        self.x_pos = 5 + (self.width + 5) * self.x
        self.y_pos = 105 + (self.height + 5) * self.y
        self.color = MED_GRAY
        self.visible = False
        self.flag = False
        self.mine = False
        self.number = 0
        self.text_color = None
        self.cells = cells
        self.level = level

    def show_cell(self):
        self.visible = True
        self.color = BG
        if self.mine == True:
            self.color = MAROON
            return False
        if self.number == 0:
            proximity = [
            (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)
            ]
            for mod in proximity:
                oob = [-1, self.level[0]]   # out of bounds
                if self.y+mod[1] not in oob and self.x+mod[0] not in oob:
                    if self.cells[self.y+mod[1]][self.x+mod[0]].visible == False:
                        self.cells[self.y+mod[1]][self.x+mod[0]].show_cell()

    def set_flag(self):
        if self.flag == False:
            self.flag = True
            return True
        else:
            self.flag = False
            return False

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x_pos,self.y_pos,self.width,self.height), 0)

        if self.number != 0 and self.visible == True:
            font = pygame.font.SysFont(None, 48)
            text = font.render(str(self.number), 1, self.text_color)
            win.blit(text, (self.x_pos + (self.width//2 - text.get_width()//2), self.y_pos + (self.height//2 - text.get_height()//2)))

    def is_over(self, pos):
        """Determines if mouse position is over the button"""
        if pos[0] > self.x_pos and pos[0] < self.x_pos + self.width:
            if pos[1] > self.y_pos and pos[1] < self.y_pos + self.height:
                return True
        return False


class Menu:
    """A class to display the difficulty menu"""

    def __init__(self):
        """Set up screen and buttons"""

        # set up screen
        pygame.init()
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((300, 480))
        pygame.display.set_caption("Minesweeper Menu")

        # set up buttons
        self.instructions = Button(50, 20, 200, 100, "Select Difficulty", BG)
        self.easy = Button(50, 130, 200, 100, "Easy")
        self.medium = Button(50, 240, 200, 100, "Medium")
        self.hard = Button(50, 350, 200, 100, "Hard")
        self.buttons = [self.easy, self.medium, self.hard]

    def start(self):
        """Run menu"""

        running = True
        while running:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == QUIT:
                    running = False

                # start game with selected difficulty if clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.easy.is_over(pos):
                        print("Difficulty selected: easy")
                        self.start_game(0)
                    elif self.medium.is_over(pos):
                        print("Difficulty selected: medium")
                        self.start_game(1)
                    elif self.hard.is_over(pos):
                        print("Difficulty selected: hard")
                        self.start_game(2)

                # change button color in event of mouseover
                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons:
                        if button.is_over(pos):
                            button.color = DARK_GRAY
                        else:
                            button.color = GRAY

            self.draw()

    def draw(self):
        """Resets screen attributes and draws buttons to screen"""

        # screen attributes
        self.screen = pygame.display.set_mode((300, 480))
        pygame.display.set_caption("Minesweeper Menu")
        self.screen.fill(BG)

        # button attributes
        self.instructions.draw(self.screen)
        self.instructions.text_color = DARK_GRAY
        self.easy.draw(self.screen)
        self.medium.draw(self.screen)
        self.hard.draw(self.screen)

        pygame.display.update()

    def start_game(self, difficulty):
        """Starts game with selected difficulty"""
        game = Game(difficulty)
        game.play()


class Game:
    """Displays the game"""

    def __init__(self, difficulty):
        """Set up board and game state attributes"""
        pygame.init()
        self.screen = pygame.display.set_mode((750, 900))
        pygame.display.set_caption("Minesweeper")
        self.level = DIFFICULTY[difficulty] # gives tuple containing grid size and number of mines
        self.state = "IN_PROGRESS"
        self.flags = 0
        self.font = pygame.font.SysFont(None, 48)
        
        # initialize all cells in a matrix
        self.cells = []
        for y in range(self.level[0]):
            self.cells.append([])
            for x in range(self.level[0]):
                self.cells[y].append(Cell(x, y, self.level, self.cells))

        # randomly set mines according to difficulty
        for _ in range(self.level[1]):
            searching = True
            while searching:
                x = random.randint(0, self.level[0] - 1)
                y = random.randint(0, self.level[0] - 1)
                if self.cells[y][x].mine == False:
                    self.cells[y][x].mine = True
                    searching = False

        # assign numbers to each cell depending on mine proximity
        proximity = [
            (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)
            ]
        for row in self.cells:
            for cell in row:
                for mod in proximity:
                    if cell.mine == False:
                        oob = [-1, self.level[0]]   # out of bounds
                        if cell.y+mod[1] not in oob and cell.x+mod[0] not in oob:
                            if self.cells[cell.y+mod[1]][cell.x+mod[0]].mine == True:
                                cell.number += 1
                if cell.number != 0:                
                    cell.text_color = TEXT_COLOR[cell.number - 1]

        # reveal first cell
        searching = True
        while searching:
            x = random.randint(0, self.level[0] - 1)
            y = random.randint(0, self.level[0] - 1)
            if self.cells[y][x].number == 0 and self.cells[y][x].mine == False:
                self.cells[y][x].show_cell()
                searching = False

    def display_info(self):
        if self.state == "IN_PROGRESS":
            text = self.font.render("Mines: " + str(self.level[1]), True, DARK_GRAY)
            text_x = text.get_rect().width
            text_y = text.get_rect().height
            self.screen.blit(text, ((150 - (text_x // 2)),(50 - (text_y // 2))))
            text = self.font.render("Flags: " + str(self.flags), True, DARK_GRAY)
            text_x = text.get_rect().width
            text_y = text.get_rect().height
            self.screen.blit(text,((350 - (text_x // 2)),(50 - (text_y // 2))))

        elif self.state == "WON":
            text = self.font.render("You Win!", True, DARK_GRAY)
            text_x = text.get_rect().width
            text_y = text.get_rect().height
            self.screen.blit(text,((150 - (text_x // 2)),(50 - (text_y // 2))))

        elif self.state == "LOST":
            text = self.font.render("Game Over", True, DARK_GRAY)
            text_x = text.get_rect().width
            text_y = text.get_rect().height
            self.screen.blit(text,((150 - (text_x // 2)),(50 - (text_y // 2))))

    def display_cells(self):
        for row in self.cells:
            for cell in row:
                cell.draw(self.screen)

    def play(self):
        running = True
        paused = False
        while running:       
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == QUIT:
                    running = False

                if not paused:
                    # change cell color in event of mouseover
                    if event.type == pygame.MOUSEMOTION:
                        for row in self.cells:
                            for cell in row:
                                if cell.flag == True:
                                    cell.color = YELLOW
                                elif cell.visible == False and cell.flag == False:
                                    if cell.is_over(pos):
                                        cell.color = DARK_GRAY
                                    else:
                                        cell.color = MED_GRAY

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 3:    # right click
                            for row in self.cells:
                                for cell in row:
                                    if cell.visible == False:
                                        if cell.is_over(pos):
                                            flag = cell.set_flag()
                                            if flag == True:
                                                self.flags += 1
                                                cell.color = YELLOW
                                            else:
                                                self.flags -= 1
                                                cell.color = DARK_GRAY

                        if event.button == 1:   # left click
                            for row in self.cells:
                                for cell in row:
                                    if cell.visible == False:
                                        if cell.is_over(pos):
                                            state = cell.show_cell()
                                            if state == False:
                                                self.state = "LOST"
                                                paused = True
                                            if cell.flag == True:
                                                cell.flag = False
                                                cell.color = BG
                                                self.flags -= 1

            victory = self.check_victory()
            if victory == True:
                self.state = "WON"
                paused = True
                
            self.draw()

    def draw(self):
        self.screen.fill(BG)
        self.display_info()
        self.display_cells()
        pygame.display.update()

    def check_victory(self):
        hidden_cells = 0
        for row in self.cells:
            for cell in row:
                if cell.visible == False:
                    hidden_cells += 1
        if hidden_cells == self.level[1]:
            return True
        return False

def main():
    menu = Menu()
    menu.start()

if __name__ == "__main__":
    main()