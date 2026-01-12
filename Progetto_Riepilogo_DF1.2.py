import random #random.randint()
import pandas as pd #df.pdDataframe()
import os
import cProfile
import timeit 

'''
🔨 Fase 1: Raccolta e gestione procedurale dei dati
📋 Obiettivo
Creare uno script procedurale che consenta:
- l’inserimento manuale di studenti;
- il salvataggio in file CSV;
- la lettura e modifica dei dati salvati.

🧩 Campi richiesti
Ogni studente dovrà avere i seguenti dati:

Campo		Tipo	Obbligatorio	Note
id		int		✅	univoco
nome		string		✅	lista nomi maschili
cognome		string		✅	lista nomi femminili
età		int		✅	14-20
genere		string		✅	M/F
ore_studio	float		✅	settimanali
assenze		int		✅	numero
media_voti	float		✅	da 4 a 10
comportamento	string		✅	Ottimo, Buono, Sufficiente, Scarso
esito_finale	string		✅	Promosso, Bocciato

🧪 Funzionalità minime
Menu testuale (in console) per:
- aggiungere nuovo studente
- mostrare tutti gli studenti
- modificare uno studente esistente
- salvare in studenti.csv
- caricare da studenti.csv
- Controlli di input validi

Per riuscire a popolare il dataset con una certa coerenza, vorrei una funzione 
che simuli la generazione di un dataset di studenti con caratteristiche casuali, 
fino a raggiungere una certa condizione statistica, ovvero devi sviluppare 
un sistema che generi un insieme di dati (dataset) di studenti. 
Ogni studente è descritto da vari attributi, come:

 -ID univoco
 -Nome (maschile o femminile)
 -Cognome
 -Età (da 14 a 20 anni)
 -Genere (M o F)
 -Ore di studio giornaliere (valore decimale realistico tra 0 e 8)
 -Numero di assenze (intero casuale)
 -Media voti (da 4 a 10, con un decimale)
 -Comportamento (tra: Ottimo, Buono, Sufficiente, Scarso)
 -Esito finale (Promosso o Bocciato), determinato da una logica specifica.

Generazione di studenti casuali:
-I nomi devono essere scelti casualmente da due liste separate (nomi maschili e femminili).
-I cognomi devono essere scelti casualmente da una lista predefinita.
-L’esito finale deve essere determinato secondo questa logica:
-Se il comportamento è “Scarso” → Bocciato
-Se la media voti è ≤ 5.3 → Bocciato
-Se le assenze sono esattamente 220 → Bocciato
-Altrimenti → Promosso

Generazione iterativa del dataset:
-Generare studenti in “batch” di dimensione definita (ad esempio 200 studenti per batch).
-Continuare a generare batch e aggiungerli al dataset totale finché la percentuale di studenti promossi non supera il 60% sul totale degli studenti generati finora.
-Stampare a video come promemoria il numero totale di studenti, il numero di promossi e la percentuale di promossi dopo ogni batch generato.

Salvataggio del dataset:
-Quando la percentuale di promossi supera il 60%, terminare la generazione.
-Salvare il dataset finale in un file CSV chiamato studenti.csv.
'''
#_____________________________________________Destinazione file_____________________________________________
folder = r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo"
# Assicurati che esista
os.makedirs(folder, exist_ok=True)

#_____________________________________________caricamento o creazione del csv_____________________________________________
csv_path = r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_df.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(columns=['id', 'nome', 'cognome', 'età', 'genere', 'ore_studio', 'assenze', 'media_voti', 'comportamento', 'esito_finale'])

# Lista Nomi e Cognomi di Simone + Modifiche Mie
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

#_____________________________________________Controlli Personali_____________________________________________
def input_int(messaggio, minimo=None, massimo=None):
    while True:
        try:
            valore = int(input(messaggio))
            if minimo is not None and valore < minimo:
                print(f"Il valore deve essere >= {minimo}")
                continue
            if massimo is not None and valore > massimo:
                print(f"Il valore deve essere <= {massimo}")
                continue
            return valore
        except ValueError:
            print("Inserisci un numero intero valido.")

def input_float(messaggio, minimo=None, massimo=None):
    while True:
        try:
            valore = float(input(messaggio))
            if minimo is not None and valore < minimo:
                print(f"Il valore deve essere >= {minimo}")
                continue
            if massimo is not None and valore > massimo:
                print(f"Il valore deve essere <= {massimo}")
                continue
            return valore
        except ValueError:
            print("Inserisci un numero decimale valido.")

def input_scelta(messaggio, scelte):
    while True:
        valore = input(messaggio).strip()
        if valore in scelte:
            return valore
        print(f"Scelta non valida. Opzioni: {', '.join(scelte)}")

#_____________________________________________Inserimento Manuale_____________________________________________
def inserisci_studente():
    global df
    # input con funzioni già fatte
    new_id = df['id'].max() + 1 if not df.empty else 1
    nome = str(input("Nome: ")).capitalize()
    # genera cognome random da lista
    cognome = str(input("Cognome: ")).capitalize()
    eta = input_int("Età: ", 14, 20)
    genere = input_scelta("Genere (M/F/A): ", ["M", "F"]).upper()
    ore_studio = input_float("Ore studio giornaliere (0-8): ", 0, 8)
    assenze = random.randint(0, 220)
    media_voti = input_float("Media voti (4-10): ", 4, 10)
    comportamento = input_scelta("Comportamento (ottimo, buono, sufficiente, scarso): ", ["ottimo", "buono", "sufficiente", "scarso"]).lower()
    # esito manuale o calcolato
    if comportamento == "scarso" or media_voti <= 5.3 or assenze == 220:
        esito_finale = "bocciato"
    else:
        esito_finale = "promosso"

    nuovo_studente = pd.DataFrame([{
        'id': new_id,
        'nome': nome,
        'cognome': cognome,
        'età': eta,
        'genere': genere,
        'ore_studio': ore_studio,
        'assenze': assenze,
        'media_voti': media_voti,
        'comportamento': comportamento,
        'esito_finale': esito_finale
    }])

    df = pd.concat([df, nuovo_studente], ignore_index=True)
    print("_______________Inserimento Manuale Studente Effettuato_______________\n")

