import copy
from nodi_percorsi_vicini_corti import *


def check_solution(percorsi, G, delta):
    """
    Verifica se la soluzione proposta è corretta, ossia:
    - Tutti i percorsi rispettano il vincolo della distanza espresso da delta.
    - Ogni nodo (eccetto la scuola) appare esattamente in un percorso.
    - La scuola appare in ogni percorso.
    """
    nodes_visited = set()  # Set per tracciare i nodi visitati
    errors = []  # Lista per accumulare errori

    # Itera su tutti i percorsi
    for idx, p in enumerate(percorsi):
        # Verifica che il percorso contenga la scuola
        if 'Scuola' not in p:
            errors.append(f"Errore: La scuola manca nel percorso {idx}.")

        # Aggiungi i nodi visitati, verificando duplicati
        for node in p:
            if node == 'Scuola':
                continue  # La scuola può comparire più volte
            if node in nodes_visited:
                errors.append(f"Errore: Il nodo {node} appare più di una volta (nel percorso {idx+1}).")
            nodes_visited.add(node)

        # Verifica la fattibilità del percorso
        if not test_percorso_feasibility(p, G, delta):
            errors.append(f"Errore: Il percorso {idx+1} non rispetta il vincolo di distanza.")


    # Verifica che tutti i nodi (eccetto la scuola) siano stati visitati
    for node in G.nodes():
        if node != 'Scuola' and node not in nodes_visited:
            errors.append(f"Errore: Il nodo {node} non è stato visitato.")

    # Verifica che il numero totale di nodi visitati sia corretto
    total_visited_nodes = len(nodes_visited) + 1  # Include la scuola
    if total_visited_nodes != len(G.nodes()):
        errors.append("Errore: Il numero di nodi visitati è errato.")

    # Stampa gli errori o conferma la validità della soluzione
    if errors:
        print("Soluzione non ammissibile. Dettagli degli errori:")
        for error in errors:
            print(f" - {error}")
        return False
    else:
        print("Soluzione ammissibile.")
        return True


def test_percorso_feasibility(percorso, G, delta):
    """
    Verifica se il percorso è ammissibile.
    La distanza totale per ogni nodo non deve eccedere delta volte la distanza minima
    tra il nodo e la scuola.

    Args:
        percorso: Lista di nodi nel percorso (da casa a scuola).
        G: Grafo con i pesi degli archi.
        delta: Fattore massimo di distanza rispetto alla distanza minima alla scuola.

    Returns:
        True se il percorso è ammissibile, False altrimenti.
    """
    if len(percorso) <= 1:
        return False  # Un percorso deve avere almeno un bambino e la scuola

    if len(percorso) == 2:
        return True  # Un percorso diretto casa-scuola è sempre ammissibile

    distanza_accumulata = 0  # Distanza totale percorsa lungo il percorso

    # Itera sui nodi del percorso, calcolando la distanza percorsa fino alla scuola
    for i in range(len(percorso) - 1):
        distanza_accumulata += G[percorso[i]][percorso[i+1]]['weight']

        # Verifica il vincolo di ammissibilità per il nodo i
        if distanza_accumulata > G.nodes[percorso[i+1]]['max_distance']:

            return False  # Il percorso non è ammissibile

    return True  # Se nessuna violazione è stata trovata, il percorso è valido



def test_node_in_percorso_feasibility(G, node, percorso, delta):
    """
    Verifica se un nodo può essere inserito in un percorso esistente, rispettando i vincoli.
    Ritorna la prima posizione trovata in cui il nodo può essere inserito oppure -1 se non è possibile.
    """
    # Verifica se il nodo può essere aggiunto alla fine del percorso
    if test_node_feasibility(G, node, percorso, delta):
        return len(percorso)  # Posizione finale

    # Verifica se il nodo può essere inserito in altre posizioni
    for i in range(len(percorso)-1): #itero fino al penultimo
        if i > 0:
          percorso_temp = percorso[:i] + [node] + percorso[i:]  # Inserisce il nodo in posizione i
          if test_percorso_feasibility(percorso_temp, G, delta):
              return i  # Ritorna la prima posizione valida

    # Nessuna posizione valida trovata
    return -1


