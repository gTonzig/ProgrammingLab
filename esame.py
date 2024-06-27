#estensione della classe Exception per la gestione dei vari errori

class ExamException(Exception):
    pass


class CSVTimeSeriesFile:

    #definisco il costruttore e prendo come parametro il file passato dall'utente e lo assegna alla variabile di istanza "self.name"

    def __init__(self, my_file):
        self.name = my_file

    def get_data(self):

        reader_my_file = self.open_my_file()        #variabile che mi permette di aprire il file attraverso il metodo "open_my_file"

        my_data_file = self.read_my_file(reader_my_file)    #variabile che mi permette di leggere il file attraverso il metodo "read_my_file"

        #print("Dati grezzi dal file:", my_data_file)

        data = self.check_data_file(my_data_file)       #variabile che mi permette di fare tutti i controlli dei dati presenti nel file attravero il metodo "check_data_file"

        #print("Dati validi filtrati:", data)

        self.check_order(data)          #metodo che mi permette di controllare se le date presenti nel file sono ordinate o che non contengano duplicati

        return data

    def open_my_file(self):
        try:
            open_my_file = open(self.name)
        except:
            raise ExamException("Impossibile aprire il file")
        return open_my_file

    def read_my_file(self, reader_my_file):
        try:
            data = reader_my_file.read()
        except:
            raise ExamException("Impossibile leggere il file")
        return data.split("\n")         #metodo che consente di generare una lista di stringhe dove ogni stringa è una riga del file

    def check_data_file(self, my_data):
        date_list = []      #inizializzo una lista vuota "date_list" che mi consente di memorizzare i dati validi

        for item in my_data:
            # Divide la riga in componenti basandosi sulla virgola
            data_split = item.split(',') # Limita la divisione ai primi due campi

            # Assicurati che ci siano almeno due campi (data e passeggeri)
            if len(data_split) < 2:
                continue  # Ignora le righe che non hanno almeno due campi

            valid_data = True
            date_str = data_split[0].strip()  # Rimuove spazi bianchi all'inizio e alla fine
            passenger_str = data_split[1].strip()  # Rimuove spazi bianchi all'inizio e alla fine

            # Prova a convertire il numero di passeggeri in intero e verifica che non sia negativo
            try:
                n_passenger = int(passenger_str.split()[0]) #la stringa "passenger_str" viene divisa e prendo solo il primo valore della lista
                if n_passenger < 0:
                    valid_data = False
            except:
                valid_data = False
                
                 

            # Controlla il formato della data e valida l'anno e il mese
            if "-" in date_str:                     #controlla se è presente il - in date_str che è obbligatorio che ci sia
                date_parts = date_str.split("-")    #divido in una sottolista in modo da avere l'anno nell'indice[0] e il mese nell'indice [1]
                if len(date_parts) != 2:            #condizione che mi verifica che la lista della data sia uguale a 2
                    valid_data = False  # Formato della data non corretto
                else:
                    year, month = date_parts  #assegno la variabile year per il primo indice e month per il secondo indice della lista date_parts
                    try:
                        #int_year = int(year)         
                        int_month = int(month)      

                        if not (1 <= int_month <= 12):
                            valid_data = False
                        
                    except:
                        valid_data = False  # mese non è un intero valido
            else:
                valid_data = False  # Formato della data non corretto

            # Se i dati sono validi, aggiungi alla lista finale
            if valid_data:
                date_list.append([date_str, n_passenger])

        return date_list

    def check_order(self, data):

        if not (len(data) < 2):     #controlla quanti elementi contiene la lista se è minore di 2 il controllo non viene fatto
            date = data[0][0]      #inizializza la variabile date con la prima data della lista
            
            for item in data[1:]:   #inizio del ciclo che itera su tutti gli elementi di data a partire dal secondo elemento presente sulla lista fino all'ultimo
                
                if item[0] <= date:     #controllo se la data è minore o uguale a quella precedente se si alzo l'eccezione (item[0] è l'anno)
                    raise ExamException("Errore: date non ordinate o con duplicati")
                date = item[0]          #eseguo lo scambio


def detect_similar_monthly_variations(time_series, years):

    try:                        # provo a convertire l'input in una lista  
        years = list(years)
    except:
        raise ExamException("Errore: dati non confromi")

    if years[0] >= years[1]:
        raise ExamException("Errore: dati non conformi")


    years_in_data = list([item[0].split("-")[0] for item in time_series])       #prendo tutti gli anni presenti in time_series e li metto all'interno di una lista
    if str(years[0]) not in years_in_data or str(years[1]) not in years_in_data:
        raise ExamException("Errore: uno o entrambi gli anni non sono presenti nei dati")

    lista_first_year = []
    lista_second_year = []

    for i in range(len(time_series)):
        if time_series[i][0].split("-")[0] == str(years[0]):
            lista_first_year.append(time_series[i][1])          #inserisco all'interno di lista_first_year il numero di passeggeri
        elif time_series[i][0].split("-")[0] == str(years[1]):
            lista_second_year.append(time_series[i][1])

    #print(lista_first_year)
    #print(lista_second_year)


    difference_list_first_year = []

    for i in range(len(lista_first_year) - 1):
        difference_list_first_year.append(
            abs(lista_first_year[i] - lista_first_year[i + 1])
        )

    #print(difference_list_first_year)

    difference_list_second_year = []

    for i in range(len(lista_first_year) - 1):
        difference_list_second_year.append(
            abs(lista_second_year[i] - lista_second_year[i + 1])
        )

    #print(difference_list_second_year)

    year_difference = []

    for i in range(len(difference_list_first_year)):
        year_difference.append(
            abs(difference_list_first_year[i] - difference_list_second_year[i])
        )

    #print(year_difference)

    out = []

    for i in range(len(year_difference)):
        if year_difference[i] > 2:
            out.append(False)
        else:
            out.append(True)

    return out


#mio_file = CSVTimeSeriesFile(my_file="data.csv")
#print('Nome del file: "{}"'.format(mio_file.name))
#print('Dati contenuti nel file: "{}"'.format(mio_file.get_data()))
#print(detect_similar_monthly_variations(mio_file.get_data(), years=[1949, 1950]))

