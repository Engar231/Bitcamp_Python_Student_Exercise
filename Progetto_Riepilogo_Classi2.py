import random #random.randint()
import pandas as pd #df.pdDataframe()
import os
import cProfile
import timeit 
'''
🧭 Fase 2: Refactoring ad oggetti (OOP)
📋 Obiettivo
Convertire il codice in stile OOP con:
-classe Studente
-classe GestoreStudenti

🧱 Struttura consigliata
class Studente:
    def __init__(self, id, nome, cognome, età, genere, ore_studio, assenze, media_voti, comportamento, esito_finale):
        ...

class GestoreStudenti:
    def __init__(self):
        self.studenti = []

    def aggiungi_studente(self, studente):
        ...

    def salva_csv(self, nome_file):
        ...

    def carica_csv(self, nome_file):
        ...
➕ Extra suggeriti
-metodo __str__() nella classe Studente
-menu testuale che richiama i metodi della classe GestoreStudenti
'''
# Cartella di destinazione cosi non creo immondizia!
folder = r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo"
# Assicurati che esista
os.makedirs(folder, exist_ok=True)

# Caricamento CSV o creazione DataFrame vuoto
csv_path = r"C:\Users\Calfi\Desktop\Python BitCamp\Python\Esercizio - Studenti_Riepilogo\studenti_riepilogo_class.csv"
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

#Fase 1 - Controlli errori di Input. (Try,Except, Value Error)
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

#fase 2 classe studente
class Studente:
    def __init__(self, id, nome, cognome, età, genere, ore_studio, assenze, media_voti, comportamento, esito_finale):
        self._id=id #Privato questo
        self.nome=nome
        self.cognome=cognome
        self.età=età
        self.__genere=genere #nascosto? proviamo? NON VA 11/08,mi stramma il csv e database
        self.ore_studio=ore_studio
        self.assenze=assenze
        self.media_voti=media_voti
        self.comportamento=comportamento
        self._esito_finale=esito_finale #Facciamo privato questo

    @property
    def id(self):
        return self._id
    @property
    def esito_finale(self):
        return self._esito_finale
    @id.setter
    def id(self,id):
        self._id=id
    @esito_finale.setter
    def esito_finale(self,esito_finale):
        self._esito_finale=esito_finale

    def __str__(self):
        return f"Dati Studente: {self._id}, {self.nome} {self.cognome}, {self.età}, {self.ore_studio},{self.__genere}, {self.assenze}, {self.media_voti}, {self.comportamento}, {self._esito_finale}"

#fase 2 classe Gestore
class GestoreStudenti:
    def __init__(self):
        self.studenti = []

#fase 2 inserisci studenti
    def inserisci_studente(self):
        # input con funzioni già fatte
        id = len(self.studenti)+1
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

        studente = Studente(id, nome, cognome, eta, genere, ore_studio, assenze, media_voti, comportamento, esito_finale)
        self.studenti.append(studente)
        print("_______________Studente Aggiunto_______________\n")

#fase 2 modifiche studente (Grazie chatgpt per il debug e la scrittura.)
    def modifica_studente(self):
        #print("ID studenti caricati:", [s.id for s in self.studenti]) Debug
        id_studente = input_int("ID studente da modificare: ")
# Trova lo studente con quell'ID
        for studente in self.studenti:
            #print(f"Controllo Studente ID: {studente.id} VS ID inserito: {id_studente} (tipi: {type(studente.id)}, {type(id_studente)})") Debug
            if studente.id == id_studente:
                print("Trovato studente! Modifico...")

                ore_studio = input_float(f"Nuove ore di studio: ")
                if ore_studio != '': #Se lascia vuoto skippa.
                    studente.ore_studio = ore_studio

                assenze = input_int(f"Nuovo numero assenze: ")
                if assenze != '': #Se lascia vuoto skippa.
                    studente.assenze = assenze

                media_voti = input_float(f"Nuova media voti: ")
                if media_voti != '': #Se lascia vuoto skippa.
                    studente.media_voti = media_voti

                comportamento = input_scelta(f"Nuovo comportamento: ", ["ottimo", "buono", "sufficiente", "scarso"]).lower()
                studente.comportamento = comportamento

                if studente.comportamento == "scarso" or studente.media_voti <= 5.3 or studente.assenze == 220:
                    studente.esito_finale = "bocciato"
                else:
                    studente.esito_finale = "promosso"
                print(f"Modificato studente: {studente.nome} {studente.cognome} - Ore studio: {studente.ore_studio}, Assenze: {studente.assenze}, Media: {studente.media_voti}, Esito: {studente.esito_finale}")

                print("_______________Modifiche Studente Effettuate_______________\n")
                return
        print("Studente non trovato!")


# fase 2 salva
    def salva_csv(self,csv_path):
        dati_studenti = []
        for s in self.studenti:
            dati_studenti.append({
                'id': s.id,
                'nome': s.nome,
                'cognome': s.cognome,
                'età': s.età,
                'genere': s._Studente__genere,  # prende il "privato"
                'ore_studio': s.ore_studio,
                'assenze': s.assenze,
                'media_voti': s.media_voti,
                'comportamento': s.comportamento,
                'esito_finale': s.esito_finale
            })
            df = pd.DataFrame(dati_studenti)
            df.to_csv(csv_path, index=False)
        print("Salvataggio completato!")
        print("_______________Salvataggio in CSV Effettuato_______________\n")

# fase 2 Carica
    def carica_csv(self,csv_path):
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            if '_id' or '__genere' or '_esito_finale' in df.columns:
                df.rename(columns={'_id': 'id', '_Studente__genere': 'genere', '_esito_finale': 'esito_finale'}, inplace=True)
            self.studenti = [Studente(**row) for _, row in df.iterrows()]
            print("_______________Caricamento CSV Effettuato_______________\n")
        else:
            print("File CSV non trovato.")
    
    def genera_studenti(self,batch_size=200, soglia=60):
        global df
        next_id = df['id'].max() + 1 if not df.empty else 1
        while True:
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
                comportamento = random.choices(["ottimo", "buono", "sufficiente", "scarso"], weights=[0.1, 0.3,0.4,0.2])[0]
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
                df.to_csv(r"C:\Users\Calfi\Desktop\Python BitCamp\Python\studenti_riepiologo_class.csv", index=False)
                break

def menu():
    gestore=GestoreStudenti()
    if os.path.exists(csv_path):
            gestore.carica_csv(csv_path)
    
    #Fase 1.4 Menù per il terminale, momentaneo
    while True:
        print("Bitcamp presenta:\nStudenti_Riepilogo di Alfio Ezechiele Cavallaro")
        print("1: Inserisci nuovo studente")
        print("2: Mostra studenti attivi")
        print("3: Modifica studente attivi")
        print("4: Carica CSV")
        print("5: Skynet, attiva protocollo.")
        print("6: Salva/Exit")
        scelta = input_int("Seleziona: ")

        if scelta == 1:
            gestore.inserisci_studente()
        elif scelta == 2:
            for s in gestore.studenti:
                print(s)
        elif scelta == 3:
            gestore.modifica_studente()
        elif scelta == 4:
            gestore.carica_csv(csv_path)
        elif scelta == 5:
            gestore.genera_studenti()
        elif scelta == 6:
            scelta = input("Vuoi salvare i dati prima di uscire? [S/N]: ").strip().upper()
            gestore.salva_csv(csv_path)
            break
        else:
            print("Scelta non valida.")

if __name__ == "__main__":
    menu()
print("__________Fine Fase 2__________")
    