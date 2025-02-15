import copy
from controlli_ammissibilita import *
import heapq

"""def find_nearest_node(G, node, percorsi):
  
  Trova il nodo più vicino al nodo node (non node stesso o scuola)
    Args:
        G: Il grafo in cui cercare il nodo più vicino.
        node: Il nodo per cui cercare il vicino più vicino.
        percorsi: Una lista di percorsi esistenti.
    
    Returns:
        Il nodo più vicino a 'node' che non è stato ancora visitato, l'indice del percorso
        in cui si trova 
  
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
  return nearest_node, nearest_percorso #prima era nearest_node, i
"""



def find_k_nearest_node(G, node, percorsi, k):
    """
    Trova i k nodi più vicini IN PERCORSI DIVERSI rispetto a quello in cui è node
    al nodo `node` (escludendo `node` stesso e "Scuola").

    Args:
        G: Il grafo in cui cercare i nodi più vicini.
        node: Il nodo per cui cercare i vicini.
        percorsi: Una lista di percorsi esistenti.
        k: Il numero di nodi più vicini da restituire.
    
    Returns:
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
            # Aggiunge il nodo e la sua distanza (negativa) all'heap (cosi da usare un heap minimo come heap massimo)
            heapq.heappush(max_heap, (-dist, nodo, i))

            # Mantiene solo i k nodi più vicini
            if len(max_heap) > k:
                heapq.heappop(max_heap)

    # Restituisce i nodi ordinati per distanza, da quello più vicino a quello più lontano
    sorted_nodes = [[node, i] for dist, node, i in sorted(max_heap, reverse=True)]

    return sorted_nodes








def nearest_neighbour(G, start, percorso, visited_nodes, delta):
    """
    Trova il nodo più vicino al nodo di partenza 'start' tra quelli non ancora visitati,
    escludendo la scuola e il nodo di partenza stesso.

    Args:
        G: Il grafo in cui cercare il nodo più vicino.
        start: Il nodo di partenza per cui cercare il vicino.
        percorso: Il percorso corrente a cui si sta cercando di aggiungere un nodo.
        visited_nodes: Un insieme di nodi che sono già stati visitati.

    Returns:
        Il nodo più vicino a 'start' che non è stato ancora visitato,
        o None se non ci sono nodi validi.
    """

    min_distance = float('inf')
    nearest_node = None

    for node in G.nodes():
        if node not in visited_nodes and node != start and node != 'Scuola':
            
            #se non è ammissibile aggiungere node alla fine del percorso passa al nodo successivo
            if not test_node_feasibility(G, node, percorso, delta):
              continue

            # Ottiene la distanza tra il nodo di partenza e il nodo corrente
            distance = G[start][node]['weight']

            if distance < min_distance:
                min_distance = distance
                nearest_node = node
    # Restituisce il nodo più vicino trovato
    return nearest_node






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


    for node in G.nodes:
        if node not in visited_nodes and node != start and node != 'Scuola':
            # Ottiene la distanza tra il nodo di partenza e il nodo corrente
            distance = G[start][node]['weight']

            # Controlla se l'aggiunta del nodo alla fine del percorso non rispetta i vincoli di ammissibilità
            if not test_node_feasibility(G, node, percorso, delta):
                continue  # Se il nodo non è ammissibile, passa al nodo successivo

            # Aggiunge il nodo e la sua distanza (negativa) all'heap
            heapq.heappush(max_heap, (-distance, node))

            # Se l'heap contiene più di k elementi, rimuove l'elemento con la distanza massima
            # (che corrisponde al nodo più lontano) per mantenere solo i k nodi più vicini
            if len(max_heap) > k:
                heapq.heappop(max_heap)

    # Restituisce i nodi ordinati per distanza, da quello più vicino a quello più lontano
    sorted_nodes = [node for dist, node in sorted(max_heap, reverse=True)]

    return sorted_nodes







def find_nearest_percorso(G, node, percorsi, delta):
    """
    Trova il percorso il cui nodo finale è più vicino a node,
    tale da garantire comunque l'ammissibilità (ossia in modo che se si aggiunge
    'node' alla fine del percorso il percorso resta ammissibile: node non compie
    più di delta volte la sua distanza minima dalla scuola).

    Args:
        G: Il grafo che rappresenta l'istanza del problema.
        node: Il nodo (bambino) per il quale si cercano i percorsi più vicini.
        percorsi: Una lista di percorsi esistenti.
        delta: Il fattore di tolleranza.

    Returns:
        Il percorso più vicino a 'node' che soddisfa il vincolo di ammissibilità,
        oppure None se non viene trovato alcun percorso valido
    """
    nearest_percorso = None  
    min_distance = float('inf')  

    for percorso in percorsi:
        last_node = percorso[-1]  

        # Calcola la distanza tra l'ultimo nodo del percorso e il nodo specificato.
        distance = G[last_node][node]['weight']

        # Se la distanza corrente è minore della distanza minima trovata finora:
        if distance <= min_distance:
            # Verifica se l'aggiunta di node alla fine di percorso è ammissibile.
            if test_node_feasibility(G, node, percorso, delta):
                # Se è ammissibile, aggiorna la distanza minima e il percorso più vicino.
                min_distance = distance
                nearest_percorso = percorso

    # Restituisci il percorso più vicino trovato (o None se non è stato trovato alcun percorso adatto).
    return nearest_percorso








def find_k_nearest_percorsi(G, node, percorsi, k, delta):
    """
    Trova fino a k percorsi il cui nodo finale è il più vicino a node,
    tale da garantire comunque l'ammissibilità. (ossia in modo che se si aggiunge
    'node' alla fine del percorso il percorso resta ammissibile: node non compie
    più di delta volte la sua distanza minima dalla scuola).

    Args:
        G: Il grafo che rappresenta l'istanza del problema.
        node: Il nodo (bambino) per il quale si cerca il percorso più vicino.
        percorsi: Una lista di percorsi esistenti.
        k: Il numero massimo di percorsi da restituire.
        delta: Il fattore di tolleranza.

    Returns:
        Una lista dei k percorsi più vicini al nodo specificato che soddisfano il vincolo di ammissibilità,
        oppure una lista vuota se non vengono trovati percorsi validi.
    """

    # Inizializza un heap massimo (usando valori di distanza negativi)
    max_heap = []

    for percorso in percorsi:
        last_node = percorso[-1]  

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