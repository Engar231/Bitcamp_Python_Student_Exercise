import random #random.randint()
import pandas as pd #df.pdDataframe()
import os
import sqlite3
import cProfile
import timeit 
import csv

'''
🧭 Fase 3: Database SQLite3
📋 Obiettivo
Trasferire la gestione dati da file CSV a database SQLite3.

📂 Database: studenti.db
Tabella: studenti
Campo		Tipo		Vincoli
id		INTEGER		PRIMARY KEY
nome		TEXT		NOT NULL
cognome		TEXT		NOT NULL
età		INTEGER		CHECK(14 ≤ età ≤ 20)
genere		TEXT		CHECK(genere IN ('M','F'))
ore_studio	REAL		≥ 0
assenze		INTEGER		≥ 0
media_voti	REAL		1-10
comportamento	TEXT		CHECK(valore valido)
esito_finale	TEXT		CHECK(valore valido)

🧪 Funzionalità minime
Creazione tabella se non esiste
-Inserimento nuovo studente
-Visualizzazione tabella
-Modifica e cancellazione record
-Esportazione completa in studenti.csv

➕ Extra suggeriti
Popola con almeno 150 studenti (puoi realizzare una funzione che realizzi il popolamento)
'''
#_____________________________________________Cartella di destinazione_____________________________________________
folder = r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo"
# Assicurati che esista
os.makedirs(folder, exist_ok=True)

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


#_____________________________________________Controllo Value Error_____________________________________________
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

def input_int_vuoto(messaggio): #Non hanno i massmi perché nel DB non c'è bisogno, bravo CHATGPT Ovviamente
    valore = input(messaggio).strip()
    if valore == '':
        return None
    try:
        return int(valore)
    except ValueError:
        print("Valore non valido, riprova.")
        return input_int_vuoto(messaggio)

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

def input_float_vuoto(messaggio):  #Non hanno i massimi perché nel DB non c'è bisogno, bravo CHATGPT Ovviamente
    valore = input(messaggio).strip()
    if valore == '':
        return None
    try:
        return float(valore)
    except ValueError:
        print("Valore non valido, riprova.")
        return input_float_vuoto(messaggio)

def input_scelta(messaggio, scelte):
    while True:
        valore = input(messaggio).strip()
        if valore in scelte:
            return valore
        print(f"Scelta non valida. Opzioni: {', '.join(scelte)}")

def input_scelta_vuoto(messaggio, scelte):  #Non hanno i massimi perché nel DB non c'è bisogno, bravo CHATGPT Ovviamente
    valore = input(messaggio).strip()
    if valore == '':
        return None
    if valore in scelte:
        return valore
    print(f"Scelta non valida. Opzioni: {', '.join(scelte)}")
    return input_scelta_vuoto(messaggio, scelte)
#_____________________________________________Lettura del CSV per prendere i file_____________________________________________
csv_path = r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_df.csv"
df = pd.read_csv(csv_path)

#_____________________________________________Creazione DB_____________________________________________
conn=sqlite3.connect(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_db.db")
c = conn.cursor()
c.execute('''
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
        )''')
#Con AUTOINCREMENT POSSO OMETTERE SOTTO, ALL'INSERT! IL DB LO GESTISCE SOLO
print("🎉 Database 'studenti_riepilogo_db.db' creato correttamente!")

c.execute("SELECT name FROM sqlite_master WHERE type='table'")
righe = c.fetchall()
for r in righe:
    print(r)


#_____________________________________________Inserisci studente_____________________________________________
def inserisci_studente():
    # input con funzioni già fatte
    nome = str(input("Nome: ")).capitalize()
    cognome = str(input("Cognome: ")).capitalize()
    eta = input_int("Età: ", 14, 20)
    genere = input_scelta("Genere (M/F): ", ["M", "F"]).upper()
    ore_studio = input_float("Ore studio giornaliere (0-8): ", 0, 8)
    assenze = random.randint(0, 220)
    media_voti = input_float("Media voti (4-10): ", 4, 10)
    comportamento = input_scelta("Comportamento (ottimo, buono, sufficiente, scarso): ", ["ottimo", "buono", "sufficiente", "scarso"]).lower()
    # esito manuale o calcolato
    if comportamento == "scarso" or media_voti <= 5.3 or assenze == 220:
        esito_finale = "bocciato"
    else:
        esito_finale = "promosso"
    # Inserisci direttamente nel DB
    conn = sqlite3.connect(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_db.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO Studenti (nome, cognome, età, genere, ore_studio, assenze, media_voti, comportamento, esito_finale)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, cognome, eta, genere, ore_studio, assenze, media_voti, comportamento, esito_finale))
    conn.commit()
    conn.close()
    print("_______________Studente Aggiunto_______________\n")

