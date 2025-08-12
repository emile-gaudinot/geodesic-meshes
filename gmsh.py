import gmsh


gmsh.initialize()

gmsh.model.add("another model")
gmsh.model.occ.addBox(0, 0, 0, 1, 1, 1)
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(2)

t1 = gmsh.view.add("A model-based view")
gmsh.view.write(t1, "x4_t1.msh")

gmsh.write("maillage.msh")
gmsh.fltk.run()
