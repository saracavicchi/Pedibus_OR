from crea_visualizza_istanza import *
from istanza_small import *

def main():
    delta_toy = 1.5
    G_toy, residui_dict_small = generate_instance(num_bambini=10, pos_min=5, pos_max=50, seed=10, delta= delta_toy)
    plot_graph(G_toy, 'grafo_toy.png')


    #Stampo i nodi e le relative posizioni
    for node, data in G_toy.nodes(data=True):
        print(f"Nodo: {node}, Posizione: {data['pos']}, Massima Distanza: {data['max_distance']}")

    #print("\n")

    #Stampo gli archi e i relativi pesi
    #for u, v, data in G_small.edges(data=True):
    #    print(f"Arco: {u} - {v}, Peso: {data['weight']}")



    ##ISTANZA SMALL
    istanza_small_main()


if __name__ == '__main__':
    main()