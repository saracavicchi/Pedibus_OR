import copy
from nodi_percorsi_vicini_corti import *
from funzione_obiettivo import *
from utils import timeit
from controlli_ammissibilita import *

@timeit
def subsequent_nearest_neighbour(G, residui_dict, delta):
    """
    Funzione per trovare percorsi utilizzando l'algoritmo del nearest neighbour,
    partendo dalla scuola e rispettando un vincolo delta.
    Parte dalla scuola. Seleziona il nodo ad essa più vicino.
    Successivamente prosegue individuando per il nodo corrente il nodo
    ad esso più vicino, quando il nodo non rispetta il limite sul suo percorso,
    si riparte con un nuovo percorso dalla scuola con il primo nodo ad essa
    più vicino ancora libero.


    Args:
        G: Il grafo che rappresenta l'istanza del problema.
        delta: Il fattore di tolleranza per la lunghezza del percorso.

    Returns:
        Una tupla contenente:
            - percorsi: Una lista di percorsi, dove ogni percorso è una lista di nodi.
            - obj_val: Il valore della funzione obiettivo (numero di percorsi).
    """
    residui_dict_copy = copy.deepcopy(residui_dict)
    percorsi = []  # Inizializza una lista vuota per memorizzare i percorsi.
    visited_nodes = set()  # Inizializza un set vuoto per memorizzare i nodi visitati.

    current_node = 'Scuola'  # Inizia dalla scuola.
    percorso = [current_node]  # Inizializza il primo percorso con la scuola.

    # Continua finché ci sono nodi non visitati.
    while len(visited_nodes) < len(G.nodes()) - 1:  # Escludi la scuola dal conteggio.
        #print(f"Nodi visitati: {visited_nodes}")  # Stampa di debug (commentata).
        nearest_node = nearest_neighbour(G, current_node, percorso, visited_nodes, delta)  # Trova il nodo più vicino non visitato.
        #print(f"Nodo corrente: {current_node}, Nodo più vicino: {nearest_node}")  # Stampa di debug (commentata).

        # Se non ci sono più nodi validi, crea un nuovo percorso.
        if nearest_node is None:
            #print("Nessun nodo valido, creando un nuovo percorso.")  # Stampa di debug (commentata).
            percorsi.append(percorso)  # Aggiungi il percorso corrente alla lista dei percorsi.
            # Reimposta il percorso e il nodo corrente alla scuola per iniziare un nuovo percorso.
            percorso = ['Scuola']
            current_node = 'Scuola'
            continue  # Salta all'iterazione successiva del ciclo.


        #Aggiorna residuo nodo
        residuo = calcola_residuo(G, nearest_node, percorso, delta)
        residui_dict_copy[nearest_node]= residuo

        # Se il nodo è ammissibile, aggiungilo al percorso corrente.
        percorso.append(nearest_node)  # Aggiungi il nodo al percorso.
        visited_nodes.add(nearest_node)  # Segna il nodo come visitato.
            #print(f"Nodo inserito: {nearest_node}, Percorso: {percorso}")  # Stampa di debug (commentata).
        current_node = nearest_node  # Aggiorna il nodo corrente.
        #else:
            #print(f"Nodo {nearest_node} non ammissibile, terminando il percorso.")  # Stampa di debug (commentata).
            # Se il nodo non è ammissibile, termina il percorso corrente e inizia uno nuovo.
            #percorsi.append(percorso)  # Aggiungi il percorso corrente alla lista dei percorsi.
            #percorso = ['Scuola']  # Reimposta il percorso alla scuola.
            #current_node = 'Scuola'  # Reimposta il nodo corrente alla scuola.

    # Aggiungi l'ultimo percorso se non è vuoto (contiene più di un nodo).
    if len(percorso) > 1:  # Se c'è un percorso reale oltre alla scuola.
        percorsi.append(percorso)  # Aggiungi il percorso alla lista dei percorsi.

    obj_val = objective_function(percorsi,G)  # Calcola il valore della funzione obiettivo.
    #obj_val = objective_function(percorsi)

    return percorsi, obj_val, residui_dict_copy # Restituisci i percorsi e il valore della funzione obiettivo.



@timeit
def school_nearest_neighbour(G, residui_dict, delta):
    """
    Ordina i bambini in base alla distanza dalla scuola.
    Parte dal bambino più vicino creando un nuovo percorso.
    Prova ad aggiungere gli altri bambini a quel percorso,
    quando un nuovo nodo non è ammissibile, crea un nuovo percorso.
    Se si hanno più percorsi, prima di creare un nuovo percorso,
    un bambino prova ad essere assegnato al percorso con il nodo finale più vicino.
    Se l'assegnamento non è ammissibile, si procede a creare un nuovo percorso.

    Args:
        G: Il grafo che rappresenta l'istanza del problema.
        delta: Il fattore di tolleranza per la lunghezza del percorso.

    Returns:
        Una tupla contenente:
            - percorsi: Una lista di percorsi, dove ogni percorso è una lista di nodi.
            - obj_val: Il valore della funzione obiettivo (numero di percorsi).
    """
    residui_dict_copy = copy.deepcopy(residui_dict)
    percorsi = []  # Inizializza una lista vuota per memorizzare i percorsi.
    visited_nodes = set()  # Inizializza un set vuoto per memorizzare i nodi visitati.

    current_node = 'Scuola'  # Inizia dalla scuola.
    percorso = [current_node]  # Inizializza il primo percorso con la scuola.
    percorsi.append(percorso)  # Aggiungi il primo percorso alla lista dei percorsi

    # Ordina i nodi in base alla distanza dalla scuola (crescente).
    # Usa una funzione lambda come chiave per l'ordinamento,
    # assegnando infinito alla scuola per posizionarla in fondo alla lista.
    sorted_nodes = sorted(G.nodes(), key=lambda x: G[x]['Scuola']['weight'] if x != 'Scuola' else float('inf'))

    # Itera attraverso i nodi ordinati.
    for node in sorted_nodes:
        # Se il nodo non è stato visitato e non è la scuola:
        if node not in visited_nodes and node != 'Scuola':
            # Cerca il percorso esistente il cui ultimo nodo è il più vicino al nodo corrente,
            # garantendo l'ammissibilità.
            nearest_percorso = find_nearest_percorso(G, node, percorsi, delta)

            #print("Percorso piu vicino",nearest_percorso)

            # Se viene trovato un percorso adatto:
            if nearest_percorso:
                #Aggiorna residuo nodo
                residuo = calcola_residuo(G, node, percorso, delta)
                residui_dict_copy[node]= residuo
                nearest_percorso.append(node)  # Aggiungi il nodo al percorso trovato.
                visited_nodes.add(node)  # Segna il nodo come visitato.
            else:
                # Se non viene trovato un percorso adatto, crea un nuovo percorso.
                percorso = ['Scuola']  # Crea un nuovo percorso
                percorsi.append(percorso)
                percorso.append(node)  # Aggiungi il nodo al nuovo percorso
                visited_nodes.add(node)  # Segna il nodo come visitato

    # Aggiungi l'ultimo percorso se non è vuoto (contiene più di un nodo).
    #if len(percorso) > 1:  # Se c'è un percorso reale oltre alla scuola.
      #percorsi.append(percorso)  # Aggiungi il percorso alla lista dei percorsi.

    #obj_val = objective_function(percorsi)  # Calcola il valore della funzione obiettivo.
    obj_val = objective_function(percorsi,G)

    return percorsi, obj_val, residui_dict_copy # Restituisci i percorsi e il valore della funzione obiettivo.