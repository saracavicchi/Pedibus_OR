
import copy
import time as tm
from utils import timeit
from funzione_obiettivo import *
from controlli_ammissibilita import *
from greedy_rand import *
from local_search import *
from visualizza_grafici import *

def prova(G, residui_dict, delta, k, num_greedy, ls, max_len):
    residui_dict_copy = copy.deepcopy(residui_dict)
    i = 83301
    best = float('inf')
    i_b = None
    while True:
        (g_percorsi, g_obj_val, residui_greedy), time = subsequent_nearest_neighbour_randomized(G, residui_dict_copy, delta, k, i)
        (ls_percorsi, ls_obj_val, residui_ls), time = local_search_bI(G, residui_greedy, g_percorsi, g_obj_val, delta, max_len)
        print (ls_obj_val, i)
        if ls_obj_val < best:
            best = ls_obj_val
            i_b = i
        print("Best ", best, "I best ", i_b)
        if ls_obj_val < 4201844:
            print("___________", i, ls_obj_val)
            break
        i += 1
    return i    