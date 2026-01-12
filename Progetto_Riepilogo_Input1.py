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
import random #random.randint()
import pandas as pd #df.pddataframe()
import os

#_____________________________________________Creazione della Variabile Folder, per evitare immondizia sparsa_____________________________________________
folder = r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo"
# Assicurati che esista
os.makedirs(folder, exist_ok=True)

studenti = [] #Lista vuota

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

#_____________________________________________Se il file esiste, riprende ID_____________________________________________
if os.path.exists(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_input.csv"):
    df = pd.read_csv(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_input.csv")
else:
    df = pd.DataFrame(columns=['id', 'nome', 'cognome', 'età', 'genere', 'ore_studio', 'assenze', 'media_voti', 'comportamento', 'esito_finale'])
    next_id = 1 #Aggiungiamo +1 all'ID ad ogni creazione nuova

#_____________________________________________Cpntrollo personalizzati dei vari Value Error_____________________________________________
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

#_____________________________________________Input Manuale degli studenti_____________________________________________
def inserisci_studente():
    id=input_int("Aggiungi ID studente: ")
    nome=str(input("Aggiungi Nome studente: ")).capitalize()
    cognome=str(input("Aggiungi Cognome studente: ")).capitalize()
    età=input_int("Aggiungi Età studente [14/20]:", 14, 20)
    genere=input_scelta("Aggiungi il genere dello studente [M,F]:", ["M", "F"]).capitalize()
    ore_studio=input_float("Aggiungi le Ore di studio giornaliere dello studente [0/8]:", 0, 8)
    #numero_assenze=int(input("Aggiungi le ore di assenze totali: ")) #Random
    numero_assenze=random.randint(0,220)
    media_voti=input_float("Aggiungi la media dei voti [4/10]:", 4, 10)
    comportamento=input_scelta("Aggiungi il comportamento dell'alunno [ottimo,buono,sufficente,scarso]:", ["ottimo", "buono", "sufficente", "scarso"]).lower()
    #esito_finale=input_scelta("Esito finale?:", ["promosso","bocciato"]).lower() #Per ora che è Manuale.
    if comportamento == "Scarso" or media_voti <= 5.3 or numero_assenze == 220:
        esito_finale = "Bocciato"
    else:
        esito_finale = "Promosso"
    
    nuovo_studente= {
    'id': id,
    'nome': nome,
    'cognome': cognome,
    'età': età,
    'genere': genere,
    'ore_studio': ore_studio,
    'assenze': numero_assenze,
    'media_voti': media_voti,
    'comportamento': comportamento,
    'esito_finale': esito_finale
}
    studenti.append(nuovo_studente)
    print("_______________Inserimento Manuale Studente Effettuato_______________\n")
    return

#_____________________________________________Definizione del comando Salva_____________________________________________
def salva_csv():
    df = pd.DataFrame(studenti)
    df.to_csv(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_input.csv" , index=False)
    print("_______________Salvataggio CSV Effettuato_______________\n")

#_____________________________________________Definizione del comando Carica_____________________________________________
def carica_csv():
    global studenti
    print("_______________Caricamento CSV Effettuato_______________\n")
    df = pd.read_csv(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_input.csv")
    studenti = df.to_dict(orient='records')

#_____________________________________________Comando Mostra Studenti_____________________________________________
def mostra_studenti():
    print("_______________Lista Alunni_______________\n")
    for studente in studenti:
        print(f"""
ID: {studente['id']}
Nome: {studente['nome']} {studente['cognome']}
Età: {studente['età']}
Genere: {studente['genere']}
Ore Studio: {studente['ore_studio']}
Numero Assenze: {studente['assenze']}
Media Voti: {studente['media_voti']}
Comportamento: {studente['comportamento']}
Esito Finale: {studente['esito_finale']}
-------------------------------
""")


#_____________________________________________Comando Modifica Studente_____________________________________________
def modifica_studente():
    global df
    id_studente = input_int("Inserisci l'ID dello studente da modificare: ")
    if id_studente not in df['id'].values:
        print("ID non trovato.")
        return
    print("Lascia vuoto un campo se non vuoi modificarlo.")
    ore_studio = input_float("Nuove ore di studio [0/8]: ", 0,8)
    assenze = input_int("Nuovo numero di assenze [0/220]: ", 0, 220)
    media_voti = input_float("Nuova media voti [4/10]: ", 4,10)
    comportamento = input_scelta("Nuovo comportamento [ottimo,buono,sufficente,scarso]", ["ottimo", "buono", "sufficente", "scarso"]).lower()
    if comportamento == "scarso" or media_voti <= 5.3 or assenze == 220:
            esito_finale = "bocciato"
    else:
            esito_finale = "promosso"

    if ore_studio:
        df.loc[df['id'] == id_studente, 'ore_studio'] = float(ore_studio)
    if assenze:
        df.loc[df['id'] == id_studente, 'numero_assenze'] = int(assenze)
    if media_voti:
        df.loc[df['id'] == id_studente, 'media_voti'] = float(media_voti)
    if comportamento:
        df.loc[df['id'] == id_studente, 'comportamento'] = comportamento
    if esito_finale:
        df.loc[df['id'] == id_studente, 'esito_finale'] = esito_finale

    print(f"Studente con ID {id_studente} modificato correttamente.")



#_____________________________________________Terminator_____________________________________________
def genera_studenti(batch_size=200, soglia=60):
    global df
    next_id = 1 if df.empty else df['id'].max()+1 #Aggiunge un +1 ad ogni studente creato per ID
    while True:
        batch = []
        for _ in range(batch_size):
            genere = random.choice(["M", "F"]) #Genere
            nome = (
            random.choice(nomi_maschili) if genere == "M" else
            random.choice(nomi_femminili) 
            )
            cognome = random.choice(cognomi)
            eta = random.randint(14,20) #Età, bloccato per valori 14,20 come richiesto
            ore_studio = round(random.uniform(0,8),1)
            numero_assenze=random.randint(0,220) #Ore assenze
            media_voti=round(random.uniform(4,10),1)
            comportamento = random.choices(["ottimo", "buono", "sufficente", "scarso"], weights=[0.1, 0.3,0.4,0.2])[0]
            if comportamento == "scarso" or media_voti <= 5.3 or numero_assenze == 220:
                esito_finale = "bocciato"
            else:
                esito_finale = "promosso"
            studente = {
                'id': next_id,
                'nome': nome,
                'cognome': cognome,
                'età': eta,
                'genere': genere,
                'ore_studio': ore_studio,
                'assenze': numero_assenze,
                'media_voti': media_voti,
                'comportamento': comportamento,
                'esito_finale': esito_finale
            }
            batch.append(studente) #Aggiungiamo al batch lo studente creato randomicamente
            next_id +=1 #ID +1
        df = pd.concat([df, pd.DataFrame(batch)], ignore_index=True) #Aggiorna Dataframe
        totali = len(df)
        promossi = (df["esito_finale"] == "promosso").sum()
        perc = (promossi/totali)*100
        print(f"Totali Studenti: {totali}\n Promossi: {promossi}\n Percentuale: {perc:.2f}%")
        if perc > soglia:
            print("Soglia Raggiunta. Salvataggio del Dataset in corso...")
            df.to_csv(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_input.csv", index=False)
            print("_______________Salvataggio CSV Effettuato_______________\n")
            break
print("_______________Studente in Batch Randomico Aggiunto_______________\n")

    
#_____________________________________________Menù Terminale_____________________________________________
while True: #Deve caricare il csv quando lo riprnde
    print("Portale Studenti - Bitcamp")
    print("1: Aggiungi nuovo studente")
    print("2: Visualizza tutti gli studenti")
    print("3: Modifica dati di uno studente già esistente")
    print("4: Carica CSV")
    print("5: Salvataggio/Exit.")
    print("6: Skynet, Aggiungi Bot!")
    scelta = int(input("Esegui azione: "))
    if scelta==1:
        inserisci_studente()
    if scelta==2:
        mostra_studenti()
    if scelta==3:
        modifica_studente()
    if scelta==4:
        carica_csv()
    if scelta==5:
        scelta = input("Vuoi salvare i dati prima di uscire? [S/N]: ").strip().upper()
        print("__________Fine Fase 1__________")
        salva_csv()
    if scelta==6:
        genera_studenti()
        print("Attivazione Skynet")
    print("Programma terminato.")