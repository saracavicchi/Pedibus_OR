import copy
from utils import timeit
from funzione_obiettivo import *
from controlli_ammissibilita import *
from trasferimenti_swap import *
from distanze_residui import *

@timeit
def local_search_bI(G, residui_dict, percorsi, obj_val, delta, max_len):
    residui_dict_copy = copy.deepcopy(residui_dict)

    current_percorsi = copy.deepcopy(percorsi)
    current_obj_val = obj_val  # Funzione obiettivo corrente

    migliorato = True

    while migliorato:
        migliorato = False
        best_percorsi = copy.deepcopy(current_percorsi)
        best_obj_val = current_obj_val
        best_residui_dict = copy.deepcopy(residui_dict_copy)

        # === FASE 1: Best Improvement su SWAP ===
        for i in range(len(current_percorsi)):

            if len(current_percorsi[i]) < 2:  # Salta percorsi con solo la scuola
                continue

            new_percorsi = copy.deepcopy(current_percorsi)
            residui_dict_temp = copy.deepcopy(residui_dict_copy)

            percorso_test = copy.deepcopy(new_percorsi[i])
            best_percorso_swap = None
            best_swap_obj_val = best_obj_val
            best_swap_residui = copy.deepcopy(residui_dict_temp)

            for k in range(1, len(percorso_test) - 1):
                for j in range(k + 1, len(percorso_test)):
                    # Scambia i nodi i e j
                    percorso_test[k], percorso_test[j] = percorso_test[j], percorso_test[k]

                    if test_percorso_feasibility(percorso_test, G, delta):
                        nuovo_obj_val = objective_function(new_percorsi, G)

                        # Se la mossa è migliorativa, aggiorna la soluzione
                        if nuovo_obj_val < best_swap_obj_val:
                            best_swap_obj_val = nuovo_obj_val
                            best_percorso_swap = copy.deepcopy(percorso_test)
                            best_swap_residui = calcola_residui_nodi_percorso(G, residui_dict_temp, percorso_test, delta)

                    # Ripristina lo scambio per provare altre combinazioni
                    percorso_test[k], percorso_test[j] = percorso_test[j], percorso_test[k]

            # Se uno swap migliorativo è stato trovato, applicalo
            if best_percorso_swap is not None:
                new_percorsi[i] = best_percorso_swap
                best_obj_val = best_swap_obj_val
                best_percorsi = copy.deepcopy(new_percorsi)
                best_residui_dict = best_swap_residui
                migliorato = True

        # === FASE 2: Intensificazione - Diversificazione (node transfer), SOLO SE Best Improvement non ha migliorato ===
        if not migliorato:
            for i in range(len(current_percorsi)):
                if len(current_percorsi[i]) <= max_len:
                    #print("prova trasferimento")
                    ris = node_transfer(current_percorsi, i, G, residui_dict_copy, delta)
                    if ris is not None:

                        temp_percorsi, temp_residui = ris  # Estrarre i valori aggiornati
                        nuovo_obj_val = objective_function(temp_percorsi, G)

                        if nuovo_obj_val < best_obj_val:
                            best_percorsi = copy.deepcopy(temp_percorsi)
                            best_residui_dict = copy.deepcopy(temp_residui)
                            best_obj_val = nuovo_obj_val
                            migliorato = True
                            break  # Applica un solo node transfer alla volta

        # Se è stato trovato un miglioramento, aggiorna la soluzione corrente
        if migliorato:
            current_percorsi = best_percorsi
            current_obj_val = best_obj_val
            residui_dict_copy = best_residui_dict

    return current_percorsi, current_obj_val, residui_dict_copy



@timeit
def local_search_fI(G, residui_dict, percorsi, obj_val, delta, max_len):

    residui_dict_copy = copy.deepcopy(residui_dict)
    current_percorsi = copy.deepcopy(percorsi)
    current_obj_val = obj_val  # Funzione obiettivo corrente

    migliorato = True

    while migliorato:
        migliorato = False

        i = 0
        # Esplora tutti i percorsi
        while i < len(current_percorsi):

            if len(current_percorsi[i]) < 2:  # Salta percorsi con solo la scuola
                i += 1
                continue

            new_percorsi = copy.deepcopy(current_percorsi)
            residui_dict_temp = copy.deepcopy(residui_dict_copy)

            # Esplora tutte le coppie di nodi nel percorso corrente per permutazioni
            percorso_test = copy.deepcopy(new_percorsi[i])
            for k in range(1, len(percorso_test) - 1):
                for j in range(k + 1, len(percorso_test)):
                    # Scambia i nodi i e j
                    percorso_test[k], percorso_test[j] = percorso_test[j], percorso_test[k]

                    if test_percorso_feasibility(percorso_test, G, delta):
                        new_percorsi[i] = percorso_test
                        nuovo_obj_val = objective_function(new_percorsi, G)

                        # Se la mossa è migliorativa, aggiorna la soluzione
                        if nuovo_obj_val < current_obj_val:
                            residui_dict_copy = calcola_residui_nodi_percorso(G,residui_dict_copy, new_percorsi[i], delta)
                            current_percorsi = copy.deepcopy(new_percorsi)
                            current_obj_val = nuovo_obj_val
                            migliorato = True
                            break
                    else:
                        # Ripristina lo scambio se la mossa non è valida
                        percorso_test[k], percorso_test[j] = percorso_test[j], percorso_test[k]
                if migliorato:
                    break
            if migliorato:
                break

            i += 1

        if not migliorato:
            # Intensificazione - Diversificazione (node transfer)
            for i in range(len(new_percorsi)):
              if len(new_percorsi[i]) <= max_len:
                  ris = node_transfer(new_percorsi, i, G, residui_dict_copy, delta)
                  if ris is not None:
                      new_percorsi, residui_dict_temp = ris
                      nuovo_obj_val = objective_function(new_percorsi, G)

                      if nuovo_obj_val < current_obj_val:
                          current_percorsi = copy.deepcopy(new_percorsi)
                          current_obj_val = nuovo_obj_val
                          residui_dict_copy = residui_dict_temp
                          migliorato = True
                          break



    return current_percorsi, current_obj_val, residui_dict_copy

