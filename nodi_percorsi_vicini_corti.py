import copy
from controlli_ammissibilita import *

def somma_residui_percorso(residui_dict, percorso):
  """
  Restituisce la somma dei residui (della distanza massima che ciascun bambino
  può ancora percorrere) per i nodi del percorso
  """

  tot_sum = sum(residui_dict[nodo]for nodo in percorso if nodo != 'Scuola')
  return tot_sum

def calcola_residuo(G, nodo, percorso, delta):
  """
  Calcola il residuo del nodo se fosse inserito inserito alla FINE di
  un percorso

  Restituisce il residuo del nodo se fosse inserito alla FINE di un percorso
  """
  dist = somma_dist_percorso(G, percorso) + G[percorso[-1]][nodo]['weight']


  return G.nodes[nodo]['max_distance'] - dist



def calcola_residui_nodi_percorso(G, residui_dict, percorso, delta):
  """
  Aggiorna il residuo di ogni nodo del percorso
  """
  residui_dict_copy = copy.deepcopy(residui_dict)

  for i, nodo in enumerate(percorso):
    if nodo == "Scuola":
      continue

    residuo = calcola_residuo(G, nodo, percorso[:i], delta)
    residui_dict_copy[nodo] = residuo

  return residui_dict_copy

def somma_dist_percorso(G, percorso):
  """
  Restituisce la somma delle distanze dei nodi del percorso
  """
  tot_sum = 0
  for i in range( len(percorso) - 1):
    if G.has_edge(percorso[i], percorso[i + 1]):
        tot_sum += G[percorso[i]][percorso[i + 1]]['weight']
    else:
      print(f"Warning: Arco tra {percorso[i]} e {percorso[i + 1]} mancante.")
      return -1
  return tot_sum

def find_nearest_node(G, node, percorsi):
  """
  Trova il nodo più vicino al nodo node (non node stesso o scuola)

  Restituisce il nodo più vicino e il percorso (indice del percorso) in cui si trova
  """
  min_dist = float('inf')
  nearest_node = None
  nearest_percorso = None

  for percorso,i in enumerate(percorsi):
    if node in percorso:
      continue
    for nodo in percorso:
      if nodo == node or nodo == "Scuola":
        continue
      dist = G[nodo][node]['weight']
      if dist < min_dist:
        min_dist = dist
        nearest_node = nodo
        nearest_percorso = i
  return nearest_node, i

import heapq

def find_k_nearest_node(G, node, percorsi, k):
    """
    Trova i k nodi più vicini IN PERCORSI DIVERSI al nodo `node` (escludendo `node` stesso, "Scuola").

    Restituisce:
    - Una lista dei k nodi più vicini e i percorsi (indici dei percorsi) in cui si trovano.
    """
    max_heap = []

    for i, percorso in enumerate(percorsi):
        if node in percorso:
            continue
        for nodo in percorso:
            if nodo == node or nodo == "Scuola":
                continue

            dist = G[nodo][node]['weight']
            # Aggiunge il nodo e la sua distanza (negativa) all'heap
            heapq.heappush(max_heap, (-dist, nodo, i))

            # Mantiene solo i k nodi più vicini
            if len(max_heap) > k:
                heapq.heappop(max_heap)

    # Ritorna i nodi più vicini con i loro percorsi
    return [[nodo, i] for dist, nodo, i in max_heap]


def nearest_neighbour(G, start, percorso, visited_nodes, delta):
    """
    Trova il nodo più vicino al nodo di partenza 'start' tra quelli non ancora visitati,
    escludendo la scuola e il nodo di partenza stesso.

    Args:
        G: Il grafo in cui cercare il nodo più vicino.
        start: Il nodo di partenza per cui cercare il vicino.
        visited_nodes: Un insieme di nodi che sono già stati visitati.

    Returns:
        Il nodo più vicino a 'start' che non è stato ancora visitato,
        o None se non ci sono nodi validi.
    """
    # Inizializza la distanza minima a infinito
    min_distance = float('inf')
    # Inizializza il nodo più vicino a None
    nearest_node = None

    # Itera attraverso tutti i nodi nel grafo
    for node in G.nodes():
        # Controlla se il nodo soddisfa le seguenti condizioni:
        # 1. Non è stato ancora visitato (non è in visited_nodes)
        # 2. Non è il nodo di partenza stesso (node != start)
        # 3. Non è la scuola (node != 'Scuola')
        # 4. Esiste un arco tra il nodo di partenza e il nodo corrente (G.has_edge(start, node))
        if node not in visited_nodes and node != start and node != 'Scuola' and G.has_edge(start, node):
            if not test_node_feasibility(G, node, percorso, delta):
              continue
            # Ottiene la distanza tra il nodo di partenza e il nodo corrente
            distance = G[start][node]['weight']

            # Se la distanza corrente è minore della distanza minima trovata finora
            if distance < min_distance:
                # Aggiorna la distanza minima e il nodo più vicino
                min_distance = distance
                nearest_node = node
    # Restituisce il nodo più vicino trovato
    return nearest_node

import heapq  # Importa il modulo heapq per utilizzare le funzionalità di heap

