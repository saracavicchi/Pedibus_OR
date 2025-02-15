import copy
from nodi_percorsi_vicini_corti import *
from funzione_obiettivo import *
from utils import timeit
from controlli_ammissibilita import *

@timeit
def subsequent_nearest_neighbour(G, residui_dict, delta):
    """
    Algoritmo Greedy.
    Parte dalla scuola. Seleziona il nodo ad essa più vicino.
    Successivamente prosegue individuando il nodo più vicino al nodo corrente, che è inseribile nello
    stesso percorso del nodo corrente, successivamente ad esso.
    Quando non esiste un nodo ammissibile termina il percorso.
    Si riparte con un nuovo percorso dalla scuola ripetendo il procedimento.


    Args:
        G: Il grafo che rappresenta l'istanza del problema.
        residui_dict: Il dizionario dei residui attuali per ogni nodo.
        delta: Il fattore di tolleranza.

    Returns:
        Una tupla contenente:
            - percorsi: Una lista di percorsi, dove ogni percorso è una lista di nodi.
            - obj_val: Il valore della funzione obiettivo (numero di percorsi).
    """

    residui_dict_copy = copy.deepcopy(residui_dict)
    percorsi = []  # Inizializza una lista vuota per memorizzare i percorsi.
    visited_nodes = set()  # Inizializza un set vuoto per memorizzare i nodi visitati.

    current_node = 'Scuola'  
    percorso = [current_node]  # Inizializza il primo percorso con la scuola.

    # Continua finché ci sono nodi non visitati.
    while len(visited_nodes) < len(G.nodes()) - 1:  # Escludi la scuola dal conteggio.

        # Trova il nodo più vicino non visitato ammissibile.
        nearest_node = nearest_neighbour(G, current_node, percorso, visited_nodes, delta)  


        # Se non ci sono più nodi validi, crea un nuovo percorso.
        if nearest_node is None:
            percorsi.append(percorso)  # Aggiungi il percorso corrente alla lista dei percorsi.
            # Reimposta il percorso e il nodo corrente alla scuola per iniziare un nuovo percorso.
            percorso = ['Scuola']
            current_node = 'Scuola'
            continue  

        #Aggiorna residuo nodo
        residuo = calcola_residuo(G, nearest_node, percorso, delta)
        residui_dict_copy[nearest_node]= residuo

        percorso.append(nearest_node)  # Aggiungi il nodo al percorso.
        visited_nodes.add(nearest_node)  # Segna il nodo come visitato.
        current_node = nearest_node  # Aggiorna il nodo corrente.

    # Aggiungi l'ultimo percorso se non è vuoto (contiene più di un nodo).
    if len(percorso) > 1:  
        percorsi.append(percorso)  

    obj_val = objective_function(percorsi,G)  

    return percorsi, obj_val, residui_dict_copy 



@timeit
def school_nearest_neighbour(G, residui_dict, delta):
    """
    Ordina i bambini in base alla distanza dalla scuola in senso crescente.
    Per ogni bambino, cerca il percorso esistente il cui ultimo nodo è il più vicino al bambino (in cui il bambino
    può essere inserito in fondo senza superare la tolleranza delta). 
    Se si trova un percorso adatto, il bambino viene aggiunto a tale percorso.
    Se non viene trovato un percorso adatto, crea un nuovo percorso.

    Args:
        G: Il grafo che rappresenta l'istanza del problema.
        delta: Il fattore di tolleranza per la lunghezza del percorso.

    Returns:
        Una tupla contenente:
            - percorsi: Una lista di percorsi, dove ogni percorso è una lista di nodi.
            - obj_val: Il valore della funzione obiettivo (numero di percorsi).
    """
    residui_dict_copy = copy.deepcopy(residui_dict)
    percorsi = []  
    visited_nodes = set()  

    current_node = 'Scuola'  
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

    obj_val = objective_function(percorsi,G)

    return percorsi, obj_val, residui_dict_copy 