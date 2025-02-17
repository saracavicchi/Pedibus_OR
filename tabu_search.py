import copy
from utils import timeit
from funzione_obiettivo import *
from controlli_ammissibilita import *
from perturbazione_svuotamento import *
from visualizza_grafici import *
import time

@timeit
def tabu_search_bI(G, residui_dict, percorsi, obj_val, delta, max_len, img):
    """
    Tabu Search con Best Improvement per migliorare la soluzione: 
    ad ogni iterazione trova la miglior soluzione nell'intorno della soluzione
    corrente (anche se peggiorativa rispetto alla soluzione corrente).

    La lista tabu impedisce lo scambio di bambini appena scambiati.

    Aggiunte: fase di intensificazione con svuotamento dei percorsi e 
    perturbazione casuale.

    Args:
        G: Grafo del problema.
        residui_dict: Dizionario con i residui per ogni nodo.
        percorsi: Soluzione iniziale (lista di percorsi).
        obj_val: Valore della funzione obiettivo della soluzione iniziale.
        delta: Fattore di tolleranza per la lunghezza del percorso.
        max_len: Lunghezza massima di un percorso per provare a svuotarlo.
        img: nome immagine per salvare l'andamento della soluzione nel tempo
    
    Returns:
        - La migliore soluzione trovata (lista di percorsi).
        - Il valore obiettivo della migliore soluzione trovata.
        - Il dizionario dei residui aggiornato.
    """

    start_time = time.time()

    residui_dict_copy = copy.deepcopy(residui_dict)
    current_percorsi = copy.deepcopy(percorsi)
    current_obj_val = obj_val  # Funzione obiettivo corrente

    best_all_percorsi = copy.deepcopy(percorsi)
    best_all_obj_val = obj_val
    best_all_residui = copy.deepcopy(residui_dict_copy)

    tabu = []  # Tabu list
    max_tabu_size = 20
    stallo = 250  # Numero massimo di iterazioni senza miglioramenti
    nonMigliorato = 0
    max_iterazioni = 900
    iterazioni = 0
    perturbazione = 10

    times_l = []
    obj_vals = []

    while nonMigliorato < stallo and iterazioni < max_iterazioni:
        print(f"Iterazione: {iterazioni}, Non migliorato: {nonMigliorato}, Current OV: {current_obj_val}, Best OV: {best_all_obj_val}")
        # Ri-inizializzo a 0 così da trovare la miglior soluzione nell'intorno della soluzione corrente
        # anche se non è migliore della soluzione corrente
        best_percorsi = None
        best_obj_val = float('inf')
        best_residui = None

        mossa_migliorativa = False
        best_mossa = None
       
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

                        # Se la mossa è migliorativa, memorizzala
                        if nuovo_obj_val < best_obj_val:
                            best_obj_val = nuovo_obj_val
                            best_percorsi = copy.deepcopy(new_percorsi)
                            mossa_migliorativa = True
                            best_mossa = (percorso_test[k], percorso_test[j])
                            best_residui = copy.deepcopy(residui_temp)

                    # Ripristina lo scambio 
                    percorso_test[k], percorso_test[j] = percorso_test[j], percorso_test[k]
                    new_percorsi[i] = percorso_test


        if mossa_migliorativa:
          # Se migliora l'ottimo candidato, aggiorna la soluzione corrente e l'incumbent
          #Criterio di Aspirazione
          if best_obj_val < best_all_obj_val:
              best_all_percorsi = copy.deepcopy(best_percorsi)
              best_all_obj_val = best_obj_val
              best_all_residui = copy.deepcopy(best_residui)
              current_percorsi = best_percorsi
              current_obj_val = best_obj_val
              residui_dict_copy = best_residui

              nonMigliorato = 0
              #Aggiungi la mossa alla tabu list se non già presente
              if best_mossa is not None:
                  bam_k, bam_j = best_mossa
                  if (bam_k, bam_j) not in tabu and (bam_j, bam_k) not in tabu:
                    tabu.append(best_mossa)
              while len(tabu) > max_tabu_size:
                      tabu.pop(0)
          else:
              # Non ho migliorato l'ottimo candidato, incremento il contatore
              nonMigliorato += 1

              if best_mossa is not None:
                  bam_k, bam_j = best_mossa
                    #Aggiungi la mossa alla tabu list se non già presente e in quel caso
                    # aggiorna la soluzione corrente
                  if (bam_k, bam_j) not in tabu and (bam_j, bam_k) not in tabu:
                        tabu.append(best_mossa)
                        current_percorsi = best_percorsi
                        current_obj_val = best_obj_val
                        residui_dict_copy = best_residui
                  while len(tabu) > max_tabu_size:
                        tabu.pop(0)
                 

          #Intensificazione: prova svuotamento percorsi corti
          while i < len(current_percorsi):
            if len(current_percorsi[i]) <= max_len:
                temp_percorsi, residui_temp, svuotato = svuota_percorso(G, residui_dict_copy, current_percorsi, i, delta)
                if svuotato:
                    nuovo_obj_val = objective_function(temp_percorsi, G)

                    if nuovo_obj_val < best_all_obj_val:
                        best_all_percorsi = copy.deepcopy(temp_percorsi)
                        best_all_obj_val = nuovo_obj_val
                        best_all_residui = copy.deepcopy(residui_temp)
                        current_obj_val = nuovo_obj_val
                        current_percorsi = copy.deepcopy(temp_percorsi)
                        residui_dict_copy = copy.deepcopy(residui_temp)
                        nonMigliorato = 0
                        break #termina se un percorso viene svuotato
            i += 1
        else: 
            nonMigliorato += 1

        #perturbazione casuale 
        if iterazioni > 0 and iterazioni%perturbazione == 0 : #prima era in or con not mossa migliorativa
          current_percorsi, residui_dict_copy = random_perturbation(G, residui_dict_copy, current_percorsi, delta, 0.5)
          current_obj_val = objective_function(current_percorsi, G)
          
          if current_obj_val < best_all_obj_val:
              best_all_percorsi = copy.deepcopy(current_percorsi)
              best_all_obj_val = current_obj_val
              best_all_residui = copy.deepcopy(residui_dict_copy)
              nonMigliorato = 0

        obj_vals.append(best_all_obj_val)
        cur_time = time.time() - start_time
        times_l.append(cur_time)
        
        iterazioni += 1


    plot_solution_over_time(times_l, obj_vals, 'Tabu Search Best Improvement', img)
    return best_all_percorsi, best_all_obj_val, best_all_residui











