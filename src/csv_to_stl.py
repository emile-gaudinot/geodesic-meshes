"""
Convert a csv point cloud to an stl file
"""
import csv
from scipy.spatial import Delaunay
import matplotlib.tri
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
# import surf2stl
from stl import mesh

# Read the csv file
file = open('resultline1.csv')
csvreader = csv.reader(file)
header = next(csvreader)
rows = []
for row in csvreader:
    rows.append(row)
file.close()

# First attempt: 3D meshing of the point cloud which returns a vector of tetrahedra
string_points = np.array(rows)
points = string_points.astype(np.float64)
tri = Delaunay(points)
# mplot3d.axes3d.Axes3D.plot_trisurf(tri)

def plot_tri(ax, points, tri):
    edges = collect_edges(tri)
    x = np.array([])
    y = np.array([])
    z = np.array([])
    for (i, j) in edges:
        x = np.append(x, [points[i, 0], points[j, 0], np.nan])
        y = np.append(y, [points[i, 1], points[j, 1], np.nan])
        z = np.append(z, [points[i, 2], points[j, 2], np.nan])
    ax.plot3D(x, y, z, color='g', lw='0.1')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='b')

def collect_edges(tri):
    edges = set()
    def sorted_tuple(a, b):
        return (a, b) if a < b else (b, a)
    # Add edges of the tetrahedron (sorted so we don't add an edge twice, even if it comes in reverse order).
    for (i0, i1, i2, i3) in tri.simplices:
        edges.add(sorted_tuple(i0, i1))
        edges.add(sorted_tuple(i0, i2))
        edges.add(sorted_tuple(i0, i3))
        edges.add(sorted_tuple(i1, i2))
        edges.add(sorted_tuple(i1, i3))
        edges.add(sorted_tuple(i2, i3))
    return edges

fig = plt.figure()
ax = plt.axes(projection='3d')
plot_tri(ax, points, tri)

# The plot works, but the mesh appears volumetric with tetrahedra, whereas we need a triangular mesh of the 3D surface

# Second attempt: obtain a triangular mesh of the 3D surface of the point cloud. Works!
X, Y, Z = points[:, 0], points[:, 1], points[:, 2]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(X, Y, Z, color='white', edgecolors='grey', alpha=0.5)
ax.scatter(X, Y, Z, c='red')
plt.show()

# import in stl
# surf2stl.write('mesh1.stl', X, Y, Z)
