import random

class Player(object):

    def __init__(self, color="black", time_limit=5, gui=None):
        self.color = color
        self.move_time_limit = time_limit
        self.gui = gui

    def get_move(self):
        raise NotImplementedError("function get_move must be implemented by subclass")

    def apply_move(self, move):
        self.gui.flash_move(move, self.color)
        self.current_board.apply_move(move, self.color)

    def set_current_board(self, board):
        self.current_board = board


class HumanPlayer(Player):

    def get_move(self):
        valid_moves = self.current_board.get_valid_moves(self.color)
        self.gui.highlight_valid_moves(valid_moves)
        while True:
            move = self.gui.get_move_by_mouse()
            if move in valid_moves:
                break
        self.apply_move(move)
        return 0, self.current_board

class RandomPlayer(Player):

    def get_move(self):
        x = random.sample(self.current_board.get_valid_moves(self.color), 1)
        self.apply_move(x[0])
        return x[0], self.current_board

class ComputerPlayer(Player):

    # Is Random For Now
    def get_move(self):
        x = random.sample(self.current_board.get_valid_moves(self.color), 1)
        self.apply_move(x[0])
        return x[0], self.current_board
