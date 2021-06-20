// header files (libraries)
# include <stdio.h> // standard input output: used to get input and show output from the user
# include <cs50.h> // custom library

// protypes
float start_check(void);
float start_end(float _start_size);

int main(void)
{

    // Prompt for start size
    float start_size = start_check();
    // Prompt for end size
    float end_size = start_end(start_size);
    // TODO: Calculate number of years until we reach threshold

    int years1 = 0; // declare variable to capture years
    int cur_size_t = (int) start_size; // declare working variable to capture current size
    while (end_size > cur_size_t)
    {
        cur_size_t = cur_size_t + (cur_size_t / 3) - (cur_size_t / 4);
        years1++;
    }
    // TODO: Print number of years
    printf("%i", years1);
}



float start_check(void)
/*
* function to receive user input of start_size_temp,
* and check if it is greater than 0
*
* :return: float
*/

{
    bool proceed1 = false; // declare indicator to proceed
    float start_size_temp = 0; // declare start_size_temp
    do
    {
        // get start size from user
        start_size_temp = get_float("start size? \n");
        // check if larger than zero
        proceed1 = !(start_size_temp > 3);
        // printf("%i", proceed1);
    }
    while (proceed1);

    // return last saved end_size_temp
    return start_size_temp;
}




float start_end(float _start_size)
/*
* function to receive user input of end_size_temp,
* and check if it is greater than _start_size
*
* :param _start_size: start size to check user input against
*
* :return: float
*/

{
    bool proceed1 = false; // declare indicator to proceed
    float end_size_temp = 0; // declare end_size_temp
    do
    {
        // get end size from user
        end_size_temp = get_float("end size? \n");
        // check if larger than start size
        proceed1 = !(end_size_temp > _start_size);
    }
    while (proceed1);

    // return last saved end_size_temp
    return end_size_temp;
}
