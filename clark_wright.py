import copy
from utils import timeit
from funzione_obiettivo import *
from controlli_ammissibilita import *


def creazione_petali(G, residui_dict, delta):
  """
  Step 1 alg. Clarke and Wright: creazione petali.
  Ogni bambino è associato ad un percorso diverso
  """

  percorsi = []

  for node in G.nodes():
    percorso = ['Scuola']
    if node != 'Scuola':
      percorso.append(node)
      percorsi.append(percorso)

  return percorsi

def best_merge(G, residui_dict, percorsi, delta):
  """
  Restituisce il miglior merge tra i percorsi: 
  la coppia di percorsi che, se uniti, massimizzano i residui 
  dei nodi del percorso che si viene a creare.
  """

  residui_dict_copy = copy.deepcopy(residui_dict)
  percorsi_copy = copy.deepcopy(percorsi)
  best_residui = float('-inf')
  best_merge = None
  best_residui_dict = None

  for i in range(len(percorsi_copy)):
    for j in range(len(percorsi_copy)):
      if i == j:
        continue


      percorso_test = percorsi_copy[i] + percorsi_copy[j][1:]


      if test_percorso_feasibility(percorso_test, G, delta):

          residui_dict_temp = calcola_residui_nodi_percorso(G, residui_dict_copy, percorso_test, delta)
          residui = sum(residui_dict_copy[nodo]for nodo in percorso_test if nodo != 'Scuola')

          if residui > best_residui:
              best_residui = residui
              best_merge = (percorso_test, i, j)
              best_residui_dict = copy.deepcopy(residui_dict_temp)

  return best_merge, best_residui_dict

def merging_petali(G, residui_dict, percorsi, delta):
  """
  Step 2 alg. Clarke and Wright: unione petali.
  Si prova ad unire ogni coppia di percorsi in modo da massimizzare i residui.
  """
  residui_dict_copy = copy.deepcopy(residui_dict)
  percorsi_copy = copy.deepcopy(percorsi)

  while True:
        merge, residui_dict_temp = best_merge(G, residui_dict_copy, percorsi_copy, delta)

        if merge is None:
            break
        #merge, residui_dict_copy = ris
        percorso_merge, i, j = merge

        percorsi_copy = [p for k,p in enumerate(percorsi_copy) if  k != i and k != j]

        percorsi_copy.append(percorso_merge)
        residui_dict_copy = residui_dict_temp


  return percorsi_copy, residui_dict_copy





@timeit
def clark_wright(G, residui_dict, delta):
  """
  Algoritmo di Clarke and Wright
  """
  residui_dict_copy = copy.deepcopy(residui_dict)
  percorsi = creazione_petali(G, residui_dict_copy, delta)
  percorsi, residui_dict_copy = merging_petali(G, residui_dict_copy, percorsi, delta)

  obj_val = objective_function(percorsi,G)

  return percorsi, obj_val, residui_dict_copy