import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
        constraints; in this case, the length of the word.)

         :return: None
        """
        variables_iter = self.domains.keys()  # init copy of domain dict() keys.
        for variable1 in variables_iter:  # for each variable,
            del_str_s = set()  # init set of str to remove for each variable
            for value1 in self.domains[variable1]:  # iterate through variable domain.
                if variable1.length != len(value1):  # if unary consistency does not hold,
                    del_str_s.add(value1)  # add to set of str to delete
            self.domains[variable1] -= del_str_s  # remove str marked for deletion
        return None

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.

        :param x: Variable() object
        :param y: Variable() object
        :return: bool; True if a revision was made to the domain of x
        """

        revised_bool = False  # init bool: True if a revision was made to the domain of x
        overlap_ret = self.crossword.overlaps[x, y]  # return from overlap function
        if overlap_ret is None:  # no overlap (Crossword().overlaps returns None)
            return revised_bool
        else:  # overlap exists
            x_str_idx, y_str_idx = overlap_ret  # get indices of str to compare
            del_str_s = set()  # init set of str to remove for x Variable.domain
            for str1_x in self.domains[x]:  # iter through x's domain.
                del_b = True  # init bool to indicate if str1_x should be deleted
                for str1_y in self.domains[y]:  # if no y in Y.domain satisfies constraint for (X,Y):
                    # if the char in y's domain corresponds to the char in x's domain,
                    if str1_x[x_str_idx] == str1_y[y_str_idx]:
                        del_b = False  # mark the str value from x's domain as do not delete
                if del_b:  # if marked for delete,
                    del_str_s.add(str1_x)  # add str to set to be deleted
            self.domains[x] -= del_str_s  # remove all str marked for deletion from x's domain
            if len(del_str_s) > 0:  # if str were deleted,
                revised_bool = True  # revision was made

            return revised_bool

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.

        :param arcs: list of tuple (x, y) of a variable x and a different variable y
        :return: {True, False}
        """

        if arcs is None:  # use all arcs if parameter is not specified
            # queue = all arcs in csp
            all_arcs = self.crossword.overlaps.copy()
            all_arcs = {
                key1: all_arcs[key1]
                for key1 in all_arcs.keys()  # key1 is in the form (var1, var2)
                if all_arcs[key1] is not None  # remove non-arcs
            }
            all_arcs = set(all_arcs.keys())  # drop coordinates
            arc_queue = list(all_arcs)  # use list as queue
        else:
            arc_queue = arcs.copy()  # use specified parameter if arcs is specified

        # ac-3 algorithm
        while len(arc_queue) > 0:  # while queue non-empty:
            w_arc = arc_queue.pop(0)  # (X, Y) = Dequeue(queue)
            if self.revise(*w_arc):  # if Revise(csp, X, Y):
                # if size of X.domain == 0:
                if len(self.domains[w_arc[0]]) == 0:
                    return False
                # for each Z in X.neighbors - {Y}:
                # Enqueue(queue, (Z,X))
                for other_arc1 in self.crossword.neighbors(w_arc[0]) - set([w_arc[0]]):
                    arc_queue.append((other_arc1, w_arc[0]))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.

        :param assignment: dict() with Variable() objects as .keys() and str as .values()
        :return: bool: True if every Variable() is assigned to a value
        """
        # take set() difference between every Variable() and assignment keys
        not_assigned_vars = self.crossword.variables - set(assignment.keys())
        if len(not_assigned_vars) == 0:  # if every Variable() had been assigned
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.

        An assignment is consistent if
        it satisfies all of the constraints of the problem:
        that is to say, all values are distinct,
        every value is the correct length,
        and there are no conflicts between neighboring variables.

        :param assignment: dict() with Variable() objects as .keys() and str as .values()
        :return: bool: True if consistency holds
        """

        if len(assignment) != len(set(assignment.values())):  # if not all values are distinct
            return False  # not consistent
        for variable1 in assignment.keys():
            # check that length of str is correct (unary constraints)
            if len(assignment[variable1]) != variable1.length:  # unary constraint violated:
                return False  # not consistent
            # check arc constraints with all other variables
            for variable2 in [var2 for var2 in assignment.keys() if var2 != variable1]:
                overlap_ret = self.crossword.overlaps[variable1, variable2]  # return from overlap function
                if overlap_ret is None:  # no overlap (Crossword().overlaps returns None)
                    pass  # pass to iterate to next other variable
                else:  # overlap exists
                    var1_str_idx, var2_str_idx = overlap_ret  # get indices of str to compare
                    # if char in var1 != char in var2 (arc constraint violated)
                    if assignment[variable1][var1_str_idx] != assignment[variable2][var2_str_idx]:
                        return False  # not consistent
        return True  # consistent if all checks passed

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.

        :param var: Variable() object
        :param assignment: dict() with Variable() objects as .keys() and str as .values()
        :return: list() of str, in ascending order of eliminating neighbour values
        """
        var_domain = list(self.domains[var])  # get domain of query Variable()
        all_arcs = self.crossword.overlaps.copy()  # get all arcs
        var_overlap = {
            key1[1]: all_arcs[key1]  # single variable to key dict()
            for key1 in all_arcs.keys()  # key1 is in the form (var1, var2)
            if all_arcs[key1] is not None  # remove non-arcs
            and key1[0] == var  # connected to the query Variable()
            and key1[1] not in assignment.keys()  # not already assigned
        }  # var_overlap in the form {overlap_var: (var_idx, overlap_var_idx)}
        # init list of neighbouring unassigned values eliminated
        var_domain_elim = []  # corresponding to each value in var_domain
        # get eliminated neighbouring values
        for value1 in var_domain:  # iter through every value in the domain of var.
            value1_elim = 0  # init count of elminated values for value1
            for var1 in var_overlap.keys():  # iter through all overlapped Variable()
                for ovlp_value1 in self.domains[var1]:  # iter through all values in neighbour Variable()
                    if value1[var_overlap[var1][0]] != ovlp_value1[var_overlap[var1][1]]:
                        value1_elim += 1  # if str at overlapping coordinates are not the same, eliminate
            var_domain_elim.append(value1_elim)  # append eliminated values for value1 to var_domain_elim
        return_sorted = [x for _, x in sorted(zip(var_domain_elim, var_domain))]  # sort ascending
        return return_sorted

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.

        :param assignment: dict() with Variable() objects as .keys() and str as .values()
        :return: Variable() object
        """

        unass_v = list(self.crossword.variables - set(assignment.keys()))  # get unassigned variables
        domain_count = []  # list corresponding to unass_v to contain count of domains
        for variable1 in unass_v:
            domain_count.append(len(self.domains[variable1]))  # get count of domain
        # get indices of unass_v with the minimum domain
        min_indices = [idx for idx in range(0, len(domain_count)) if domain_count[idx] == min(domain_count)]
        min_tie_list = [unass_v[idx] for idx in min_indices]  # list of variables with min domain
        if len(min_indices) == 1:  # if only 1 variable with minimum domain,
            return min_tie_list[0]  # return variable with smallest domain
        else:  # > 1 variable with minimum domain (tie),
            # get degree
            all_arcs = self.crossword.overlaps.copy()  # get all arcs
            all_arcs = [
                key1[0]  # single variable
                for key1 in all_arcs.keys()  # key1 is in the form (var1, var2)
                if all_arcs[key1] is not None  # remove non-arcs
                and key1[0] in min_tie_list  # inside minimum tie list
            ]
            # list of degrees corresponding to min_tie_list
            degree_l = [all_arcs.count(var1) for var1 in min_tie_list]
            # get indices of min_tie_list with the maximum degree
            max_degree_idx = [idx for idx in range(0, len(degree_l)) if degree_l[idx] == max(degree_l)]
            return min_tie_list[max_degree_idx[0]]  # return first one

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.

        :param assignment: dict() with Variable() objects as .keys() and str as .values()
        """

        if self.assignment_complete(assignment):  # if assignment complete:
            return assignment
        #  var = Select-Unassigned-Var(assignment, csp)
        variable1 = self.select_unassigned_variable(assignment)
        # for value in Domain-Values(var, assignment, csp):
        domain_values_list = self.order_domain_values(variable1, assignment)
        for value1 in domain_values_list:
            assignment_test = assignment.copy()  # init new assignment
            assignment_test[variable1] = value1  # create new assignment
            if self.consistent(assignment_test):  # to test consistency
                assignment[variable1] = value1  # add {var = value} to assignment
                result1 = self.backtrack(assignment)
                if result1 is not None:  # if result !≠ failure
                    return result1
                else:  # remove {var = value} and inferences from assignment
                    del assignment[variable1]
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
