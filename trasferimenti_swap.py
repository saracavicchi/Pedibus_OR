import copy
from controlli_ammissibilita import *
from nodi_percorsi_vicini_corti import *

def node_transfer(percorsi, src, G, residui_dict, delta):
    """
    Prova a svuotare il percorso src trasferendo tutti i suoi nodi ad altri percorsi.
    Se anche solo un nodo non può essere trasferito, nessuna modifica viene applicata.

    Args:
        percorsi: Lista di percorsi
        src: Indice del percorso da svuotare
        G: Grafo del problema
        residui_dict: Dizionario dei residui attuali per ogni nodo
        delta: Fattore di tolleranza

    Returns:
        - (percorsi_modificati, residui_modificati) se il percorso viene svuotato con successo
        - (percorsi_originali, residui_originali) se almeno un nodo non può essere trasferito
    """


    percorsi_temp = copy.deepcopy(percorsi)
    residui_dict_temp = copy.deepcopy(residui_dict)

    k_nn = 50  # Numero massimo di nodi vicini da controllare

    # Lista di nodi da trasferire, escludendo la "Scuola"
    nodes_to_transfer = percorsi_temp[src][1:]

    # Contatore di nodi trasferiti con successo
    nodes_moved = 0

    for node in nodes_to_transfer:
        nodi_vicini = find_k_nearest_node(G, node, percorsi, k_nn)

        # Ottieni gli indici unici dei percorsi vicini
        percorsi_vicini = list(set(vicino[1] for vicino in nodi_vicini))
        
        moved = False  # Flag per capire se il nodo è stato trasferito

        for vicino in percorsi_vicini:
            # Verifica se il nodo può essere inserito nel percorso vicino
            ris = test_node_in_percorso_best_pos_feasibility(G, residui_dict_temp, node, percorsi_temp[vicino], delta)
            
            # il nodo può essere inserito
            if ris is not None:
                pos, residuo = ris
                percorsi_temp[src].remove(node)
                percorsi_temp[vicino].insert(pos, node)
                

                # Aggiorna residui
                residui_dict_temp[node] = residuo
                residui_dict_temp = calcola_residui_nodi_percorso(G, residui_dict_temp, percorsi_temp[src], delta)
                residui_dict_temp = calcola_residui_nodi_percorso(G, residui_dict_temp, percorsi_temp[vicino], delta)

                moved = True
                nodes_moved += 1
                break  # Passa al nodo successivo

        # Se il nodo non è stato spostato, annulla tutte le modifiche e ritorna l'originale
        if not moved:
            return percorsi, residui_dict

    # Se il percorso è stato completamente svuotato, lo rimuoviamo
    if len(percorsi_temp[src]) == 1:  # Rimasta solo la scuola
        percorsi_temp.pop(src)
        return percorsi_temp, residui_dict_temp  # Restituisce i percorsi aggiornati

    # Se il percorso non è stato completamente svuotato, annulliamo tutte le modifiche
    return percorsi, residui_dict









### FUNZIONE NON USATA
def node_swap(G, percorso, delta):
  """
  Prova a scambiare due nodi del percorso.
  Valuta tutti gli scambi possibili e restituisce il migliore.
  Attenzione: non applica di suo lo swap, ma restituisce i nodi da scambiare.

  Args:
  - G: il grafo.
  - percorso: il percorso da modificare.
  - delta: il parametro di tolleranza per la durata del percorso.

  Ritorna:
  - La coppia di nodi migliore da scambiare e i residui dei nodi del percorso
    dopo lo scambio o None se non è possibile
    fare nessuno scambio.
  """
  percorso_test = copy.deepcopy(percorso)
  best_residui = somma_residui_percorso(G, percorso)
  best_swap = None

  for i in range(1, len(percorso_test) - 1):
    for j in range(i + 1, len(percorso_test)):

      # Scambia i nodi i e j
      percorso_test[i], percorso_test[j] = percorso_test[j], percorso_test[i]
      
      # Verifica se il percorso con lo scambio è ammissibile
      if test_percorso_feasibility(percorso_test, G, delta):
        residui = somma_residui_percorso(G, percorso_test)
        if residui > best_residui:
          best_residui = residui
          best_swap = (i, j)

  if best_swap is not None:
    return best_swap, best_residui
  else:
    return None







### FUNZIONE NON USATA
def apply_swap(G, percorsi, residui_dict, percorso, swap):
  """
  Applica lo swap al percorso specificato e aggiorna i percorsi.
  CALCOLA ANCHE I RESIDUI AGGIORNATI DEL PERCORSO.

  Args: 
  - G: il grafo.
  - percorsi: lista dei percorsi.
  - residui_dict: i residui dei nodi.
  - percorso: il percorso da modificare.
  - swap: la coppia di nodi da scambiare.

  Ritorna:
  - I percorsi aggiornati e i residui dei nodi aggiornati.
  """
  residui_dict_copy = copy.deepcopy(residui_dict)
  percorsi_test = copy.deepcopy(percorsi)
  percorso_test = copy.deepcopy(percorso)
  percorso_test[swap[0]], percorso_test[swap[1]] = percorso_test[swap[1]], percorso_test[swap[0]]
  # Ricalcola i residui
  residui_dict_copy = calcola_residui_nodi_percorso(G, residui_dict_copy, percorso)
  percorsi_test[percorso] = percorso_test
  return percorsi_test, residui_dict_copy