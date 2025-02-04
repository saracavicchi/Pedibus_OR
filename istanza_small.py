from crea_visualizza_istanza import *
from controlli_ammissibilita import *
from greedy import *
from local_search import *
from greedy_rand import *
from grasp import *
from tabu_search import *
from iterated_local_search import *
from visualizza_grafici import *


def istanza_small_main():
    delta_small = 1.5
    G_small, residui_dict_small = generate_instance(num_bambini=100, pos_min=20, pos_max=50, seed=10, delta= delta_small)
    #plot_graph(G_small, 'grafo_dim_ridotte.png')


    #Stampo i nodi e le relative posizioni
    for node, data in G_small.nodes(data=True):
        print(f"Nodo: {node}, Posizione: {data['pos']}, Massima Distanza: {data['max_distance']}")

    #print("\n")

    #Stampo gli archi e i relativi pesi
    #for u, v, data in G_small.edges(data=True):
    #    print(f"Arco: {u} - {v}, Peso: {data['weight']}")

    subsequentNN = []
    schoolNN = []
    ls_subsequentNN = []
    ls_schoolNN = []
    grasp_subsequentNN = []
    grasp_schoolNN = []
    Ils_subsequentNN = []
    Ils_schoolNN = []
    grasp_bI = []
    tabu = []
    ils_bI = []



    percorsi_sub_NN, sub_NN_obj_val, residui_dict_small_sub_NN = subsequent_nearest_neighbour(G_small, residui_dict_small, delta_small)
    #stampa_percorsi(percorsi_sub_NN)
    print(f"Funzione obiettivo: {sub_NN_obj_val}")
    check_solution(percorsi_sub_NN, G_small, delta_small)
    subsequentNN.append(sub_NN_obj_val)

    percorsi_sch_NN, sch_NN_obj_val, residui_dict_small_sch_NN = school_nearest_neighbour(G_small, residui_dict_small, delta_small)
    #stampa_percorsi(percorsi_sch_NN)
    print(f"Funzione obiettivo: {sch_NN_obj_val}")
    check_solution(percorsi_sch_NN, G_small, delta_small)
    schoolNN.append(sch_NN_obj_val)

    percorsi_sub_NN_R, sub_NN_R_obj_val, residui_dict_small_sub_NN_R = subsequent_nearest_neighbour_randomized(G_small, residui_dict_small, delta_small, k=3)
    #stampa_percorsi(percorsi_sub_NN)
    print(f"Funzione obiettivo: {sub_NN_R_obj_val}")
    check_solution(percorsi_sub_NN_R, G_small, delta_small)
    subsequentNN.append(sub_NN_R_obj_val)

    percorsi_sch_NN_R, sch_NN_R_obj_val, residui_dict_small_sch_NN_R = school_nearest_neighbour_randomized(G_small,residui_dict_small, delta_small, k=3)
    #stampa_percorsi(percorsi_sch_NN_R)
    print(f"Funzione obiettivo: {sch_NN_R_obj_val}")
    check_solution(percorsi_sch_NN, G_small, delta_small)
    schoolNN.append(sch_NN_R_obj_val)

    plotSubSchResults(subsequentNN, schoolNN, "Greedy")

    #percorsi_cw, cw_obj_val, residui_dict_small_cw = clark_wright(G_small, residui_dict_small, delta_small)
    #stampa_percorsi(percorsi_cw)
    #print(f"Funzione obiettivo: {cw_obj_val}")
    #check_solution(percorsi_cw, G_small, delta_small)
    #ls_subsequentNN.append(cw_obj_val)

    percorsi_ls_bI, ls_bI_obj_val, residui_dict_small_sub_ls_bI = local_search_bI(G_small, residui_dict_small_cw, percorsi_cw, cw_obj_val, delta_small, max_len=5)
    stampa_percorsi(percorsi_ls_bI)
    print(f"Funzione obiettivo: {ls_bI_obj_val}")
    check_solution(percorsi_ls_bI, G_small, delta_small)
    ls_subsequentNN.append(ls_bI_obj_val)

    percorsi_ls_bI, ls_bI_obj_val, residui_dict_small_sub_ls_bI = local_search_bI(G_small, residui_dict_small_sub_NN, percorsi_sub_NN, sub_NN_obj_val, delta_small, max_len=5)
    #stampa_percorsi(percorsi_ls_bI)
    print(f"Funzione obiettivo: {ls_bI_obj_val}")
    check_solution(percorsi_ls_bI, G_small, delta_small)
    ls_subsequentNN.append(ls_bI_obj_val)

    percorsi_ls_bI, ls_bI_obj_val, residui_dict_small_ls_sch_bI = local_search_bI(G_small, residui_dict_small_sch_NN, percorsi_sch_NN, sch_NN_obj_val, delta_small, max_len=5)
    #stampa_percorsi(percorsi_ls_bI)
    print(f"Funzione obiettivo: {ls_bI_obj_val}")
    check_solution(percorsi_ls_bI, G_small, delta_small)
    ls_schoolNN.append(ls_bI_obj_val)

    percorsi_sub_ls_fI, sub_ls_fI_obj_val, residui_dict_small_sub_ls_fI = local_search_fI(G_small, residui_dict_small_sub_NN, percorsi_sub_NN, sub_NN_obj_val, delta_small, max_len=5)
    #stampa_percorsi(percorsi_ls_fI)
    print(f"Funzione obiettivo: {sub_ls_fI_obj_val}")
    check_solution(percorsi_sub_ls_fI, G_small, delta_small)
    ls_subsequentNN.append(sub_ls_fI_obj_val)

    percorsi_sch_ls_fI, sch_ls_fI_obj_val, residui_dict_small_sch_ls_fI = local_search_fI(G_small, residui_dict_small_sch_NN, percorsi_sch_NN, sch_NN_obj_val, delta_small, max_len=5)
    #stampa_percorsi(percorsi_ls_bI)
    print(f"Funzione obiettivo: {sch_ls_fI_obj_val}")
    check_solution(percorsi_sch_ls_fI, G_small, delta_small)
    ls_schoolNN.append(sch_ls_fI_obj_val)

    plotSubSchResults(ls_subsequentNN, ls_schoolNN, 'Ls')



    percorsi_G_sub_NN_bI, G_sub_NN_bI_obj_val, residui_dict_small_G_sub_NN_bI = GRASP_subsequent_NN(G_small, residui_dict_small, delta_small, k=2, num_greedy=5, ls = "local_search_bI", max_len=5)
    #stampa_percorsi(percorsi_G_sub_NN_bI)
    print(f"Funzione obiettivo: {G_sub_NN_bI_obj_val}")
    check_solution(percorsi_G_sub_NN_bI, G_small, delta_small)
    grasp_subsequentNN.append(G_sub_NN_bI_obj_val)
    grasp_bI.append(G_sub_NN_bI_obj_val)

    percorsi_G_sch_bI, G_sch_bI_obj_val, residui_dict_small_G_sch_NN_bI = GRASP_School_NN(G_small, residui_dict_small, delta_small, k=2, num_greedy=5, ls = "local_search_bI", max_len=5)
    #stampa_percorsi(percorsi_G_sch_bI)
    print(f"Funzione obiettivo: {G_sch_bI_obj_val}")
    check_solution(percorsi_G_sch_bI, G_small, delta_small)
    grasp_schoolNN.append(G_sch_bI_obj_val)
    grasp_bI.append(G_sch_bI_obj_val)

    percorsi_G_sub_NN_fI, G_sub_NN_fI_obj_val, residui_dict_small_G_sub_NN_fI = GRASP_subsequent_NN(G_small, residui_dict_small, delta_small, k=2, num_greedy=5, ls = "local_search_fI", max_len=5)
    #stampa_percorsi(percorsi_G_sub_NN_fI)
    print(f"Funzione obiettivo: {G_sub_NN_fI_obj_val}")
    check_solution(percorsi_G_sub_NN_fI, G_small, delta_small)
    grasp_subsequentNN.append(G_sub_NN_fI_obj_val)

    percorsi_G_sch_fI, G_sch_fI_obj_val, residui_dict_small_G_sch_NN_fI = GRASP_School_NN(G_small,residui_dict_small, delta_small, k=2, num_greedy=5, ls = "local_search_fI", max_len=5)
    #stampa_percorsi(percorsi_G_sch_fI)
    print(f"Funzione obiettivo: {G_sch_fI_obj_val}")
    check_solution(percorsi_G_sch_fI, G_small, delta_small)
    grasp_schoolNN.append(G_sch_fI_obj_val)

    plotSubSchResults(grasp_subsequentNN, grasp_schoolNN, 'GRASP' )

    percorsi_tabu_sub, tabu_sub_obj_val, residui_dict_small_tabu_sub = tabu_search_bI(G_small, residui_dict_small_cw, percorsi_cw, cw_obj_val, delta_small, max_len=5)
    #stampa_percorsi(percorsi_sub_NN)
    print(f"Funzione obiettivo: {tabu_sub_obj_val}")
    check_solution(percorsi_tabu_sub, G_small, delta_small)
    tabu.append(tabu_sub_obj_val)

    percorsi_tabu_sub, tabu_sub_obj_val, residui_dict_small_tabu_sub = tabu_search_bI(G_small, residui_dict_small_sub_NN, percorsi_sub_NN, sub_NN_obj_val, delta_small, max_len=5)
    #stampa_percorsi(percorsi_sub_NN)
    print(f"Funzione obiettivo: {tabu_sub_obj_val}")
    check_solution(percorsi_tabu_sub, G_small, delta_small)
    tabu.append(tabu_sub_obj_val)

    percorsi_tabu_sch, tabu_sch_obj_val, residui_dict_small_tabu_sch = tabu_search_bI(G_small, residui_dict_small_sch_NN, percorsi_sch_NN, sch_NN_obj_val, delta_small, max_len=5)
    #stampa_percorsi(percorsi_sub_NN)
    print(f"Funzione obiettivo: {tabu_sch_obj_val}")
    check_solution(percorsi_tabu_sch, G_small, delta_small)
    tabu.append(tabu_sch_obj_val)

    percorsi_ILS_sub_bI, ILS_sub_bI_obj_val, residui_dict_small_ILS_sub_bI = iterated_local_search(G_small, residui_dict_small_sub_NN, percorsi_sub_NN, sub_NN_obj_val, delta_small, max_len=5, ls = "local_search_bI")
    #stampa_percorsi(percorsi_sub_NN)
    print(f"Funzione obiettivo: {ILS_sub_bI_obj_val}")
    check_solution(percorsi_ILS_sub_bI, G_small, delta_small)
    Ils_subsequentNN.append(ILS_sub_bI_obj_val)
    ils_bI.append(ILS_sub_bI_obj_val)

    percorsi_ILS_sub_fI, ILS_sub_fI_obj_val, residui_dict_small_ILS_sub_fI = iterated_local_search(G_small, residui_dict_small_sub_NN, percorsi_sub_NN, sub_NN_obj_val, delta_small, max_len=5, ls = "local_search_fI")
    #stampa_percorsi(percorsi_sub_NN)
    print(f"Funzione obiettivo: {ILS_sub_fI_obj_val}")
    check_solution(percorsi_ILS_sub_fI, G_small, delta_small)
    Ils_subsequentNN.append(ILS_sub_fI_obj_val)

    percorsi_ILS_sch_bI, ILS_sch_bI_obj_val, residui_dict_small_ILS_sch_bI = iterated_local_search(G_small, residui_dict_small_sch_NN, percorsi_sch_NN, sch_NN_obj_val, delta_small, max_len=5, ls = "local_search_bI")
    #stampa_percorsi(percorsi_sub_NN)
    print(f"Funzione obiettivo: {ILS_sch_bI_obj_val}")
    check_solution(percorsi_ILS_sch_bI, G_small, delta_small)
    Ils_schoolNN.append(ILS_sch_bI_obj_val)
    ils_bI.append(ILS_sch_bI_obj_val)

    percorsi_ILS_sch_fI, ILS_sch_fI_obj_val, residui_dict_small_ILS_sch_fI = iterated_local_search(G_small, residui_dict_small_sch_NN, percorsi_sch_NN, sch_NN_obj_val, delta_small, max_len=5, ls = "local_search_fI")
    #stampa_percorsi(percorsi_sub_NN)
    print(f"Funzione obiettivo: {ILS_sch_fI_obj_val}")
    check_solution(percorsi_ILS_sch_fI, G_small, delta_small)
    Ils_schoolNN.append(ILS_sch_fI_obj_val)

    plotSubSchResults(Ils_subsequentNN, Ils_schoolNN, 'ILS')

    plotMetaheuristicsResults(grasp_bI, tabu, ils_bI)