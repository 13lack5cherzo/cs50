# N*N TIC TAC TOE

#### Video Demo:  <URL HERE>

#### Description:
This is an N*N Tic Tac Toe game.
To start the game, run the program:
```sh
$ tictactoe [INTEGER]
```
> `[INTEGER]` is an integer between 3-9 (inclusive)

#### Game Rules:
players take turn to play.
player 1 starts first and plays the X tokens.
player 2 goes second and plays the O tokens.
the first player that gets `[INTEGER]` adjacent tokens in a row wins!

#### Other Information
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

