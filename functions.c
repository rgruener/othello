#include <stdio.h>
#include <stdlib.h>

#define EMPTY 0
#define BLACK 1
#define WHITE 2

#if __GNUC__
#if __x86_64__ || __ppc64__
#define BOARD_TYPE long long int
#else
#define BOARD_TYPE int
#endif
#endif

int pieces_to_flip_in_row_bool(BOARD_TYPE board[8][8], int row, int col, int color, int direction){
    int other = BLACK;
    int row_inc = 0;
    int col_inc = 0;
    if (direction >= 5){
        direction += 1;
    }
    if (direction >= 1 && direction <= 3){
        row_inc = -1;
    } else if (direction >= 7 && direction <= 9){
        row_inc = 1;
    }
    if (direction == 1 || direction == 4 || direction == 7){
        col_inc = -1;
    } else if (direction == 3 || direction == 6 || direction == 9){
        col_inc = 1;
    }

    if (color == BLACK){
        other = WHITE;
    }

    int i = row + row_inc;
    int j = col + col_inc;

    if ((i >= 0 && i < 8) && (j >= 0 && j < 8) && board[i][j] == other){
        i += row_inc;
        j += col_inc;
        while ((i >= 0 && i < 8) && (j >= 0 && j < 8) && board[i][j] == other){
            i += row_inc;
            j += col_inc;
        }
        if ((i >= 0 && i < 8) && (j >= 0 && j < 8) && board[i][j] == color){
            return 1;
        }
    }

    return 0;
}

int **pieces_to_flip_in_row(BOARD_TYPE board[8][8], int row, int col, int color, int direction){
    int other = BLACK;
    int row_inc = 0;
    int col_inc = 0;

    int num_moves = 0;
    int **pieces = malloc(9 * sizeof(int *));
    pieces[0] = malloc(sizeof(int));
    pieces[0][0] = num_moves;

    if (direction >= 5){
        direction += 1;
    }
    if (direction >= 1 && direction <= 3){
        row_inc = -1;
    } else if (direction >= 7 && direction <= 9){
        row_inc = 1;
    }
    if (direction == 1 || direction == 4 || direction == 7){
        col_inc = -1;
    } else if (direction == 3 || direction == 6 || direction == 9){
        col_inc = 1;
    }

    if (color == BLACK){
        other = WHITE;
    }

    int i = row + row_inc;
    int j = col + col_inc;

    if ((i >= 0 && i < 8) && (j >= 0 && j < 8) && board[i][j] == other){
        num_moves++;
        pieces[num_moves] = malloc(2 * sizeof(int));
        pieces[num_moves][0] = i;
        pieces[num_moves][1] = j;
        i += row_inc;
        j += col_inc;
        while ((i >= 0 && i < 8) && (j >= 0 && j < 8) && board[i][j] == other){
            num_moves++;
            pieces[num_moves] = malloc(2 * sizeof(int));
            pieces[num_moves][0] = i;
            pieces[num_moves][1] = j;
            i += row_inc;
            j += col_inc;
        }
        if ((i >= 0 && i < 8) && (j >= 0 && j < 8) && board[i][j] == color){
            pieces[0][0] = num_moves;
        }
    }
    return pieces;
}

int **get_valid_moves_by_empty_squares(BOARD_TYPE board[8][8], int color){

    int num_moves = 0;
    long i, j, dir;
    int **moves = malloc(61 * sizeof(int *));
    moves[0] = malloc(sizeof(int));
    moves[0][0] = num_moves;

    for (i=0; i < 8; i++){
        for (j=0; j < 8; j++){
            if (board[i][j] == EMPTY){
                for (dir=1; dir < 9; dir++){
                    if (pieces_to_flip_in_row_bool(board, i, j, color, dir) > 0){
                        num_moves++;
                        moves[num_moves] = malloc(2 * sizeof(int));
                        moves[num_moves][0] = i;
                        moves[num_moves][1] = j;
                        moves[0][0] = num_moves;
                        break;
                    }
                }
            }
        }
    }
    return moves;
}

void add_moves_in_direction(BOARD_TYPE board[8][8], int other, int ***moves, int i, int j, int row_inc, int col_inc, int *num_moves){
    int row = i + row_inc;
    int column = j + col_inc;
    if (row >= 0 && column < 8 && board[row][column] == other){
        row += row_inc;
        column += col_inc;
        while (row >= 0 && column < 8 && board[row][column] == other){
            row += row_inc;
            column += col_inc;
        }
        if (row >= 0 && column < 8 && board[row][column] == 0){
            (*num_moves)++;
            *moves = realloc(*moves, (*num_moves+1) * sizeof(int *));
            (*moves)[*num_moves] = malloc(2 * sizeof(int));
            (*moves)[*num_moves][0] = row;
            (*moves)[*num_moves][1] = column;
            (*moves)[0][0] = *num_moves;
        }
    }
}

int **get_valid_moves_by_pieces(BOARD_TYPE board[8][8], int color){
    int other;
    if (color == BLACK){
        other = WHITE;
    } else {
        other = BLACK;
    }

    int num_moves = 0;
    long i, j, dir;
    int **moves = malloc(sizeof(int *));
    moves[0] = malloc(sizeof(int));
    moves[0][0] = num_moves;

    for (i=0; i < 8; i++){
        for (j=0; j < 8; j++){
            if (board[i][j] == color){
                for (dir=1; dir < 9; dir++){
                    add_moves_in_direction(board, other, &moves, i, j, -1, 0, &num_moves); // north
                    add_moves_in_direction(board, other, &moves, i, j, -1, 1, &num_moves); // northeast
                    add_moves_in_direction(board, other, &moves, i, j, 0, 1, &num_moves); // east
                    add_moves_in_direction(board, other, &moves, i, j, 1, 1, &num_moves); // southeast
                    add_moves_in_direction(board, other, &moves, i, j, 1, 0, &num_moves); // south
                    add_moves_in_direction(board, other, &moves, i, j, 1, -1, &num_moves); // southwest
                    add_moves_in_direction(board, other, &moves, i, j, 0, -1, &num_moves); // west
                    add_moves_in_direction(board, other, &moves, i, j, -1, -1, &num_moves); // northwest

                }
            }
        }
    }
    return moves;
}

int **get_valid_moves(BOARD_TYPE board[8][8], int color){
    return get_valid_moves_by_empty_squares(board, color);
}

void free_moves(int **moves, int num_moves){
    int i;
    for (i=0; i <= num_moves; i++){
        free(moves[i]);
    }
    free(moves);
}
