# N*N TIC TAC TOE

#### Video Demo:  <URL HERE>

#### Description
This is an N*N Tic Tac Toe game.
To start the game, run the program:
```sh
$ tictactoe [N]
```
> `[N]` is an integer between 3-9 (inclusive), determining the size of the N*N board

#### Game Rules
players take turns to play
player 1 starts first and plays the X tokens
player 2 goes second and plays the O tokens
the first player that gets `[N]` adjacent tokens wins (horizontally, vertically, or diagonally)

#### Interface
before a player's turn, the interface will display the board
at a given player's turn, the program will prompt the player for the coordinates at which to place a token
if the player inputs invalid coordinates, the program will prompt the player again

#### Source Code
`tictactoe.c` contains the source code

#### Example
```sh
$ tictactoe 3

###########
game start!
###########

TURN 1 {player 1 : X, player 2 : O}
|00||01||02|
|10||11||12|
|20||21||22|
player 1 plays: 11

TURN 2 {player 1 : X, player 2 : O}
|00||01||02|
|10||X ||12|
|20||21||22|
player 2 plays: 21

TURN 3 {player 1 : X, player 2 : O}
|00||01||02|
|10||X ||12|
|20||O ||22|
player 1 plays: 20

TURN 4 {player 1 : X, player 2 : O}
|00||01||02|
|10||X ||12|
|X ||O ||22|
player 2 plays: 02

TURN 5 {player 1 : X, player 2 : O}
|00||01||O |
|10||X ||12|
|X ||O ||22|
player 1 plays: 10

TURN 6 {player 1 : X, player 2 : O}
|00||01||O |
|X ||X ||12|
|X ||O ||22|
player 2 plays: 12

TURN 7 {player 1 : X, player 2 : O}
|00||01||O |
|X ||X ||O |
|X ||O ||22|
player 1 plays: 00

GAME OVER
|X ||01||O |
|X ||X ||O |
|X ||O ||22|

##############
player 1 wins!
##############
```

#### Functions

`int main(int argc, char *argv[]);`
> main function where the game runs
1. check input parameters
2. set up the game
    * generate the board
    * initialise with player 1
3. primary game loop
    * print game board
    * get user input
    * update board with user input
    * check if the player wins
    * check for a draw
4. if (the player wins) or (game is a draw), end the game
5. else switch player and repeat (3)


`int print_board(int **board, int bn);`
> function to print the board
X is printed where player 1 has a token
O is printed where player 2 has a token
where there are no tokens, the coordinates are printed


`int *get_input(int player_turn, int **board, int bn);`
> function to get input from the user and check validity
1. get user input
2. check validity
    * check if the input is on the board
    * check if the input does not already have a token on it
3. if input is not valid, go back to (1)


`int switch_player(int current_player);`
> function to switch from one player to the other
if currently on player 1, switch to player 2
if currently on player 2, switch to player 1


`int check_win(int player_turn, int *last_play, int **board, int bn);`
> function to check winning condition for the current player
1. based on the last token played by the current player,
    * check the row of the last token for `[N]` horizontally adjacent tokens
    * check the column of the last token for `[N]` vertically adjacent tokens
2. check the 2 board diagonals for `[N]` diagonally adjacent tokens



