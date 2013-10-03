#!/usr/bin/env python

import pygame
import board
import player
from gui import Gui
from config import BLACK, WHITE

class Othello:

    def __init__(self):
        self.gui = Gui()
        self.setup_game()
        self.gui.show_game(self.board)

    def setup_game(self):
        #self.board.print_board()
        #self.gui.show_options()
        ans = raw_input("Will black (makes first move) be a computer player? (Y/N): ")
        if ans == "Y" or ans == "y":
            while True:
                ans = raw_input("Please enter a computer integer time limit (3 - 60): ")
                if ans.isdigit():
                    limit = int(ans)
                    if limit in range(3, 61):
                        break
            self.now_playing = player.RandomPlayer(BLACK, limit)
        else:
            self.now_playing = player.HumanPlayer(BLACK, gui=self.gui)
        ans = raw_input("Will white be a computer player? (Y/N): ")
        if ans == "Y" or ans == "y":
            while True:
                ans = raw_input("Please enter a computer integer time limit (3 - 60): ")
                if ans.isdigit():
                    limit = int(ans)
                    if limit in range(3, 61):
                        break
            self.other_player = player.RandomPlayer(WHITE, limit)
        else:
            self.other_player = player.HumanPlayer(WHITE, gui=self.gui)
        ans = raw_input("Would you like to load a board from a text file? (Y/N): ")
        if ans == "y" or ans == "y":
            infile = raw_input("Please enter filename: ")
            # TODO: Open File and Read in Current Board State
        else:
            self.board = board.Board()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            winner = self.board.game_won()
            if winner is not None:
                break
            self.now_playing.set_current_board(self.board)
            if self.board.get_valid_moves(self.now_playing.color) != []:
                score, self.board = self.now_playing.get_move()
                self.gui.update(self.board)
            self.now_playing, self.other_player = self.other_player, self.now_playing
        print "Game Won By: " + str(winner)
        pygame.time.wait(1000)
        self.restart()

    def restart(self):
        self.board = board.Board()
        self.setup_game()
        self.run()

def main():
    game = Othello()
    game.run()

if __name__ == '__main__':
    main()
