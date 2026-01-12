'''
🧭 Fase 7: GUI con tkinter
📋 Obiettivo
Creare un’interfaccia semplice con le seguenti funzioni:
-Inserimento dati nuovo studente V
-Salvataggio dati nuovo studente su database V
-Predizione del modello salvato per nuovo studente V
-Visualizzazione statistiche V
-Esportazione in PDF del report con grafici

🧭 Fase 8: Report PDF
📋 Contenuti
-Elenco studenti (nome + esito previsto)
-Grafici: Matrice di Confusione, KMeans, Voti/Assenze
-Sommario delle metriche
-Timestamp, autore, modello usato

📦 Librerie suggerite: reportlab o fpdf, + matplotlib

🧭 Fase 9: Compilazione in eseguibile + installer
-Realizza l'eseguibile per il programma di classificazione/predizione
-Realizza l'installer per il programma di classificazione/predizione
'''
import tkinter as tk #Ui funzioni base
from tkinter import ttk, messagebox #UI messaggi e funzioni avanzate
import joblib #Carica/salvataggi
import numpy as np
import matplotlib.pyplot as plt #immagini di statistica
import pandas as pd #Dataframe
import reportlab #Funzioni di PDF
from fpdf import FPDF #Export pdf
import os #Ricarica/salvataggi dati su pc
from PIL import Image as PilImage, ImageTk #per evitare conflitti con quelli del pdf
import pyttsx3 #Voce
import sqlite3 #Database
import threading #Far partire voce + ui separati
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


#_____________________________________________Lista Nomi per il Random_____________________________________________
nomi_maschili = ['Dino', 'Alfio', 'Ezechiele','Filippo','Jack','Agamennone','Pdor','Luca', 'Marco', 'Andrea', 'Matteo', 'Francesco', 'Giovanni', 'Alessandro', 'Davide', 'Simone', 'Gabriele',
                 'Federico', 'Riccardo', 'Lorenzo', 'Tommaso', 'Emanuele', 'Daniele', 'Nicola', 'Stefano', 'Antonio', 'Fabio',
                 'Paolo', 'Giuseppe', 'Vincenzo', 'Roberto', 'Salvatore', 'Claudio', 'Enrico', 'Michele', 'Alberto', 'Maurizio']

nomi_femminili = ['Laura', 'Alessandra', 'Andrea','Giulia', 'Francesca', 'Sara', 'Martina', 'Chiara', 'Alessia', 'Valentina', 'Federica', 'Elena', 'Ilaria',
                  'Laura', 'Simona', 'Angela', 'Anna', 'Maria', 'Sofia', 'Claudia', 'Veronica', 'Camilla', 'Eleonora',
                  'Paola', 'Cristina', 'Silvia', 'Barbara', 'Roberta', 'Alice', 'Marta', 'Beatrice', 'Nicole', 'Elisa']

cognomi = ['Cavallaro', 'Pdor', 'Hallal','Zhing','Crodino','Rossi', 'Russo', 'Ferrari', 'Esposito', 'Bianchi', 'Romano', 'Colombo', 'Ricci', 'Marino', 'Greco',
           'Bruno', 'Gallo', 'Conti', 'De Luca', 'Mancini', 'Costa', 'Giordano', 'Rizzo', 'Lombardi', 'Moretti',
           'Barbieri', 'Fontana', 'Santoro', 'Mariani', 'Rinaldi', 'Caruso', 'Ferraro', 'Fabbri', 'Galli', 'Martini',
           'Leone', 'Longo', 'Gentile', 'Martinelli', 'Serra', 'Villa', 'Cattaneo', 'Sala', 'Pellegrini', 'Farina',
           'Orlando', 'Sanna', 'Piras', 'Lopes', 'Grassi', 'De Santis', 'Monti', 'Bellini', 'Marchetti', 'Valentini']


