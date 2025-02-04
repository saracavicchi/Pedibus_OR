import copy
from utils import timeit
from funzione_obiettivo import *
from controlli_ammissibilita import *
import random
from perturbazione_svuotamento import *

@timeit
def tabu_search_bI(G, residui_dict, percorsi, obj_val, delta, max_len):

    residui_dict_copy = copy.deepcopy(residui_dict)
    current_percorsi = copy.deepcopy(percorsi)
    current_obj_val = obj_val  # Funzione obiettivo corrente

    best_all_percorsi = copy.deepcopy(percorsi)
    best_all_obj_val = obj_val
    best_all_residui = copy.deepcopy(residui_dict_copy)

    tabu = []  # Tabu list
    max_tabu_size = 10
    stallo = 150  # Numero massimo di iterazioni senza miglioramenti
    nonMigliorato = 0
    max_iterazioni = 250
    iterazioni = 0
    perturbazione = 10

    while nonMigliorato < stallo and iterazioni < max_iterazioni:
        print(f"Iterazione: {iterazioni}, Non migliorato: {nonMigliorato}, Current OV: {current_obj_val}, Best OV: {best_all_obj_val}")
        # Ri-inizializzo a 0 così da trovare la miglior soluzione nell'intorno della soluzione corrente
        # anche se non è migliore della soluzione corrente
        best_percorsi = None
        best_obj_val = float('inf')
        best_residui = None

        mossa_migliorativa = False
        best_mossa = None
        intensification_nodes = []


        ## Esplora tutti i percorsi
        for i in range(len(current_percorsi)):

            if len(current_percorsi[i]) < 2:  # Salta percorsi con solo la scuola
                continue

            new_percorsi = copy.deepcopy(current_percorsi)
            residui_temp = copy.deepcopy(residui_dict_copy)

            # Esplora tutte le coppie di nodi nel percorso corrente per permutazioni
            percorso_test = copy.deepcopy(new_percorsi[i])
            for k in range(1, len(percorso_test) - 1):
                for j in range(k + 1, len(percorso_test)):
                    # Scambia i nodi i e j
                    percorso_test[k], percorso_test[j] = percorso_test[j], percorso_test[k]

                    if test_percorso_feasibility(percorso_test, G, delta):
                        residui_temp = calcola_residui_nodi_percorso(G, residui_dict_copy, percorso_test, delta)
                        new_percorsi[i] = percorso_test
                        nuovo_obj_val = objective_function(new_percorsi, G)

                        # Se la mossa è migliorativa, aggiorna la soluzione
                        if nuovo_obj_val < best_obj_val:
                            best_obj_val = nuovo_obj_val
                            best_percorsi = copy.deepcopy(new_percorsi)
                            mossa_migliorativa = True
                            best_mossa = (percorso_test[k], percorso_test[j])
                            best_residui = copy.deepcopy(residui_temp)


                    percorso_test[k], percorso_test[j] = percorso_test[j], percorso_test[k]



        if mossa_migliorativa:
          # Se è stato trovato un miglioramento, aggiorna la soluzione corrente
          if best_obj_val < best_all_obj_val:
              best_all_percorsi = copy.deepcopy(best_percorsi)
              best_all_obj_val = best_obj_val
              best_all_residui = copy.deepcopy(best_residui)
              current_percorsi = best_percorsi
              current_obj_val = best_obj_val
              residui_dict_copy = best_residui

              nonMigliorato = 0
              if best_mossa is not None:
                  if best_mossa not in tabu:
                    tabu.append(best_mossa)
              #if intensification_nodes:
                  #for node in intensification_nodes:
                      #if node not in tabu:
                          #tabu.append(node)
              while len(tabu) > max_tabu_size:
                      tabu.pop(0)
          else:
              nonMigliorato += 1

              if best_mossa is not None:
                  bam_k, bam_j = best_mossa
                  #print(bam_k)
                  if (bam_k,bam_j) not in tabu and (bam_j, bam_k) not in tabu:
                      tabu.append(best_mossa)
                  while len(tabu) > max_tabu_size:
                      tabu.pop(0)
                  current_percorsi = best_percorsi
                  current_obj_val = best_obj_val
                  residui_dict_copy = best_residui



          #Intensificazione
          while i < len(current_percorsi):
            if len(current_percorsi[i]) <= max_len:
                current_percorsi, residui_temp, svuotato = svuota_percorso(G, residui_dict_copy, current_percorsi, i, delta)
                if svuotato:
                    nuovo_obj_val = objective_function(current_percorsi, G)

                    if nuovo_obj_val < best_all_obj_val:
                        best_all_percorsi = copy.deepcopy(current_percorsi)
                        best_all_obj_val = nuovo_obj_val
                        best_all_residui = copy.deepcopy(residui_temp)
                        current_obj_val = nuovo_obj_val
                        residui_dict_copy = copy.deepcopy(residui_temp)
                        nonMigliorato = 0
            i += 1


        if not mossa_migliorativa or ( iterazioni > 0 and iterazioni%perturbazione == 0 ):
          #print("perturbazione random")
          #check_solution(current_percorsi, G, delta)
          #print("________")
          current_percorsi, residui_dict_copy = random_perturbation(G, residui_dict_copy, current_percorsi, delta, 0.5)
          #print(current_percorsi)
          current_obj_val = objective_function(new_percorsi, G)
          #print("dopo perturbazione random")
          #check_solution(new_percorsi, G, delta)
          #print("________")
          #current_obj_val = nuovo_obj_val
          #current_percorsi = copy.deepcopy(new_percorsi)
          #residui_dict_copy = copy.deepcopy(residui_temp)
          if current_obj_val < best_all_obj_val:
              best_all_percorsi = copy.deepcopy(new_percorsi)
              best_all_obj_val = nuovo_obj_val
              best_all_residui = copy.deepcopy(residui_temp)
              nonMigliorato = 0


        iterazioni += 1



    return best_all_percorsi, best_all_obj_val, best_all_residui

