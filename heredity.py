import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.

    assume that either mother and father are both blank (no parental information in the data set),
    or mother and father will both refer to other people in the people dictionary.

    :param people: dict() of persons, each a dict() of variables
    :param one_gene: set() of persons to compute Pr{one_gene}
    :param two_genes: set() of persons to compute Pr{two_genes}
    :param have_trait: set() of persons to compute Pr{have_trait}
    :return: float of the joint probability that, for person:
            person has gene={0,1,2} and trait={True, False}
    """

    ####
    # set up
    ####
    P_INHERIT = {0: 0, 1: 0.5, 2: 1}  # dict() of P{inherit gene | parent's gene}
    # gene_event = dict() of gene event by person, to compute probability for.
    # trait_event = dict() of trait event by person, to compute probability for.
    gene_event, trait_event = parse_events(  # parse input
        list(people.keys()), one_gene, two_genes, have_trait
    )

    ####
    # Pr{ gene={0,1,2} }
    ####
    p_gene_event = {}  # dict() of Pr{gene event} by person, corresponding to gene_event
    for person1 in people.keys():
        if (  # if no parents,
                (people[person1]["mother"] is None)
                | (people[person1]["father"] is None)
        ):  # use unconditional probability.
            p_gene_event[person1] = PROBS["gene"][gene_event[person1]]
        else:  # if parents exist,
            p_got1gene = {}  # dict() of Pr{inherit or mutate 1 gene | parent's gene} per parent
            for parent1 in ["mother", "father"]:  # for each parent
                # Pr{inherit gene | parent's gene}
                p_inherit = P_INHERIT[gene_event[people[person1][parent1]]]
                # Pr{inherit or mutate 1 gene | parent's gene}
                # = Pr{inherit gene | parent's gene} * (1 - Pr{mutate})
                #   + (1 - Pr{inherit gene | parent's gene}) * Pr{mutate}
                p_got1gene_temp = p_inherit * (1 - PROBS["mutation"]) \
                    + (1 - p_inherit) * PROBS["mutation"]
                p_got1gene[parent1] = p_got1gene_temp  # add to dict

            p_binomial = {  # dict to store binomial distribution
                0: (1-p_got1gene["mother"]) * (1-p_got1gene["father"]),
                2: p_got1gene["mother"] * p_got1gene["father"],
            }
            p_binomial[1] = 1 - p_binomial[0] - p_binomial[2]
            p_gene_event[person1] = p_binomial[gene_event[person1]]  # read of binomial distribution

    ####
    # Pr{ trait={True, False} }
    ####
    p_trait_event = {}  # dict() of P{trait event} by person, corresponding to trait_event
    for person1 in people.keys():
        p_trait_event[person1] = PROBS["trait"][gene_event[person1]][trait_event[person1]]

    p_joint = 1  # initialise joint probability
    for p_gene_event1 in p_gene_event.values():
        p_joint = p_joint * p_gene_event1  # multiply Pr{ gene={0,1,2} }
    for p_trait_event1 in p_trait_event.values():
        p_joint = p_joint * p_trait_event1  # multiply Pr{ trait={True, False} }

    return p_joint
    # joint_probability(people, {"Harry"}, {"James"}, {"James"})  # debug


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.

    :param probabilities: dict() of probability distribution per person over gene and trait
    :param one_gene: set() of persons to compute Pr{one_gene}
    :param two_genes: set() of persons to compute Pr{two_genes}
    :param have_trait: set() of persons to compute Pr{have_trait}
    :param p: joint probability
    :return: None
    """

    gene_event, trait_event = parse_events(  # parse input
        list(probabilities.keys()), one_gene, two_genes, have_trait
    )

    for person1 in probabilities.keys():
        probabilities[person1]["gene"][gene_event[person1]] += p  # update Pr{gene}
        probabilities[person1]["trait"][trait_event[person1]] += p  # update Pr{trait}

    return None


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).

    :param probabilities: dict() of probability distribution per person over gene and trait
    :return: None
    """
    p_sum = {}  # initialise sum of probabilities
    # sum probabilities
    for person1 in probabilities.keys():  # for each person,
        p_sum[person1] = {}
        for rv1 in probabilities[person1].keys():  # for each random variable,
            p_sum[person1][rv1] = 0
            for rv_state1 in probabilities[person1][rv1].keys():  # for each random variable state
                p_sum[person1][rv1] += probabilities[person1][rv1][rv_state1]

    # divide probabilities
    for person1 in probabilities.keys():  # for each person,
        for rv1 in probabilities[person1].keys():  # for each random variable,
            for rv_state1 in probabilities[person1][rv1].keys():  # for each random variable state
                probabilities[person1][rv1][rv_state1] = probabilities[person1][rv1][rv_state1] / p_sum[person1][rv1]

    return None


def parse_events(all_persons, one_gene, two_genes, have_trait):
    """
    function to parse inputs into event dictionary

    :param all_persons: list() of all persons
    :param one_gene: set() of persons to compute Pr{one_gene}
    :param two_genes: set() of persons to compute Pr{two_genes}
    :param have_trait: set() of persons to compute Pr{have_trait}
    """
    gene_event = {}  # dict() of gene event by person, to compute probability for
    trait_event = {}  # dict() of trait event by person, to compute probability for
    for person1 in all_persons:
        # assign gene event to compute probability for
        if person1 in one_gene:
            gene_event[person1] = 1
        elif person1 in two_genes:
            gene_event[person1] = 2
        else:
            gene_event[person1] = 0
        # assign gene event to compute probability for
        if person1 in have_trait:
            trait_event[person1] = True
        else:
            trait_event[person1] = False

    return gene_event, trait_event


if __name__ == "__main__":
    main()
