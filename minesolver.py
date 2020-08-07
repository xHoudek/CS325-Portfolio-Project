# Xander Houdek
# 08/02/20
# minesolver.py - automatically solves a game of minesweeper.py, used for
# my CS325 Algorithms portfolio project

import random
import pygame
from pygame.locals import *
from minesweeper import *

# Global constant, used to check all adjacent cells
PROXIMITY = [
            (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)
            ]


class ModdedGame(Game):
    def __init__(self, difficulty):
        Game.__init__(self, difficulty)
        self.completed_cells = []


    def check_cell(self, cell):
        """
        Checks a cell to see if it is possible to add flags and does so if possible.
        Checks to see if all flags are checked and reveals other cells if possible.
        Adds cell to list of completed cells to be skipped if possible.
        """

        # check adjacent cells for flags and visibility
        adj_flags = 0
        hidden_cells = 0
        did_something = False
        for mod in PROXIMITY:
            oob = [-1, cell.level[0]]   # out of bounds
            if cell.y+mod[1] not in oob and cell.x+mod[0] not in oob:
                neighbor = self.cells[cell.y+mod[1]][cell.x+mod[0]]
                if neighbor.visible == False:
                    hidden_cells += 1
                if neighbor.flag == True:
                    adj_flags += 1

        # add flags
        if hidden_cells == cell.number:
            for mod in PROXIMITY:
                oob = [-1, cell.level[0]]   # out of bounds
                if cell.y+mod[1] not in oob and cell.x+mod[0] not in oob:
                    neighbor = self.cells[cell.y+mod[1]][cell.x+mod[0]]
                    if neighbor.flag == False and neighbor.visible == False:
                        flag = neighbor.set_flag()
                        did_something = True
                        if flag == True:
                            self.flags += 1
                            neighbor.color = YELLOW
                        else:
                            self.flags -= 1
                            neighbor.color = DARK_GRAY
                        self.draw()

        # reveal cells
        if adj_flags == cell.number:
            for mod in PROXIMITY:
                oob = [-1, cell.level[0]]   # out of bounds
                if cell.y+mod[1] not in oob and cell.x+mod[0] not in oob:
                    neighbor = self.cells[cell.y+mod[1]][cell.x+mod[0]]
                    if neighbor.flag == False and neighbor.visible == False:
                        state = neighbor.show_cell()
                        did_something = True
                        if state == False:
                            self.state = "LOST"
                            solved = True
                        if cell.flag == True:
                            cell.flag = False
                            cell.color = BG
                            self.flags -= 1
                        self.draw()

        # add cell to completed_cells
        if hidden_cells == adj_flags:
            self.completed_cells.append(cell)
            did_something = True

        return did_something

    def play(self):
        self.draw()
        running = True
        solved = False
        count = 0
        while running:

            # solving algorithm
            if not solved:
                did_nothing = True
                for row in self.cells:
                    for cell in row:
                        if cell.visible == True and cell.number != 0:
                            if cell not in self.completed_cells:
                                mid_x = cell.x_pos + cell.length // 2
                                mid_y = cell.y_pos + cell.length // 2
                                pygame.mouse.set_pos((mid_x, mid_y))
                                did_something = self.check_cell(cell)
                                if did_something == True:
                                    did_nothing = False
                                #self.draw()
                if did_nothing == True:
                    guess = self.make_guess()
                    if guess == False:
                        solved = True
                count += 1
                print(count)

            # quit game
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN and event.key == K_q:
                    running = False

            victory = self.check_victory()
            if victory == True:
                self.state = "WON"
                solved = True

            self.draw()

    def make_guess(self):

        print("The game is currently unsolvable without guessing.")
        print("The program will make a random guess.")
        print()
                                
        # pick a random unflagged cell
        searching = True
        while searching:
            x = random.randint(
                0, self.level[0] - 1)
            y = random.randint(0, self.level[0] - 1)
            cell = self.cells[y][x]
            if cell.flag == False and cell.visible == False:
                searching = False
                mid_x = cell.x_pos + cell.length // 2
                mid_y = cell.y_pos + cell.length // 2
                pygame.mouse.set_pos((mid_x, mid_y))
                state = cell.show_cell()
                if state == False:
                    self.state = "LOST"
                    self.draw()
                    return False
                self.draw()
                return True


class ModdedMenu(Menu):
    def __init__(self):
        Menu.__init__(self)

    def start_game(self, difficulty):
        """Starts a modded game with selected difficulty"""
        game = ModdedGame(difficulty)
        game.play()


def main():
    print("Game made by Xander Houdek")
    print("Solver also made by Xander Houdek :)")
    print()
    menu = ModdedMenu()
    menu.start()

if __name__ == "__main__":
    main()