// header files (libraries)
# include <stdio.h> // standard input output: used to get input and show output from the user
# include <cs50.h> // custom library

// code
int main(void) // main script
{
    // assign string to answer1
    string answer1 = get_string("What is your name? \n");
    // print
    printf("hello, %s", answer1);
}



// in terminal:
// compile
// $ make hello
// run
// $ ./hello



