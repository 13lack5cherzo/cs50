import os
import sys
import string
import nltk
import math


FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.

    :param directory: str of corpus data directory
    :return: dict() of str containing corpus
    """
    corpus_dict = {}  # init dict containing corpus
    for txt1 in os.listdir(directory):
        with open(os.path.join(directory, txt1), encoding="utf8") as f:
            corpus_dict[txt1] = f.read()
    return corpus_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.

    :param document: str of document
    :return: list() of words
    """
    punc_str = string.punctuation  # get punctuation
    stop_l = nltk.corpus.stopwords.words("english")  # get stopwords
    docu_clean = "".join([char1.lower() for char1 in document if char1 not in punc_str])  # remove punctuation
    tokenised_l = nltk.word_tokenize(docu_clean)  # tokenise
    tokenised_l = [w1 for w1 in tokenised_l if (w1 not in stop_l)]  # remove stopwords
    return tokenised_l


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.

    :param documents: dict() of word list() as values() with documents as keys() in the corpus
    :return: dict() of IDF values() with words as keys()
    """
    doc_set = dict()  # init dict() of word set() as values() with documents as keys() in the corpus
    all_words = set()  # init set of all words
    idf_dict = {}  # init dictionary of idf values
    n_docs = len(documents.keys())

    for doc1 in documents.keys():  # iter each document
        doc_set[doc1] = set(documents[doc1])  # create set() of words in document
        all_words.update(doc_set[doc1])  # add words into all_words set()

    for word1 in all_words:  # iter through all words
        w_idf = 0  # init number of documents containing word1 = 0
        for doc1 in documents.keys():  # iter through doc words sets()
            if word1 in doc_set[doc1]:  # if word1 in document
                w_idf += 1  # add 1 to number of documents containing word1
        idf_dict[word1] = math.log(n_docs / w_idf)  # compute idf

    return idf_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.

    :param query: list() of str
    :param files: dict() of word list() as values() with documents as keys() in the corpus
    :param idfs: dict() of IDF float values() mapped by documents as keys()
    :param n: int for number of top files
    :return: list() of len() == n containing str
    """
    tfidf_d = {}  # dict() to hold tf-idf for each document for each word in query
    doc_scores_dict = {}  # init dict to hold document scores
    for doc1 in files.keys():  # iter documents
        tfidf_d[doc1] = {}  # init dict() to hold tf-idf for each word
        doc_scores_dict[doc1] = 0  # init document score as zero
        for word1 in query:
            w_tfidf = files[doc1].count(word1)  # count number of word1 in doc1 (tf)
            w_tfidf = w_tfidf * idfs[word1]  # multiply by idf
            tfidf_d[doc1][word1] = w_tfidf  # add to dict()
            doc_scores_dict[doc1] += w_tfidf  # add to document score

    docs_sort = list(doc_scores_dict.keys())  # init sorted list of documents
    docs_sort.sort(key=lambda x1: doc_scores_dict[x1], reverse=True)  # sort descending

    return docs_sort[:n]  # return top n


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.

    :param query: list() of str
    :param sentences: dict() of word list() as values() with documents as keys() in the corpus
    :param idfs: dict() of IDF float values() mapped by documents as keys()
    :param n: int for number of top files
    :return: list() of len() == n containing str
    """
    sen_density_dict = {}  # init dict to hold sentence density
    sen_scores_dict = {}  # init dict to hold sentence scores (sum of idf)
    for sen1 in sentences.keys():  # iter sentences
        sen_density_dict[sen1] = 0  # init dict() to hold tf-idf for each word
        sen_scores_dict[sen1] = 0  # init sentence score as zero
        for word1 in query:  # iter word
            w_count = sentences[sen1].count(word1)  # count number of word1 in sen1 (tf)
            if w_count > 0:  # if sentence contains word,
                sen_scores_dict[sen1] += idfs[word1]  # add idf to sentence score
            sen_density_dict[sen1] += w_count  # add number to density (temp holding count)
        sen_density_dict[sen1] = sen_density_dict[sen1] / len(sentences[sen1])  # compute density

    sen_sort = list(sen_scores_dict.keys())  # init sorted list of documents
    sen_sort.sort(key=lambda x1: (sen_scores_dict[x1], sen_density_dict[x1]), reverse=True)  # sort descending

    return sen_sort[:n]  # return top n


if __name__ == "__main__":
    main()
