import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker
import numpy as np
from crea_visualizza_istanza import save_img



def plotSubSchResults(subsequentNN, schoolNN, name, img):
    """
    Crea un grafico a barre che mostra i risultati ottenuti.
    Due barre per ogni tick, uno per la versione dell'algoritmo che usa la greedy subsequent NN 
    e uno per la greedy school NN.
    """

    if name == "Greedy":
      labels = ['Greedy', 'Gr Rand']
      colors = ['#03fcc2','#39996a' ] #verde
    elif name == "Ls":
      labels = ['Best Imp', 'First Imp']
      colors =['#8803fc', '#c286f7'] #viola
    elif name == "GRASP":
      labels = ['Best Imp', 'First Imp']
      colors =['#49bff5', '#036bfc'] #blu
    elif name == "Tabu":
      labels = ['Best Imp', 'First Imp']
      colors =['#fca103', '#fcc603'] #arancio
    elif name == "ILS":
      labels = ['Best Imp', 'First Imp']
      colors =['#fc0335', '#ed728a'] #rosso
    else:
      print("Errore, name non valido!")



    x = np.arange(len(labels))  # Posizioni delle etichette
    width = 0.20  
    cm = 1/2.54  
    fig, ax = plt.subplots(figsize=(20*cm, 15*cm))

    # Formatta i numeri sull'asse Y come interi
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    # Crea le barre
    rects1 = ax.bar(x - width/2, schoolNN, width, label=f'{name} School NN', color=colors[0])
    rects2 = ax.bar(x + width/2, subsequentNN, width, label=f'{name} Subsequent NN', color=colors[1])


    ax.set_ylabel(f'Risultati {name}')
    ax.set_title('Valore funzione obiettivo')
    ax.set_xticks(x, labels)
    ax.legend()

    # Formatta le etichette delle barre
    ax.bar_label(rects1, padding=3, labels=[f'{int(v)}' for v in rects1.datavalues], fmt='%d')
    ax.bar_label(rects2, padding=3, labels=[f'{int(v)}' for v in rects2.datavalues], fmt='%d')

    fig.tight_layout()

    save_img(img)

    # Mostra il grafico
    plt.show(block=False)






def plotBestFirstResults(best, first, name, img):
    """
    Crea un grafico a barre che mostra i risultati ottenuti.
    Due barre per ogni tick, uno per la versione dell'algoritmo che usa la best improvement
    e uno per la first improvement.
    """

    if name == "Ls":
      colors =['#8803fc', '#c286f7'] #viola
    elif name == "GRASP":
      colors =['#49bff5', '#036bfc'] #blu
    elif name == "Tabu":
      colors =['#fca103', '#fcc603'] #arancio
    elif name == "ILS":
      colors =['#fc0335', '#ed728a'] #rosso
    else:
      print("Errore, name non valido!")

    labels = ['Subsequent NN', 'School NN']

    x = np.arange(len(labels))  # posizione etichette
    width = 0.20  
    cm = 1/2.54
    fig, ax = plt.subplots(figsize=(20*cm, 15*cm))

    # Formatta i numeri sull'asse Y come interi
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    rects1 = ax.bar(x - width/2, best, width, label=f'{name} Best Improvement', color=colors[0])

    if name != "Tabu":
      rects2 = ax.bar(x + width/2, first, width, label=f'{name} First Improvement', color=colors[1])
    else:
      rects2 = ax.bar(x + width/2, first, width, label=f'{name} Adapted First Improvement', color=colors[1])

    ax.set_ylabel(f'Risultati {name}')
    ax.set_title('Valore funzione obiettivo')
    ax.set_xticks(x, labels)
    ax.legend()

  
    ax.bar_label(rects1, padding=3, labels=[f'{int(v)}' for v in rects1.datavalues], fmt='%d')
    ax.bar_label(rects2, padding=3, labels=[f'{int(v)}' for v in rects2.datavalues], fmt='%d')


    fig.tight_layout()
    save_img(img)
    plt.show(block=False)








def plotMetaheuristicsResults(grasp, tabu, ils, img, bestImp = True):
    """
    Crea un grafico a barre che mostra i risultati ottenuti.
    Tre barre per tick, uno per ogni metaeuristica.
    Due tick sull'asse X: uno per la greedy subsequent NN e uno per la greedy school NN.
    """

    labels = ['Greedy Subsequent NN', 'Greedy School NN']


    x = np.arange(len(labels))  
    width = 0.25  
    cm = 1/2.54 
    fig, ax = plt.subplots(figsize=(30*cm, 20*cm))

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    # Centra le barre rispetto ai tick sull'asse x
    rects1 = ax.bar(x - width, grasp, width, label='Grasp', color='#49bff5')  # Grasp
    rects2 = ax.bar(x, tabu, width, label='Tabu Search', color='#fca103')  # Tabu Search
    rects3 = ax.bar(x + width, ils, width, label='Iterated Local Search', color='#fc0335')  # Iterated Local Search


    if bestImp == True:
      ax.set_ylabel('Risultati Metaeuristiche (best improvement)')
    else:
       ax.set_ylabel('Risultati Metaeuristiche (first improvement)')
    ax.set_title('Valore funzione obiettivo')
    ax.set_xticks(x, labels)
    ax.legend()


    ax.bar_label(rects1, padding=3, labels=[f'{int(v)}' for v in rects1.datavalues], fmt='%d')
    ax.bar_label(rects2, padding=3, labels=[f'{int(v)}' for v in rects2.datavalues], fmt='%d')
    ax.bar_label(rects3, padding=3, labels=[f'{int(v)}' for v in rects3.datavalues], fmt='%d')

    fig.tight_layout()
    save_img(img)
    plt.show(block=False)









