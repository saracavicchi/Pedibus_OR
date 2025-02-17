import copy
import random
import math
from local_search import *
from utils import timeit
from funzione_obiettivo import *
from controlli_ammissibilita import *
from perturbazione_svuotamento import *
from visualizza_grafici import *
import time as tm



@timeit
def iterated_local_search(G, residui_dict, percorsi, obj_val, delta, max_len, ls, img):
    """
    Implementazione dell'Iterated Local Search (ILS) con Simulated Annealing per migliorare la soluzione.

    Args:
        G: Grafo del problema.
        residui_dict: Dizionario con i residui per ogni nodo.
        percorsi: Soluzione iniziale (lista di percorsi).
        obj_val: Valore della funzione obiettivo della soluzione iniziale.
        delta: Fattore di tolleranza per la lunghezza del percorso.
        max_len: Lunghezza massima di un percorso per provare a svuotarlo.
        ls: Tipo di ricerca locale da utilizzare ("local_search_bI" o "local_search_fI").
        img: nome immagine per salvare l'andamento della soluzione nel tempo

    Returns:
        - La migliore soluzione trovata (lista di percorsi).
        - Il valore obiettivo della migliore soluzione trovata.
        - Il dizionario dei residui aggiornato.
    """
    start_time = tm.time()
    times_l = []

    # Dizionario per la mappatura della local search
    funzioni = {
        "local_search_bI": local_search_bI,
        "local_search_fI": local_search_fI,
    }

    residui_dict_copy = copy.deepcopy(residui_dict)
    current_percorsi = copy.deepcopy(percorsi)
    current_obj_val = obj_val  # Funzione obiettivo corrente

    best_all_percorsi = copy.deepcopy(percorsi)
    best_all_obj_val = obj_val
    best_all_residui_dict = copy.deepcopy(residui_dict)
    obj_vals = []


    T = 160  # Temperatura iniziale 
    T_frozen = 1  # Temperatura minima (quando fermiamo la ricerca) 
    alpha = 0.6  # Fattore di raffreddamento

    # Applica la ricerca locale
    if ls not in funzioni:
        raise ValueError(f"Tipo di ricerca locale non valido: {ls}")
    
    #Applico Local Search alla soluzione iniziale
    (ls_percorsi, ls_obj_val, residui_dict_temp), time = funzioni[ls](G, residui_dict_copy, current_percorsi, current_obj_val, delta, max_len)


    # Ciclo principale dell'ILS: Principio del Simulated Annealing
    while T > T_frozen:
        
        for _ in range(10):  # Numero di iterazioni interne per raggiungere condizione di equilibrio
            print(f"Temperatura: {T}, Current OV: {current_obj_val}, Best OV: {best_all_obj_val}")
            
            # Perturbazione casuale della soluzione corrente
            perturbed_percorsi, residui_dict_temp = random_perturbation(G, residui_dict_temp, ls_percorsi, delta)
            perturbed_obj_val = objective_function(perturbed_percorsi, G)
            
            # Applica la ricerca locale alla soluzione perturbata
            (ls_percorsi, ls_obj_val, residui_dict_temp), time = funzioni[ls](G, residui_dict_temp, perturbed_percorsi, perturbed_obj_val, delta, max_len)
           
            print(f"Temperatura: {T}, ls OV: {ls_obj_val}, Best OV: {best_all_obj_val}")
            
            delta_E = ls_obj_val - current_obj_val  # Differenza tra nuovo e vecchio valore obiettivo

            if delta_E < 0:
                #se soluzione migliora quella corrente, accettala sempre**
                current_percorsi = copy.deepcopy(ls_percorsi)
                current_obj_val = ls_obj_val
                residui_dict_copy = copy.deepcopy(residui_dict_temp)

                if ls_obj_val < best_all_obj_val:
                    best_all_percorsi = copy.deepcopy(ls_percorsi)
                    best_all_obj_val = ls_obj_val
                    best_all_residui_dict = copy.deepcopy(residui_dict_temp)
            else:
                # se la soluzione peggiora la soluzione corrente, accettala con una certa probabilità
                r = random.random()
                print("r :", r, "soglia: ", math.exp(-delta_E / T))
                if r < math.exp(-delta_E / T):
                    current_percorsi = copy.deepcopy(ls_percorsi)
                    current_obj_val = ls_obj_val
                    residui_dict_copy = copy.deepcopy(residui_dict_temp)
            
            obj_vals.append(best_all_obj_val)
            cur_time = tm.time() - start_time
            times_l.append(cur_time)

        # Raffredda la temperatura
        T *= alpha

    
    if ls == "local_search_bI":
        name = "LS Best Improvement"
    elif ls == "local_search_fI":
        name = "LS First Improvement"
   
    plot_solution_over_time(times_l, obj_vals, "Iterated Local Search " + name, img)
    return best_all_percorsi, best_all_obj_val, best_all_residui_dict

