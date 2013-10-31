import random
from config import BLACK, WHITE
from game_ai import GameArtificialIntelligence
from heuristic import OthelloHeuristic

class Player(object):

    def __init__(self, color, time_limit=-1, gui=None):
        self.color = color
        self.time_limit = time_limit
        self.gui = gui

    def get_move(self):
        raise NotImplementedError("function get_move must be implemented by subclass")

    def apply_move(self, move):
        self.gui.flash_move(move, self.color)
        self.current_board.apply_move(move, self.color)

    def set_current_board(self, board):
        self.current_board = board

    def set_time_limit(self, new_limit):
        self.time_limit = new_limit

class HumanPlayer(Player):

    def get_move(self):
        valid_moves = self.current_board.get_valid_moves(self.color)
        self.gui.highlight_valid_moves(valid_moves)
        while True:
            move = self.gui.get_move_by_mouse()
            if move in valid_moves:
                break
        self.apply_move(move)
        return self.current_board

class RandomPlayer(Player):

    def get_move(self):
        x = random.sample(self.current_board.get_valid_moves(self.color), 1)
        self.apply_move(x[0])
        return self.current_board

class ComputerPlayer(Player):

    def __init__(self, color="black", time_limit=5, gui=None):
        super(ComputerPlayer, self).__init__(color, time_limit, gui)
        heuristic = OthelloHeuristic()
        self.ai = GameArtificialIntelligence(heuristic.evaluate)

    # Is Random For Now
    def get_move(self):
        import datetime
        import sys
        other_color = BLACK
        if self.color == BLACK:
            other_color = WHITE
        start = datetime.datetime.now()
        move = self.ai.move_search(self.current_board, self.time_limit, self.color, other_color)
        delta = datetime.datetime.now() - start
        print >> sys.stderr, "Time taken:", delta
        self.apply_move(move)
        return self.current_board
