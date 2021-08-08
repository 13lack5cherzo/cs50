import os
import random
import re
import sys
import numpy as np

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.

    If page has no outgoing links,
    then transition_model should return
    a probability distribution that chooses randomly
    among all pages with equal probability.
    (In other words, if a page has no links,
    we can pretend it has links to all pages in the corpus,
    including itself.)

    :param corpus: dict(), of set()s, of str mapping a page name to a set of all pages linked to by that page
    :param page: str representing which page the random surfer is currently on
    :param damping_factor: float
    :return: dict() of float, for the probability that a random surfer would choose that page next
    """

    df = min(max(damping_factor, 0), 1)  # floor, cap damping factor at 0, 1
    dfc = 1 - df  # complement probability of damping factor
    linked_set_str = corpus[page]  # set of str links from page
    all_pages = list(corpus.keys())  # list of str keys, in the same order as corpus

    if len(linked_set_str) == 0:  # if page has no outgoing links,
        # transition_model should return a probability distribution that chooses
        random_p = 1 / len(all_pages)  # randomly among all pages with equal probability
        linked_p = 0  # P{choosing link from page} <- 0
    else:  # if page does have outgoing links,
        # With probability 1 - damping_factor, the random surfer should randomly choose
        # one of all pages in the corpus with equal probability.
        random_p = dfc / len(all_pages)  # P{choosing any page}
        # With probability damping_factor, the random surfer should randomly choose
        # one of the links from page with equal probability.
        linked_p = df / len(linked_set_str)  # P{choosing link from page}

    # assign probabilities
    effective_p = {}  # dict to return,
    for page_str1 in all_pages:  # with keys in the same order as corpus
        effective_p[page_str1] = random_p  # init value as P{choosing any page}
        if page_str1 in linked_set_str:  # if page_str1 is linked from input page,
            effective_p[page_str1] += linked_p  # add P{choosing link from page}

    return effective_p  # return dictionary of probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    You may assume that n will be at least 1

    :param corpus: dict(), of set()s, of str mapping a page name to a set of all pages linked to by that page
    :param damping_factor: float
    :param n: int for number of monte-carlo simulations
    :return: dict() of float, for PageRank value
    """
    ####
    # set up
    ####
    df = min(max(damping_factor, 0), 1)  # floor, cap damping factor at 0, 1
    all_pages = list(corpus.keys())  # list of str keys, in the same order as corpus
    sims_all = np.zeros(shape=len(all_pages))  # init np 1d-array to store simulations

    # generate transition matrix as np array
    tm = np.zeros(shape= [len(all_pages), len(all_pages)])  # init np 2d-array
    for page_idx1 in range(0, len(all_pages)):  # for each page (row of transition matrix)
        tm_row = transition_model(corpus, all_pages[page_idx1], df)  # compute transition probabilities
        tm[page_idx1] = np.array(list(tm_row.values()))  # add to transition matrix

    ####
    # simulation method
    ####
    for sim_n in range(0, max([n, 1])):
        if sim_n == 0:  # first simulation with equal probability
            w_sim = np.random.choice(len(all_pages), size= None, replace= True)
        else:  # subsequent simulations with transition probability based on previous
            w_sim = np.random.choice(len(all_pages), size= None, replace= True, p= tm[w_sim])
        sims_all[w_sim] += 1  # update simulation counts
    # compute pagerank
    pr = sims_all / sims_all.sum()

    ####
    # power method
    ####
    # pr_power = np.ones(tm.shape[0]) @ np.linalg.matrix_power(tm, max([n, 1]))  # matrix power
    # pr_power = pr_power / pr_power.sum()  # normalise to probability measure

    ####
    # output
    ####
    pr_dict = dict(zip(all_pages, pr))  # parse into dict()
    return pr_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    A page that has no links at all
    should be interpreted as
    having one link for every page in the corpus (including itself)

    :param corpus: dict(), of set()s, of str mapping a page name to a set of all pages linked to by that page
    :param damping_factor: float
    :return: dict() of float, for PageRank value
    """

    ####
    # set up
    ####
    df = min(max(damping_factor, 0), 1)  # floor, cap damping factor at 0, 1
    dfc = 1 - df  # complement probability of damping factor
    all_pages = list(corpus.keys())  # list of str keys, in the same order as corpus
    pr_etol = 0.0001  # PageRank error tolerance

    ####
    # compute components
    ####
    pr0 = np.ones(shape= len(all_pages))  # init PageRank as np 2d-array
    pr0 = pr0 / pr0.sum()  # 1 / n
    damp_term = dfc / len(all_pages) * np.ones(shape= len(all_pages))  # (1-d) / n

    # compute adjacency matrix
    adj = np.zeros(shape= [len(all_pages), len(all_pages)])  # init adjacency matrix as np 2d-array
    for from_page_idx in range(0, len(all_pages)):  # from each page
        adj_d = {}  # init adjacency dictionary
        for to_page in all_pages:  # for all possible to_page,
            if to_page in corpus[all_pages[from_page_idx]]:  # if there is link from from_page to to_page,
                adj_d[to_page] = 1  # assign 1 from from_page to to_page,
            else:
                adj_d[to_page] = 0  # assign 0 from from_page to to_page,
        adj[from_page_idx] = np.array(list(adj_d.values()))

    outd = adj.sum(axis=1)  # outdegree
    outd = np.where(outd == 0, len(all_pages), outd)  # all links for pages with no links
    inv_outd_diag = np.diag(outd ** (-1))  # diagonal matrix containing inverse of outdegree
    inv_numlinks = (inv_outd_diag @ adj).T  # 1 / (number of links)
    df_inv_numlinks = df * inv_numlinks  # (dampen factor) / (number of links)

    ####
    # iterative computation
    ####
    iter_continue = True  # bool to do next iteration
    while iter_continue:
        pr1 = damp_term + df_inv_numlinks @ pr0  # compute
        if (abs(pr1 - pr0) > pr_etol).sum() == 0:  # if no PageRank changes by more than error tolerance
            iter_continue = False  # stop iteration
        else:
            pr0 = pr1  # assign to next iteration
    pr1 = pr1 / pr1.sum()

    ####
    # output
    ####
    pr_dict = dict(zip(all_pages, pr1))  # parse into dict()
    return pr_dict


if __name__ == "__main__":
    main()
