from crea_visualizza_istanza import *
from istanza_small import *
from istanza_media import *

def main():
    delta_toy = 1.5
    G_toy, residui_dict_toy = generate_instance(num_bambini=10, pos_min=5, pos_max=50, seed=10, delta= delta_toy)
    plot_graph(G_toy, 'grafo_toy.png')



    #Stampo i nodi e le relative posizioni
    for node, data in G_toy.nodes(data=True):
        print(f"Nodo: {node}, Posizione: {data['pos']}, Massima Distanza: {data['max_distance']}")

    #print("\n")

    #Stampo gli archi e i relativi pesi
    #for u, v, data in G_small.edges(data=True):
    #    print(f"Arco: {u} - {v}, Peso: {data['weight']}")

    percorsi_sub_NN, sub_NN_obj_val, residui_dict_toy_sub_NN = subsequent_nearest_neighbour(G_toy, residui_dict_toy, delta_toy)
    stampa_percorsi(percorsi_sub_NN)
    print(f"Funzione obiettivo: {sub_NN_obj_val}")
    check_solution(percorsi_sub_NN, G_toy, delta_toy)
    plot_graph_results( G_toy, percorsi_sub_NN, 'G_toy_results')

    ##ISTANZA SMALL

    istanza_small_main()
    istanza_media_main()


if __name__ == '__main__':
    main()