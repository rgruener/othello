import pygame
import sys
from pygame.locals import *
import time
from config import BLACK, WHITE, DEFAULT_LEVEL, HUMAN, COMPUTER
import os

class Gui :

    def __init__ (self):
        pygame.init()

        # colors
        self.BLACK = (0, 0, 0)
        self.BACKGROUND = (10, 10, 10)
        self.WHITE = (255, 255, 255)
        self.BLUE = (100, 100, 255)

        # display
        self.SCREEN_SIZE = (840, 480)
        self.BOARD_POS = (20, 20)
        self.BOARD = (40, 40)
        self.BOARD_SIZE = 400
        self.SQUARE_SIZE = 50
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

        # fonts
        self.font = pygame.font.SysFont("Times New Roman" , 22)
        self.score_font = pygame.font.SysFont("Serif", 24)
        self.title_font = pygame.font.SysFont("Times New Roman", 34)

        # image files
        self.board_img = pygame.image.load(os.path.join("images", "board.bmp")).convert()
        self.black_img = pygame.image.load(os.path.join("images", "preta.bmp")).convert()
        self.white_img = pygame.image.load(os.path.join("images", "branca.bmp")).convert()
        self.tip_img = pygame.image.load(os.path.join("images","tip.bmp")).convert()
        self.clear_img = pygame.image.load(os.path.join("images","nada.bmp")).convert()

    def show_game (self, board):
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill (self.BACKGROUND)
        self.screen.blit(self.background, (0, 0), self.background.get_rect())
        self.screen.blit(self.board_img, self.BOARD_POS, self.board_img.get_rect())
        self.put_stone((3, 3), WHITE)
        self.put_stone((4, 4), WHITE)
        self.put_stone((3, 4), BLACK)
        self.put_stone((4, 3), BLACK)
        self.showGameInformation(board)
        pygame.display.flip()

    def show_options(self):

        # default values
        black_player = HUMAN
        white_player = COMPUTER
        ai_time = DEFAULT_LEVEL

        black_player_string = "Set Black Player (Moves First)"
        white_player_string = "Set White Player"
        ai_time_string = "Set Computer AI Move Time"

        while True:
            self.screen.fill(self.BACKGROUND)

            title = title_font.render("Othello", True, self.WHITE)
            title_pos = title.get_rect(centerx = self.screen.get_width()/2, centery = 60)

            start_txt = self.font.render("Start", True, self.WHITE)
            start_pos = start_txt.get_rect(centerx = self.screen.get_width()/2, centery = 220)

            black_player_txt = self.font.render(black_player_string, True, self.WHITE)
            black_player_pos = black_player_txt.get_rect(centerx = self.screen.get_width()/2, centery = 260)
            white_player_txt = self.font.render(white_player_string, True, self.WHITE)
            white_player_pos = white_player_txt.get_rect(centerx = self.screen.get_width()/2, centery = 300)
            ai_time_txt = self.font.render(ai_time_string, True, self.WHITE)
            ai_time_pos = ai_time_txt.get_rect(centerx = self.screen.get_width()/2, centery = 340)

            self.screen.blit(title, title_pos)
            self.screen.blit(start_txt, start_pos)
            self.screen.blit(black_player_txt, black_player_pos)
            self.screen.blit(white_player_txt, white_player_pos)
            self.screen.blit(ai_time_txt, ai_time_pos)

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()
                    if start_pos.collidepoint(mouse_x, mouse_y):
                        return (black_player, white_player, ai_time)
                    elif black_player_pos.collidepoint(mouse_x, mouse_y):
                        black_player = self.get_chosen_player(black_player_string)
                    elif white_player_pos.collidepoint(mouse_x, mouse_y):
                        white_player = self.get_chosen_player(white_player_string)
                    elif ai_time_pos.collidepoint(mouse_x, mouse_y):
                        ai_time = self.get_chosen_level(ai_time_string)

            pygame.display.flip()

    def show_winner(self, player_color, board):
        self.screen.fill( pygame.Color( 0, 0, 0, 50))
        font = pygame.font.SysFont("Courier New", 34)
        if player_color == WHITE:
            msg = font.render("White player wins", True, self.WHITE)
        elif player_color == BLACK:
            msg = font.render("Black player wins", True, self.WHITE)
        else:
            msg = font.render( "Tie!", True, self.WHITE)

        blacks_str = 'Black Pieces: %02d ' % int(board.black_pieces)
        whites_str = 'White Pieces: %02d ' % int(board.white_pieces)
        black_pieces_text = self.score_font.render(blacks_str, True, self.WHITE, self.BACKGROUND)
        white_pieces_text = self.score_font.render(whites_str, True, self.WHITE, self.BACKGROUND)

        self.screen.blit(msg, msg.get_rect(centerx = self.screen.get_width()/2, centery = 120))
        self.screen.blit(black_pieces_text, black_pieces_text.get_rect(centerx = self.screen.get_width()/2, centery = 240))
        self.screen.blit(white_pieces_text, white_pieces_text.get_rect(centerx = self.screen.get_width()/2, centery = 280))
        pygame.display.flip()

    def get_chosen_player(self, option_title_string):
        while True:
            self.screen.fill(self.BACKGROUND)
            title_fnt = pygame.font.SysFont("Times New Roman", 34)
            title = title_fnt.render("Othello", True, self.WHITE)
            title_pos = title.get_rect(centerx = self.screen.get_width()/2, centery = 60)
            option_title = self.font.render(option_title_string, True, self.WHITE)

            human_txt = self.font.render("Human", True, self.WHITE)
            human_pos = human_txt.get_rect(centerx = self.screen.get_width()/2, centery = 220)
            comp_ai_txt = self.font.render("Computer with AI", True, self.WHITE)
            comp_ai_pos = comp_ai_txt.get_rect(centerx = self.screen.get_width()/2, centery = 260)
            comp_random_txt = self.font.render("Computer with Random Moves", True, self.WHITE)
            comp_random_pos = comp_random_txt.get_rect(centerx = self.screen.get_width()/2, centery = 300)

            self.screen.blit(title, title_pos)
            self.screen.blit(human_txt, human_pos)
            self.screen.blit(comp_ai_txt, comp_ai_pos)
            self.screen.blit(comp_random_txt, comp_random_pos)

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()
                    if human_pos.collidepoint(mouse_x, mouse_y):
                        return HUMAN
                    elif comp_ai_pos.collidepoint(mouse_x, mouse_y):
                        return COMPUTER
                    elif comp_random_pos.collidepoint(mouse_x, mouse_y):
                        return RANDOM

            pygame.display.flip()

    def get_chosen_level(self):
        """ Level options
        """

        while True:
            self.screen.fill(self.BACKGROUND)
            title_fnt = pygame.font.SysFont("Times New Roman", 34)
            title = title_fnt.render("Othello", True, self.BLUE)
            title_pos = title.get_rect(centerx = self.screen.get_width()/2, \
                                         centery = 60)
            one_txt = self.font.render("1 Second", True, self.WHITE)
            one_pos = one_txt.get_rect(centerx = self.screen.get_width()/2, \
                                             centery = 120)
            two_txt = self.font.render("Level 2", True, self.WHITE)
            two_pos = two_txt.get_rect(centerx = self.screen.get_width()/2, \
                                       centery = 240)

            three_txt = self.font.render("Level 3", True, self.WHITE)
            three_pos = three_txt.get_rect(centerx = self.screen.get_width()/2, \
                                       centery = 360)

            self.screen.blit(title, title_pos)
            self.screen.blit(one_txt, one_pos)
            self.screen.blit(two_txt, two_pos)
            self.screen.blit(three_txt, three_pos)

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()
                    if one_pos.collidepoint(mouse_x, mouse_y):
                        return 1
                    elif two_pos.collidepoint(mouse_x, mouse_y):
                        return 2
                    elif three_pos.collidepoint(mouse_x, mouse_y):
                        return 3

            pygame.display.flip()
            time.sleep(.05)

    def highlight_valid_moves(self, valid_moves):
        for move in valid_moves:
            move = (move[1], move[0])
            x = move[0]*self.SQUARE_SIZE + self.BOARD[0]
            y = move[1]*self.SQUARE_SIZE + self.BOARD[1]
            pygame.draw.rect(self.screen, (255, 215, 0), \
                    (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE), 1)
        pygame.display.flip()

    def flash_move(self, pos, color):
        for i in range(0, 3):
            self.put_stone(pos, color)
            time.sleep(.1)
            self.clear_square(pos)
            time.sleep(.1)
        self.put_stone(pos, color)
        time.sleep(.3)

    def put_stone(self, pos, color):
        """ draws piece with given position and color """
        if pos == None:
            return

        # flip orientation (because xy screen orientation)
        pos = (pos[1], pos[0])

        if color == BLACK:
            img = self.black_img
        elif color == WHITE:
            img = self.white_img
        else:
            img = self.tip_img

        x = pos[0]*self.SQUARE_SIZE + self.BOARD[0]
        y = pos[1]*self.SQUARE_SIZE + self.BOARD[1]

        self.screen.blit(img, (x, y), img.get_rect())
        pygame.display.flip()

    def clear_square (self, pos):
        # flip orientation
        pos =(pos[1], pos[0])

        x = pos[0]*self.SQUARE_SIZE + self.BOARD[0]
        y = pos[1]*self.SQUARE_SIZE + self.BOARD[1]
        self.screen.blit(self.clear_img,(x, y), self.clear_img.get_rect())
        pygame.display.flip()

    def get_move_by_mouse(self):
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()
                    # Check to see if click was on the board
                    if mouse_x < self.BOARD_SIZE + self.BOARD[0] or \
                       mouse_x > self.BOARD[0] or \
                       mouse_y < self.BOARD_SIZE + self.BOARD[1] or \
                       mouse_y > self.BOARD[1] :
                        position =((mouse_x - self.BOARD[0]) / self.SQUARE_SIZE), \
                                  ((mouse_y - self.BOARD[1]) / self.SQUARE_SIZE)
                        # flip orientation
                        position =(position[1], position[0])
                    return position

                elif event.type == QUIT:
                    sys.exit(0)
            time.sleep(.05)

    def update(self, board, next_player):
        self.background.fill(self.BACKGROUND)
        self.screen.blit(self.background, (0, 0), self.background.get_rect())
        self.screen.blit(self.board_img, self.BOARD_POS, self.board_img.get_rect())
        for i in range(8):
            for j in range(8):
                if board.board[i][j] != 0:
                    self.put_stone(( i, j), board.board[i][j])

        self.showGameInformation(board, next_player)
        pygame.display.flip()


    def showGameInformation(self, board, next_player=None):
        title = self.title_font.render("Othello", True, self.WHITE, self.BACKGROUND)
        blacks_str = 'Black Pieces: %02d ' % int(board.black_pieces)
        whites_str = 'White Pieces: %02d ' % int(board.white_pieces)
        black_pieces_text = self.score_font.render(blacks_str, True, self.WHITE, self.BACKGROUND)
        white_pieces_text = self.score_font.render(whites_str, True, self.WHITE, self.BACKGROUND)

        if not next_player or next_player.color == BLACK:
            pygame.draw.circle(self.screen, (255, 215, 0), (550, 83), 7)
        else:
            pygame.draw.circle(self.screen, (255, 215, 0), (550, 123), 7)

        self.screen.blit(title, (600, 20))
        self.screen.blit(black_pieces_text,(565, 70))
        self.screen.blit(white_pieces_text,(565, 110))