# Fase 1 Mostra Studenti
def mostra_studenti():
    for idx, stud in df.iterrows():
        print(f"ID: {stud['id']}, Nome: {stud['nome']} {stud['cognome']}, Età: {stud['età']}, Genere: {stud['genere']}, Ore Studio: {stud['ore_studio']}, Assenze: {stud['assenze']}, Media: {stud['media_voti']}, Comportamento: {stud['comportamento']}, Esito: {stud['esito_finale']}")

#_____________________________________________Modifica Studente_____________________________________________
def modifica_studente():
    global df
    id_studente = input_int("ID studente da modificare: ")
    if id_studente not in df['id'].values:
        print("ID non trovato.")
        return

    idx = df.index[df['id'] == id_studente][0]
    print("Lascia vuoto se non vuoi modificare.")
    ore_studio = input("Nuove ore di studio (vuoto per saltare): ")
    if ore_studio != '':
        df.at[idx, 'ore_studio'] = float(ore_studio)
    assenze = input("Nuovo numero assenze (vuoto per saltare): ")
    if assenze != '':
        df.at[idx, 'assenze'] = int(assenze)
    media_voti = input("Nuova media voti (vuoto per saltare): ")
    if media_voti != '':
        df.at[idx, 'media_voti'] = float(media_voti)
    comportamento = input("Nuovo comportamento (ottimo, buono, sufficiente, scarso) (vuoto per saltare): ").lower()
    if comportamento in ["ottimo", "buono", "sufficiente", "scarso"]:
        df.at[idx, 'comportamento'] = comportamento
#Vogliamo cambiarlo noi?
    esito_finale = input("Nuovo esito finale (promosso, bocciato) (vuoto per saltare): ").lower()
    if esito_finale in ["promosso", "bocciato"]:
        df.at[idx, 'esito_finale'] = esito_finale
    print("_______________Modifiche Studente Effettuate_______________\n")

#_____________________________________________Salva_____________________________________________
def salva_csv():
    df.to_csv(csv_path, index=False)
    print("_______________Salvataggio in CSV Effettuato_______________\n")

#_____________________________________________Carica_____________________________________________
def carica_csv():
    global df
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print("_______________Caricamento CSV Effettuato_______________\n")
    else:
        print("File CSV non trovato.")

#_____________________________________________Terminator_____________________________________________
def genera_studenti(batch_size=200, soglia=60):
    global df
    next_id = df['id'].max() + 1 if not df.empty else 1
    while True:
        batch = []
        for _ in range(batch_size):
            genere = random.choice(["M", "F"])
            nome = (
            random.choice(nomi_maschili) if genere == "M" else
            random.choice(nomi_femminili)
            )
            cognome = random.choice(cognomi)
            eta = random.randint(14, 20)
            ore_studio = round(random.uniform(0,8),1)
            assenze = random.randint(0,220)
            media_voti = round(random.uniform(4,10),1)
            comportamento = random.choices(["ottimo", "buono", "sufficiente", "scarso"], weights=[0.2, 0.3, 0.4, 0.2])[0]
            #si aggiunge una S al choice, così possiamo usare la funzione peso, in modo da gestire la differenza del random
            if comportamento == "scarso" or media_voti <= 5.3 or assenze == 220:
                esito_finale = "bocciato"
            else:
                esito_finale = "promosso"

            batch.append({
                'id': next_id,
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
            next_id += 1

        df = pd.concat([df, pd.DataFrame(batch)], ignore_index=True)

        totali = len(df)
        promossi = (df["esito_finale"] == "promosso").sum()
        perc = (promossi/totali)*100
        print(f"Totali: {totali}, Promossi: {promossi}, Percentuale: {perc:.2f}%")

        if perc > soglia:
            print("_______________Soglia Raggiunta, Creazione Terminator Completata_______________\n")
            df.to_csv(csv_path)
            break

#_____________________________________________Menù Terminale_____________________________________________
while True:
    print("1: Inserisci nuovo studente")
    print("2: Mostra studenti attivi")
    print("3: Modifica studente attivi")
    print("4: Carica CSV")
    print("5: Skynet, attiva protocollo.")
    print("6: Salva/Exit")
    scelta = input_int("Bitcamp Presente\nTerminale Studenti_Riepilogo.\nSeleziona: ")

    if scelta == 1:
        inserisci_studente()
    elif scelta == 2:
        mostra_studenti()
    elif scelta == 3:
        modifica_studente()
    elif scelta == 4:
        carica_csv()
    elif scelta == 5:
        genera_studenti()
    elif scelta == 6:
        scelta = input("Vuoi salvare i dati prima di uscire? [S/N]: ").strip().upper()
        salva_csv()
        break
print("__________Fine Fase 1__________")