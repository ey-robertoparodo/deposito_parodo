import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

df = pd.read_csv("creditcard.csv")

X = df.drop("Class", axis=1)
y = df["Class"].astype(int)

X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.15, stratify=y, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.176, stratify=y_temp, random_state=42)

print(f"Train: {X_train.shape}, Validation: {X_val.shape}, Test: {X_test.shape}")


tree = DecisionTreeClassifier(max_depth=5, random_state=42, class_weight='balanced')
tree.fit(X_train, y_train)

y_pred_tree = tree.predict(X_val)
print(classification_report(y_val, y_pred_tree, digits=3))

y_pred_tree = tree.predict(X_test)
print(classification_report(y_test, y_pred_tree, digits=3))