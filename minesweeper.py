import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.

        :param self:
        :return: set() containing tuples (i, j) of coordinates
        """

        # if number of squares equal number of mines,
        if len(self.cells) == self.count:
            return self.cells  # all squares are mines
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.

        :param self:
        :return: set() containing tuples (i, j) of coordinates
        """
        # if number of mines is zero
        if self.count == 0:
            return self.cells # no squares are mines
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.

        If cell is in the sentence, the function should update the sentence
        so that cell is no longer in the sentence,
        but still represents a logically correct sentence
        given that cell is known to be a mine.
        If cell is not in the sentence, then no action is necessary.

        :param self:
        :param cell: 1d-tuple of length 2, (i, j) of mine coordinates
        :return: None
        """
        # if the mine cell is in the sentence
        if cell in self.cells:
            self.cells.remove(cell)  # remove cell from sentence
            self.count += -1  # subtract 1 from mine count
        else:
            pass  # do nothing

        return None

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.

        If cell is in the sentence,
        the function should update the sentence
        so that cell is no longer in the sentence,
        but still represents a logically correct sentence
        given that cell is known to be safe.
        If cell is not in the sentence, then no action is necessary.

        :param self:
        :param cell: 1d-tuple of length 2, (i, j) of safe square coordinates
        :return: None
        """
        # if the safe cell is in the sentence
        if cell in self.cells:
            self.cells.remove(cell)  # remove cell from sentence
        else:
            pass  # do nothing

        return None


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge

        :param cell: 1d-tuple of length 2, (i, j) of cell (square) coordinates
        :param count: corresponding count of cell (square)
        :return: None
        """

        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        self.last_move = cell  # store last move

        # 2) mark the cell as safe,
        # updating any sentences that contain the cell
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base
        #    based on the value of `cell` and `count`
        self.knowledge.append(
            Sentence(
                cells=self.get_surrounding_cells(cell, self.height, self.width),
                count=count,
            )
        )

        # 4) mark any additional cells as safe or as mines
        #    if it can be concluded based on the AI's knowledge base
        add_safes = set()  # newly concluded safe cells
        add_mines = set()  # newly concluded mine cells
        for sentence1 in self.knowledge:  # from existing knowledge,
            add_safes.update(sentence1.known_safes())  # conclude more safe cells
            add_mines.update(sentence1.known_mines())  # conclude more mine cells
        # for the newly concluded cells,
        self.safes.update(add_safes)  # add to ai safe set
        self.mines.update(add_mines)  # add to ai mine set

        # update knowledge with ai safes and mines
        for safe1 in self.safes:  # for each newly concluded safe cell,
            self.mark_safe(safe1)  # update knowledge base.
        for mine1 in self.mines:  # for each newly concluded mine cell,
            self.mark_mine(mine1)  # update knowledge base.

        # clean up knowledge base
        rem_knowledge = []  # list knowledge idx to remove
        for sentence_idx1 in range(0, len(self.knowledge)):  # from existing knowledge,
            if len(self.knowledge[sentence_idx1].cells) == 0:  # if empty set
                rem_knowledge.append(sentence_idx1)  # store index for removal
        for sentence_idx1 in sorted(rem_knowledge, reverse=True):  # for all indexes for removal
            del self.knowledge[sentence_idx1]  # remove

        # 5) add any new sentences to the AI's knowledge base
        #    if they can be inferred from existing knowledge
        add_sentences = []  # newly concluded sentences
        for sentence1 in self.knowledge:  # compare sentences,
            for sentence2 in self.knowledge:  # from existing knowledge.
                # attempt to infer new sentence
                new_sentence = self.subset_reason(sentence1, sentence2)
                if new_sentence is not None:  # if new sentence can be inferred,
                    add_sentences.append(new_sentence)  # add to list of newly concluded sentences
        # add newly concluded sentences to ai knowledge base
        self.knowledge.extend(add_sentences)

        return None

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.

        1d-tuple of length 2, (i, j) of cell (square) coordinates
        If no safe move can be guaranteed, the function should return None.

        :return: {(i, j), None}
        """
        # update list of self.possible_safe_moves
        self.possible_safe_moves = list(self.safes - self.moves_made)
        if len(self.possible_safe_moves) > 0:  # if possible safe move exists,
            return random.choice(self.possible_safe_moves)  # return a random safe move
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines

        1d-tuple of length 2, (i, j) of cell (square) coordinates
        If no (not mined) move can be made, the function should return None.

        :return: {(i, j), None}
        """
        # if the all_board attribute has not been defined,
        if not hasattr(self, "all_board"):  # get set of the entire board
            self.all_board = set([(i, j) for i in range(0, self.height) for j in range(0, self.width)])
        # update list of possible maybe moves (could be mines)
        self.possible_maybe_moves = list(self.all_board - self.moves_made - self.mines)
        if len(self.possible_maybe_moves) > 0:  # if possible maybe move exists,
            if hasattr(self, "last_move"):  # select last move as anchor cell
                anchor_cell = random.choice(list(self.moves_made))
            else:  # very first move is random
                return random.choice(self.possible_maybe_moves)
            manhattan_dist = []  # initialise list of manhattan distances corresponding to maybe move list
            for maybe_move1 in self.possible_maybe_moves:  # for all maybe moves,
                # compute manhattan distance
                md1 = abs(maybe_move1[0] - anchor_cell[0]) + abs(maybe_move1[1] - anchor_cell[1])
                if md1 < 3:  # if manhattan distance is less than 3 (de-prioritise adjacent cells),
                    md1 = self.height * self.width  # set distance as board height * width
                manhattan_dist.append(md1)
            # get index of maybe move with the furthest manhattan distance to anchor
            closest_idx = manhattan_dist.index(min(manhattan_dist))
            return self.possible_maybe_moves[closest_idx]  # return a random maybe move
        else:
            return None

    @staticmethod
    def get_surrounding_cells(cell, _h1, _w1):
        """
        function to get cells around original cell,
        excluding original cell

        :param cell: 1d-tuple of length 2, (i, j) of cell (square) coordinates
        :param _h1: height of board
        :param _w1: width of board
        :return: set() containing tuples (i, j) of coordinates
        """
        # generate cells around original cell:
        s_cells = set()  # initialise empty set
        # limit at 0 and height
        for i in range(max([cell[0]-1, 0]), min([cell[0]+2, _h1])):
            # limit at 0 and width
            for j in range(max([cell[1]-1, 0]), min([cell[1]+2, _w1])):
                s_cells.add((i, j))  # add indices as tuple to set
        # exclude original cell
        s_cells.remove(cell)
        # return set
        return s_cells

    @staticmethod
    def subset_reason(sentence1, sentence2):
        """
        function to reason a new sentence if
        sentence1 is a proper subset of sentence2.
        Otherwise return None

        :param sentence1: Sentence() object
        :param sentence2: Sentence() object
        :return: {Sentence(), None}
        """
        # check that sentence2.cells is a proper subset of sentence1.cells
        if sentence1.cells > sentence2.cells:
            new_sentence_cells = sentence1.cells - sentence2.cells  # difference cells
            new_sentence_count = sentence1.count-sentence2.count  # difference count
            # return new differenced sentence that contains
            return Sentence(cells=new_sentence_cells, count=new_sentence_count)
        else:  # otherwise return None
            return None