def plot_all_results(results, img, cw=False):
    """
    Crea un grafico a barre che mostra i risultati complessivi ottenuti.
    Una barra per ogni algoritmo.
    """
    width = 0.25  
    cm = 1 / 2.54  
    fig, ax = plt.subplots(figsize=(70 * cm, 30 * cm))

    # Etichette degli assi X
    x_labels = ['greedy subsequent NN', 'greedy school NN', 'greedy Rand subsequent NN', 'greedy Rand school NN', 
            'ls best Imp subsequent NN', 'ls first Imp subsequent NN', 'ls best Imp school NN', 'ls first Imp school NN', 
            'grasp best Imp subsequent NN', 'grasp first Imp subsequent NN', 'grasp best Imp school NN','grasp first Imp school NN', 
            'tabu best Imp subsequent NN', 'tabu first Imp subsequent NN', 'tabu best Imp school NN', 'tabu first Imp school NN',
            'ils best Imp subsequent NN', 'ils first Imp subsequent NN', 'ils best Imp school NN', 'ils first Imp school NN']
    
    # Aggiungi Clark-Wright se richiesto
    if cw == True:
       x_labels.append('Clark-Wright')


    # Numero di elementi da rappresentare
    n = len(results)

    # Genera colori da una mappa di colori
    colors = [plt.cm.get_cmap('rainbow')(i / n) for i in range(n)]

    # Grafico a barre
    rects = ax.bar(x_labels, results, color=colors)

    # Formatta i numeri sull'asse Y come interi
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    ax.bar_label(rects, fmt='%d')
    ax.set_ylabel('Valore funzione obiettivo')
    ax.set_title('Risultati complessivi')

    # Ruota le etichette dell'asse X
    plt.xticks(rotation=-25)
    fig.tight_layout()
    save_img(img)
    plt.show(block=False)









def plot_greedy_based_results(results, img, name):
    """
    Crea un grafico a barre che mostra i risultati ottenuti.
    Due barre per ogni tick, una per la versione dell'algoritmo che usa la greedy subsequent NN 
    e uno per la versione che usa la greedy school NN.
    """
    width = 0.20  
    cm = 1 / 2.54 
    fig, ax = plt.subplots(figsize=(40 * cm, 30 * cm))

    if name == "SubsequentNN":
      # Etichette degli assi X
      x_labels = ['greedy subsequent NN', 'greedy Rand subsequent NN', 
              'ls best Imp subsequent NN', 'ls first Imp subsequent NN', 
              'grasp best Imp subsequent NN', 'grasp first Imp subsequent NN', 
              'tabu best Imp subsequent NN', 'tabu first Imp subsequent NN', 
              'ils best Imp subsequent NN', 'ils first Imp subsequent NN']
    elif name == "SchoolNN":
      # Etichette degli assi X
      x_labels = ['greedy school NN', 'greedy Rand school NN', 
              'ls best Imp school NN', 'ls first Imp school NN', 
              'grasp best Imp school NN', 'grasp first Imp school NN', 
              'tabu best Imp school NN', 'tabu first Imp school NN', 
              'ils best Imp school NN', 'ils first Imp school NN']
    else:
      print("Errore, name non valido!")
      
    # Numero di elementi da rappresentare
    n = len(results)

    # Genera colori da una mappa di colori
    colors = [plt.cm.get_cmap('rainbow')(i / n) for i in range(n)]

    # Grafico a barre
    rects = ax.bar(x_labels, results, color=colors)

    # Formatta i numeri sull'asse Y
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    ax.bar_label(rects, fmt='%d')


    ax.set_ylabel('Valore funzione obiettivo')
    ax.set_title('Risultati complessivi')

    # Ruota le etichette dell'asse X
    plt.xticks(rotation=-25)
    fig.tight_layout()

    # Salva l'immagine
    save_img(img)
    plt.show(block=False)






# Funzione per formattare l'asse delle y in secondi
def seconds_formatter(x, pos):
    return f'{int(x)} sec' 






