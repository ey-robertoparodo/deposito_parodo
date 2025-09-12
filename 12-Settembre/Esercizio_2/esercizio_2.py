import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

df = pd.read_csv("Wholesale_customers_data.csv")

X = df.drop(columns=["Channel", "Region"])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

min_samples = 5
neighbors = NearestNeighbors(n_neighbors=min_samples)
neighbors_fit = neighbors.fit(X_scaled)
distances, indices = neighbors_fit.kneighbors(X_scaled)

distances = np.sort(distances[:, -1])
plt.figure(figsize=(8,5))
plt.plot(distances)
plt.title("K-distance plot (k=min_samples)")
plt.xlabel("Punti ordinati")
plt.ylabel("Distanza")
plt.show()

eps_value = 2.0
db = DBSCAN(eps=eps_value, min_samples=min_samples)
labels = db.fit_predict(X_scaled)

n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
n_outliers = list(labels).count(-1)

print(f"Numero di cluster trovati: {n_clusters}")
print(f"Numero di outlier: {n_outliers}")


pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(8,6))
sns.scatterplot(x=X_pca[:,0], y=X_pca[:,1], hue=labels, palette="tab10", s=50)
plt.title("DBSCAN clustering (ridotto a 2D con PCA)")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.legend(title="Cluster")
plt.show()

"""
COmmento:
- I cluster rappresentano profili di clienti con schemi di spesa simili.
- Variare eps (più grande = cluster più ampi, meno outlier) e min_samples (più alto = cluster più rigorosi) cambia molto il risultato.
- Gli outlier (-1) sono clienti con consumi molto diversi dagli altri: possono essere clienti atipici o con esigenze speciali.
"""