def test_node_feasibility(G, node, percorso, delta):
    """
    Verifica se l'aggiunta di un nodo alla fine di un percorso è ammissibile,
    considerando il vincolo di lunghezza del percorso definito da delta.

    Restituisce True o False
    """

    # Se il percorso contiene solo la scuola, è sempre ammissibile
    if len(percorso) == 1:
        return True
    else:
      dist = somma_dist_percorso(G, percorso)
      final_node = percorso[-1]
      if G.nodes[node]['max_distance'] >= dist + G[final_node][node]['weight']:
        return True
      else:
        return False

import copy

def test_node_pos_k_feasibility(G, residui_dict, node, percorso, delta, k):
    """
    Verifica se l'aggiunta di un nodo alla k-esima posizione di un percorso è ammissibile,
    considerando il vincolo di lunghezza del percorso definito da delta.

    Args:
        G: Il grafo che rappresenta l'istanza del problema.
        residui_dict: Il dizionario che contiene i residui di ciascun nodo.
        node: Il nodo che si sta considerando di aggiungere al percorso.
        percorso: Il percorso corrente (con la scuola sempre in posizione 0).
        delta: Il fattore di tolleranza per la lunghezza del percorso.
        k: La posizione in cui si vuole aggiungere il nodo (k >= 1).

    Returns:
        - None se il nodo non è inseribile in posizione k.
        - La somma dei residui del percorso e il residuo del nodo se è inseribile.
    """
    residui_dict_copy = copy.deepcopy(residui_dict)

    # === CASO 1: INSERIMENTO IN ULTIMA POSIZIONE ===
    if k == -1 or k >= len(percorso):
        percorso_test = copy.deepcopy(percorso)
        if test_node_feasibility(G, node, percorso_test, delta):
            residuo_node = G.nodes[node]['max_distance'] - (somma_dist_percorso(G, percorso_test) + G[percorso_test[-1]][node]['weight'])
            return somma_residui_percorso(residui_dict_copy, percorso_test) + residuo_node, residuo_node
        return None

    # === CASO 2: INSERIMENTO IN UNA POSIZIONE SPECIFICA ===
    if k >= 1:  # k = 1 è il nodo più vicino alla scuola

        # Calcola la distanza aggiuntiva per i nodi successivi
        dist_aggiuntiva = G[percorso[k-1]][node]['weight'] + G[node][percorso[k]]['weight'] - G[percorso[k-1]][percorso[k]]['weight']

        percorso_test = percorso[:k] + [node] + percorso[k:]  # Crea il percorso di test con il nodo inserito

        # Calcola la distanza accumulata fino al nodo inserito
        somma_dist_vic_scuola = somma_dist_percorso(G, percorso_test[:k+1])

        # Verifica il vincolo di distanza massima
        if somma_dist_vic_scuola > G.nodes[node]['max_distance']:
            return None


        # Verifica che i nodi successivi abbiano abbastanza residuo
        valid = True
        for i in range(k, len(percorso_test)):  # Controlliamo a partire da `k`
            if residui_dict_copy[percorso_test[i]] < dist_aggiuntiva:
                valid = False
                break

        # Se la condizione non è rispettata, il nodo non può essere inserito
        if not valid:
            return None

        # Calcola il residuo del nodo
        residuo_node = G.nodes[node]['max_distance'] - somma_dist_vic_scuola

        # Solo ora restituiamo il risultato
        return somma_residui_percorso(residui_dict_copy, percorso_test), residuo_node

    # === CASO 3: POSIZIONE K NON VALIDA ===
    return None


def test_node_in_percorso_best_pos_feasibility(G,residui_dict, node, percorso, delta):
    """
    Verifica se 'node' può essere inserito in 'percorso', rispettando i vincoli.
    Ritorna la MIGLIOR posizione in cui il nodo può essere inserito
    e il residuo del nodo se fosse spostato nel percorso oppure None se non è possibile.
    Migliore nel senso che va a massimizzare la somma dei residui del percorso
    """

    max_residui_percorso = float('-inf')
    best_pos = None
    best_residuo = -1

    residui_dict_copy = copy.deepcopy(residui_dict)

    for k in range(1, len(percorso)):

      pos = test_node_pos_k_feasibility(G, residui_dict_copy, node, percorso, delta, k)
      if pos != None:
        residui_percorso_con_node, residuo_node = pos
        if residui_percorso_con_node > max_residui_percorso:
          max_residui_percorso = residui_percorso_con_node
          best_pos = k
          best_residuo = residuo_node
      else:
        continue

    if best_pos is not None:
        return best_pos, best_residuo
    else:
        return None



