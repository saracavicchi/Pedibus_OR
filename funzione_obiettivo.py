def objective_function(percorsi, G):
    """
    Calcola la funzione obiettivo come:
    - Penalità per il numero di percorsi (minimizzare `len(percorsi)`).
    - Somma delle lunghezze/distanze dei percorsi.

    Parametri:
    - percorsi: lista di percorsi (ogni percorso è una lista di nodi del grafo G).
    - G: grafo NetworkX che contiene i nodi e i loro attributi.

    Ritorna:
    - Valore della funzione obiettivo.
    """
    M = 100000  # Penalità per il numero di percorsi

    # Penalità per il numero di percorsi
    penalita_percorsi = M * len(percorsi)

    # Calcola la somma dei pesi dei nodi nei percorsi
    somma_dist = 0
    for p in percorsi:
        for i,nodo in enumerate(p):
            if i == len(p) - 1: # Se è l'ultimo nodo del percorso, esci
                break
            j = i+1
            nodo_dest = p[j]
            somma_dist = somma_dist + G[nodo][nodo_dest]["weight"]


    # Calcola il valore totale della funzione obiettivo
    obj = penalita_percorsi + somma_dist
    return obj