def k_nearest_neighbours(G, start, percorso, visited_nodes, k, delta):
    """
    Trova i massimo k nodi più vicini al nodo di partenza 'start' tra quelli non
    ancora visitati, considerando i vincoli di ammissibilità del percorso e il
    parametro delta.

    Args:
        G: Il grafo in cui cercare i nodi più vicini.
        start: Il nodo di partenza per cui cercare i vicini.
        percorso: Il percorso corrente a cui si sta cercando di aggiungere un nodo.
        visited_nodes: Un insieme di nodi che sono già stati visitati.
        k: Il numero di nodi più vicini da restituire.
        delta: Il fattore di tolleranza per la lunghezza del percorso.

    Returns:
        Una lista dei massimo k nodi più vicini a 'start' che soddisfano i vincoli.
    """
    # Inizializza un heap massimo (usando valori di distanza negativi)
    # per memorizzare i k nodi più vicini
    max_heap = []

    # Itera attraverso tutti i nodi nel grafo
    for node in G.nodes:
        # Controlla se il nodo è valido: non visitato, diverso dal nodo di partenza,
        # diverso dalla scuola e connesso al nodo di partenza
        if node not in visited_nodes and node != start and node != 'Scuola' and G.has_edge(start, node):
            # Ottiene la distanza tra il nodo di partenza e il nodo corrente
            distance = G[start][node]['weight']

            # Controlla se l'aggiunta del nodo al percorso rispetta i vincoli di ammissibilità
            # utilizzando la funzione test_node_feasibility (non definita in questo snippet)
            if not test_node_feasibility(G, node, percorso, delta):
                continue  # Se il nodo non è ammissibile, passa al nodo successivo

            # Aggiunge il nodo e la sua distanza (negativa) all'heap
            heapq.heappush(max_heap, (-distance, node))

            # Se l'heap contiene più di k elementi, rimuove l'elemento con la distanza massima
            # (che corrisponde al nodo più lontano) per mantenere solo i k nodi più vicini
            if len(max_heap) > k:
                heapq.heappop(max_heap)

    # Restituisce una lista contenente solo i nodi dall'heap,
    # che sono già ordinati in base alla distanza grazie alle proprietà dell'heap
    return [node for dist, node in max_heap]

def find_nearest_percorso(G, node, percorsi, delta):
    """
    Trova il percorso il cui nodo finale è più vicino al nodo specificato,
    tale da garantire comunque l'ammissibilità (ossia in modo che se si aggiunge
    'node' alla fine del percorso il percorso resta ammissibile: node non compie
    più di delta volte la sua distanza minima dalla scuola).

    Args:
        G: Il grafo che rappresenta l'istanza del problema.
        node: Il nodo (bambino) per il quale si cercano i percorsi più vicini.
        percorsi: Una lista di percorsi esistenti.
        delta: Il fattore di tolleranza per la lunghezza del percorso.

    Returns:
        lista di al massimo k percorsi più vicini al nodo specificato che
        soddisfano il vincolo di ammissibilità, oppure None se non viene trovato
        alcun percorso adatto.
    """
    nearest_percorso = None  # Inizializza il percorso più vicino a None.
    min_distance = float('inf')  # Inizializza la distanza minima a infinito.

    # Itera attraverso ogni percorso nella lista dei percorsi.
    for percorso in percorsi:
        last_node = percorso[-1]  # Ottiene l'ultimo nodo del percorso corrente.
        # Calcola la distanza tra l'ultimo nodo del percorso e il nodo specificato.
        distance = G[last_node][node]['weight']
        # Se la distanza corrente è minore della distanza minima trovata finora:
        if distance <= min_distance:
            # Verifica se l'aggiunta del nodo al percorso corrente è ammissibile.
            if test_node_feasibility(G, node, percorso, delta):
                # Se è ammissibile, aggiorna la distanza minima e il percorso più vicino.
                min_distance = distance
                nearest_percorso = percorso

    # Restituisci il percorso più vicino trovato (o None se non è stato trovato alcun percorso adatto).
    return nearest_percorso

import heapq

def find_k_nearest_percorsi(G, node, percorsi, k, delta):
    """
    Trova fino a k percorsi il cui nodo finale è il più vicino al nodo specificato,
    tale da garantire comunque l'ammissibilità. (ossia in modo che se si aggiunge
    'node' alla fine del percorso il percorso resta ammissibile: node non compie
    più di delta volte la sua distanza minima dalla scuola).

    Args:
        G: Il grafo che rappresenta l'istanza del problema.
        node: Il nodo (bambino) per il quale si cerca il percorso più vicino.
        percorsi: Una lista di percorsi esistenti.
        k: Il numero massimo di percorsi da restituire.
        delta: Il fattore di tolleranza per la lunghezza del percorso.

    Returns:
        Una lista dei k percorsi più vicini al nodo specificato che soddisfano il vincolo di ammissibilità,
        oppure una lista vuota se non vengono trovati percorsi validi.
    """

    # Inizializza un heap massimo (usando valori di distanza negativi)
    max_heap = []

    for percorso in percorsi:
        last_node = percorso[-1]  # Ottiene l'ultimo nodo del percorso corrente.

        # Verifica l'ammissibilità del percorso con il nuovo nodo
        if not test_node_feasibility(G, node, percorso, delta):
            continue  # Se il nodo non è ammissibile, passa al nodo successivo

        # Calcola la distanza tra l'ultimo nodo del percorso e il nodo specificato.
        distance = G[last_node][node]['weight']

        # Aggiunge il nodo e la sua distanza (negativa per fare il max-heap) all'heap
        heapq.heappush(max_heap, (-distance, percorso))

        # Se l'heap contiene più di k percorsi, rimuove quello con la maggiore distanza
        if len(max_heap) > k:
            heapq.heappop(max_heap)

    # Restituisce i percorsi ordinati per distanza, da quello più vicino a quello più lontano
    return [percorso for dist, percorso in sorted(max_heap, reverse=True)]

import heapq

def k_shortest_percorsi(percorsi, k):
  """
  Restituisce i k percorsi più corti
  """
  heap = []
  for i, percorso in enumerate(percorsi):
    heapq.heappush(heap, (somma_dist_percorso(percorso), i))
    if len(heap) > k:
      heapq.heappop(heap)

  return [i for _, i in sorted(heap, key=lambda x: x[0])]