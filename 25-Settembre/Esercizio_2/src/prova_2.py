"""Iris classification pipeline using a Decision Tree classifier.

This module loads the Iris dataset, splits it into train/test sets, trains a
DecisionTreeClassifier, and evaluates its performance using standard
classification metrics.

Key functions
- load_data(test_size=0.2, random_state=42):
  Loads the Iris dataset and splits it into training and test sets.
  Returns: X_train, X_test, y_train, y_test.

- train_classifier(X_train, y_train, random_state=42):
  Trains a DecisionTreeClassifier on the training data.
  Returns: the trained classifier (DecisionTreeClassifier).

- evaluate_model(y_true, y_pred):
  Prints the confusion matrix, classification report, and accuracy score.

- main():
  Runs the full pipeline: load_data → train_classifier → predict → evaluate.

Dependencies
- scikit-learn: datasets, model_selection, tree, metrics

Example (API usage)
>>> from prova_2 import load_data, train_classifier, evaluate_model
>>> X_train, X_test, y_train, y_test = load_data(test_size=0.25, random_state=0)
>>> clf = train_classifier(X_train, y_train, random_state=0)
>>> y_pred = clf.predict(X_test)
>>> evaluate_model(y_test, y_pred)

Command line execution
- python prova_2.py
  Runs the full pipeline and prints evaluation metrics.

Notes
- For reproducibility, set random_state in both load_data and train_classifier.
- The Iris dataset has three balanced classes; accuracy is a meaningful metric.
"""

from typing import Tuple, Sequence
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


def load_data(
    test_size: float = 0.2, random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Load the Iris dataset and split it into training and testing sets.

    Args:
        test_size (float, optional):
            Proportion of the dataset to include in the test split. Defaults to 0.2.
        random_state (int, optional):
            Controls the shuffling applied to the data before applying the split.
            Defaults to 42.

    Returns:
        tuple: x_train, x_test, y_train, y_test
    """
    features, labels = load_iris(return_X_y=True)
    x_train, x_test, y_train, y_test = train_test_split(
        features, labels, test_size=test_size, random_state=random_state
    )
    return x_train, x_test, y_train, y_test


def train_classifier(
    x_train: np.ndarray,
    y_train: np.ndarray,
    random_state: int = 42,
) -> DecisionTreeClassifier:
    """Train a Decision Tree Classifier on the training data.

    Args:
        x_train (array-like): Training features.
        y_train (array-like): Training labels.
        random_state (int, optional): Random state for reproducibility.
            Defaults to 42.

    Returns:
        DecisionTreeClassifier: Trained classifier.
    """
    clf: DecisionTreeClassifier = DecisionTreeClassifier(random_state=random_state)
    clf.fit(x_train, y_train)
    return clf


def evaluate_model(
    y_true: Sequence[int] | np.ndarray, y_pred: Sequence[int] | np.ndarray
) -> None:
    """Print evaluation metrics for the classification model.

    Args:
        y_true (array-like): True labels.
        y_pred (array-like): Predicted labels.
    """
    print("Confusion Matrix:")
    print(confusion_matrix(y_true, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred))
    print("Accuracy Score:", accuracy_score(y_true, y_pred))


def main() -> None:
    """Main function to load data, train the model, and evaluate it."""
    x_train, x_test, y_train, y_test = load_data()
    clf: DecisionTreeClassifier = train_classifier(x_train, y_train)
    y_pred: np.ndarray = clf.predict(x_test)
    evaluate_model(y_test, y_pred)


if __name__ == "__main__":
    main()
