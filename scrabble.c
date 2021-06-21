#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>



// Points assigned to each letter of the alphabet
const int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
// array of alphabet
const char ALPH[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};
const int alpha_n = 26; // number of letter in the alphabet

// prototype
int compute_score(string word);

int main(void)
{

    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    printf("%i, %i \n", score1, score2);

    // Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!");
    }
    else
    {
        printf("Tie!");
    }

    return 0;
}

int compute_score(string word)
{
    /*
    *function to compute and return score for string
    */

    int score = 0; // initialise score
    for ( // loop through each letter in word
        int widx = 0, wordlen = strlen(word); // length of the word
        widx < wordlen;
        widx++
        )
        {
            char word_l = tolower(word[widx]); // convert to lower case

            for ( // loop through each alphabet
                int aidx = 0;
                aidx < alpha_n;
                aidx++
                )
                { // if matches alphabet in ALPH array,
                    if (word_l == ALPH[aidx])
                    { // add correponding points to score
                        score += POINTS[widx];
                    }
                }
        }
    return score;
}