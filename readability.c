// header files (libraries)
# include <ctype.h>
# include <stdio.h> // standard input output: used to get input and show output from the user
# include <string.h>
# include <math.h>

# include <cs50.h> // custom library


// prototypes
void get_text_counts(
    string text1,
    int *lettercount,
    int *wordcount,
    int *sentcount
    );

// code
int main(void) // main script
{
    // get user input
    string text1 = get_string("TEXT: ");
    printf("%s\n", text1); // print

    // count the number of letters and words
    int n_letters, n_words, n_sent;
    get_text_counts(text1, &n_letters, &n_words, &n_sent);

    // printf("%i letter(s)\n", n_letters); // debug
    // printf("%i word(s)\n", n_words); // debug
    // printf("%i sentence(s)\n", n_sent); // debug

    // compute Coleman-Liau index
    float L = n_letters / (float) n_words * 100;
    float S = n_sent / (float) n_words * 100;
    float cl_idx = 0.0588 * L - 0.296 * S - 15.8;
    // round to int
    int cl_idx_round = round(cl_idx);
    // printf("%i cl_idx_round\n", cl_idx_round); // debug


    // print results
    if (cl_idx < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (cl_idx >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", cl_idx_round);
    }

    return cl_idx;
}


void get_text_counts(
    string text1,
    int *lettercount,
    int *wordcount,
    int *sentcount
    )
{
    /*
    * function to get the count of alphabetical letters in a string
    */
    *lettercount = 0;
    *wordcount = 1; // start from 1, assuming spaces are only between words
    *sentcount = 0;

    for ( // loop through each letter in word
        int tidx = 0, textlen = strlen(text1); // length of the text
        tidx < textlen;
        tidx++
        )
    {
        // add letter
        if (isalpha(text1[tidx]) != 0)
        {
            *lettercount = *lettercount + 1;
        }
        // add word
        if (isspace(text1[tidx]) != 0)
        {
            *wordcount = *wordcount + 1;
        }
        // add sentence
        if (
            (text1[tidx] == '.')
            || (text1[tidx] == '!')
            || (text1[tidx] == '?')
            )
        {
            *sentcount = *sentcount + 1;
        }

    }


}







