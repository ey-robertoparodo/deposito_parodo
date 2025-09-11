import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

df = pd.read_csv("creditcard.csv")

X = df.drop("Class", axis=1)
y = df["Class"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.20, random_state=42
)

# Decision Tree
tree = DecisionTreeClassifier(max_depth=5, random_state=42, class_weight='balanced')
tree.fit(X_train, y_train)
y_pred_tree = tree.predict(X_test)

print(classification_report(y_test, y_pred_tree, digits=3))
plt.figure(figsize=(18, 10))
plot_tree(tree, feature_names=X.columns, class_names=["legit", "fraud"], filled=True)
plt.title("Risultati")
plt.show()


#Random Forest
rfc = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42, class_weight='balanced')

rfc.fit(X_train, y_train)
y_pred_tree = rfc.predict(X_test)
print(classification_report(y_test, y_pred_tree, digits=3))



# Over sampling
smote = SMOTE()
X_resampled, y_resampled = smote.fit_resample(X, y)

tree = DecisionTreeClassifier(max_depth=5, random_state=42)
tree.fit(X_resampled, y_resampled)
y_pred_tree = tree.predict(X_test)
print(classification_report(y_test, y_pred_tree, digits=3))


rfc = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
rfc.fit(X_resampled, y_resampled)
y_pred_tree = rfc.predict(X_test)
print(classification_report(y_test, y_pred_tree, digits=3))