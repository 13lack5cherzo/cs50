#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    string name;
    int votes;
    bool eliminated;
}
candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes
    for (int i = 0; i < voter_count; i++)
    {

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            // Record vote, unless it's invalid
            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }


    int elect_round = 0; // election round for debug

    // Keep holding runoffs until winner exists
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        printf("election round: %i \n", elect_round); // debug
        for (int i = 0; i < candidate_count; i++) // debug
        {
            printf("%s, %i, %i \n", candidates[i].name, candidates[i].votes, candidates[i].eliminated);
        }


        // Check if election has been won
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }

        elect_round++; // debug
    }
    return 0;
}

// Record preference if vote is valid
bool vote(int voter, int rank, string name)
{
    /*
    * function to Record preference if vote is valid
    */
    // find name
    for (int nidx = 0; nidx < candidate_count; nidx++)
    {
        // if user input name is in candidate array,
        if (strcmp(name, candidates[nidx].name) == 0)
        {
            // add name to voter preferences array
            preferences[voter][rank] = nidx;
            // exit
            return true;
        }
    }
    // exit if unsuccessful
    return false;
}

// Tabulate votes for non-eliminated candidates
void tabulate(void)
{
    /*
    * function to Tabulate votes for non-eliminated candidates
    */

    // loop through each voter
    for (int vidx = 0; vidx < voter_count; vidx++)
    {
        // printf("vidx %i\n", vidx); // debug
        // declare variable to store voter's effective choice that round,
        // corresponding to a candidate
        int e_choice = -1;

        // loop through each preference
        int pidx = 0; // declare preference index
        bool ploop_b = true; // declare flag to continue preference looping
        while (ploop_b)
        {
            // printf("pidx %i\n", pidx); // debug
            if ( // if candidate is eliminated
                candidates[
                    preferences[vidx][pidx] // for candidate index in voter_vidx preference_pidx,
                    ].eliminated) // get eliminated status
                {
                    // candidate was eliminated, so use the next preference
                    pidx++;
                }
            else
            { // candidate was not eliminated, so
                // add vote to that candidate for that round
                candidates[preferences[vidx][pidx]].votes = candidates[preferences[vidx][pidx]].votes + 1;
                ploop_b = false; // stop loop
            }

        }

    }

    return;
}

// Print the winner of the election, if there is one
bool print_winner(void)
{
    /*
    * function to Print the winner of the election, if there is one
    */

    // required votes to win
    float win_cond = voter_count / 2.0;

    // for each candidate,
    for (int cidx = 0; cidx < candidate_count; cidx++)
    {
        // if the candidate has more than 1/2 the votes,
        if ((float) candidates[cidx].votes > win_cond)
        {
            // there exists a winner
            printf("%s\n", candidates[cidx].name);
            return true;
        }
    }
    // else exit
    return false;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    /*
    * function to Return the minimum number of votes any remaining candidate has
    */
    // declare working minimum as number of voters as placeholder
    int working_min = voter_count;

    // for each candidate,
    for (int cidx = 0; cidx < candidate_count; cidx++)
    {
        // check that the candidate is in the election
        if (!candidates[cidx].eliminated) // not eliminated
        {
            // if the candidate has less votes than the current minimum,
            if (candidates[cidx].votes < working_min)
            {
                // use that candidates' vote count
                working_min = candidates[cidx].votes;
            }
        }
    }

    return working_min;
}

// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min)
{
    /*
    * function to Return true if the election is tied between all candidates, false otherwise
    */
    // declare working tie as true
    int working_tie = true;

    // for each candidate,
    for (int cidx = 0; cidx < candidate_count; cidx++)
    {
        // check that the candidate is in the election
        if (!candidates[cidx].eliminated) // not eliminated
        {
            // if the candidate's votes not equal the min,
            if (!(candidates[cidx].votes == min))
            {
                // it is not a winner tie
                working_tie = false;
            }
        }
    }
    return working_tie;
}

// Eliminate the candidate (or candidates) in last place
void eliminate(int min)
{
    /*
    * function to Eliminate the candidate (or candidates) in last place
    */
    // for each candidate,
    for (int cidx = 0; cidx < candidate_count; cidx++)
    {
        // check that the candidate is in the election
        if (!candidates[cidx].eliminated) // not eliminated
        {
            // if the candidate's votes not equal the min,
            if (candidates[cidx].votes == min)
            {
                // eliminate
                candidates[cidx].eliminated = true;
            }
        }
    }

    return;
}