#_____________________________________________Mostra studente_____________________________________________
def mostra_studenti():
    conn=sqlite3.connect(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_db.db")
    conn.row_factory=sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM Studenti")
    righe=c.fetchall()
    conn.close()
    for r in righe:
        print(dict(r))
    return

#_____________________________________________Terminator_____________________________________________
def genera_studenti(batch_size=150, soglia=60):
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

        #Inserimento in DB
        conn = sqlite3.connect(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_db.db")
        c = conn.cursor()
        #Prima sbagliavo perché mettevo execute, salvando solo l'ultimo, andava il many!
        c.executemany("""
        INSERT INTO Studenti (nome, cognome, età, genere, ore_studio, assenze, media_voti, comportamento, esito_finale)
        VALUES (:nome,:cognome,:età,:genere,:ore_studio,:assenze,:media_voti,:comportamento,:esito_finale)
        """, batch)
        conn.commit()
        conn.close()
        return batch

#_____________________________________________Modifica Studente_____________________________________________
def modifica_studente(): 
    #Ci connettiamo sennò non abbiamo modo di trovarlo
    conn = sqlite3.connect(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_db.db")
    c = conn.cursor()
    id_studente = input_int("ID studente da modificare: ")
    #Verifica se esiste lo studente da dentro il DB, quindi dal numero in print, prende l'id dal DB
    c.execute("SELECT * FROM Studenti WHERE id = ?", (id_studente,))
    #Qui selezione lo studente
    studente = c.fetchone()

    if not studente:
        print("Studente non trovato!")
        conn.close()
        return
    #Se non lo trova torna indietro

    print("Trovato studente! Modifico...")

    #Richiedi i nuovi dati
    ore_studio = input_float_vuoto("Nuove ore di studio (vuoto per non modificare)(4/8): ")
    assenze = input_int("Nuovo numero assenze (vuoto per non modificare): ")
    media_voti = input_float_vuoto("Nuova media voti (vuoto per non modificare)/(4/10): ")
    comportamento = input_scelta_vuoto("Nuovo comportamento [ottimo, buono, sufficiente, scarso] (vuoto per non modificare): ",  ["ottimo", "buono", "sufficiente", "scarso"])

    # Converti e aggiorna solo se non vuoto. Questa è una figata da ricordare fissa
    if ore_studio is not None:
        c.execute("UPDATE Studenti SET ore_studio = :ore_studio WHERE id = :id", {'ore_studio': ore_studio, 'id': id_studente})
    if assenze is not None:
        c.execute("UPDATE Studenti SET assenze = :assenze WHERE id = :id", {'assenze':assenze, 'id':id_studente})
    if media_voti is not None:
        c.execute("UPDATE Studenti SET media_voti = :media_voti WHERE id = :id", {'media_voti':media_voti, 'id' :id_studente})
    if comportamento is not None:
        c.execute("UPDATE Studenti SET comportamento = :comportamento WHERE id = :id", {'comportamento' :comportamento.lower(), 'id' :id_studente})

    #Aggiorna l'esito finale in base alle nuove regole. Set/Case/When/Then è l'IF,ELIF,ELSE del DB
    #Set esito_finale=case è voglio aggiornare questa riga in queste condizioni:
    #When se è almeno una di queste condizioni è vera.
    #then è la risposta all'IF in pratica
    #Else è sempre else.
    #End è fine e chiude il CASE
    #Where id = ?
    #Dava errore eprché avevo scirtto assenza = 220, invece di >= BASTARDIIII
    c.execute("""
        UPDATE Studenti
        SET esito_finale = CASE
            WHEN comportamento = 'scarso' OR media_voti <= 5.3 OR assenze >= 220
            THEN 'bocciato'
            ELSE 'promosso'
        END
        WHERE id = ?
    """, (id_studente,))

    conn.commit()
    conn.close()

    print("_______________Modifiche Studente Effettuate_______________\n")

#_____________________________________________Rimozione studente DB_____________________________________________
def rimuovi_studente(): #Tolgo id studente dalle () perch* così possiamo metterlo in input
    id_studente = int(input("Inserisci l'ID dello studente da eliminare: "))

    conn = sqlite3.connect(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_db.db")
    cursor = conn.cursor()
    #Controllo esistenza studente per ID
    cursor.execute('SELECT id FROM Studenti WHERE id = :id', {'id': id_studente})
    dati = cursor.fetchone()
    if dati is None:
        print(f"Nessuno studente trovato con ID {id_studente}")
    else:
    # Estraggo l'ID come intero
        id_studente = dati[0]
    # Cancello dalla tabella corretta (qui Dipendenti: verifica se è giusto)
        cursor.execute('DELETE FROM Studenti WHERE id = :id', {'id': id_studente})
        conn.commit()
        print(f"Tutti i dati dello studente con ID {id_studente} sono stati rimossi")
    conn.close()

def esporta_studenti_csv():
    conn = sqlite3.connect(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_db.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Studenti")
    rows = cursor.fetchall()

    # prendo i nomi delle colonne
    colonne = [desc[0] for desc in cursor.description]

    with open(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_dbcsv.csv", "w", newline="", encoding="utf-8") as f: #tips chatgpt, se lo usi per excel, usare utf-8-sig
        writer = csv.writer(f) #serve import csv, sennò me lo da rosso
        writer.writerow(colonne)  # intestazione
        writer.writerows(rows)    # dati

    conn.close()
    print("Esportazione completata: studenti_riepilogo_db.csv")
#_____________________________________________Menù Terminale_____________________________________________
while True:
    conn = sqlite3.connect(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_db.db")
    print("1: Inserisci nuovo studente")
    print("2: Mostra studenti attivi")
    print("3: Modifica studente attivi")
    print("4: Rimuovi Studente")
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
        rimuovi_studente()
    elif scelta == 5:
        genera_studenti()
    elif scelta == 6:
        scelta = input("Vuoi salvare i dati prima di uscire? [S/N]: ").strip().upper()
        esporta_studenti_csv()
        break
print("__________Fine Fase 1__________")
#Modalità veloce, però non possiamo modificarlo almeno che non tocchiamo il DB! Buono però da sapere.
# # Se vuoi, puoi creare la tabella con la struttura che vuoi (opzionale se usi solo to_sql)
# create_table_sql = '''
# CREATE TABLE IF NOT EXISTS studenti (
#     id INTEGER PRIMARY KEY,
#     nome TEXT NOT NULL,
#     cognome TEXT NOT NULL,
#     età INTEGER CHECK(età BETWEEN 14 AND 20),
#     genere TEXT CHECK(genere IN ('M','F')),
#     ore_studio REAL CHECK(ore_studio >= 0),
#     assenze INTEGER CHECK(assenze >= 0),
#     media_voti REAL CHECK(media_voti BETWEEN 1 AND 10),
#     comportamento TEXT CHECK(comportamento IN ('ottimo','buono','sufficiente','scarso')),
#     esito_finale TEXT CHECK(esito_finale IN ('promosso','bocciato'))
# );
# '''

# conn.execute(create_table_sql)

# # Carichi il tuo DataFrame df (esempio, o da csv)
# # df = pd.read_csv('studenti_riepilogo.csv')

# # Scrivi il DataFrame nella tabella SQLite: se la tabella esiste puoi sostituirla o aggiungere
# df.to_sql('studenti', conn, if_exists='replace', index=False)  # 'replace' cancella e ricrea

# # Oppure usa if_exists='append' per aggiungere righe senza cancellare

# conn.commit()
# conn.close()

