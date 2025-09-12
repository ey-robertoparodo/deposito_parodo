import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix

import time

df = pd.read_csv("train.csv")

X = df.drop("label", axis=1)
y = df["label"].astype(int)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

"""
for n in range(2, len(X.columns)):
    pca = PCA(n_components=n)
    X_pca = pca.fit_transform(X_scaled)
    print(f"Totale varianza spiegata con {n} componenti:", pca.explained_variance_ratio_.sum())
"""

pca = PCA(n_components=0.95, whiten=True)
X_pca = pca.fit_transform(X_scaled)

X_train, X_test, y_train, y_test = train_test_split(
    X_pca, y, stratify=y, test_size=0.20, random_state=42
)

# Decision Tree con PCA
print("Decision Tree con PCA")

tree = DecisionTreeClassifier(random_state=42, class_weight='balanced')

start_time = time.time()
tree.fit(X_train, y_train)
end_time = time.time()
training_time = end_time - start_time

print("Training time tree with PCA, ", training_time)

y_pred_tree = tree.predict(X_test)
print(classification_report(y_test, y_pred_tree, digits=3))
print(confusion_matrix(y_test, y_pred_tree))


X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.20, random_state=42
)

# Decision Tree senza PCA
print("Decision Tree senza PCA")
tree = DecisionTreeClassifier(random_state=42, class_weight='balanced')
start_time = time.time()
tree.fit(X_train, y_train)
end_time = time.time()
training_time = end_time - start_time

print("Training time tree, ", training_time)
y_pred_tree = tree.predict(X_test)
print(classification_report(y_test, y_pred_tree, digits=3))
print(confusion_matrix(y_test, y_pred_tree))

# commento
"""
L'addestramento dell'albero decisionale con PCA richiede più tempo rispetto all'addestramento senza PCA. 
Tuttavia, la differenza di accuratezza tra i due modelli è di circa lo 0,5% a favore del modello senza PCA.
Nonostante ciò, l'utilizzo di PCA permette di ridurre la dimensionalità di oltre la metà delle feature, 
migliorando la semplicità e l'interpretabilità del modello, a fronte di una minima perdita di accuratezza.
"""