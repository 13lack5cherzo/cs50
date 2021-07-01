def get_textcounts(text1):
    """
    function to get counts in text
    """
    lettercount = 0
    wordcount = 1
    sentcount = 0

    # interate through every character
    for char1 in text1:
        if (char1.isalpha()):
            lettercount += 1
        if (char1 == " "):
            wordcount += 1
        if (char1 in [".", "!", "?"]):
            sentcount += 1

    return lettercount, wordcount, sentcount

def main():
    # retrieve text from user
    input_text = input("Text: ")

    # get counts
    counts = get_textcounts(input_text)
    counts = dict(zip(["n_letter", "n_word", "n_sent"], counts))
    # print(counts) # debug

    # compute Coleman-Liau index
    L = counts["n_letter"] / counts["n_word"] * 100;
    S = counts["n_sent"] / counts["n_word"] * 100;
    cl_idx = 0.0588 * L - 0.296 * S - 15.8
    cl_idx_round = round(cl_idx)
    # print(cl_idx) # debug

    # print results
    if (cl_idx < 1):
        print("Before Grade 1")
    elif (cl_idx >= 16):
        print("Grade 16+")
    else:
        print("Grade {}".format(cl_idx_round))

    return 0

if __name__ == "__main__":
    main()






