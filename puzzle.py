from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

####
# set up
####


def knight_or_knave(knowledge_base1):
    """
    function that adds the logic (knight <=> !knave) to knowledge base
    :param knowledge_base1: And() object
    """
    role_list = [[AKnight, AKnave], [BKnight, BKnave], [CKnight, CKnave]]
    for person1 in role_list:
        knowledge_base1.add(Biconditional(person1[0], Not(person1[1])))


####
# Puzzle 0
####
# A says "I am both a knight and a knave."
####

knowledge0 = And()  # initialise blank knowledge base
knight_or_knave(knowledge0)  # knight <=> !knave
knowledge0.add(  # AKnight <=> AKnight & AKnave
    Biconditional(AKnight, And(AKnight, AKnave))
)
# print("knowledge0", knowledge0.formula())  # display knowledge base

####
# Puzzle 1
####
# A says "We are both knaves."
# B says nothing.
####

knowledge1 = And()  # initialise blank knowledge base
knight_or_knave(knowledge1)  # knight <=> !knave
knowledge1.add(  # AKnight <=> AKnave & BKnave
    Biconditional(AKnight, And(AKnave, BKnave))
)
# print("knowledge1", knowledge1.formula())  # display knowledge base

####
# Puzzle 2
####
# A says "We are the same kind."
# B says "We are of different kinds."
####

knowledge2 = And()  # initialise blank knowledge base
knight_or_knave(knowledge2)  # knight <=> !knave
knowledge2.add(  # AKnight <=> ((AKnight & BKnight) || (AKnave & BKnave))
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
)
knowledge2.add(  # BKnight <=> ((AKnight & BKnight) || (AKnave & BKnave))
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)
# print("knowledge2", knowledge2.formula())  # display knowledge base

####
# Puzzle 3
####
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
####

knowledge3 = And()  # initialise blank knowledge base
knight_or_knave(knowledge3)  # knight <=> !knave
ASaysKnight = Symbol("A says, 'I am a knight.'")  # new symbol representing what A said
knowledge3.add(  # (AKnight & ASaysKnight) <=> AKnight
    Biconditional(And(AKnight, ASaysKnight), AKnight)
)  # if A is a Knight and said that he is a Knight, A is a Knight
knowledge3.add(  # (AKnave & ASaysKnight) <=> AKnave
    Biconditional(And(AKnave, ASaysKnight), AKnave)
)  # if A is a AKnave and said that he is a Knight, A is a AKnave
knowledge3.add(  # BKnight <=> !ASaysKnight
    Biconditional(BKnight, Not(ASaysKnight))
)
knowledge3.add(  # BKnight <=> CKnave
    Biconditional(BKnight, CKnave)
)
knowledge3.add(  # CKnight <=> AKnight
    Biconditional(CKnight, AKnight)
)
# print("knowledge3", knowledge3.formula())  # display knowledge base

####
# main
####


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
