import copy
from nodi_percorsi_vicini_corti import *
from funzione_obiettivo import *
from utils import timeit
import random

@timeit
def subsequent_nearest_neighbour_randomized(G, residui_dict, delta, k, seed=None):
    """
    Algoritmo Greedy Randomizzato.
    Parte dalla scuola. Seleziona casualmente un nodo tra i massimo k ad essa più vicini.
    Successivamente prosegue individuando casualmente un nodo tra i massimo k ad essa più vicini al nodo corrente, 
    che è inseribile nello stesso percorso del nodo corrente, successivamente ad esso.
    Quando non esiste un nodo ammissibile termina il percorso.
    Si riparte con un nuovo percorso dalla scuola ripetendo il procedimento.


    Args:
        G: Il grafo che rappresenta l'istanza del problema.
        residui_dict: Il dizionario dei residui attuali per ogni nodo.
        delta: Il fattore di tolleranza.
        k: Il numero di nodi più vicini da considerare.
        seed: Il seed per la riproducibilità.

    Returns:
        Una tupla contenente:
            - percorsi: Una lista di percorsi, dove ogni percorso è una lista di nodi.
            - obj_val: Il valore della funzione obiettivo (numero di percorsi).
    """

    residui_dict_copy = copy.deepcopy(residui_dict)
    percorsi = []  
    visited_nodes = set()  # Inizializza un set vuoto per memorizzare i nodi visitati.

    current_node = 'Scuola'  
    percorso = [current_node]  

    # Impostare un seed fisso per la riproducibilità
    if seed is not None:
        random.seed(seed)
    else:
        random.seed() 

    # Continua finché ci sono nodi non visitati.
    while len(visited_nodes) < len(G.nodes()) - 1:  # Escludi la scuola dal conteggio.
        # Trova i k nodi più vicini non visitati e ammissibili.
        k_nearest_nodes = k_nearest_neighbours(G, current_node, percorso, visited_nodes, k, delta)

        # Se non ci sono più nodi validi, crea un nuovo percorso.
        if not k_nearest_nodes:
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
        current_node = node  # Aggiorna il nodo corrente al nodo selezionato.

    # Aggiungi l'ultimo percorso se non è vuoto (contiene più di un nodo).
    if len(percorso) > 1:  
        percorsi.append(percorso)  

   
    obj_val = objective_function(percorsi,G)

    return percorsi, obj_val, residui_dict_copy









@timeit
def school_nearest_neighbour_randomized(G, residui_dict, delta, k, seed=None):
    """
    Ordina i bambini in base alla distanza dalla scuola.
    Parte dal bambino più vicino creando un nuovo percorso.
    Prova ad aggiungere gli altri bambini a quel percorso,
    quando un nuovo nodo non è ammissibile, crea un nuovo percorso.
    Se si hanno più percorsi, prima di creare un nuovo percorso,
    un bambino prova ad essere assegnato al percorso 'aperto' con il nodo finale più vicino ammissibile.
    Se non è possibile inserire il nodo in coda ad alcun percorso 
    iniziato, si procede a creare un nuovo percorso.

    Args:
        G: Il grafo che rappresenta l'istanza del problema.
        delta: Il fattore di tolleranza per la lunghezza del percorso.
        k: Il numero di vicini da considerare nella greedy randomizzata.
        seed: Il seed per la riproducibilità.

    Returns:
        Una tupla contenente:
            - percorsi: Una lista di percorsi, dove ogni percorso è una lista di nodi.
            - obj_val: Il valore della funzione obiettivo (numero di percorsi).
    """

    # Impostare un seed fisso per la riproducibilità
    if seed is not None:
        random.seed(seed)
    else:
        random.seed() 

    residui_dict_copy = copy.deepcopy(residui_dict)
    percorsi = []  
    visited_nodes = set()  # Set per tenere traccia dei nodi già visitati

    # Ordina i nodi in base alla distanza dalla scuola (eccetto la scuola stessa)
    sorted_nodes = sorted(G.nodes(), key=lambda x: G[x]['Scuola']['weight'] if x != 'Scuola' else float('inf'))

    # Inizia creando il primo percorso che parte dalla scuola
    percorso = ['Scuola']
    percorsi.append(percorso)  

    # Itera sui nodi (eccetto la scuola)
    for node in sorted_nodes:
        if node != 'Scuola' and node not in visited_nodes:
            # Trova i k nodi più vicini non visitati e ammissibili
            nearest_k_percorsi = find_k_nearest_percorsi(G, node, percorsi, k, delta)
            
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

    obj_val = objective_function(percorsi,G)

    return percorsi, obj_val, residui_dict_copy  