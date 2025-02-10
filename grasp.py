import copy
import time as tm
from utils import timeit
from funzione_obiettivo import *
from controlli_ammissibilita import *
from greedy_rand import *
from local_search import *
from visualizza_grafici import *



@timeit
def GRASP_subsequent_NN(G, residui_dict, delta, k, num_greedy, ls, max_len, img):
    """
    Ripete num_iterations volte una local search su una delle soluzioni prodotte dalla greedy randomizzata
    e restituisce la soluzione migliore trovata.

    Parametri:
    - Gr: il grafo.
    - delta: il parametro di tolleranza per la durata del percorso.
    - k: numero di vicini da considerare nella greedy randomizzata.
    - num_greedy: numero di esecuzioni della greedy.
    - ls: nome della local search da eseguire
    - max_len: lunghezza massima del percorso da provare a svuotare

    Ritorna:
    - best_percorsi: i percorsi della soluzione migliore.
    - best_obj_val: il valore obiettivo della soluzione migliore.
    """
    start_time = tm.time()
    times_l = []
    best_percorsi = None
    best_obj_val = float('inf')  # Inizializza con un valore molto alto
    residui_best = None

    
    obj_vals = []

    # Dizionario per la mappatura della local search
    funzioni = {
        "local_search_bI": local_search_bI,
        "local_search_fI": local_search_fI,
    }

    for i in range(num_greedy):
        print(i+1)

        # Genera una soluzione greedy randomizzata
        residui_dict_copy = copy.deepcopy(residui_dict)
        (g_percorsi, g_obj_val, residui_greedy), time = subsequent_nearest_neighbour_randomized(G, residui_dict_copy, delta, k, i+25200)

        # Esegui la local search sulla soluzione generata
        if ls in funzioni:
            (ls_percorsi, ls_obj_val, residui_ls), time = funzioni[ls](G, residui_greedy, g_percorsi, g_obj_val, delta, max_len)


            # Aggiorna la soluzione migliore se necessario
            if ls_obj_val < best_obj_val:
                best_percorsi = copy.deepcopy(ls_percorsi)
                best_obj_val = ls_obj_val
                residui_best = copy.deepcopy(residui_ls)
            
            cur_time = tm.time() - start_time
            times_l.append(cur_time)
            obj_vals.append(best_obj_val)
        else:
            print("Local search non valida")

    plot_solution_over_time(times_l, obj_vals, 'Grasp Subsequent NN', img)
    

    return best_percorsi, best_obj_val, residui_best

@timeit
def GRASP_School_NN(G, residui_dict, delta, k, num_greedy, ls, max_len, img):
    """
    Ripete una local search su una delle soluzioni prodotte dalla greedy randomizzata
    e restituisce la soluzione migliore trovata.

    Parametri:
    - G: il grafo.
    - delta: il parametro di tolleranza per la durata del percorso.
    - k: numero di opzioni alternative internamente a greedy.
    - num_greedy: numero di esecuzioni della greedy.
    - ls: local searh da eseguire
    - max_len: lunghezza massima del percorso da provare a svuotare

    Ritorna:
    - best_percorsi: i percorsi della soluzione migliore.
    - best_obj_val: il valore obiettivo della soluzione migliore.
    """
    start_time = tm.time()
    times_l = []
    best_percorsi = None
    best_obj_val = float('inf')  # Inizializza con un valore molto alto

    obj_vals = []


    # Dizionario per la mappatura della local search
    funzioni = {
        "local_search_bI": local_search_bI,
        "local_search_fI": local_search_fI,
    }

    for i in range(num_greedy):
        print(i+1)
        residui_dict_copy = copy.deepcopy(residui_dict)
        # Genera una soluzione greedy randomizzata
        (g_percorsi, g_obj_val, residui_greedy), time = school_nearest_neighbour_randomized(G, residui_dict_copy, delta, k)

        # Esegui la local search sulla soluzione generata
        if ls in funzioni:
            (ls_percorsi, ls_obj_val, residui_ls), time = funzioni[ls](G, residui_greedy, g_percorsi, g_obj_val, delta, max_len)


            # Aggiorna la soluzione migliore se necessario
            if ls_obj_val < best_obj_val:
                best_percorsi = copy.deepcopy(ls_percorsi)
                best_obj_val = ls_obj_val
                residui_best = copy.deepcopy(residui_ls)
            
            cur_time = tm.time() - start_time
            times_l.append(cur_time)
            obj_vals.append(best_obj_val)
        else:
            print("Local search non valida")

    plot_solution_over_time(times_l, obj_vals, 'Grasp School NN', img)

    return best_percorsi, best_obj_val, residui_best