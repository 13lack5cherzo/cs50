// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

void free_ll(node *nf);

// Number of buckets in hash table
const unsigned int N = 26 * 26 + 1;

// Number of words in dictionary
unsigned int w_count = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // hash word
    unsigned int hidx = hash(word);

    // traverse nodes in table[hidx] to find match
    for (node *tempnode = table[hidx]; tempnode != NULL; tempnode = tempnode->next)
    {
        // if match is found,
        if (strcasecmp(tempnode->word, word) == 0)
        {
            return true;
        }
    }
    // if no match is found,
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    if (isalpha(word[0]) == 0)
    {
        // not alphabet
        return (N - 1);
    }
    else
    {
        // get alphabet index of first and second letters
        // 'a' starts from 1
        int l1 = tolower(word[0]) - 'a' + 1;
        int l2 = tolower(word[1]) - 'a' + 1;

        // handle edge cases
        if ((l1 < 1) || (l1 > 26))
        {
            l1 = 26; // put in last bucket
        }
        if ((l2 < 1) || (l2 > 26))
        {
            l2 = 26; // put in last bucket
        }

        return (l1 * l2 - 1);
    }
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // open dictionary file
    FILE *dic_pointer = fopen(dictionary, "r");
    if (dic_pointer == NULL)
    {
        printf("Error: cannot open %s\n", dictionary);
        return 2;
    }

    // Set hash table all to null
    for (int tidx = 0; tidx < N; tidx++)
    {
        table[tidx] = NULL;
    }

    // read strings from file one at a time
    char word[LENGTH + 1]; // placeholder
    int hidx = 0; // hashed word index
    while(fscanf(dic_pointer, "%s", word) != EOF)
    {
        // allocate memory for node
        node *n = malloc(sizeof(node));
        if (n == NULL) // exit if not read
        {
            return false;
        }

        // copy word into node
        strcpy(n->word, word);

        // hash word
        hidx = hash(word);

        // insert node into hash table
        n->next = table[hidx];
        table[hidx] = n;

        // keep track of number of words in dictionary
        w_count++;
    }

    fclose(dic_pointer);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return w_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int tidx = 0; tidx < N; tidx++)
    {
        free_ll(table[tidx]);
    }
    return true;
}

// free linked list
void free_ll(node *nf)
{
    // Handle base case
    if (nf == NULL)
    {
        return;
    }
    // linked nodes
    free_ll(nf->next);
    // free node
    free(nf);
}
