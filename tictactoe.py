"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.

    :return: 2d-list of shape (3, 3)
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    Any return value is acceptable if
    a terminal board is provided as input (i.e., the game is already over).

    :param board: 2d-list of shape (3, 3)
    :return: str
    """

    # count the number of x and o on the board
    x_count, o_count = 0, 0  # initialise tile count
    for each_row in board:  # iterating through rows
        for each_col in each_row:  # iterating through cols
            if each_col == X:  # x
                x_count += 1
            elif each_col == O:  # o
                o_count += 1
            else:  # empty
                pass

    # return player turn
    if x_count == o_count:
        return X
    elif x_count < o_count:
        raise ValueError("more Os than Xs")
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    Any return value is acceptable if a terminal board is provided as input.

    :param board: 2d-list of shape (3, 3)
    :return: set of tuples (i, j)
    """

    boardlen = len(board)  # length of board
    actions_return = set()  # initialise empty set
    for row_idx in range(0, boardlen):  # iterating through rows
        for col_idx in range(0, boardlen):  # iterating through cols
            if board[row_idx][col_idx] == EMPTY:  # if empty,
                actions_return.add((row_idx, col_idx))  # append coordinates to set
            else:  # not empty
                pass

    return actions_return


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    If action is not a valid action for the board, your program should raise an exception.

    :param board: 2d-list of shape (3, 3)
    :param action: tuple (i, j) of coordinates
    :return: 2d-list of shape (3, 3)

    """

    next_board = copy.deepcopy(board)  # initialise next board as a deep copy

    # check validity of action
    if not next_board[action[0]][action[1]] == EMPTY:  # if not empty
        raise ValueError("invalid action at position {}".format(action))  # raise error

    # place token on the board
    next_board[action[0]][action[1]] = player(next_board)

    return next_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    If there is no winner of the game
    (either because the game is in progress, or because it ended in a tie),
    the function should return None.

    :param board: 2d-list of shape (3, 3)
    :return: {X, O, None}

    """

    winner_return = None  # initialise with no winner
    boardlen = len(board)  # length of board

    # get last player that played
    if player(board) == X:  # it is now X's turn
        last_player = O  # last player was O
    else:  # it is now O's turn
        last_player = X  # last player was X

    # create list containing last player's token,
    winner_list = [last_player] * boardlen  # to check for winner

    ####
    # check for win
    ####
    # check row-wise win
    for row1 in range(0, boardlen):
        if board[row1] == winner_list:
            winner_return = last_player
    # check col-wise win
    for col1 in range(0, boardlen):
        if [row[col1] for row in board] == winner_list:
            winner_return = last_player
    # check win in top left to bottom right diag
    if [board[i][i] for i in range(0, len(board))] == winner_list:
        winner_return = last_player
    # check win in top right to bottom left diag
    if [board[i][len(board)-1 - i] for i in range(0, len(board))] == winner_list:
        winner_return = last_player

    return winner_return