# Funzione per formattare l'asse delle y in minuti
def minutes_formatter(x, pos):
    minutes = x / 60  # Converte i secondi in minuti
    return f'{int(minutes)} min'  # Formatta il valore come minuti






# Funzione per formattare il tempo in ore, minuti e secondi
def time_formatter(x):
    hours = int(x // 3600)
    minutes = int((x % 3600) // 60)
    seconds = int(x % 60)
    return f'{hours}h {minutes}m {seconds}s'






# Funzione per formattare il tempo in minuti, secondi e millisecondi
def time_formatter_small(x):
    hours = int(x // 3600)
    minutes = int((x % 3600) // 60)
    seconds = int(x % 60)
    milliseconds = int((x - int(x)) * 1000)  # Calcola i millisecondi
    return f'{minutes}m {seconds}s {milliseconds}ms'








def plot_time_results(results, img, medium=True, cw=False):
    """
    Crea un grafico a barre che mostra i tempi di esecuzione.
    Una barra per ogni algoritmo con il tempo impiegato.
    """
   
    width = 0.2 
    cm = 1 / 2.54 
    fig, ax = plt.subplots(figsize=(70 * cm, 30 * cm))

    # Etichette degli assi X
    x_labels = ['greedy subsequent NN', 'greedy school NN', 'greedy Rand subsequent NN', 'greedy Rand school NN', 
            'ls best Imp subsequent NN', 'ls first Imp subsequent NN', 'ls best Imp school NN', 'ls first Imp school NN', 
            'grasp best Imp subsequent NN', 'grasp first Imp subsequent NN', 'grasp best Imp school NN','grasp first Imp school NN', 
            'tabu best Imp subsequent NN', 'tabu first Imp subsequent NN', 'tabu best Imp school NN', 'tabu first Imp school NN',
            'ils best Imp subsequent NN', 'ils first Imp subsequent NN', 'ils best Imp school NN', 'ils first Imp school NN']
    
    # Aggiungi Clark-Wright se richiesto
    if cw == True:
       x_labels.append('Clark-Wright')


    # Numero di elementi da rappresentare
    n = len(results)

    # Genera colori da una mappa di colori
    colors = [plt.cm.get_cmap('rainbow')(i / n) for i in range(n)]

    # Grafico a barre
    rects = ax.bar(x_labels, results, color=colors)

    if medium :
      # Applica il formattatore all'asse Y
      plt.gca().yaxis.set_major_formatter(FuncFormatter(minutes_formatter))
      # Crea etichette per le barre (BarContainer)
      labels = [time_formatter(x) for x in results]  # Usa i valori di 'results' per formattare il tempo
    else:
       # Applica il formattatore all'asse Y
      plt.gca().yaxis.set_major_formatter(FuncFormatter(seconds_formatter))
      # Crea etichette per le barre (BarContainer)
      labels = [time_formatter_small(x) for x in results]  # Usa i valori di 'results' per formattare il tempo
       

    # Etichette per le barre
    ax.bar_label(rects, labels=labels, padding=3)

    # Aggiungi etichetta e titolo
    ax.set_ylabel('Valore funzione obiettivo')
    ax.set_title('Risultati complessivi')

    # Ruota le etichette dell'asse X
    plt.xticks(rotation=-25)

    # Salva l'immagine
    save_img(img)
    plt.show(block=False)










def plot_solution_over_time(time_in_seconds, obj_vals, name, img):
    """
    Grafica l'andamento del valore della funzione obiettivo nel tempo
    """
    # Converti il tempo in minuti
    time_in_minutes = np.array(time_in_seconds) / 60
    
    # Controlla se l'ultimo elemento di time_in_minutes ha parte intera 0
    if int(time_in_minutes[-1]) == 0:
        x = np.array(time_in_seconds)
        x_label = 'Tempo (secondi)'
    else:
        x = time_in_minutes
        x_label = 'Tempo (minuti)'
    
    y = np.array(obj_vals)
    plt.scatter(x, y, color='#10a0e8')
    plt.plot(x, y, color='#10a0e8')

    # Trova il valore minimo e il suo indice
    min_val = np.min(y)
    min_idx = np.argmin(y)

    # Evidenzia il valore minimo con un colore diverso
    plt.scatter(x[min_idx], min_val, color='#081dd4', zorder=5)
    plt.axhline(y=min_val, color='#081dd4', linestyle='--')
    plt.text(x[min_idx], min_val, f'{min_val:,}', color='#081dd4', verticalalignment='bottom')

    ax = plt.gca()

    # Formatta i numeri sull'asse Y
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    # Imposta i tick dell'asse X per mostrare solo numeri interi
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Aggiungi etichette e titolo
    plt.xlabel(x_label)
    plt.ylabel('Valore funzione obiettivo dell\'ottimo candidato')
    plt.title(f'Andamento obj_val dell\'incumbent nel tempo ({name})')

    # Salva l'immagine
    save_img(img)

    plt.show()
  