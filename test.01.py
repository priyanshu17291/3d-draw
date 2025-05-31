import pyvista as pv
import vtk

# Create a PyVista Plotter
plotter = pv.Plotter()

# Add a simple 3D mesh (sphere)
plotter.add_mesh(pv.Sphere(radius=5), color='orange')
plotter.set_background("navy")

# Create a custom annotated cube (like a ViewCube)
cube = vtk.vtkAnnotatedCubeActor()
cube.SetXPlusFaceText("R")
cube.SetXMinusFaceText("L")
cube.SetYPlusFaceText("F")
cube.SetYMinusFaceText("B")
cube.SetZPlusFaceText("U")
cube.SetZMinusFaceText("D")
cube.GetTextEdgesProperty().SetColor(1, 1, 1)
cube.GetTextEdgesProperty().SetLineWidth(2)
cube.GetCubeProperty().SetColor(0.5, 0.5, 0.5)  # cube color

# Add the orientation widget to the plotter (uses VTK internally)
plotter.add_orientation_widget(cube)

# Show the plotter window
plotter.show()
