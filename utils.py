import time 
import copy 

def timeit(func):
    """
    Decorator che calcola il tempo impiegato per eseguire una funzione.

    Args:
    - func: la funzione da decorare.

    Returns:
    - Il risultato della funzione e il tempo impiegato.
    """
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start

        # Converti a ore minuti e secondi
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = elapsed % 60

        print(f'Tempo impiegato: {hours:02d}:{minutes:02d}:{seconds:.6f}')
        return result, elapsed
    return wrapper






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
    tot_sum += G[percorso[i]][percorso[i + 1]]['weight']
    
  return tot_sum