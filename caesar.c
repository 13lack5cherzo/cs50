// header files (libraries)
# include <ctype.h>
# include <stdio.h> // standard input output: used to get input and show output from the user
# include <stdlib.h>
# include <string.h>
# include <math.h>


# include <cs50.h> // custom library


// prototypes
bool isnumber(string text1);
const char* ccipher(string text1, int key);

// code
int main( // main script
    int argc,
    string argv[]
    )
{
    // Check that program was run with one command-line argument
    if (argc != 2)
    {
        printf("Usage: %s key\n", argv[0]);
        return 1; // number of arguments are incorrect
    }
    // check that argument is a number
    if (!isnumber(argv[1]))
    {
        printf("Usage: %s key\n", argv[0]);
        return 2; // not a number
    }

    // Convert that command-line argument from a string to an int
    int c_key = atoi(argv[1]);
    // check that argument is positive
    if (c_key < 0)
    {
        printf("Usage: %s key\n", argv[0]);
        return 3; // negative number
    }
    // printf("%i\n", c_key); // debug


    // Prompt user for plaintext
    string text1 = get_string("plaintext: ");
    // printf("%s\n", text1); // debug

    // encrypt
    const char* ciphertext = ccipher(text1, c_key);
    // print result
    printf("ciphertext: %s\n", ciphertext);

    return 0; // exit code
}




bool isnumber(string text1)
{
    /*
    * function to check if input is a number
    */

    // output
    bool accept_text = true;
    // Iterate over the provided argument to make sure all characters are digits
    for (
        int tidx = 0, tlen = strlen(text1);
        tidx < tlen;
        tidx++
    )

    {
        if (!isdigit(text1[tidx]))
        {
            accept_text = false;
        }
    }

    return accept_text;

}




const char* ccipher(string text1, int key)
{
    /*
    * function to apply caesar cipher
    */

    // initialise text len
    int tlen = strlen(text1);
    // initialise new text
    char new_text[tlen + 1]; // +1 for '\0'

    for (
        int tidx = 0;
        tidx < tlen;
        tidx++
        )
    {
        // check if char is an alphabet
        if (isalpha(text1[tidx]) != 0)
        {

            int l1 = (int) text1[tidx]; // store letter as ascii int value
            int new_l = 1; // declare for encrypted int value
            char new_c = 'a'; // declare for encrypted letter

            // uppercase
            if ((text1[tidx] >= 'A') && (text1[tidx] <= 'Z'))
            {
                l1 = l1 - (int) 'A' + 1; // convert "alphabet index" to start from 1
                new_l = (l1 + key) % 26 + (int) 'A' - 1; // encrypt
            }
            else if ((text1[tidx] >= 'a') && (text1[tidx] <= 'z'))
            {
                l1 = l1 - (int) 'a' + 1; // convert "alphabet index" to start from 1
                new_l = (l1 + key) % 26 + (int) 'a' - 1; // encrypt
            }
            new_text[tidx] = (char) new_l;
        }
        else // if not an alphabet,
        {
            // return as is
            new_text[tidx] = text1[tidx];
        }
    }

    // put in '\0'
    new_text[tlen] = '\0';

    // declare pointer to return result
    char *new_textr = new_text;
    return new_textr;
}


