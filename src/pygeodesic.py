"""
This code takes as input a basic .txt mesh (points/faces).
It returns the geodesic distances (displayed as a color gradient) from
each point to a predefined boundary that uses the mesh to calculate geodesic distances.
Works in 3D.
"""
import pygeodesic.geodesic as geodesic
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.tri as mtri


""" Recreate a mesh """ 
filename = r'flat_triangular_mesh.txt'
result = geodesic.read_mesh_from_file(filename)
if result:
  points_bruts_tab, faces_brutes_tab = result
  
def liste(t):
  l = []
  for i in range(len(t)):
    tt = []
    for j in range(len(t[0])):
      tt.append(t[i, j])
    l.append(tt)
  return l
  
def tab(l):
  t = np.array(dtype=(len(l), len(l[0])))
  for i in range(len(t)):
    tt = []
    for j in range(len(t[0])):
      tt.append(t[i, j])
  l.append(tt)
  return l
  
points_bruts = liste(points_bruts_tab)
faces_brutes = liste(faces_brutes_tab)

def cond(x, y):
  if x <= 2.1:
    if x+y > 2.5:
      return False
    else:
      return True
  elif x < 2.9:
    if y > 0.4:
      return False
    else:
      return True
  else:
    if y > x-2.5 + 0.1:
      return False
    else:
      return True
      
tabBoolPoints = np.zeros(len(points_bruts))
tabBoolPoints = tabBoolPoints == 0
points = []
X, Y, Z = [], [], []
for i in range(len(points_bruts_tab)):
  x, y, z = points_bruts_tab[i]
  #if cond(x,y):
  X.append(x)
  Y.append(y)
  Z.append(z)
  points.append([x, y, z])
  
#dist eucli entre les pts i et j
def norm(i, j, points):
  x, y, z = points[i]
  xx, yy, zz = points[j]
  return np.sqrt((x-xx)**2 + (y-yy)**2 + (z-zz)**2)
  
#on crée maillage : on associe à chaque pt ses deux pts les plus proches -> donne un triangle
def creaMaille(points):
  faces = []
  for i in range(len(points)):
    dist = []
    for j in range(len(points)):
      dist.append(norm(i, j, points))
    dist[i] = 10*(dist[0]+1)
    
  m1 = min(dist)
  for l1 in range(len(dist)):
    if dist[l1] == m1:
      indiceMin1 = l1
      dist[l1] = 10*(dist[0]+1)
      break
      
  m2 = min(dist)
  for l2 in range(len(dist)):
    if dist[l2] == m2:
      indiceMin2 = l2
      dist[l2] = 10*(dist[0]+1)
      break
      
  m3 = min(dist)
  for l3 in range(len(dist)):
    if dist[l3] == m3:
      indiceMin3 = l3
      dist[l3] = 10*(dist[0]+1)
      break
    
  m4 = min(dist)
  for l4 in range(len(dist)):
    if dist[l4] == m4:
      indiceMin4 = l4
      break
    
  faces.append([i, indiceMin1, indiceMin2])
  faces.append([i, indiceMin2, indiceMin3])
  faces.append([i, indiceMin3, indiceMin4])
  
  return(faces)

faces = creaMaille(points)
points, faces = np.array(points), np.array(faces)

""" On définit le bord """
# True si le sommet est sur le bord d'étude, False sinon
def bord(S, eps=0.001):
  x, y, z = S
  if 0 <= x <= 2.1:
    return (abs(x+y-2.5) < eps)
  elif 2.1 < x <= 2.9:
    return (abs(y - 0.4) < eps)
  else:
    return (abs(y - (x-2.5)) < eps)
    
Xbord, Ybord, Zbord = [], [], []
bords = []
for i in range(len(X)):
  if bord((X[i], Y[i], Z[i])):
    Xbord.append(X[i])
    Ybord.append(Y[i])
    Zbord.append(Z[i])
    bords.append([i, [X[i], Y[i], Z[i]]])
  
#plt.scatter(X, Y)
#triang = mtri.Triangulation(X, Y, faces)
#plt.triplot(triang)

""" On calcule la distance géodésique de chaque point au bord """
def conv(S):
  return(np.array([S]))
  
# renvoie la distance géodésique d'un point quelconque au bord
def distBord(S, geoalg, bords):
  dist, resInutile = geoalg.geodesicDistances(conv(S)) # dist entre S et ts les
  sommets
  distMin = dist[bords[0][0]]
  for B in bords:
    i, b = B
    d = dist[i] # distance entre S et sommet i du bord
    if d < distMin:
      distMin = d
  return distMin
  
# Display contour lines based on geodesic distances
def lignesNiveau(points, faces, nbNiveaux=10, ratioPlusGdeDist=1):
  geoalg = geodesic.PyGeodesicAlgorithmExact(points, faces)
  dist, resInutile = geoalg.geodesicDistances(conv(bords[0][0]))
  distMaxEntre2Points = max(dist) * ratioPlusGdeDist  # arbitrary value
  X, Y, Z, couleurs = [], [], [], []
  
  for S in range(len(points)):
    distanceAuBord = distBord(S, geoalg, bords)
    c = int(distanceAuBord / distMaxEntre2Points * nbNiveaux)
    couleurs.append(c)
    x, y, z = points[S]
    X.append(x)
    Y.append(y)
    Z.append(z)
    
  # Graphical display
  cmap = plt.cm.Spectral
  norm = plt.Normalize(vmin=0, vmax=nbNiveaux)
  plt.scatter(X, Y, s=30, c=cmap(norm(couleurs)))
  plt.show()

lignesNiveau(points_bruts_tab, faces_brutes_tab, nbNiveaux=25, ratioPlusGdeDist=1)
plt.scatter(Xbord, Ybord, c='blue')
