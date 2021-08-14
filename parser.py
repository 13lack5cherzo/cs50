import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> CL | CL Conj CL | CL Conj CL
CL -> NP VP
CL -> VP NP

NP -> AdN | Det AdN
AdN -> N | Adj N | Adj AdN
NP -> NP P NP
NP -> NP Adv

VP -> V | V NP
VP -> VP P | VP P NP
VP -> Adv VP | VP Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.

    :param sentence: str()
    :return: list() of pre-processed words
    """
    tokenizer1 = nltk.tokenize.RegexpTokenizer(r'[a-zA-Z]+')  # only letter char
    w_list = tokenizer1.tokenize(sentence)  # tokenise
    w_list = [str1.lower() for str1 in w_list]  # lower case
    return w_list


def tree_check_label(check_tree, label_str="NP"):
    """
    function to check if tree is has noun phrase label
    :param check_tree: nltk.tree() objects
    :param label_str: str label to check
    :return: {[nltk.tree()], []}
    """
    if check_tree._label == label_str:
        return [check_tree]
    else:  # does not have label
        return []


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.

    :param tree: nltk.tree() objects
    :return: list() of nltk.tree() objects
    """
    if tree.height() == 2:  # terminal subtree
        return tree_check_label(tree)  # return list() containing tree if noun phrase
    else:  # not terminal subtree
        np_trees = []  # init list of noun phrase trees
        for subtree1 in tree:  # one level down
            np_trees.extend(np_chunk(subtree1))  # recursively get noun phrase trees
        if len(np_trees) > 0:  # at least 1 noun phrase tree found
            return np_trees  # return all lower level noun phrase trees
        else:  # no noun phrase tree found
            return tree_check_label(tree)  # return list() containing tree if noun phrase


if __name__ == "__main__":
    main()
