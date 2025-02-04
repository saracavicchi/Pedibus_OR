import copy
import random
from controlli_ammissibilita import *
from trasferimenti_swap import *


def random_perturbation(G, residui_dict, percorsi, delta, prob_perturbazione=0.5):
    """
    Applica una perturbazione casuale ai percorsi.
    Termina se un percorso viene svuotato.

    Parametri:
    - G: grafo
    - residui_dict: dizionario dei residui per ogni nodo.
    - percorsi: lista di percorsi (ogni percorso è una lista di nodi).
    - prob_perturbazione: probabilità che un percorso venga perturbato (default: 0.5).

    Se un percorso viene perturbato, si cercano di spostare i suoi nodi in altri percorsi.

    Ritorna:
    - Una lista di percorsi perturbati.
    - Un dizionario aggiornato dei residui.
    """
    residui_dict_copy = copy.deepcopy(residui_dict)
    percorsi_perturbati = copy.deepcopy(percorsi)

    fine = False  # Flag per terminare se un percorso viene eliminato

    i = 0
    while i < len(percorsi_perturbati):
        r = random.random()

        if r < prob_perturbazione:  # Perturba il percorso con probabilità 'prob_perturbazione'
            j = 0
            while j < len(percorsi_perturbati):
                if i == j:
                    j += 1
                    continue

                percorsi_test = copy.deepcopy(percorsi_perturbati)

                nodi_da_rimuovere = []
                nodi_spostati = False  # Flag per verificare se almeno un nodo è stato spostato

                for nodo in percorsi_test[i]:
                    if nodo == 'Scuola':
                        continue

                    ris = test_node_in_percorso_best_pos_feasibility(G, residui_dict_copy, nodo, percorsi_test[j], delta)

                    if ris is not None:
                        #print(nodo, ris)
                        pos, residuo = ris
                        nodi_da_rimuovere.append(nodo)
                        percorsi_test[j].insert(pos, nodo)
                        percorsi_test[i].remove(nodo)
                        #residui_dict_copy[nodo] = residuo
                        nodi_spostati = True

                        #Aggiornamento immediato dei residui
                        residui_dict_copy = calcola_residui_nodi_percorso(G, residui_dict_copy, percorsi_test[j], delta)
                        residui_dict_copy = calcola_residui_nodi_percorso(G, residui_dict_copy, percorsi_test[i], delta)

                # Rimuovi i nodi spostati da percorso_i
                #for nodo in nodi_da_rimuovere:
                    #percorsi_test[i].remove(nodo)

                # Se il percorso `i` è stato svuotato, termina
                if len(percorsi_test[i]) == 1:
                    percorsi_perturbati = [p for p in percorsi_test if len(p) > 1]
                    fine = True
                    #print("Svuotato")
                    break

                # Applica le modifiche solo se almeno un nodo è stato spostato
                if nodi_spostati:
                    percorsi_perturbati = percorsi_test

                j += 1

        if fine:
            break

        i += 1

    return percorsi_perturbati, residui_dict_copy


def svuota_percorso(G, residui_dict, percorsi, src, delta, ):
  """
  Intensficazione: si cerca di svuotare il percorso con indice src con len <= max_len
  """
  ris = None
  residui_dict_copy = copy.deepcopy(residui_dict)
  new_percorsi = copy.deepcopy(percorsi)

  ris = node_transfer(new_percorsi, src, G, residui_dict_copy, delta)

  if ris is not None:
      new_percorsi, residui_dict_copy = ris
      return new_percorsi, residui_dict_copy, True
  else:
    return percorsi, residui_dict, False