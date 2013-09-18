#!/usr/bin/env python

import pygame
import board
import player
from gui import Gui
from config import BLACK, WHITE

class Othello:

    def __init__(self):
        self.board = board.Board()
        self.gui = Gui()
        self.setup_game()
        
    def setup_game(self):
        self.now_playing = player.Human(BLACK)
        self.other_player = player.RandomPlayer(WHITE)
        self.board.print_board()
        self.gui.show_options()
        self.gui.show_game()

    def run ( self ):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            winner = self.board.game_won()
            if winner is not None:
                break
            self.now_playing.set_current_board(self.board)
            if self.board.get_valid_moves(self.now_playing.color) != []:
                score, self.board = self.now_playing.get_move()
                print 'White Pieces:', self.board.white_pieces,
                print ' Black Pieces:', self.board.black_pieces
                self.board.print_board()
            self.now_playing, self.other_player = self.other_player, self.now_playing
        print "Game Won By: " + str(winner)
        pygame.time.wait(1000)
        self.restart()

    def restart( self ):
        self.board = board.Board()
        self.setup_game()
        self.run()

def main():
    game = Othello()
    game.run()

if __name__ == '__main__':
    main()
