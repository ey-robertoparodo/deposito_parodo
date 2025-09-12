import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Mall_Customers.csv")

df_selezionato = df[["Annual Income (k$)", "Spending Score (1-100)"]]

scaler = StandardScaler()
df_selezionato = scaler.fit_transform(df_selezionato)

list_silhoutte = []

for k in range(2, 10):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(df_selezionato)

    score = silhouette_score(df_selezionato, labels)
    print(f"Silhouette per k={k}:", score)
    list_silhoutte.append(score)
    print(f"Inertia per k={k}", kmeans.inertia_)
    
    plt.figure(figsize=(6, 6))
    plt.scatter(df_selezionato[:, 0], df_selezionato[:, 1], c=labels, cmap='viridis')
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
                c='red', marker='X', s=200, label='Centroidi')
    plt.title("Cluster trovati con k-Means")
    plt.xlabel("Annual Income")
    plt.ylabel("Spending Score")
    plt.legend()
    plt.grid(True)
    plt.show()
    
plt.figure(figsize=(8, 5))
sns.lineplot(x=list(range(2, 10)), y=list_silhoutte, marker='o')
plt.title("Silhouette Score al variare di k")
plt.xlabel("Numero di cluster (k)")
plt.ylabel("Silhouette Score")
plt.grid(True)
plt.tight_layout()
plt.show()

# scelgo k = 5 perchè massimizza la silhoutte
kmeans = KMeans(n_clusters=5, random_state=42)
labels = kmeans.fit_predict(df_selezionato)
plt.figure(figsize=(6, 6))
plt.scatter(df_selezionato[:, 0], df_selezionato[:, 1], c=labels, cmap='viridis')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
            c='red', marker='X', s=200, label='Centroidi')
plt.title("Cluster trovati con k-Means")
plt.xlabel("Annual Income")
plt.ylabel("Spending Score")
plt.legend()
plt.grid(True)
plt.show()

# commento
"""
Guardando il grafico delle silhouette si nota come il numero di cluster pari a 5 è quello che massimizza la silhouette

Il punto logico tra 5 e 6

Con k=5
Cluster giallo (in basso a sinistra)
    -Reddito basso
    -Spending score basso
    -Clienti poco redditizi, probabilmente non spendono molto e non sono target prioritari.

Cluster viola (centrale in basso)
    -Reddito medio-basso
    -Spending score medio

Sono clienti non hanno grande capacità di spesa ma sono più attivi dei gialli.

Cluster verde (in basso a destra)
    -Reddito medio-alto
    -Spending score basso

Sono clienti con alto reddito ma bassa propensione a spendere.

Cluster blu (in alto a destra)
    -Reddito medio-alto
    -Spending score alto

Sono clienti molto redditizi, spesa elevata e capacità economica.

Cluster turchese (in alto a sinistra)
    -Reddito basso-medio
    -Spending score alto

Sono clienti che spendono molto pur avendo reddito più basso.
"""