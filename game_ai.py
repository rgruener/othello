import datetime
import sys
import random
from Queue import PriorityQueue

class GameArtificialIntelligence(object):

    def __init__(self, heuristic_fn):
        self.heuristic = heuristic_fn

    def move_search(self, starting_node, time_limit, current_player, other_player):
        self.player = current_player
        self.other_player = other_player
        possible_moves = starting_node.get_valid_moves(current_player)
        if len(possible_moves) == 1:
            print >> sys.stderr, "Only 1 Possible Move:", possible_moves[0]
            return possible_moves[0]
        depth = 0
        score = -sys.maxint - 1
        move = None
        time_start = datetime.datetime.now()
        self.time_done = time_start + datetime.timedelta(seconds=time_limit)
        time_cutoff = time_start + datetime.timedelta(seconds=time_limit/2.0)
        self.cutoff = False
        WIN = sys.maxint - 1000
        self.queue = PriorityQueue(len(possible_moves))
        self.first = True
        while datetime.datetime.now() < time_cutoff and not self.cutoff and starting_node.empty_spaces >= depth:
            depth += 1
            self.all_terminal = False
            (new_move, new_score) = self.alpha_beta_wrapper(starting_node, depth, current_player, other_player)
            if new_move is not None and not self.cutoff:
                move = new_move
                score = new_score
                if score > WIN:
                    print >> sys.stderr, "Got to Depth:", depth, "Move:", move, "Win by ", score - WIN, "pieces"
                elif score < -WIN-1:
                    print >> sys.stderr, "Got to Depth:", depth, "Move:", move, "Loss by ", -WIN-1-score, "pieces"
                else:
                    print >> sys.stderr, "Got to Depth:", depth, "Move:", move, "Score:", score
            else:
                print >> sys.stderr, "Cutoff at depth", depth
        return move

    def alpha_beta_wrapper(self, node, depth, current_player, other_player):
        alpha = -sys.maxint-1
        beta = sys.maxint
        num_equal = 1
        if self.first:
            children = node.child_nodes(current_player)
            # Shuffle order of moves evaluated to prevent playing the same game every time
            random.shuffle(children)
            for (child, move) in children:
                new_alpha = self.alpha_beta_search(child, depth-1, other_player, current_player, alpha, beta, False)
                if new_alpha is None:
                    return (None, None)
                else:
                    self.queue.put((-new_alpha, child, move))
                if new_alpha > alpha:
                    alpha = new_alpha
                    best_move = move
                    num_equal = 1
                #print >> sys.stderr, "Possible move:", move, "Score:", new_alpha
            self.first = False
        else:
            children = self.queue.queue
            self.queue = PriorityQueue(self.queue.maxsize)
            for (x, child, move) in children:
                new_alpha = self.alpha_beta_search(child, depth-1, other_player, current_player, alpha, beta, False)
                if new_alpha is None:
                    return (None, None)
                else:
                    self.queue.put((-new_alpha, child, move))
                if new_alpha > alpha:
                    alpha = new_alpha
                    best_move = move
                    num_equal = 1
                #print >> sys.stderr, "Possible move:", move, "Score:", new_alpha
        return (best_move, alpha)


    def alpha_beta_search(self, node, depth, current_player, other_player, alpha=-sys.maxint-1, beta=sys.maxint, maximizing=True):
        if datetime.datetime.now() > self.time_done - datetime.timedelta(milliseconds=10):
            self.cutoff = True
            return None
        if depth == 0 or node.game_won() is not None:
            return self.heuristic(node, self.player, self.other_player)
        children = node.child_nodes(current_player)
        if maximizing:
            if len(children) == 0:
                new_alpha = self.alpha_beta_search(node, depth-1, other_player, current_player, alpha, beta, False)
                if new_alpha is None:
                    return None
                alpha = max(alpha, new_alpha)
            else:
                for (child, move) in children:
                    new_alpha = self.alpha_beta_search(child, depth-1, other_player, current_player, alpha, beta, False)
                    if new_alpha is None:
                        return None
                    alpha = max(alpha, new_alpha)
                    if alpha >= beta:
                        break
            return alpha
        else:
            if len(children) == 0:
                new_beta = self.alpha_beta_search(node, depth-1, other_player, current_player, alpha, beta)
                if new_beta is None:
                    return None
                beta = min(beta, new_beta)
            else:
                for (child, move) in children:
                    new_beta = self.alpha_beta_search(child, depth-1, other_player, current_player, alpha, beta)
                    if new_beta is None:
                        return None
                    beta = min(beta, new_beta)
                    if beta <= alpha:
                        break
            return beta
