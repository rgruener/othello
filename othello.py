#!/usr/bin/env python

import board
import player
import numpy as np
from gui import Gui
from config import BLACK, WHITE, HUMAN, COMPUTER

class Othello:

    def __init__(self):
        self.gui = Gui()
        self.setup_game()

    def read_board_file(self, file_name):
        f = open(file_name)
        lines = [line.strip() for line in f]
        f.close()
        board = np.zeros((8, 8), dtype=np.integer)
        # Read In Board File
        i = 0
        for line in lines[:8]:
            j = 0
            for char in line.split():
                board[i][j] = int(char)
                j += 1
            i += 1
        # Set Current Turn
        if int(lines[8]) == WHITE:
            self.now_playing, self.other_player = self.other_player, self.now_playing

        return board

    def setup_game(self):
        options = self.gui.show_options()
        if options['player_1'] == COMPUTER:
            self.now_playing = player.ComputerPlayer(BLACK, int(options['player_1_time']), self.gui)
        else:
            self.now_playing = player.HumanPlayer(BLACK, gui=self.gui)
        if options['player_2'] == COMPUTER:
            self.other_player = player.ComputerPlayer(WHITE, int(options['player_2_time']), self.gui)
        else:
            self.other_player = player.HumanPlayer(WHITE, gui=self.gui)
        if options.has_key('load_file'):
            self.board = board.Board(self.read_board_file(options['load_file']))
        else:
            self.board = board.Board()

    def run(self):
        self.gui.show_game(self.board)
        while True:
            winner = self.board.game_won()
            if winner is not None:
                break
            self.now_playing.set_current_board(self.board)
            if self.board.get_valid_moves(self.now_playing.color) != []:
                self.board = self.now_playing.get_move()
            self.gui.update(self.board, self.other_player)
            self.now_playing, self.other_player = self.other_player, self.now_playing
        self.gui.show_winner(winner, self.board)
        self.restart()

    def restart(self):
        self.setup_game()
        self.run()

def main():
    game = Othello()
    game.run()

if __name__ == '__main__':
    main()