@timeit
def tabu_search_fI(G, residui_dict, percorsi, obj_val, delta, max_len, img):
    """
    Tabu Search con un First Improvement adattato per migliorare la soluzione: 
    ad ogni iterazione trova la prima soluzione nell'intorno della soluzione
    corrente migliorativa di quest'ultima, sennò la migliore dell'intorno 
    anche se peggiorativa rispetto alla soluzione corrente.

    La lista tabu impedisce lo scambio di bambini appena scambiati.

    Aggiunte: fase di intensificazione con svuotamento dei percorsi e 
    perturbazione casuale.

    Args:
        G: Grafo del problema.
        residui_dict: Dizionario con i residui per ogni nodo.
        percorsi: Soluzione iniziale (lista di percorsi).
        obj_val: Valore della funzione obiettivo della soluzione iniziale.
        delta: Fattore di tolleranza per la lunghezza del percorso.
        max_len: Lunghezza massima di un percorso per provare a svuotarlo.
        img: nome immagine per salvare l'andamento della soluzione nel tempo
    
    Returns:
        - La migliore soluzione trovata (lista di percorsi).
        - Il valore obiettivo della migliore soluzione trovata.
        - Il dizionario dei residui aggiornato.
    """
    start_time = time.time()
    residui_dict_copy = copy.deepcopy(residui_dict)
    current_percorsi = copy.deepcopy(percorsi)
    current_obj_val = obj_val  # Funzione obiettivo corrente

    best_all_percorsi = copy.deepcopy(percorsi)
    best_all_obj_val = obj_val
    best_all_residui = copy.deepcopy(residui_dict_copy)

    tabu = []  # Tabu list
    max_tabu_size = 20
    stallo = 250  # Numero massimo di iterazioni senza miglioramenti
    nonMigliorato = 0
    max_iterazioni = 900
    iterazioni = 0
    perturbazione = 10

    times_l = []
    obj_vals = []


    while nonMigliorato < stallo and iterazioni < max_iterazioni:
        print(f"Iterazione: {iterazioni}, Non migliorato: {nonMigliorato}, Current OV: {current_obj_val}, Best OV: {best_all_obj_val}")
        # Ri-inizializzo a 0 così da trovare la miglior soluzione nell'intorno della soluzione corrente
        # anche se non è migliore della soluzione corrente
        best_worse_percorsi = None
        best_worse_obj_val = float('inf')
        best_worse_residui = None

        
        mossa_migliorativa = False
        mossa_worse_migliorativa = False
        best_worse_mossa = None
   
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

                        # Se la mossa è migliorativa, memorizzala
                        if nuovo_obj_val < current_obj_val:
                            best_worse_obj_val = nuovo_obj_val
                            best_worse_percorsi = copy.deepcopy(new_percorsi)
                            mossa_migliorativa = True
                            best_worse_mossa = (percorso_test[k], percorso_test[j])
                            best_worse_residui = copy.deepcopy(residui_temp)

                        elif nuovo_obj_val < best_worse_obj_val:
                            best_worse_obj_val = nuovo_obj_val
                            mossa_worse_migliorativa = True
                            best_worse_percorsi = copy.deepcopy(new_percorsi)
                            best_worse_mossa = (percorso_test[k], percorso_test[j])
                            best_worse_residui = copy.deepcopy(residui_temp)


                    percorso_test[k], percorso_test[j] = percorso_test[j], percorso_test[k]
                    new_percorsi[i] = percorso_test

                    if mossa_migliorativa:
                        break
                
                if mossa_migliorativa:
                    break


        # se ho trovato una mossa migliorativa rispetto alla soluzione corrente
        if mossa_migliorativa or mossa_worse_migliorativa:
            # Se è stato trovato un miglioramento rispetto all'ottimo candidato, aggiorna la soluzione corrente
            # e aggiorna incumbent
            if best_worse_obj_val < best_all_obj_val:
                best_all_percorsi = copy.deepcopy(best_worse_percorsi)
                best_all_obj_val = best_worse_obj_val
                best_all_residui = copy.deepcopy(best_worse_residui)
                current_percorsi = best_worse_percorsi
                current_obj_val = best_worse_obj_val
                residui_dict_copy = best_worse_residui

                nonMigliorato = 0
                #Aggiungi la mossa alla tabu list se non già presente
                if best_worse_mossa is not None:
                    if best_worse_mossa not in tabu:
                        tabu.append(best_worse_mossa)
                
                while len(tabu) > max_tabu_size:
                        tabu.pop(0)

            # Se non ho migliorato l'ottimo candidato, incremento il contatore
            else:
                nonMigliorato += 1
                
            #Aggiungi la mossa alla tabu list se non già presente
            if best_worse_mossa is not None:
                bam_k, bam_j = best_worse_mossa
                if (bam_k,bam_j) not in tabu:
                    tabu.append(best_worse_mossa)
                    current_percorsi = best_worse_percorsi
                    current_obj_val = best_worse_obj_val
                    residui_dict_copy = best_worse_residui
                while len(tabu) > max_tabu_size:
                    tabu.pop(0)
                

            #Intensificazione: prova svuotamento percorsi corti
            while i < len(current_percorsi):
                if len(current_percorsi[i]) <= max_len:
                    temp_percorsi, residui_temp, svuotato = svuota_percorso(G, residui_dict_copy, current_percorsi, i, delta)
                    if svuotato:
                        nuovo_obj_val = objective_function(temp_percorsi, G)

                        if nuovo_obj_val < best_all_obj_val:
                            best_all_percorsi = copy.deepcopy(temp_percorsi)
                            best_all_obj_val = nuovo_obj_val
                            best_all_residui = copy.deepcopy(residui_temp)
                            current_obj_val = nuovo_obj_val
                            current_percorsi = copy.deepcopy(temp_percorsi)
                            residui_dict_copy = copy.deepcopy(residui_temp)
                            nonMigliorato = 0
                            break #termina se un percorso viene svuotato
                i += 1
        else: 
            nonMigliorato += 1

        #perturbazione casuale 
        if iterazioni > 0 and iterazioni%perturbazione == 0 : #prima era in or con not mossa migliorativa
          current_percorsi, residui_dict_copy = random_perturbation(G, residui_dict_copy, current_percorsi, delta, 0.5)
          current_obj_val = objective_function(current_percorsi, G)
          
          if current_obj_val < best_all_obj_val:
              best_all_percorsi = copy.deepcopy(current_percorsi)
              best_all_obj_val = current_obj_val
              best_all_residui = copy.deepcopy(residui_dict_copy)
              nonMigliorato = 0

        obj_vals.append(best_all_obj_val)
        cur_time = time.time() - start_time
        times_l.append(cur_time)
        
        iterazioni += 1


    plot_solution_over_time(times_l, obj_vals, 'Tabu Search Adapted First Improvement', img)
    return best_all_percorsi, best_all_obj_val, best_all_residui



