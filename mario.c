// header files (libraries)
# include <stdio.h> // standard input output: used to get input and show output from the user
# include <cs50.h> // custom library

// protypes
int valid_check(void);

int main(void)
{
    // get height from user input
    int height1 = valid_check();
    // printf("%i", height1);

    // iterate print
    for (int row1 = 1; row1 <= height1; row1++) // working variable row1 for height1 user input
    {
        // print appropriate number of " "
        for (int col1 = height1; col1 > row1; col1--) // working variable col1 for row1 user input
        {
            printf(" ");
        }
        // print appropriate number of "#"
        for (int col1 = 0; col1 < row1; col1++) // working variable col1 for row1 user input
        {
            printf("#");
        }
    printf("\n");
    }
}




int valid_check(void)
/*
* function to receive user input of height_temp,
* and check if it is an int greater than 0 and less than 9
*
* :return: int
*/

{
    bool proceed1 = false; // declare indicator to proceed
    int height_temp = 0; // declare height_temp
    do
    {
        // get start size from user
        height_temp = get_int("height? \n");
        // check if
        proceed1 = !(
            (height_temp > 0) // larger than zero
            && (height_temp < 9) // less than nine
            );
        // printf("%i", proceed1);
    }
    while (proceed1);

    // return last saved height_temp
    return height_temp;
}
