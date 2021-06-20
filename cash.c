// header files (libraries)
# include <stdio.h> // standard input output: used to get input and show output from the user
# include <cs50.h> // custom library

// protypes
float valid_check(void);

int main(void)
{

    float change1 = valid_check(); // get change from user input
    float c_left = change1; // change left
    int coin_n = 0; // initialise number of coins as zero


    // check if non-zero
    if (change1 > 0)
    {
        // greedy algorithm

        int n_denom1; // declare number of coins of denomination
        // float denom1; // declare denomination

        const int unique_coins = 4; // define array length for number of unique denominated-coins

        // array of unique denominated-coin values (descending)
        float denom_a[] = {0.25, 0.1, 0.05, 0.01}; // array of unique denominated-coin values (descending)

        for (int denom_idx = 0; denom_idx < unique_coins; denom_idx++)
        {
            n_denom1 = 0; // set to zero
            if (c_left >= denom_a[denom_idx])
            {
                n_denom1 = (int) (c_left / denom_a[denom_idx]); // get number of coins of denomination
                c_left = c_left - n_denom1 * denom_a[denom_idx]; // subtract to get outstanding change
                c_left = c_left + 0.000001; // add tolerance
                coin_n = coin_n + n_denom1; // add to coin base
            }
        }


    }

    // print
    printf("%i", coin_n);
    printf("\n");

}




float valid_check(void)
/*
* function to receive user input,
* and check if it is >= 0
*
* :return: float
*/

{
    bool proceed1 = false; // declare indicator to proceed
    float userput1 = 0; // declare userput1
    do
    {
        // get start size from user
        userput1 = get_float("input? \n");
        // check if
        proceed1 = !(
            (userput1 >= 0) // >= 0
            );
        // printf("%i", proceed1);
    }
    while (proceed1);

    // return last saved userput1
    return userput1;
}
