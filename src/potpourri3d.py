"""
From a .csv point cloud (without tabs), this script generates an image that
visualizes geodesic distances using a gradient.
Scale issues have been resolved. The low number of points has been increased
(1min16 for 5726 points).
"""

import potpourri3d as pp
import numpy as np
from matplotlib import pyplot as plt
import time
import csv
# from mpl_toolkits.mplot3d import axes3d, Axes3D


def tps(t):
  print('Execution time:', int((time.time()-t)//60), 'min', int((time.time()-t)%60), 's')
  
# Display points using a gradient from 0 to 665
def degrade(X, Y):
  col = np.arange(len(X))
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.scatter(X, Y, s=20, c=col, marker='o')
  plt.show()
  
# Returns the list of boundaries and their index in VV
def bordsTab(points):
  bords = []
  for i in range(1):
    b = points[i]
    bords.append([i, b])
  return bords
  
# Returns the geodesic distance from any point to the boundary
def distBord(S, solver, bords):
  dist = solver.compute_distance(S)  # distances between S and all vertices
  distMin = dist[bords[0][0]]
  for B in bords:
    i, b = B
    d = dist[i]  # distance between S and vertex i of the boundary
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
  
# Display contour lines based on geodesic distances
def lignesNiveau(points, nbNiveaux=25, ratioPlusGdeDist=1):
  t = time.time()
  print('Number of points:', len(points))
  solver = pp.PointCloudHeatSolver(points)  # does not require faces!
  # solver = pp.MeshHeatMethodDistanceSolver(VV, FF)
  bords = bordsTab(points)
  dist = solver.compute_distance(bords[0][0])
  distMaxEntre2Points = max(dist) * ratioPlusGdeDist  # arbitrary value
  X, Y, Z, couleurs = [], [], [], []
  
  for S in range(len(points)):
    distanceAuBord = distBord(S, solver, bords)
    c = int(distanceAuBord / distMaxEntre2Points * nbNiveaux)
    couleurs.append(c)
    x, y, z = points[S]
    X.append(x)
    Y.append(y)
    Z.append(z)
  
  # Graphical display
  cmap = plt.cm.Spectral
  norm = plt.Normalize(vmin=0, vmax=nbNiveaux)
  ax = plt.axes(projection="3d")
  ax.set_xlabel('x')
  ax.set_ylabel('y')
  ax.set_zlabel('z')
  
  # Change limits for all 3 axes
  m, M = 20, 75
  ax.set_xlim(m, M)
  ax.set_ylim(m, M)
  ax.set_zlim(m, M)
  
  # Plotting
  ax.scatter3D(X, Y, Z, s=30, c=cmap(norm(couleurs)))
  plt.show()
  
  tps(t)

points = csv2array('Resultlines/resultline1_0.3SansTabulation.csv')
lignesNiveau(points)
