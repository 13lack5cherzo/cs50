#include <ctype.h>
#include <string.h>
#include <strings.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#define imax(x,y) (((x) >= (y)) ? (x) : (y))
#define imin(x,y) (((x) <= (y)) ? (x) : (y))


// prototypes
int print_board(int **board, int bn);
int *get_input(int player_turn, int **board, int bn);
int switch_player(int current_player);
int check_win(int player_turn, int *last_play, int **board, int bn);


int main(int argc, char *argv[])
{
    ////
    // check input
    ////
    char *usage = "Usage: tictactoe [INTEGER>2]\n";
    // Check for invalid usage
    if (argc != 2)
    {
        printf("%s", usage);
        return 1;
    }
    // Check that all letters of input is int
    for (int i=0; i<strlen(argv[1]); i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("%s", usage);
            return 1;
        }
    }
    // coerce argument into integer as board size
    int bn = atoi(argv[1]);
    // Check that first letter of parameter is int
    if ((bn < 3) || (bn > 10))
    {
        printf("%s", usage);
        return 1;
    }

    ////
    // setup
    ////
    // generate board
    int **main_board;
    // allocate memory for the array
    main_board = malloc(bn * sizeof *main_board); // columns
    for (int i=0; i<bn; i++)
    {
        main_board[i] = malloc(bn * sizeof *main_board[i]); // rows
    }
    // fill board with zeros
    for (int row1=0; row1 < bn; row1++)
    {
        for (int col1=0; col1 < bn; col1++)
        {
            main_board[row1][col1] = 0; // put in board_fill
        }
    }

    // state variables
    int *user_input; // integer for user input
    int player_turn = 1; // player 1 starts
    int game_turn = 1; // game turn

    ////
    // game
    ////
    printf("###########\n");
    printf("game start!\n");
    printf("###########\n");

    while (true)
    {
        // print player tiles
        printf("\nTURN %i ", game_turn);
        printf("{player 1 : X, player 2 : O}\n");

        // display board for text-based user interface
        print_board(main_board, bn);

        // receive user input
        user_input = get_input(player_turn, main_board, bn);

        // update board
        main_board[user_input[0]][user_input[1]] = player_turn;

        // check win condition
        if (check_win(
            player_turn,
            user_input,
            main_board,
            bn
            ))
        {
            // display board for text-based user interface
            printf("\nGAME OVER\n");
            print_board(main_board, bn);

            // print winner
            printf("\n");
            printf("##############\n");
            printf("player %i wins!\n", player_turn);
            printf("##############\n");
            player_turn = 0;
        }

        // check tie
        if (game_turn == bn * bn)
        {
            // print draw
            printf("\n");
            printf("#####\n");
            printf("draw!\n");
            printf("#####\n");
            player_turn = 0;
        }

        // post turn
        if (player_turn != 0) // switch player if no winner
        {
            player_turn = switch_player(player_turn);
        }
        else // clean up and exit
        {
            // deallocate memory for the array
            for (int i=0; i<bn; i++)
            {
                free(main_board[i]); // rows
            }
            free(main_board); // columns

            return 0; // exit
        }

        // next game turn
        game_turn++;
    }
}



// function to print board
int print_board(int **board, int bn)
{
    for (int row1=0; row1 < bn; row1++)
    {
        for (int col1=0; col1 < bn; col1++)
        {
            int pos_int = board[row1][col1];
            if (pos_int == 1) // -1:X for 1st player
            {
                printf("|X |");
            }
            else if (pos_int == 2) // -2:O for 2nd player
            {
                printf("|O |");
            }
            else
            {
                // print board index otherwise
                printf("|%i%i|", row1, col1);
            }
        }
        printf("\n"); // new line after printing every column for each row
    }
    return 0;
}

// function to get user output and check
int *get_input(int player_turn, int **board, int bn)
{
    char user_input[20];
    int input_row;
    int input_col;
    bool invalid_flag = false;
    static int return_a[2]; // array to return

    while (true) // get user input again if not valid
    {
        // ask for input
        printf("player %i plays: ", player_turn);
        scanf("%s", user_input);

        // cast to integer
        input_row = user_input[0] - '0';
        input_col = user_input[1] - '0';

        ////
        // checks
        ////
        if (!invalid_flag)
        {
            // check that the values are less than the board size
            if (
                (input_row < 0) || (input_row >= bn)
                || (input_col < 0) || (input_col >= bn)
                )
            {
                invalid_flag = true; // set invalid flag as true
            }
        }
        if (!invalid_flag)
        {
            // check that the value at the index is 0
            if (board[input_row][input_col] != 0)
            {
                invalid_flag = true; // set invalid flag as true
            }
        }
        if (invalid_flag) // if input is deemed not valid
        {
            printf("invalid. ");
            invalid_flag = false; // set invalid flag as false for next roiund
        }
        else // if valid,
        {
            break; // exit while loop
        }
    }
    // assign to array to return
    return_a[0] = input_row;
    return_a[1] = input_col;

    return return_a;
}

// function to switch player
int switch_player(int current_player)
{
    int next_player;
    if (current_player == 1)
    {
        next_player = 2;
    }
    if (current_player == 2)
    {
        next_player = 1;
    }
    return next_player;
}


// function to check winner
int check_win(
    int player_turn,
    int *last_play,
    int **board,
    int bn)
{
    int longest1 = 0; // player's longest line
    int len1 = 0; // working length (used to check)
    int player_win = 0; // flag if player wins

    // check row of latest point
    for (int col1=0; col1<bn; col1++)
    {
        if (board[last_play[0]][col1] == player_turn)
        {
            len1++;
        }
    }
    longest1 = imax(longest1, len1); // get longest length
    len1 = 0; // reset length

    // check col of latest point
    for (int row1=0; row1<bn; row1++)
    {
        if (board[row1][last_play[1]] == player_turn)
        {
            len1++;
        }
    }
    longest1 = imax(longest1, len1); // get longest length
    len1 = 0; // reset length

    // check topleft to botright diagonal
    for (int rowcol1=0; rowcol1<bn; rowcol1++)
    {
        if (board[rowcol1][rowcol1] == player_turn)
        {
            len1++;
        }
    }
    longest1 = imax(longest1, len1); // get longest length
    len1 = 0; // reset length

    // check topright to botleft diagonal
    for (int rowcol1=0; rowcol1<bn; rowcol1++)
    {
        if (board[rowcol1][bn-1-rowcol1] == player_turn)
        {
            len1++;
        }
    }
    longest1 = imax(longest1, len1); // get longest length
    len1 = 0; // reset length

    // if the player's longest line is equal to the board length
    if (longest1 == bn)
    {
        player_win = 1; // player wins
    }

    return player_win;
}


// make tictactoe
// ./tictactoe 3
