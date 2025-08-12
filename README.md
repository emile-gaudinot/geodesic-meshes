# Geodesic Meshes

## **Optimization of 3D Surface Meshing for Cardiac Valves**
*Émile Gaudinot, Charlotte Voisin, Julien Bouchet*
*Centrale Nantes, in collaboration with Institut du Thorax*

---

### **1. Scientific Context & Objectives**

#### **Context**
- **Pathology:** Mitral valve prolapse (MVP) affects **2–4% of the population**, involving deformation of the valve between the left atrium and ventricle.
- **Clinical Need:** Studying MVP requires **comparative analysis** of valve geometries across patients. This necessitates **standardized, high-quality meshes** that can be overlaid for statistical shape modeling (e.g., Principal Component Analysis).
- **Challenge:** Existing meshes (e.g., triangular) lack the **regularity and consistency** needed for accurate superposition and comparison.

#### **Objective**
Develop an **automated pipeline** to generate **geodesic quadrilateral meshes** of cardiac valves from 3D binary images, ensuring:
- **Regularity** (uniform element distribution).
- **Consistency** (same number of points across meshes).
- **Geometric fidelity** (adaptation to valve deformations).

---

### **2. Methods**

#### **Key Concepts**
- **Geodesic Distance:** Shortest path between two points on a surface, enabling **surface-aware** mesh generation.
- **Quadrilateral Meshing:** Preferred for **regularity** and **alignment with anatomical features** (e.g., valve leaflets).
- **Input Data:** 3D binary images (`.tif`) of valve-like cylinders (simplified proxies for real valves).

#### **Approaches**
Two parallel strategies were pursued:

1. **Manual Approach (Python-Based)**
   - **Tools:** `GMSH`, `pygeodesic`, `potpourri3d`, `vtk`.
   - **Steps:**
     - Extract point clouds from binary images using `vtk`.
     - Compute geodesic distances from user-defined borders (e.g., valve edges).
     - Visualize distance fields to validate geodesic calculations.
     - *(Note: Full automation of quad meshing was not achieved in this approach.)*

2. **Collaborative Approach (External Algorithm)**
   - **Partnership:** Collaboration with **Wei Chen** (Dalian University of Technology), author of a novel quadrilateral geodesic meshing algorithm [[4]](#references).
   - **Steps:**
     - Generate **triangular surface meshes** from binary images using `vtkMarchingCubes`.
     - Export meshes to `.stl`/`.obj` format.
     - Submit to Wei Chen’s algorithm for **quad-dominant geodesic remeshing**.
     - Receive optimized quadrilateral meshes for validation.

#### **Technical Workflow**
| Step                | Tool/Method                          | Output                          |
|---------------------|--------------------------------------|---------------------------------|
| Binary Image Input  | `.tif` (3D valve-like cylinders)     | Volumetric pixel data           |
| Surface Extraction  | `vtkMarchingCubes`                   | Triangular surface mesh        |
| Geodesic Analysis   | `pygeodesic`/`potpourri3d`            | Distance fields (validation)   |
| Quad Meshing        | Wei Chen’s algorithm                 | Quad-dominant geodesic mesh     |
| Visualization       | `MeshLab`, `GMSH`                    | 3D mesh models                  |

---

### **3. Results**

#### **Geodesic Distance Visualization**
- Successfully computed and visualized geodesic distances from arbitrary borders on synthetic valve models.
- **Example:** Distance fields propagate uniformly, even on irregular surfaces (Figure 9–10 in report).

  ![Geodesic distance visualization](placeholder_for_geodesic_fig)
  *Gradient-colored points show geodesic distance to a user-defined border (blue).*

#### **Quadrilateral Meshing**
- **Collaborative Approach Yielded Optimal Results:**
  - Wei Chen’s algorithm produced **high-quality quadrilateral meshes** from triangular inputs.
  - Meshes exhibit:
    - **Regular element distribution** (minimal distortion).
    - **Consistency** (suitable for superposition in PCA).
    - **Adaptability** to surface irregularities (e.g., prolapse-like deformations).

  ![Quadrilateral mesh result](placeholder_for_quad_mesh)
  *Quad-dominant geodesic mesh of a cylinder (proxy for cardiac valve).*

#### **Validation**
- Meshes were validated for:
  - **Topological correctness** (no self-intersections).
  - **Geometric accuracy** (faithful to input surface).
  - **Computational efficiency** (scalable to larger datasets).

---

### **4. Scientific Implications**
- **Advancement for MVP Research:**
  - Enables **standardized shape analysis** of mitral valves via PCA.
  - Facilitates **quantitative comparison** of pathological vs. healthy valves.
- **Broader Applications:**
  - Pipeline adaptable to other **biological surfaces** (e.g., aortic valves, vascular structures).
  - Potential integration into **clinical workflows** for automated mesh generation.

---

### **5. Future Directions**
- **Extension to Real Valve Data:** Apply pipeline to **patient-specific mitral valve images** (from CT/MRI).
- **Parameter Optimization:** Refine mesh density and geodesic border definitions for **clinical relevance**.
- **Open-Source Collaboration:** Publish tools/code to support reproducibility in the community.

---
### **References**
[1] Novotni & Klein (2002). *Computing geodesic distances on triangular meshes.*
[2] Surazhsky et al. (2005). *Fast exact and approximate geodesics on meshes.*
[3] Chen et al. (2018). *Metric based quadrilateral mesh generation.* [[arXiv:1811.12604]](#)
[4] Crane et al. (2017). *The heat method for distance computation.*
