import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split  # Divisione train/test (fase 4)
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, confusion_matrix, ConfusionMatrixDisplay,f1_score, roc_curve, auc, adjusted_rand_score #(Fase 5) #(Fase 5)
from sklearn.cluster import KMeans #(Fase 8)
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree #Fase 5)
from sklearn.ensemble import RandomForestClassifier #(Fase 5)
from sklearn.neighbors import KNeighborsClassifier #(Fase 5)
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB #(Fase 5)
from sklearn.preprocessing import StandardScaler, LabelEncoder , MinMaxScaler, OneHotEncoder#(fase 4)
from sklearn.svm import SVC #(Fase 5)
import joblib
import os

'''
🧭 Fase 4: Preprocessing e trasformazione in DataFrame
📋 Obiettivo
Convertire i dati da studenti.db o studenti.csv in un DataFrame per il ML.

🔁 Trasformazioni da applicare
-Codifica label (es. comportamento → numeri)
-Normalizzazione delle variabili numeriche
-Split train/test (es. 80/20)
-Salvataggio dei DataFrame in file CSV per debug

'''
#_____________________________________________Folder di ricollocazione dei file_____________________________________________
folder = r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo"
# Assicurati che esista
os.makedirs(folder, exist_ok=True)

#_____________________________________________Loading di ogni dataframe per testare chi è il migliore_____________________________________________
r'''
df = pd.read_csv(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_class.csv")
df = pd.read_csv(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_df.csv")
df = pd.read_csv(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_input.csv")
'''
df = pd.read_csv(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_dbcsv.csv", sep=";")
df.to_csv(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_dbcsv.csv",index=False, sep=";")
print("_______________Reading Database Effettuato_______________\n")
print("Colonne:", df.columns) #Debuf, impara alfio
# 2. Analisi iniziale 

print(df.head())
print(df.info())

# Data columns (total 11 columns):
#  0   Unnamed: 0     201 non-null    int64
#_____________________________________________DFDF mi dava una colonna in più_____________________________________________
r'''
df.drop(columns=["Unnamed: 0"], axis=1, inplace=True) #Per eliminare colonna 0, se index = false non và. Ok non và! va fatto nel salvataggio! , index=False
print(df.info()) #Fixed
df.to_csv(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\studenti_riepiologo_df.csv", index=False)
'''
#_____________________________________________Drop prima di X e Y delle caselle Inutili_____________________________________________
df.drop(["id","nome", "cognome"], axis=1, inplace=True)
# Salvataggio corretto senza pd.concat
print("_______________Eliminazioni Colonne Superflue_______________\n")
#_____________________________________________Label Encoder_____________________________________________
str_colonne = ["comportamento", "genere"]
encoders = {} #Per salvarli meglio, consiglio di chatgpt per il predict

for col in str_colonne:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

#_____________________________________________Encoder del target Divisio_____________________________________________
le_ytarget = LabelEncoder()
df["esito_finale"] = le_ytarget.fit_transform(df["esito_finale"])

encoders["esito_finale"] = le_ytarget
joblib.dump(encoders, "encodersriepilogodb.joblib")  # tutti gli encoder insieme, chatgpt lo consiglia perché sono simili.. vedremo
print(df[["comportamento", "genere"]])
print(df[["esito_finale"]])
print("_______________Label separati per Target e Stringhe_______________\n")

#_____________________________________________Standard Scaler delle colonne numeriche_____________________________________________
int_colonne = ["età", "ore_studio", "assenze", "media_voti"] #Non mettiamo comportamento, genere ed esito perché sono etichette.

scaler = StandardScaler()
df[int_colonne] = scaler.fit_transform(df[int_colonne])
joblib.dump(scaler, os.path.join(folder, "scalerdb.joblib"))
#Uno scaler per ogni dataset, a differenza del label, che essendo simili hanno lo stesso numero, con lo scaler cambia e bisogna farlo 1per1
print("_______________Scaler su tutte le colonne Intere_______________\n")
print(df[["età", "ore_studio", "assenze", "media_voti"]])

print("_______________X_train/Y_train_______________\n")
print(df.head())
print(df.info())
#_____________________________________________X e Y_____________________________________________
X = df.drop("esito_finale", axis=1)
y = df["esito_finale"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("_______________X_train_______________\n") 
X_train.info()
print("_______________y_train_______________\n")
y_train.info()
#print("Distribuzione target (y_train):")
#print(y_train.value_counts(normalize=True)) #Per vedere com'è combinato il dataset a livello numerico.
print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)
# 5. Salvataggio CSV
X_train.assign(esito_finale=y_train).to_csv(os.path.join(folder, "train.csv"), index=False)
X_test.assign(esito_finale=y_test).to_csv(os.path.join(folder, "test.csv"), index=False)


'''
🧭 Fase 5: Machine Learning supervisionato
📋 Obiettivo
Allenare più modelli di classificazione per prevedere esito_finale.

✅ Modelli obbligatori
-DecisionTreeClassifier
-KNNeighborsClassifier
-GaussianNB
-SVM
-RandomForestClassifier

📈 Metriche richieste
-Accuratezza
-Matrice di confusione
-Precision / Recall / F1

➕ Extra suggeriti
-salvataggio del modello joblib
-confronto prestazioni dei modelli
'''
#_____________________________________________Tutti i modelli Summer Love_____________________________________________
modelli = {
    "Albero_Gini": DecisionTreeClassifier(criterion='gini', random_state=42),  # Albero decisionale usando l’indice di Gini
    "Albero_Entropia": DecisionTreeClassifier(criterion='entropy', random_state=42),  # Variante con entropia
    "Naive_Bayes": GaussianNB(),  # Classificatore bayesiano semplice
    "KNN": KNeighborsClassifier(),  # K-Nearest Neighbors con 5 vicini
    "Regole_Semplici": DecisionTreeClassifier(max_depth=2, random_state=42),  # Albero molto semplice, simula modello basato su regole
    "SVM": SVC(probability=True, random_state=42),
    "SVM_lineare" : SVC(C=1, kernel="linear", random_state=42), #SVM lineare
    "SVM_non_lineare" : SVC(C=1, kernel="rbf", random_state=42), #SVM non lineare
    "RandomForest": RandomForestClassifier(random_state=42)
}

risultati = {}
'''
#_____________________________________________Controllo Accuracy di ogni modello_____________________________________________
for nome, mod in modelli.items(): #Perché è un dizionario
    mod.fit(X_train, y_train)  # .values.ravel() converte da (n,1) a (n,)
    pred = mod.predict(X_test)
    acc = accuracy_score(y_test, pred)
    cm = confusion_matrix(y_test, pred)
    f1 = f1_score(y_test, pred,average='weighted')
    # Salvataggio in dizionario
    risultati[nome] = {"Accuratezza": acc, "F1": f1, "Predizione": pred, "Modello": mod}
    # Stampa report
    print(f"__________{nome}__________")
    print(f"Accuratezza: {acc:.3f}, F1-score: {f1:.3f}")
    print(classification_report(y_test, pred))
    # Stampa matrice di confusione
    cm = confusion_matrix(y_test, pred)
    disp = ConfusionMatrixDisplay(cm)
    disp.plot()
    plt.show()
    print("\n")
'''
#_____________________________________________
# Controllo Accuracy di ogni modello
#_____________________________________________

fig, axes = plt.subplots(len(modelli),1, figsize=(8,16*len(modelli)))  # 1 riga, n colonne
if len(modelli) == 1:   # Caso speciale: se hai solo 1 modello, axes non è iterabile
    axes = [axes]

for i, (nome, mod) in enumerate(modelli.items()):
    mod.fit(X_train, y_train)
    pred = mod.predict(X_test)
    acc = accuracy_score(y_test, pred)
    f1 = f1_score(y_test, pred, average='weighted')
    
    # Salvataggio in dizionario
    risultati[nome] = {
        "Accuratezza": acc,
        "F1": f1,
        "Predizione": pred,
        "Modello": mod
    }
    
    # Stampa report testuale
    print(f"__________{nome}__________")
    print(f"Accuratezza: {acc:.3f}, F1-score: {f1:.3f}")
    print(classification_report(y_test, pred))
    
    # Confusion matrix nel subplot
    cm = confusion_matrix(y_test, pred)
    disp = ConfusionMatrixDisplay(cm)
    disp.plot(ax=axes[i], colorbar=False)   # niente barra colore per compattezza
    axes[i].set_title(nome)

plt.tight_layout()
plt.show()

#Questafunzione prendeva l'1, rendendolo overfittato
#_____________________________________________Filtro di un vero modello "realistico"_____________________________________________
# Filtra i modelli che non hanno F1 = 1.0
modelli_realistici = {nome: info for nome, info in risultati.items() if info['F1']} #Eliminazione filtyro < 0.940

if modelli_realistici:  # se ce ne sono
    migliore_realistico = sorted(modelli_realistici.items(), key=lambda x: (-x[1]['F1'], x[0]))[0][0]
    migliore_modello_realistico = modelli_realistici[migliore_realistico]['Modello']
    print(f"Modello realistico migliore: {migliore_realistico} con F1={modelli_realistici[migliore_realistico]['F1']:.3f}")
    joblib.dump(migliore_modello_realistico, os.path.join(folder, f"{migliore_realistico}_DF.joblib"))
    print(f"Modello {migliore_modello_realistico} salvato su disco come f'{migliore_modello_realistico}DF.joblib'")
else:
    print("Tutti i modelli hanno F1 = 1.0, nessuno sotto 1.0 da scegliere.")

'''
🧭 Fase 6: Clustering non supervisionato (KMeans)
📋 Obiettivo
-Segmentare gli studenti in gruppi basati su performance/assenze/ore studio.
-Grafico a dispersione (Matplotlib)
-Esportazione cluster nel report
'''

#_____________________________________________K-Means_____________________________________________
# Definisco X = tutte le feature tranne il target
X_kmeans = df[["ore_studio", "assenze", "media_voti"]]

# -Esportazione cluster nel report
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_kmeans)

# Centroidi
centers = kmeans.cluster_centers_
#_____________________________________________Matplot 3d_____________________________________________
# Supponiamo che X abbia le tre colonne: ore_studio, media_voti, assenze. In questo caso sarà3d
fig = plt.figure(figsize=(10, 7)) # Creo una figura grande 10x7 pollici
ax = fig.add_subplot(111, projection='3d') # Aggiungo un subplot 3D
#111 significa = 1 riga, 1 colonna 1 posizione subplot, il primo. In questo sarebbe 3d.
#221 sarebbe stato griglia 2x2 e prende la posizione alto a sinistra

# scatter 3D con colori dei cluster. Attento a ciò che scrivi nelò kmeans per missmatch
ax.scatter(
    df["ore_studio"], 
    df["assenze"], 
    df["media_voti"], 
    c=kmeans.labels_, # Colori in base al cluster assegnato
    cmap="viridis", # Mappa di colori (verde-blu)
    s=18, # Dimensione dei punti (piccoli ma visibili)
    alpha=0.4 # Trasparenza → 0.9 = quasi opaco
)

# centri dei cluster
centers = kmeans.cluster_centers_ 
ax.scatter(
    centers[:, 0], centers[:, 1], centers[:, 2],  # Coordinate centroidi
    c="red",  # Colore rosso
    s=200,  # Grandezza molto maggiore degli studenti (200)
    alpha=1.0, # Trasparenza leggermente più bassa (si vedono bene)
    marker="X", # Simbolo a X (per differenziarli dai cerchietti)
    label="Centroidi"
)

#stessa cosa qui, rispetta il match del kmeans
ax.set_xlabel("Ore di studio")
ax.set_ylabel("Assenze")
ax.set_zlabel("Media voti")
ax.set_title("Cluster studenti (KMeans 3D)")
# Colore rosso
ax.legend()
# Vista 3D più leggibile
ax.view_init(elev=20, azim=35)
# Imposto un punto di vista 3D più leggibile
# elev=20 → inclinazione verticale di 20 gradi
# azim=35 → rotazione orizzontale di 35 gradi

#plt.show()
#FIGATA il 3D!