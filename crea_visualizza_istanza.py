import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def save_img(name):
  """
  Salva l'immagine corrente in un file con il nome specificato.
  """
  plt.savefig(name, bbox_inches='tight')


def plot_graph(G, name_img):
  """
  Disegna un grafo con i nodi posizionati in base alle coordinate (x, y) specificate per ciascun nodo.

  Args:
      G: Grafo da disegnare.
      name_img: Nome dell'immagine da salvare.
  """

  # Crea una lista di tutti i nodi nel grafo
  node_list = list(G.nodes())

  # Crea un dizionario che mappa ogni nodo alla sua posizione (x, y)
  # Le posizioni sono estratte dall'attributo 'pos' di ogni nodo nel grafo
  pos = {node: G.nodes[node]['pos'] for node in node_list}


  # dimensione 8x8 pollici
  plt.figure(figsize=(8, 8))

  # Disegna il grafo usando le posizioni specificate
  # with_labels=True mostra le etichette dei nodi
  nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)

  # Ottiene gli attributi 'weight' (pesi) di tutti gli archi nel grafo
  edge_labels = nx.get_edge_attributes(G, 'weight')

  # Disegna le etichette degli archi con i pesi, formattati 
  # edge_labels è un dizionario che mappa ogni arco al suo peso
  nx.draw_networkx_edge_labels(G, pos, edge_labels={(i, j): f"{d['weight']:.0f}" for (i, j, d) in G.edges(data=True)})

  plt.title("Grafo con pesi che riflettono le distanze euclidee")

  save_img(name_img)
  plt.show(block=False)









def plot_graph_results(G, percorsi, name_img):
  """
  Disegna un grafo con i nodi posizionati in base alle coordinate (x, y) specificate per ciascun nodo.
  Disegna anche i percorsi specificati nel grafo, con colori diversi per ciascun percorso.

  Args:
      G: Grafo da disegnare.
      percorsi: Una lista di percorsi. Ogni percorso è una lista di nodi.
      name_img: Nome dell'immagine da salvare.
  """

  # Crea una lista di tutti i nodi nel grafo
  node_list = list(G.nodes())

  # Crea un dizionario che mappa ogni nodo alla sua posizione (x, y)
  # Le posizioni sono estratte dall'attributo 'pos' di ogni nodo nel grafo
  pos = {node: G.nodes[node]['pos'] for node in node_list}

  plt.figure(figsize=(8, 8))

  # Numero di elementi da rappresentare
  n = len(percorsi)

  # Genera colori da una mappa di colori
  colors = [plt.cm.get_cmap('rainbow')(i / n) for i in range(n)]

  # Disegna il grafo usando le posizioni specificate
  nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='lightblue', font_size=10)

  # Disegna il grafo
  for i,p in enumerate(percorsi):
    nx.draw_networkx_edges(G, pos, edgelist=list(zip(p[:-1], p[1:])), edge_color=colors[i], width=2)
    p.remove("Scuola")
    nx.draw_networkx_nodes(G, pos, nodelist=p, node_color=colors[i], node_size=500)


  # Ottiene gli attributi 'weight' (pesi) di tutti gli archi nel grafo
  edge_labels = nx.get_edge_attributes(G, 'weight')

  # Disegna le etichette degli archi con i pesi, formattati
  # edge_labels è un dizionario che mappa ogni arco al suo peso
  nx.draw_networkx_edge_labels(G, pos, edge_labels={(i, j): f"{d['weight']:.0f}" for (i, j, d) in G.edges(data=True)})

  plt.title("Grafo risultante")

  save_img(name_img)
  plt.show(block=False)








def stampa_percorsi(percorsi):
    """
    Stampa la rappresentazione visiva dei percorsi, numerandoli e
    mostrando la sequenza di nodi connessi da frecce.

    Args:
        percorsi: Una lista di percorsi. Ogni percorso è una lista di nodi.
    """
   
    print("### Visualizzazione dei Percorsi ###\n")

    # Itera attraverso la lista di percorsi usando enumerate per ottenere sia l'indice (i) che il percorso
    # start=1 fa sì che l'indice parta da 1 invece che da 0 (il primo elemento ha quindi indice 1)

    for i, percorso in enumerate(percorsi, start=1):
        # Converte il percorso (lista di nodi) in una stringa leggibile,
        # unendo i nodi con il simbolo " → "
        percorso_str = " - ".join(percorso)  # Combina i nodi con la freccia

        print(f"Percorso {i}: {percorso_str}")







def generate_instance(num_bambini, pos_min, pos_max, seed, delta):
    """
    Genera un'istanza del problema "Pedibus" come un grafo.

    Args:
        num_bambini: Il numero di bambini (nodi) da generare.
        pos_min: Il valore minimo per le coordinate x e y delle posizioni dei nodi.
        pos_max: Il valore massimo per le coordinate x e y delle posizioni dei nodi.
        seed: Il seed per il generatore di numeri casuali (per la riproducibilità).
        delta: Il fattore di tolleranza per la distanza percorribile da ogni bambino.

    Returns:
        Un grafo networkx che rappresenta l'istanza del problema.
    """


    scuola = "Scuola"

    # Imposta il seed per il generatore di numeri casuali di numpy se viene fornito
    if seed is not None:
        np.random.seed(seed)

    # Crea una lista di nomi di nodi per i bambini e aggiunge il nodo della scuola
    nodi = [f"Bambino_{i+1}" for i in range(num_bambini)] + [scuola]

    # Genera posizioni casuali (x, y) per ogni nodo (bambino e scuola)
    # Le posizioni sono all'interno di un rettangolo definito da pos_min e pos_max
    positions = np.array([(np.random.rand(2) * (pos_max - pos_min) + pos_min) for _ in range(len(nodi))])

    # Calcola la matrice delle distanze euclidee tra tutti i nodi
    weights_f = np.linalg.norm(positions[:, None, :] - positions[None, :, :], axis=2)
    # Converte le distanze in interi
    weights = weights_f.astype(int)

    # Imposta la diagonale della matrice delle distanze a -1 (distanza di un nodo da se stesso)
    np.fill_diagonal(weights, -1)

    # Se ci sono distanze pari a 0 (oltre alla diagonale), aggiungi 1 per evitare problemi
    if np.any(weights == 0):
        weights += 1

    # Reimposta la diagonale della matrice delle distanze a 0
    np.fill_diagonal(weights, 0)

    # Crea un grafo non orientato usando la libreria networkx
    G = nx.Graph()

    # Aggiunge ogni nodo al grafo con la sua posizione
    for i, node in enumerate(nodi):
        G.add_node(node, pos=positions[i])

    # Aggiunge gli archi al grafo, collegando ogni coppia di nodi con il peso corrispondente alla distanza tra loro
    for i in range(len(nodi)):
        for j in range(i + 1, len(nodi)):
            G.add_edge(nodi[i], nodi[j], weight=weights[i, j])

    residui_dict = dict()

    for node in G.nodes():
      if node != "Scuola":
        G.nodes[node]['max_distance'] = delta * G[node]["Scuola"]['weight'] #Aggiungo attributo relativo alla distanza massima che ciascun bambino può percorrere
        residui_dict[node] = delta * G[node]["Scuola"]['weight'] #distanza residua che ciascun bambino può ancora percorrere
      else:
        G.nodes[node]['max_distance'] = 0 #Scuola ha distanza massima nulla
        residui_dict[node] = 0 #Scuola ha residuo nullo



    # Restituisce il grafo creato
    return G, residui_dict
