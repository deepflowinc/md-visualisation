# This script takes .vtk file loaded in Paraview and takes it as an active source. Output is visualised tensorGlyph.

# trace generated using paraview version 5.10.1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10

# import the simple module from the paraview
from paraview.simple import *
# disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get the active source
activeSource = GetActiveSource()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# turn off scalar coloring of vtk
activeSource_Display = GetDisplayProperties(activeSource, view=renderView1)
ColorBy(activeSource_Display, None)

# create a new 'Tensor Glyph'
tensorGlyph1 = TensorGlyph(registrationName='TensorGlyph1', Input=activeSource,
                           GlyphType='Sphere')
tensorGlyph1.Tensors = ['POINTS', 'tensors']
tensorGlyph1.Scalars = ['POINTS', 'scale']
renderView1.AxesGrid.Visibility = 1
tensorGlyph1.ExtractEigenvalues = 0
tensorGlyph1.ScaleFactor = 1

# show data in view
tensorGlyph1Display = Show(tensorGlyph1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
tensorGlyph1Display.Representation = 'Surface'
tensorGlyph1Display.ColorArrayName = ['POINTS', 'scale']
#tensorGlyph1Display.LookupTable = thetaLUT
tensorGlyph1Display.SelectTCoordArray = 'None'
tensorGlyph1Display.SelectNormalArray = 'Normals'
tensorGlyph1Display.SelectTangentArray = 'None'
tensorGlyph1Display.OSPRayScaleArray = 'scale'
tensorGlyph1Display.OSPRayScaleFunction = 'PiecewiseFunction'
tensorGlyph1Display.SelectOrientationVectors = 'None'
tensorGlyph1Display.ScaleFactor = 6.865732884407044
tensorGlyph1Display.SelectScaleArray = 'scale'
tensorGlyph1Display.GlyphType = 'Arrow'
tensorGlyph1Display.GlyphTableIndexArray = 'scale'
tensorGlyph1Display.GaussianRadius = 0.34328664422035216
tensorGlyph1Display.SetScaleArray = ['POINTS', 'scale']
tensorGlyph1Display.ScaleTransferFunction = 'PiecewiseFunction'
tensorGlyph1Display.OpacityArray = ['POINTS', 'scale']
tensorGlyph1Display.OpacityTransferFunction = 'PiecewiseFunction'
tensorGlyph1Display.DataAxesGrid = 'GridAxesRepresentation'
tensorGlyph1Display.PolarAxes = 'PolarAxesRepresentation'

# hide data in view
Hide(activeSource, renderView1)

# show color bar/color legend
tensorGlyph1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# ===================================
# This section add light

# get property of TensorGlyph1
xmin, xmax, ymin, ymax, zmin, zmax = tensorGlyph1.GetDataInformation(
).DataInformation.GetBounds()

x_mid = (xmax - xmin)/2
y_mid = (ymax - ymin)/2


# Create a new 'Light'
light0 = AddLight(view=renderView1)


# Properties modified on light0
light0.Intensity = 0.1
light0.Position = [x_mid, y_mid, 100.0]
light0.FocalPoint = [x_mid, y_mid, 0.0]
# toggle 3D widget visibility (only when running from the GUI)
Show3DWidgets(proxy=light0)
Hide3DWidgets(proxy=light0)

# Create a new 'Light'
light1 = AddLight(view=renderView1)

# Properties modified on light1
light1.Intensity = 0.1
light1.Position = [x_mid, y_mid, -100.0]
light1.FocalPoint = [x_mid, y_mid, 0.0]
# toggle 3D widget visibility (only when running from the GUI)
Show3DWidgets(proxy=light1)
Hide3DWidgets(proxy=light1)
# ====================================

# get layout
layout1 = GetLayout()

# --------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(741, 793)

# -----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [33.71678388118744,
                              33.697817265987396, 200.82274923928756]
renderView1.CameraFocalPoint = [
    33.71678388118744, 33.697817265987396, 1.0005327090620995]
renderView1.CameraParallelScale = 51.938933255047004
# reset view to fit data
renderView1.ResetCamera()
