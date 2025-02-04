from crea_visualizza_istanza import *

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