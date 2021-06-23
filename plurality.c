#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();

    return 0;
}

// Update vote totals given a new vote
bool vote(string name)
{
    /*
    * function to Update vote totals given a new vote
    */

    // find name
    for (int nidx = 0; nidx < candidate_count; nidx++)
    {
        // if user input name is in candidate array,
        if (strcmp(name, candidates[nidx].name) == 0)
        {
            // add one vote to corresponding name
            candidates[nidx].votes = candidates[nidx].votes + 1;
            // exit
            return true;
        }
    }
    // exit if unsuccessful
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    /*
    * function to Print the winner (or winners) of the election
    * 1. get the maximum score of all candidates
    * 2. print all the candidates with that maximum score
    */

    ////
    // 1
    ////
    // declare variable to store maximum score
    int maxscore = 0;

    // find the maximum score amongst all candidates
    for (int cidx = 0; cidx < candidate_count; cidx++)
    {
        // if candidate has higher votes than the current maxscore,
        if (candidates[cidx].votes > maxscore)
        {
            // set that number of votes as the maxscore
            maxscore = candidates[cidx].votes;
        }
    }

    ////
    // 2
    ////
    // print the candidate name with that max score
    for (int cidx = 0; cidx < candidate_count; cidx++)
    {
        // if candidate has the same number of votes as the  maxscore,
        if (candidates[cidx].votes == maxscore)
        {
            // print the candidate name
            printf("%s\n", candidates[cidx].name);
        }
    }

}

