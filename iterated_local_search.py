import copy
import random
import math
from local_search import *
from utils import timeit
from funzione_obiettivo import *
from controlli_ammissibilita import *
from perturbazione_svuotamento import *


@timeit
def iterated_local_search(G, residui_dict, percorsi, obj_val, delta, max_len, ls):
    """
    Implementazione dell'Iterated Local Search (ILS) con Simulated Annealing per migliorare la soluzione.

    Args:
        G: Grafo del problema.
        residui_dict: Dizionario con i residui per ogni nodo.
        percorsi: Soluzione iniziale (lista di percorsi).
        obj_val: Valore della funzione obiettivo della soluzione iniziale.
        delta: Fattore di tolleranza per la lunghezza del percorso.
        max_len: Lunghezza massima di un percorso per l'intensificazione.
        ls: Tipo di ricerca locale da utilizzare ("local_search_bI" o "local_search_fI").

    Returns:
        - La migliore soluzione trovata (lista di percorsi).
        - Il valore obiettivo della migliore soluzione trovata.
        - Il dizionario dei residui aggiornato.
    """

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

    iterazioni = 0
    max_iterazioni = 4

    T = 160  # Temperatura iniziale (più alta per accettare peggioramenti iniziali)
    T_frozen = 50  # Temperatura minima (quando fermiamo la ricerca)
    alpha = 0.9  # Fattore di raffreddamento

    while iterazioni < max_iterazioni and T > T_frozen:
        print("Temperatura: ", T)
        for _ in range(5):  # Numero di iterazioni interne
            print(f"Iterazione: {iterazioni}, Current OV: {current_obj_val}, Best OV: {best_all_obj_val}")
            #print(check_solution(current_percorsi, G, delta))
            #print("________")
            residui_dict_temp = copy.deepcopy(residui_dict_copy)

            # Applica la ricerca locale
            if ls not in funzioni:
                raise ValueError(f"Tipo di ricerca locale non valido: {ls}")
            ls_percorsi, ls_obj_val, residui_dict_temp = funzioni[ls](G, residui_dict_temp, current_percorsi, current_obj_val, delta, max_len)
            #print("LS", check_solution(ls_percorsi, G, delta))
            #print("________")
            #Applica la perturbazione
            perturbed_percorsi, residui_dict_temp = random_perturbation(G, residui_dict_temp, ls_percorsi, delta)
            #print("P",check_solution(perturbed_percorsi, G, delta))
            #print("________")
            #Ricalcola la funzione obiettivo
            perturbed_obj_val = objective_function(perturbed_percorsi, G)
            print(f"Iterazione: {iterazioni}, peturbed OV: {perturbed_obj_val}, Best OV: {best_all_obj_val}")
            delta_E = perturbed_obj_val - current_obj_val  # Differenza tra nuovo e vecchio valore obiettivo

            if delta_E < 0:
                #se soluzione migliora, accettala sempre**
                current_percorsi = copy.deepcopy(perturbed_percorsi)
                current_obj_val = perturbed_obj_val
                residui_dict_copy = copy.deepcopy(residui_dict_temp)

                if perturbed_obj_val < best_all_obj_val:
                    best_all_percorsi = copy.deepcopy(perturbed_percorsi)
                    best_all_obj_val = perturbed_obj_val
                    best_all_residui_dict = copy.deepcopy(residui_dict_temp)
            else:
                # se la soluzione peggiora, accettala con una certa probabilità
                r = random.random()
                print(r, math.exp(-delta_E / T))
                if r < math.exp(-delta_E / T):
                    current_percorsi = copy.deepcopy(perturbed_percorsi)
                    current_obj_val = perturbed_obj_val
                    residui_dict_copy = copy.deepcopy(residui_dict_temp)

        # Raffredda la temperatura
        T *= alpha
        iterazioni += 1


    return best_all_percorsi, best_all_obj_val, best_all_residui_dict