def terminal(board):
    """
    Returns True if game is over, False otherwise.

    :param board: 2d-list of shape (3, 3)
    :return: {True, False}
    """
    # if winner exists
    if not (winner(board) is None):
        return True

    # check if board is full
    full_board = True  # initialise bool for full board
    for each_row in board:  # iterating through rows
        for each_col in each_row:  # iterating through cols
            if each_col == EMPTY:
                full_board = False

    if full_board:  # if board is full,
        return True
    else:  # board is not full
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    You may assume utility will only be called on a board if terminal(board) is True.

    :param board: 2d-list of shape (3, 3)
    :return: {-1, 0, 1}

    """
    utility_map = {
        X: 1,
        None: 0,
        O: -1,
    }

    # get win status and map utility from dictionary
    return utility_map[winner(board)]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    If the board is a terminal board, the minimax function should return None.

    :param board: 2d-list of shape (3, 3)
    :return: 1d-tuple of len 2 with coordinates (i, j)
    """
    ####
    # return None if board is a terminal state
    ####
    if terminal(board):
        return None

    ####
    # recursive minimax functions
    ####
    def minimax_value(bstate, a1=-math.inf, b1=math.inf, max_option=True):
        """
        function to get max(min)imising value,
        via recursively and alternating calling min(max)imising function

        :param bstate: 2d-list of shape (3, 3)
        :param a1: int, min score (min'ed by min player) that the max player is assured of
        :param b1: int, max score (max'ed by min player) that the min player is assured of
        :param max_option: bool, {True: maximise, False: minimise}
        :return: int
        """
        # initialise value representing the working value of the current node
        # as player iterates through subnodes.
        if max_option:  # set value as -inf so that maximising agent will play.
            minimax_value1 = -math.inf
        else:  # set value as inf so that minimising agent will play.
            minimax_value1 = math.inf

        # recursively and alternating to (max/min) agent, until terminal state is reached.
        if terminal(bstate):  # if terminal state is reached,
            return utility(bstate)  # return utility of the terminal node.
        else:  # elif not a terminal node,
            # for all subnodes below (possible actions at) the current node,
            for maction1 in actions(bstate):
                # recursively call other (max/min) agent
                # to get value all of subnodes in the current node.
                minimax_value_try = minimax_value(result(bstate, maction1), a1, b1, not max_option)

                if max_option:  # max agent wants to maximise utility.
                    minimax_value1 = max(minimax_value1, minimax_value_try)  # compute max
                    if minimax_value1 == 1:  # if found value is max already
                        return minimax_value1  # use it.
                    # if value (max'ed by max player) is more than,
                    if minimax_value1 >= b1:  # what min player is assured of (beta),
                        break  # skip calculation of branch.
                    # alpha, the score that max player is assured of,
                    # gets passed into for loop,
                    # iterating through all subnodes of max player subnode actions
                    a1 = max(a1, minimax_value1)

                else:  # min agent wants to minimise utility.
                    minimax_value1 = min(minimax_value1, minimax_value_try)  # compute min
                    if minimax_value1 == -1:  # if found value is min already
                        return minimax_value1  # use it.
                    # if value (min'ed by min player) is less than,
                    if minimax_value1 <= a1:  # what max player is assured of (alpha),
                        break  # skip calculation of branch.
                    # beta, the score that min player is assured of,
                    # gets passed into for loop,
                    # iterating through all subnodes of min player subnode actions
                    b1 = min(b1, minimax_value1)

            return minimax_value1  # return result

    ####
    # main
    ####
    max_option_d = {  # dictionary of minimax functions to use
        X: False,  # X is maximising; wants to get O's best play
        O: True,  # O is minimising; wants to get X's best play
    }
    minimax_func_d = {  # dictionary of minimax functions to use
        X: max,  # X is maximising
        O: min,  # O is minimising
    }

    next_player = player(board)  # get next player.
    all_actions = list(actions(board))  # all possible actions as list.
    all_actions_u = []  # initialise list with corresponding utility of all possible actions list.

    # if first player (number of possible actions equal all spaces on board)
    if len(all_actions) == len(board) ** 2:
        # always start in a random corner
        return (random.randint(0, 1) * 2, random.randint(0, 1) * 2)
    # if not first player
    else:
        # get utility of all possible actions
        for action1 in all_actions:
            # The maximizing player picks action a in Actions(s)
            # that produces the highest value of Min-Value(Result(s, a)).
            # The minimizing player picks action a in Actions(s)
            # that produces the lowest value of Max-Value(Result(s, a)).
            all_actions_u.append(
                minimax_value(
                    bstate=result(board, action1),  # current board and possible action
                    max_option=max_option_d[next_player]  # max or min
                )
            )

        # get index of max/min utility action
        opt_action_idx = all_actions_u.index(minimax_func_d[next_player](all_actions_u))
        opt_action = all_actions[opt_action_idx] # get max/min action

        # return
        return opt_action
