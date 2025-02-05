import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from crea_visualizza_istanza import save_img

def plotSubSchResults(subsequentNN, schoolNN, name, img):

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



    x = np.arange(len(labels))  # the label locations
    width = 0.20  # the width of the bars
    cm = 1/2.54  # centimeters in inches
    fig, ax = plt.subplots(figsize=(20*cm, 15*cm))

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    rects1 = ax.bar(x - width/2, schoolNN, width, label=f'{name} School NN', color=colors[0])
    rects2 = ax.bar(x + width/2, subsequentNN, width, label=f'{name} Subsequent NN', color=colors[1])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(f'Risultati {name}')
    ax.set_title('Valore funzione obiettivo')
    ax.set_xticks(x, labels)
    ax.legend()

    # Format
    ax.bar_label(rects1, padding=3, labels=[f'{int(v)}' for v in rects1.datavalues], fmt='%d')
    ax.bar_label(rects2, padding=3, labels=[f'{int(v)}' for v in rects2.datavalues], fmt='%d')


    #ax.bar_label(rects1, padding=3)
    #ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    save_img(img)

    # Mostra il grafico
    plt.show(block=False)


def plotMetaheuristicsResults(grasp, tabu, ils, img):

    labels = ['Greedy Subsequent NN', 'Greedy School NN']


    x = np.arange(len(labels))  # the label locations
    width = 0.25  # the width of the bars
    cm = 1/2.54  # centimeters in inches
    fig, ax = plt.subplots(figsize=(30*cm, 20*cm))

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    # Centra le barre rispetto ai tick sull'asse x
    rects1 = ax.bar(x - width, grasp, width, label='Grasp', color='#49bff5')  # Grasp
    rects2 = ax.bar(x, tabu, width, label='Tabu Search', color='#fca103')  # Tabu Search
    rects3 = ax.bar(x + width, ils, width, label='Iterated Local Search', color='#fc0335')  # Iterated Local Search


    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Risultati Metaeuristiche')
    ax.set_title('Valore funzione obiettivo')
    ax.set_xticks(x, labels)
    ax.legend()

    # Format
    ax.bar_label(rects1, padding=3, labels=[f'{int(v)}' for v in rects1.datavalues], fmt='%d')
    ax.bar_label(rects2, padding=3, labels=[f'{int(v)}' for v in rects2.datavalues], fmt='%d')
    ax.bar_label(rects3, padding=3, labels=[f'{int(v)}' for v in rects3.datavalues], fmt='%d')


    #ax.bar_label(rects1, padding=3)
    #ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    save_img(img)

    # Mostra il grafico
    plt.show(block=False)


def plot_all_results(results, img):
    width = 0.25  # the width of the bars
    cm = 1 / 2.54  # centimeters in inches
    fig, ax = plt.subplots(figsize=(30 * cm, 20 * cm))

    # Etichette degli assi X
    x_labels = ['greedy subsequent NN', 'greedy school NN', 'ls best Imp subsequent NN', 'ls first Imp subsequent NN', 'ls best Imp school NN', 
                'ls first Imp school NN', 'grasp best Imp subsequent NN', 'grasp first Imp subsequent NN', 'grasp best Imp school NN',
                'grasp first Imp school NN', 'tabu subsequent NN', 'tabu school NN', 'ils best Imp subsequent NN', 'ils first Imp subsequent NN',
                'ils best Imp school NN', 'ils first Imp school NN']

    # Numero di elementi da rappresentare
    n = len(results)

    # Genera colori da una mappa di colori
    colors = [plt.cm.get_cmap('rainbow')(i / n) for i in range(n)]

    # Grafico a barre
    rects = ax.bar(x_labels, results, color=colors)

    # Formatta i numeri sull'asse Y
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    # Etichette per le barre - usiamo rects (BarContainer)
    ax.bar_label(rects, fmt='%d')

    # Aggiungi etichette e titolo
    ax.set_ylabel('Valore funzione obiettivo')
    ax.set_title('Risultati complessivi')

    # Ruota le etichette dell'asse X
    plt.xticks(rotation=-25)

    # Salva l'immagine
    save_img(img)

    # Mostra il grafico
    plt.show(block=False)

# Definisci una funzione per formattare l'asse delle y in minuti
def minutes_formatter(x, pos):
    return f'{int(x)} min'  # Formatta il valore come minuti



def plot_time_results(results, img):
  
  width = 0.25  # the width of the bars
  cm = 1/2.54  # centimeters in inches
  fig, ax = plt.subplots(figsize=(30*cm, 20*cm))
  

  x_labels = ['greedy subsequent NN', 'greedy school NN', 'ls best Imp subsequent NN', 'ls first Imp subsequent NN', 'ls best Imp school NN', 
              'ls first Imp school NN', 'grasp best Imp subsequent NN', 'grasp first Imp subsequent NN', 'grasp best Imp school NN',
              'grasp first Imp school NN', 'tabu subsequent NN', 'tabu school NN', 'ils best Imp subsequent NN', 'ils first Imp subsequent NN',
              'ils best Imp school NN', 'ils first Imp school NN' ]


    # Numero di elementi da rappresentare
  n = len(results)

  # Genera colori da una mappa di colori
  colors = [plt.cm.get_cmap('rainbow')(i / n) for i in range(n)]

  # Grafico a barre
  rects = ax.bar(x_labels, results, color=colors)
  
  ax.bar(x_labels, results, color=colors)
  # Applica il formattatore all'asse y
  plt.gca().yaxis.set_major_formatter(FuncFormatter(minutes_formatter))

  # Etichette per le barre(BarContainer)
  ax.bar_label(rects, fmt='%d')

  
  ax.set_ylabel('Valore funzione obiettivo')
  ax.set_title('Risultati complessivi')
  
  # Rotating X-axis labels
  plt.xticks(rotation = -25)
  save_img(img)

  # Mostra il grafico
  plt.show(block=False)