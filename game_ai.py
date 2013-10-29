import datetime
import sys
import random

class GameArtificialIntelligence(object):

    def __init__(self, heuristic_fn):
        self.heuristic = heuristic_fn

    def move_search(self, starting_node, time_limit, current_player, other_player):
        self.player = current_player
        self.other_player = other_player
        possible_moves = starting_node.get_valid_moves(current_player)
        if len(possible_moves) == 1:
            return possible_moves[0]
        depth = 0
        time_start = datetime.datetime.now()
        self.time_done = time_start + datetime.timedelta(seconds=time_limit)
        time_cutoff = time_start + datetime.timedelta(seconds=time_limit/3.0)
        while datetime.datetime.now() < time_cutoff:
            depth += 1
            (score, move) = self.alpha_beta_search(starting_node, depth, current_player, other_player)
        print >> sys.stderr, "Got to Depth:", depth
        #import pdb
        #pdb.set_trace()
        #(score, move) = self.alpha_beta_search(starting_node, 4, current_player, other_player)
        return move

    def alpha_beta_search(self, node, depth, current_player, other_player, alpha=-sys.maxint-1, beta=sys.maxint, last_move=None, maximizing=True):
        #if datetime.datetime.now() > self.time_done - datetime.timedelta(milliseconds=1000):
            #if maximizing:
                #return (-sys.maxint-1, None)
            #else:
                #return (sys.maxint, None)
        best_move = last_move
        if depth == 0 or node.game_won() is not None:
            return (self.heuristic(node, self.player, self.other_player), last_move)
        if maximizing:
            num_equal = 2
            for (child, move) in node.child_nodes(current_player):
                new_alpha, new_move = self.alpha_beta_search(child, depth-1, other_player, current_player, alpha, beta, move, False)
                if new_alpha > alpha or best_move is None:
                    alpha = new_alpha
                    best_move = new_move
                elif new_alpha == alpha:
                    # Randomly pick a move
                    if random.uniform(0, 1.0) < 1.0/num_equal:
                        best_move = new_move
                    num_equal += 1
                if alpha > beta:
                    break
            #if datetime.datetime.now() > self.time_done - datetime.timedelta(milliseconds=1000):
                #return (0, None)
            return alpha, best_move
        else:
            for (child, move) in node.child_nodes(current_player):
                new_beta, new_move = self.alpha_beta_search(child, depth-1, other_player, current_player, alpha, beta, move)
                beta = min(beta, new_beta)
                if beta < alpha:
                    break
            #if datetime.datetime.now() > self.time_done - datetime.timedelta(milliseconds=1000):
                #return (0, None)
            return beta, best_move
