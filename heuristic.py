import sys
from config import BLACK, WHITE, EMPTY

class OthelloHeuristic(object):

    WIN = sys.maxint - 1000
    PIECE_COUNT_FACTOR = [0, 0, 1]
    CORNER_FACTOR = [1000, 1000, 0]
    MOBILITY_FACTOR = [80, 100, 0]
    EDGE_FACTOR = [5, 5, 0]
    CORNER_EDGE_FACTOR = [200, 200, 0]

    START_GAME = 0
    MID_GAME = 1
    END_GAME = 2

    def evaluate(self, board, current_player, other_player):

        if current_player == BLACK:
            OthelloHeuristic.PIECE_COUNT_FACTOR = [0, 0, 1]
            OthelloHeuristic.CORNER_FACTOR = [1000, 1000, 0]
            OthelloHeuristic.MOBILITY_FACTOR = [40, 45, 0]
            OthelloHeuristic.EDGE_FACTOR = [5, 5, 0]
            OthelloHeuristic.CORNER_EDGE_FACTOR = [400, 400, 0]
        else:
            OthelloHeuristic.PIECE_COUNT_FACTOR = [0, 0, 1]
            OthelloHeuristic.CORNER_FACTOR = [1000, 1000, 0]
            OthelloHeuristic.MOBILITY_FACTOR = [100, 150, 0]
            OthelloHeuristic.EDGE_FACTOR = [5, 5, 0]
            OthelloHeuristic.CORNER_EDGE_FACTOR = [400, 400, 0]

        # Check for win conditions
        winner = board.game_won()
        if winner is not None:
            if winner == current_player:
                return OthelloHeuristic.WIN + self.evaluate_piece_count(board, current_player, other_player, OthelloHeuristic.END_GAME)
            elif winner == other_player:
                return -OthelloHeuristic.WIN-1 + self.evaluate_piece_count(board, current_player, other_player, OthelloHeuristic.END_GAME)

        # Determine Game State to Determine Heuristic Values
        if board.empty_spaces >= 45:
            game_state = OthelloHeuristic.START_GAME
        elif board.empty_spaces >= 2:
            game_state = OthelloHeuristic.MID_GAME
        else:
            game_state = OthelloHeuristic.END_GAME

        score = 0
        if OthelloHeuristic.CORNER_FACTOR[game_state] != 0:
            score += self.evaluate_corner_pieces(board, current_player, other_player, game_state)
        if OthelloHeuristic.PIECE_COUNT_FACTOR[game_state] != 0:
            score += self.evaluate_piece_count(board, current_player, other_player, game_state)
        if OthelloHeuristic.MOBILITY_FACTOR[game_state] != 0:
            score += self.evaluate_mobility(board, current_player, other_player, game_state)
        if OthelloHeuristic.EDGE_FACTOR[game_state] != 0:
            score += self.evaluate_edge_pieces(board, current_player, other_player, game_state)
        if OthelloHeuristic.CORNER_EDGE_FACTOR[game_state] != 0:
            score += self.evaluate_corner_edge(board, current_player, other_player, game_state)
        return score

    def evaluate_piece_count(self, board, current_player, other_player, game_state):
        score = 0
        if current_player == WHITE:
            score += OthelloHeuristic.PIECE_COUNT_FACTOR[game_state]*board.white_pieces
            score -= OthelloHeuristic.PIECE_COUNT_FACTOR[game_state]*board.black_pieces
        else:
            score += OthelloHeuristic.PIECE_COUNT_FACTOR[game_state]*board.black_pieces
            score -= OthelloHeuristic.PIECE_COUNT_FACTOR[game_state]*board.white_pieces
        return score

    def evaluate_corner_pieces(self, board, current_player, other_player, game_state):
        score = 0
        for i in [0, 7]:
            for j in [0, 7]:
                if board.board[i][j] == current_player:
                    score += OthelloHeuristic.CORNER_FACTOR[game_state]
                elif board.board[i][j] == other_player:
                    score -= OthelloHeuristic.CORNER_FACTOR[game_state]
        return score

    def evaluate_edge_pieces(self, board, current_player, other_player, game_state):
        score = 0
        # Compute Horizontal Edges
        for i in [0, 7]:
            for j in range(2, 6):
                if board.board[i][j] == current_player:
                    score += OthelloHeuristic.EDGE_FACTOR[game_state]
                elif board.board[i][j] == other_player:
                    score -= OthelloHeuristic.EDGE_FACTOR[game_state]
        # Comput Vertical Edges
        for i in range(2, 6):
            for j in [0, 7]:
                if board.board[i][j] == current_player:
                    score += OthelloHeuristic.EDGE_FACTOR[game_state]
                elif board.board[i][j] == other_player:
                    score -= OthelloHeuristic.EDGE_FACTOR[game_state]
        return score

    def evaluate_corner_edge(self, board, current_player, other_player, game_state):
        score = 0
        corner = (0, 0)
        for (i, j) in [(1, 0), (1, 1), (0, 1)]:
            if board.board[i][j] == current_player:
                if board.board[corner[0]][corner[1]] == EMPTY:
                    score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                elif board.board[corner[0]][corner[1]] == current_player:
                    score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
            elif board.board[i][j] == other_player:
                if board.board[corner[0]][corner[1]] == EMPTY:
                    score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                elif board.board[corner[0]][corner[1]] == other_player:
                    score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
        corner = (7, 0)
        for (i, j) in [(6, 0), (6, 1), (7, 1)]:
            if board.board[i][j] == current_player:
                if board.board[corner[0]][corner[1]] == EMPTY:
                    score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                elif board.board[corner[0]][corner[1]] == current_player:
                    score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
            elif board.board[i][j] == other_player:
                if board.board[corner[0]][corner[1]] == EMPTY:
                    score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                elif board.board[corner[0]][corner[1]] == other_player:
                    score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
        corner = (7, 7)
        for (i, j) in [(7, 6), (6, 6), (6, 7)]:
            if board.board[i][j] == current_player:
                if board.board[corner[0]][corner[1]] == EMPTY:
                    score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                elif board.board[corner[0]][corner[1]] == current_player:
                    score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
            elif board.board[i][j] == other_player:
                if board.board[corner[0]][corner[1]] == EMPTY:
                    score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                elif board.board[corner[0]][corner[1]] == other_player:
                    score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
        corner = (0, 7)
        for (i, j) in [(0, 6), (1, 6), (1, 7)]:
            if board.board[i][j] == current_player:
                if board.board[corner[0]][corner[1]] == EMPTY:
                    score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                elif board.board[corner[0]][corner[1]] == current_player:
                    score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
            elif board.board[i][j] == other_player:
                if board.board[corner[0]][corner[1]] == EMPTY:
                    score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                elif board.board[corner[0]][corner[1]] == other_player:
                    score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
        return score

    def evaluate_mobility(self, board, current_player, other_player, game_state):
        score = 0
        score += len(board.get_valid_moves(current_player))*OthelloHeuristic.MOBILITY_FACTOR[game_state]
        score -= len(board.get_valid_moves(other_player))*OthelloHeuristic.MOBILITY_FACTOR[game_state]
        return score

