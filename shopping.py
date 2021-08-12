import csv
import os
import sys
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.

    :param filename: str
    :return: tuple (evidence, labels)
    """

    ####
    # load
    ####
    dtypes_d = {}  # init dtypes dict()
    dtypes_d.update({  # int dtypes
        'Administrative': int,
        'Informational': int,
        'ProductRelated': int,
        'OperatingSystems': int,
        'Browser': int,
        'Region': int,
        'TrafficType': int,
        'Weekend': int,
        'Revenue': int,
    })
    dtypes_d.update({  # float dtypes
        'Administrative_Duration': float,
        'Informational_Duration': float,
        'ProductRelated_Duration': float,
        'BounceRates': float,
        'ExitRates': float,
        'PageValues': float,
        'SpecialDay': float,
    })

    shopping_df = pd.read_csv(  # read dataset as pd df
        os.getcwd() + "/" + filename,
        dtype=dtypes_d,
    )

    ####
    # clean
    ####
    # clean Month to int
    shopping_df["Month"] = pd.to_datetime(  # convert to datetime
        shopping_df["Month"].str[:3],  # make string 3 char
        format='%b').dt.month  # get month as int

    # clean VisitorType
    shopping_df["VisitorType"] = np.where(  # if str contains returning
        shopping_df["VisitorType"].str.upper().str.contains("RETURNING") == True,
        1, 0  # {1: returning visitors, 0: not returning visitors}
    ).astype(int)  # coerce to int

    X = [list(row1[1:]) for row1 in shopping_df.iloc[:, :-1].itertuples()]  # parse data into list
    y = shopping_df["Revenue"].tolist()  # parse data into list

    return X, y


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.

    :param evidence: list() of list() of features
    :param labels: list() of labels
    :return: sklearn KNeighborsClassifier
    """

    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.

    :param labels: list() of labels
    :param predictions: list() of predictions
    :return: (float, float) of (sensitivity, specificity)
    """
    labels_a = np.array(labels)  # convert to np 1d-array

    sensitivity1 = np.where(labels_a == 1, predictions, 0).sum() / labels_a.sum()
    specificity1 = np.where(labels_a == 0, predictions == 0, 0).sum() / (labels_a == 0).sum()

    return sensitivity1, specificity1


if __name__ == "__main__":
    main()
