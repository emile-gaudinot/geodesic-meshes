"""
A partir d'un nuage de points .csv (sans tabulations), on arrive à générer une image qui
permet de visualiser les distances géodésiques grâce à un dégradé.
Les problèmes d'échelle ont été réglés. Le faible de nombre de point a été
augmenté (1min16 pour 5726 points).
"""

import potpourri3d as pp
import numpy as np
from matplotlib import pyplot as plt
import time
import csv
#from mpl_toolkits.mplot3d import axes3d, Axes3D


def tps(t):
  print('Temps d\'exécution :', int((time.time()-t)//60), 'min',
int((time.time()-t)%60), 's')
  
# afficher les points en dégradé du 0 au 665
def degrade(X, Y):
  col = np.arange(len(X))
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.scatter(X, Y, s=20, c=col, marker='o')
  plt.show()
  
# renvoie liste des bords et leur indice dans VV
def bordsTab(points):
  bords = []
  for i in range(1):
    b = points[i]
    bords.append([i, b])
  return bords
  
# renvoie la distance géodésique d'un point quelconque au bord
def distBord(S, solver, bords):
  dist = solver.compute_distance(S) # dist entre S et ts les sommets
  distMin = dist[bords[0][0]]
  for B in bords:
    i, b = B
    d = dist[i] # distance entre S et sommet i du bord
    if d < distMin:
      distMin = d
  return distMin

def csv2array(nom):
  file = open(nom)
  csvreader = csv.reader(file)
  header = next(csvreader)
  rows = []
  
  for row in csvreader:
    rows.append(row)
    file.close()
    
  string_points = np.array(rows)
  points = string_points.astype(np.float64)
  
  #Pb avec le vertice 575, stackoverflow nous dit d'appliquer un jitter
  jitter = np.random.rand(len(points))/100
  points[:,0] = points[:,0] + jitter
  
  return points
  
# afficher des lignes de niveau en fonction des distances géodésiques
def lignesNiveau(points, nbNiveaux=25, ratioPlusGdeDist=1):
  t = time.time()
  print('Nombre de points :', len(points))
  solver = pp.PointCloudHeatSolver(points) #ne nécessite pas les faces !
  #solver = pp.MeshHeatMethodDistanceSolver(VV, FF)
  bords = bordsTab(points)
  dist = solver.compute_distance(bords[0][0])
  distMaxEntre2Points = max(dist) * ratioPlusGdeDist # valeur arbitraire
  X, Y, Z, couleurs = [], [], [], []
  
  for S in range(len(points)):
    distanceAuBord = distBord(S, solver, bords)
    c = int(distanceAuBord / distMaxEntre2Points * nbNiveaux)
    couleurs.append(c)
    x, y, z = points[S]
    X.append(x)
    Y.append(y)
    Z.append(z)
  
  # affichage graphique
  cmap = plt.cm.Spectral
  norm = plt.Normalize(vmin=0, vmax=nbNiveaux)
  ax = plt.axes(projection ="3d")
  ax.set_xlabel('x')
  ax.set_ylabel('y')
  ax.set_zlabel('z')
  
  #on change les limites selon les 3 axes
  m, M = 20, 75
  ax.set_xlim(m, M)
  ax.set_ylim(m, M)
  ax.set_zlim(m, M)
  
  #on plot
  ax.scatter3D(X, Y, Z, s=30, c=cmap(norm(couleurs)))
  plt.show()
  
  tps(t)

points = csv2array('Resultlines/resultline1_0.3SansTabulation.csv')
lignesNiveau(points)
