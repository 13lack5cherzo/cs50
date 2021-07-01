import os
import sys
import pandas as pd

def get_max_seq(fullstr1, substr1):
    """
    function to obtain max adjacent occurences of substr1
    """
    n_seq = 1 # number of sequences
    # do while less than max possible checks
    while True:
        # create long sequence using n_seq
        findseq = substr1 * n_seq
        # if can be found
        if (fullstr1.find(findseq) != -1):
            n_seq += 1 # increase n_seq
        else: # cannot be found
            return n_seq - 1
    return 1 # return error value

def main():

    # Ensure correct usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # read csv
    db_df = pd.read_csv(os.getcwd() + "/" + sys.argv[1])
    # read sequence
    seq1 = open(os.getcwd() + "/" + sys.argv[2], "r").read()

    # get max sequences
    max_seq = {}
    for str1 in db_df.columns[1:]:
        max_seq[str1] = get_max_seq(seq1, str1)

    # get individual
    ind1 = db_df.copy()
    for str1 in db_df.columns[1:]:
        ind1 = ind1[(ind1[str1] == max_seq[str1])]

    # print result
    if ind1.empty: # no match
        print("No match")
    else:
        print(ind1["name"].values[0])

    # return 0
    return 0


if __name__ == "__main__":
    main()
