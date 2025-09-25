from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


def load_data(test_size=0.2, random_state=42):
    """Load the Iris dataset and split it into training and testing sets.

    Args:
        test_size (float, optional): Proportion of the dataset to include in the test split. Defaults to 0.2.
        random_state (int, optional): Controls the shuffling applied to the data before applying the split. Defaults to 42.

    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    iris = load_iris()
    X = iris.data
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


def train_classifier(X_train, y_train, random_state=42):
    """Train a Decision Tree Classifier on the training data.

    Args:
        X_train (array-like): Training features.
        y_train (array-like): Training labels.
        random_state (int, optional): Random state for reproducibility. Defaults to 42.

    Returns:
        DecisionTreeClassifier: Trained classifier.
    """
    clf = DecisionTreeClassifier(random_state=random_state)
    clf.fit(X_train, y_train)
    return clf


def evaluate_model(y_true, y_pred):
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


def main():
    """Main function to load data, train the model, and evaluate it."""
    X_train, X_test, y_train, y_test = load_data()
    clf = train_classifier(X_train, y_train)
    y_pred = clf.predict(X_test)
    evaluate_model(y_test, y_pred)


if __name__ == "__main__":
    main()
