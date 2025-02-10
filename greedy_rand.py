import copy
from nodi_percorsi_vicini_corti import *
from funzione_obiettivo import *
from utils import timeit
import random

@timeit
def subsequent_nearest_neighbour_randomized(G, residui_dict, delta, k, seed=None):
    """
    Funzione per trovare percorsi utilizzando l'algoritmo del nearest neighbour,
    partendo dalla scuola e rispettando un vincolo delta.
    RANDOMIZED:
    Invece di scegliere il più vicino, scelgo a caso tra i k più vicini

    Args:
        G: Il grafo che rappresenta l'istanza del problema.
        delta: Il fattore di tolleranza per la lunghezza del percorso.
        k: Il numero di vicini più vicini da considerare per la selezione casuale.

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

    # Impostare un seed fisso per la riproducibilità
    if seed is not None:
        random.seed(seed)
    else:
        random.seed() 

    # Continua finché ci sono nodi non visitati.
    while len(visited_nodes) < len(G.nodes()) - 1:  # Escludi la scuola dal conteggio.
        #print(f"Nodi visitati: {visited_nodes}")  # Stampa di debug (commentata).
        # Trova i k nodi più vicini non visitati e ammissibili.
        k_nearest_nodes = k_nearest_neighbours(G, current_node, percorso, visited_nodes, k, delta)


        # Se non ci sono più nodi validi, crea un nuovo percorso.
        if not k_nearest_nodes:
            #print("Nessun nodo valido, creando un nuovo percorso.")  # Stampa di debug (commentata).
            percorsi.append(percorso)  # Aggiungi il percorso corrente alla lista dei percorsi.
            # Reimposta il percorso e il nodo corrente alla scuola per iniziare un nuovo percorso.
            percorso = ['Scuola']
            current_node = 'Scuola'
            continue  # Salta all'iterazione successiva del ciclo.



        # Seleziona casualmente un nodo tra i k nodi più vicini.
        node = random.choice(k_nearest_nodes)
        #Aggiorna residuo nodo
        residuo = calcola_residuo(G, node, percorso, delta)
        residui_dict_copy[node]= residuo
        percorso.append(node)  # Aggiungi il nodo selezionato al percorso.
        visited_nodes.add(node)  # Segna il nodo come visitato.
        #print(f"Nodo inserito: {node}, Percorso: {percorso}")  # Stampa di debug (commentata).
        current_node = node  # Aggiorna il nodo corrente al nodo selezionato.

    # Aggiungi l'ultimo percorso se non è vuoto (contiene più di un nodo).
    if len(percorso) > 1:  # Se c'è un percorso reale oltre alla scuola.
        percorsi.append(percorso)  # Aggiungi il percorso alla lista dei percorsi.

    #obj_val = objective_function(percorsi)  # Calcola il valore della funzione obiettivo.
    obj_val = objective_function(percorsi,G)

    return percorsi, obj_val, residui_dict_copy # Restituisci i percorsi e il valore della funzione obiettivo.



@timeit
def school_nearest_neighbour_randomized(G, residui_dict, delta, k):
    """
    Ordina i bambini in base alla distanza dalla scuola.
    Parte dal bambino più vicino creando un nuovo percorso.
    Prova ad aggiungere gli altri bambini a quel percorso,
    quando un nuovo nodo non è ammissibile, crea un nuovo percorso.
    Se si hanno più percorsi, prima di creare un nuovo percorso,
    un bambino prova ad essere assegnato CASUALMENTE ad uno dei percorsi con
    i k percorsi finali più vicini.
    Se l'assegnamento non è ammissibile, si procede a creare un nuovo percorso.
    """
    residui_dict_copy = copy.deepcopy(residui_dict)
    percorsi = []  # Lista per memorizzare i percorsi
    visited_nodes = set()  # Set per tenere traccia dei nodi già visitati

    # Ordina i nodi in base alla distanza dalla scuola (eccetto la scuola stessa)
    sorted_nodes = sorted(G.nodes(), key=lambda x: G[x]['Scuola']['weight'] if x != 'Scuola' else float('inf'))

    # Inizia creando il primo percorso che parte dalla scuola
    percorso = ['Scuola']
    percorsi.append(percorso)  # Aggiungi il primo percorso alla lista dei percorsi

    # Impostare un seed fisso per la riproducibilità
    #random.seed(42)

    # Itera sui nodi (eccetto la scuola)
    for node in sorted_nodes:
        if node != 'Scuola' and node not in visited_nodes:
            nearest_k_percorsi = find_k_nearest_percorsi(G, node, percorsi, k, delta)
            #print(f"Percorsi piu vicini {nearest_k_percorsi}")
            # Se non ci sono percorsi validi, crea un nuovo percorso
            if not nearest_k_percorsi:
                nuovo_percorso = ['Scuola']  # Crea un nuovo percorso
                percorsi.append(nuovo_percorso)
                nuovo_percorso.append(node)  # Aggiungi il nodo al nuovo percorso
                visited_nodes.add(node)  # Segna il nodo come visitato
                continue  # Vai al prossimo nodo

            # Se ci sono percorsi validi, scegli uno dei percorsi migliori casualmente
            percorso = random.choice(nearest_k_percorsi)
            #Aggiorna residuo nodo
            residuo = calcola_residuo(G, node, percorso, delta)
            residui_dict_copy[node] = residuo
            percorso.append(node)  # Aggiungi il nodo al percorso
            visited_nodes.add(node)  # Segna il nodo come visitato


    # Calcola il valore della funzione obiettivo (ad esempio, minimizzare il numero di percorsi)
    #obj_val = objective_function(percorsi)
    obj_val = objective_function(percorsi,G)

    return percorsi, obj_val, residui_dict_copy  # Restituisci i percorsi e il valore della funzione obiettivo