#_____________________________________________Caricamento vari Encoder_____________________________________________
try:
    modello = joblib.load(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\Regole_Semplici_DF.joblib")
    encoder = joblib.load("encodersriepilogodb.joblib")
    scaler = joblib.load(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\scalerdb.joblib")
except Exception as e:
    messagebox.showerror("Errore", f"Errore nel caricamento dei file .joblib:\n{e}")
    raise SystemExit
print("Feature names attese dal modello:", modello.feature_names_in_)
#_____________________________________________Creazione classe DB_____________________________________________
class Dbmanager:
    def __init__(self, db_path):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # per accedere ai campi come dict
        self.cursor = self.conn.cursor()
        self.avvio_db()

    def avvio_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Studenti(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cognome TEXT NOT NULL,
                età INTEGER CHECK(età BETWEEN 14 AND 20),
                genere TEXT CHECK(genere IN ('M','F')),
                ore_studio REAL CHECK(ore_studio BETWEEN 0 AND 8),
                assenze INTEGER CHECK(assenze >= 0),
                media_voti REAL CHECK(media_voti BETWEEN 1 AND 10),
                comportamento TEXT CHECK(comportamento IN ('ottimo','buono','sufficiente','scarso')),
                esito_finale TEXT CHECK(esito_finale IN ('promosso','bocciato'))
            )
        ''')
        self.conn.commit()

    def inserisci_studente(self, studente):
        self.cursor.execute('''
            INSERT INTO Studenti (nome, cognome, età, genere, ore_studio, assenze, media_voti, comportamento, esito_finale)
            VALUES (:nome,:cognome,:età,:genere,:ore_studio,:assenze,:media_voti,:comportamento,:esito_finale)
        ''', studente)
        self.conn.commit()
    
    def inserisci_batch(self, studenti):
        self.cursor.executemany('''
            INSERT INTO Studenti (nome, cognome, età, genere, ore_studio, assenze, media_voti, comportamento, esito_finale)
            VALUES (:nome,:cognome,:età,:genere,:ore_studio,:assenze,:media_voti,:comportamento,:esito_finale)
        ''', studenti)
        self.conn.commit()

    def seleziona_tutti(self):
        self.cursor.execute("SELECT * FROM Studenti")
        return self.cursor.fetchall()

    def chiudi(self):
        self.conn.close()
#_____________________________________________File + Apertura_____________________________________________
DB_PATH = r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_UI.db"
db = Dbmanager(DB_PATH)  # crea DB + tabella se non esistono

#_____________________________________________Cartella di Destinazione_____________________________________________
folder = r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo"
# Assicurati che esista
os.makedirs(folder, exist_ok=True)
#_____________________________________________Test Vocale_____________________________________________
def parliamo(parla):
    def parti():
        engine = pyttsx3.init()
        engine.setProperty('rate', 190) # Imposto una velocità più lenta (es. 150 parole/min)
        engine.say(parla) # Impostare la chiamate alla funzione, cosi quando parla devo solo scrivere parlare("testo")
        engine.runAndWait()
    threading.Thread(target=parti).start()

#_____________________________________________Finestra Principale_____________________________________________
db.avvio_db() #chiamato prima così il database è attivo all'avvio
root = tk.Tk()
root.title("Studenti Riepi(O)logo")
root.geometry("250x300")
root.configure(bg="black")
parliamo("Benvenuti a Studenti Riepiologo.\n A sinistra troverete , in ordine, i tasti per inserire studenti, visualizza e predizione. Più una chicca!") # 100 ms dopo che la finestra è renderizzata
#_____________________________________________FONT_____________________________________________
font_sub = ("Segoe UI", 10, "italic")
font_title = ("Segoe UI", 16, "bold italic")
font_btn = ("Segoe UI", 12, "bold")
#_____________________________________________Immagine_____________________________________________
img = PilImage.open(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\laurea.png")
img = img.resize((100, 100))  # ridimensiona a lato, non enorme
tk_img = ImageTk.PhotoImage(img)
# Label per immagine con stesso bg della finestra
img_label = tk.Label(root, image=tk_img, bg="black")
img_label.place(x=150, y=90)  # posizione laterale, cambiabile


# Frame per titolo e sottotitolo
title_frame = tk.Frame(root, bg="black")
title_frame.place(x=5, y=5)

# Titolo
sottotitolo = tk.Label(title_frame, text="BitCamp Presenta:", bg="black", fg="white", font=font_sub)
sottotitolo.pack(anchor="nw", pady=1,padx=20)


titolo = tk.Label(title_frame, text="Studenti Riepi(o)logo", bg="black", fg="white", font=font_title)
titolo.pack(anchor="center", pady=2,padx=20)


#_____________________________________________Top Level(Finestra a comparsa)_____________________________________________
def apri_toplevel_inserimento():
    parliamo("Inserisci i dati dello studente")
    top = tk.Toplevel(root)
    top.title("Inserisci Studente")
    top.geometry("300x310")
    top.configure(bg="black")
     # Dizionario con i campi da compilare
    campi = {
        "nome": tk.StringVar(),
        "cognome": tk.StringVar(),
        "età": tk.IntVar(),
        "genere": tk.StringVar(),
        "ore_studio": tk.DoubleVar(),
        "assenze": tk.IntVar(),
        "media_voti": tk.DoubleVar(),
        "comportamento": tk.StringVar(),
        # "esito_finale": tk.StringVar()
    }

#_____________________________________________Creazione label con le varie combobox per limitare le scelte_____________________________________________
    row = 0
    for label, var in campi.items():
        tk.Label(top, text=label, font=font_sub, fg="white", bg="black").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        if label == "età":
            combo = ttk.Combobox(top, textvariable=var, values=[14,15,16,17,18,19,20], state="readonly")
            combo.grid(row=row, column=1, padx=10, pady=5)  
        elif label == "genere":
            combo = ttk.Combobox(top, textvariable=var, values=["M", "F"], state="readonly")
            combo.grid(row=row, column=1, padx=10, pady=5)
        elif label == "comportamento":
            combo = ttk.Combobox(top, textvariable=var, values=["ottimo", "buono", "sufficiente","scarso"], state="readonly")
            combo.grid(row=row, column=1, padx=10, pady=5)
        # elif label == "esito_finale": Se il prof lo vuole attivo lo rimetto
        #     combo = ttk.Combobox(top, textvariable=var, values=["promosso", "bocciato"], state="readonly")
        #     combo.grid(row=row, column=1, padx=10, pady=5)
        else:
            tk.Entry(top, textvariable=var).grid(row=row, column=1, padx=10, pady=5)
        row += 1
#_____________________________________________Da far vedere al prof, sono impazzito. aiuto_____________________________________________
        def predici_studente(studente):
            parliamo("Predizione")
            # 1. Seleziona solo le feature usate dal modello
            df = pd.DataFrame([{
                'età': studente['età'],
                'genere': studente['genere'],
                'ore_studio': studente['ore_studio'],
                'assenze': studente['assenze'],
                'media_voti': studente['media_voti'],
                'comportamento': studente['comportamento']
            }])

            # Trasformazione manuale
            for col in ['genere','comportamento']:
                df[col] = encoder[col].transform(df[col])

            # 3. Applica lo scaler sulle colonne numeriche
            num_cols = ['età', 'ore_studio', 'assenze', 'media_voti']
            df[num_cols] = scaler.transform(df[num_cols])

            # 4. Predizione
            pred = modello.predict(df)  # restituisce array tipo [0] o [1] a seconda di come l'hai allenato

            # 5. Converti predizione in stringa
            if pred[0] == 1 or pred[0] == "promosso":  # dipende come l’hai salvato
                return "promosso"
            else:
                return "bocciato"
#_____________________________________________Comando Salva_____________________________________________
        def salva():
            # Recupero valori dai campi
            nuovo_studente = {campo: var.get() for campo, var in campi.items()}
            nuovo_studente["nome"] = nuovo_studente["nome"].title()
            nuovo_studente["cognome"] = nuovo_studente["cognome"].title()

            # Validazioni
            errori = []
            if not nuovo_studente["nome"].strip():
                errori.append("Il campo Nome è obbligatorio.")
            if not nuovo_studente["cognome"].strip():
                errori.append("Il campo Cognome è obbligatorio.")
            if not (14 <= nuovo_studente["età"] <= 20):
                errori.append("Età deve essere tra 14 e 20 anni.")
            if nuovo_studente["genere"] not in ["M","F"]:
                errori.append("Genere non valido.")
            if not (0 <= nuovo_studente["ore_studio"] <= 8):
                errori.append("Ore studio tra 0 e 8.")
            if not (0 <= nuovo_studente["assenze"] <= 220):
                errori.append("Assenze tra 0 e 220.")
            if not (4 <= nuovo_studente["media_voti"] <= 10):
                errori.append("Media voti tra 4 e 10.")
            if errori:
                messagebox.showerror("Errore di validazione", "\n".join(errori))
                return

            # Predizione automatica
            nuovo_studente["esito_finale"] = predici_studente(nuovo_studente)

            # Salvataggio DB
            db.inserisci_studente(nuovo_studente)
                # Mostra messaggio con predizione
            messagebox.showinfo(
                "Successo",
                f"Studente {nuovo_studente['nome']} {nuovo_studente['cognome']} inserito con successo!\n"
                f"Esito previsto: {nuovo_studente['esito_finale']}"
    )

#_____________________________________________Terminator nel Top Level_____________________________________________
    import random #random.randint(
    def genera_studenti(batch_size=200, soglia = 60):
        parliamo("Teeerminator")
        batch = []
        for _ in range(batch_size):
            genere = random.choice(["M", "F"])
            nome = random.choice(nomi_maschili) if genere == "M" else (
            random.choice(nomi_femminili)
            )
            cognome = random.choice(cognomi)
            eta = random.randint(14, 20)
            ore_studio = round(random.uniform(0,8),1)
            assenze = random.randint(0,220)
            media_voti = round(random.uniform(4,10),1)
            comportamento = random.choices(["ottimo", "buono", "sufficiente", "scarso"],weights=[0.1, 0.3,0.4,0.2])[0]
            if comportamento == "scarso" or media_voti <= 5.3 or assenze == 220:
                esito_finale = "bocciato"
            else:
                esito_finale = "promosso"
            batch.append({
                    'nome': nome,
                    'cognome': cognome,
                    'età': eta,
                    'genere': genere,
                    'ore_studio': ore_studio,
                    'assenze': assenze,
                    'media_voti': media_voti,
                    'comportamento': comportamento,
                    'esito_finale': esito_finale
                })
        #Statistica
        totali = len(batch)
        promossi = sum(1 for stud in batch if stud["esito_finale"] == "promosso")
        perc = (promossi/totali)*100
        print(f"Totali: {totali}, Promossi: {promossi}, Percentuale: {perc:.2f}%")
        if perc > soglia:
            print("_______________Soglia Raggiunta, Creazione Terminator Completata_______________\n")

        # Salvataggio nel DB usando la classe
        db.inserisci_batch(batch)
#_____________________________________________Potremmo fare anche 1 ad 1, ma diventa più lento_____________________________________________
        # for stud in batch:
        #     db.inserisci_studente(stud)
        return batch
#_____________________________________________Bottoni top Level_____________________________________________
    tk.Button(top, text="🤖",command= genera_studenti,font=font_btn, bg="black", fg="white").grid(row=row, column=1, columnspan=1,padx=20, pady=1)
    tk.Button(top, text="🖫/🧠",font=font_btn, bg="black", fg="white", command=salva).grid(row=row, column=0, columnspan=1,padx=20, pady=1)

def topvisualizza():
    parliamo("Visualizza Studenti sul Database")
    vis = tk.Toplevel(root)
    vis.title("Visualizza Studenti")
    vis.geometry("700x400")  # più larga per contenere le colonne
    vis.configure(bg="black")

    # Frame per la Treeview
    frame = tk.Frame(vis)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Definisco le colonne
    colonne = ["id", "nome", "cognome", "età", "genere", "ore_studio",
               "assenze", "media_voti", "comportamento", "esito_finale"]

    tree = ttk.Treeview(frame, columns=colonne, show="headings", height=15)
    tree.pack(side="left", fill="both", expand=True)

    # Scrollbar verticale
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    # Titoli colonne
    for col in colonne:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=70, anchor="center")  # regola larghezza

    # Recupero dati dal DB
    studenti = db.seleziona_tutti()  # usa il metodo della classe DB
    for stud in studenti:
        tree.insert("", "end", values=[stud[col] for col in colonne])

#_____________________________________________Statistica in Top Level_____________________________________________
def topstatistiche():
    parliamo("Tutte le statistiche")
    # Calcola dati
    studenti = db.seleziona_tutti()
    df = pd.DataFrame(studenti, columns=[
        "id", "nome", "cognome", "età", "genere", "ore_studio", 
        "assenze", "media_voti", "comportamento", "esito_finale"
    ])
    
    counts = df['esito_finale'].value_counts()

    # Grafico a torta
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90)
    plt.title("Distribuzione Esito Finale")
    plt.tight_layout()   # <-- evita tagli
    
    # 🔹 Salva prima di mostrare
    grafico_path = "grafico_statistiche.png"
    plt.savefig(grafico_path)
    plt.close()  # <-- chiude la figura per evitare conflitti con Tkinter

    # 🔹 Mostra grafico in una nuova finestra Tkinter
    grafico_img = PilImage.open(grafico_path)
    grafico_img_tk = ImageTk.PhotoImage(grafico_img)
    grafico_window = tk.Toplevel(root)
    grafico_window.title("Grafico Esito Finale")
    tk.Label(grafico_window, image=grafico_img_tk).pack()
    # Mantieni riferimento per evitare garbage collection
    grafico_window.image = grafico_img_tk

    # 🔹 Crea PDF in automatico
    doc = SimpleDocTemplate("Report_Studenti.pdf")
    story = []
    styles = getSampleStyleSheet()
    
    # Titolo e timestamp
    story.append(Paragraph("📊 Report Statistiche Studenti", styles["Title"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Generato il: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1, 20))
    
    # Aggiungi grafico
    story.append(Image(grafico_path, width=400, height=400))
    story.append(Spacer(1, 20))
    
    # Aggiungi tabella esiti
    for esito, num in counts.items():
        story.append(Paragraph(f"{esito}: {num}", styles["Normal"]))
    
    doc.build(story)
    
    # 🔹 Notifica
    messagebox.showinfo("Statistiche", "Grafico visualizzato ed esportato in Report_Studenti.pdf")
#_____________________________________________Proviamolo tutta_____________________________________________
def super_stats():
    parliamo("Proviamo tutto! Se funziona.")
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.ensemble import RandomForestClassifier
    import matplotlib.pyplot as plt
    from PIL import Image as PilImage, ImageTk
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet
    from datetime import datetime
    import os
    # Recupero dati dal DB
    studenti = db.seleziona_tutti()
    df = pd.DataFrame(studenti, columns=[
        "id","nome","cognome","età","genere","ore_studio","assenze",
        "media_voti","comportamento","esito_finale"
    ])
    
    if df.empty:
        messagebox.showinfo("Statistiche", "Non ci sono dati nel database!")
        return
    # Filtra solo righe con esito_finale valido
    df.drop(["id","nome", "cognome"], axis=1, inplace=True)
    # Salvataggio corretto senza pd.concat

    str_colonne = ["comportamento", "genere"]
    encoders = {} 
    for col in str_colonne:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    le_ytarget = LabelEncoder()
    df["esito_finale"] = le_ytarget.fit_transform(df["esito_finale"])
    encoders["esito_finale"] = le_ytarget

    int_colonne = ["età", "ore_studio", "assenze", "media_voti"] #Non mettiamo comportamento, genere ed esito perché sono etichette.
    scaler = StandardScaler()
    df[int_colonne] = scaler.fit_transform(df[int_colonne])

    X = df.drop("esito_finale", axis=1)
    y = df["esito_finale"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Definizione modelli
    modelli = {
        "Albero_Gini": DecisionTreeClassifier(criterion='gini', random_state=42),
        "Albero_Entropia": DecisionTreeClassifier(criterion='entropy', random_state=42),
        "Naive_Bayes": GaussianNB(),
        "KNN": KNeighborsClassifier(),
        "Regole_Semplici": DecisionTreeClassifier(max_depth=2, random_state=42),
        "SVM": SVC(probability=True, random_state=42),
        "SVM_lineare": SVC(C=1, kernel="linear", random_state=42),
        "SVM_non_lineare": SVC(C=1, kernel="rbf", random_state=42),
        "RandomForest": RandomForestClassifier(random_state=42)
    }

    # Lista immagini per il PDF
    grafici_paths = []

    # Fitta e genera grafici dei modelli
    for nome_modello, modello in modelli.items():
        modello.fit(X_train, y_train)
        y_pred = modello.predict(X_test)
        cm = confusion_matrix(y_test, y_pred, labels=[0,1])
        disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                    display_labels=le_ytarget.inverse_transform([0,1]))
        fig, ax = plt.subplots(figsize=(4,4))
        disp.plot(ax=ax)
        ax.set_title(nome_modello)
        plt.tight_layout()
        path = f"{nome_modello}.png"
        plt.savefig(path)
        grafici_paths.append(path)
        plt.close()

    # KMeans
    X_kmeans = df[['ore_studio','assenze','media_voti']].copy()
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X_kmeans)
    fig, ax = plt.subplots(figsize=(6,6))
    scatter = ax.scatter(X_kmeans['ore_studio'], X_kmeans['media_voti'], c=kmeans.labels_, cmap='viridis')
    ax.set_xlabel("Ore Studio")
    ax.set_ylabel("Media Voti")
    ax.set_title("KMeans Clustering")
    plt.legend(*scatter.legend_elements(), title="Cluster")
    plt.tight_layout()
    km_path = "KMeans.png"
    plt.savefig(km_path)
    grafici_paths.append(km_path)
    plt.close()

    # Creazione PDF
    pdf_path = "Report_Studenti_Modelli.pdf"
    doc = SimpleDocTemplate(pdf_path)
    story = []
    styles = getSampleStyleSheet()
    story.append(Paragraph("📊 Report Statistiche Studenti", styles["Title"]))
    story.append(Spacer(1,20))
    story.append(Paragraph(f"Generato il: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1,20))

    for path in grafici_paths:
        story.append(Image(path, width=400, height=400))
        story.append(Spacer(1,10))

    doc.build(story)

    # Mostra messaggio
    messagebox.showinfo("Statistiche", f"Tutti i grafici dei modelli + KMeans salvati in {pdf_path}")




#_____________________________________________Bottoni alti_____________________________________________
buttons_frame = tk.Frame(root, bg="black")
buttons_frame.place(x=1, y=100)
#Così riuniamo tutti i bottoni in un unico frame e possiamo gestirli meglio senza farli andare via
btn_studenti = tk.Button(buttons_frame, text="👥", 
                          command=apri_toplevel_inserimento,
                          font=font_btn, bg="black", fg="white")
btn_studenti.pack(anchor="w", pady=2, padx=10)

btn_visual = tk.Button(buttons_frame, text="👁️", 
                    command=topvisualizza,
                    font=font_btn, bg="black", fg="white")
btn_visual.pack(anchor="w", pady=2, padx=10)

btn_db = tk.Button(buttons_frame, text="📈", 
                    command=topstatistiche,
                    font=font_btn, bg="black", fg="white")
btn_db.pack(anchor="w", pady=2, padx=10)

btn_db = tk.Button(buttons_frame, text="⭐", 
                    command=super_stats,
                    font=font_btn, bg="black", fg="white")
btn_db.pack(anchor="w", pady=2, padx=10)

root.mainloop()