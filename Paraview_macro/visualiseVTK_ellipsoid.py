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


# get color transfer function/color map for 'theta'
thetaLUT = GetColorTransferFunction('theta')
thetaLUT.ColorSpace = 'RGB'
# Rescale transfer function
thetaLUT.RescaleTransferFunction(-90.0, 90.0)

# colormap
thetaLUT.RGBPoints = [
    -90,
    0.0,
    1.0,
    1.0,
    -75,
    0.0,
    0.66666666666666663,
    0.0,
    -60,
    0.0,
    0.66666666666666663,
    0.0,
    -45,
    0.0,
    0.66666666666666663,
    0.0,
    -30,
    1.0,
    1.0,
    0.0,
    -15,
    0.99215686274509807,
    0.0,
    0.0,
    0,
    0.98431372549019602,
    0.015686274509803921,
    0.015686274509803921,
    15,
    0.81568627450980391,
    0.0,
    0.0,
    30,
    0.66666666666666663,
    0.33333333333333331,
    1.0,
    45,
    0.0,
    0.33333333333333331,
    1.0,
    60,
    0.0,
    0.33333333333333331,
    1.0,
    75,
    0.0,
    0.33333333333333331,
    1.0,
    90,
    0.0,
    1.0,
    1.0
]

# get opacity transfer function/color map for 'theta'
theta_opacity = GetOpacityTransferFunction('theta')

theta_opacity.Points = [
    -90,
    0.95,
    0.5,
    0.0,
    -75,
    0.95,
    0.5,
    0.0,
    -60,
    0.95,
    0.5,
    0.0,
    -45,
    0.95,
    0.5,
    0.0,
    -30,
    0.95,
    0.5,
    0.0,
    -15,
    0.95,
    0.5,
    0.0,
    0,
    0.95,
    0.5,
    0.0,
    15,
    0.95,
    0.5,
    0.0,
    30,
    0.95,
    0.5,
    0.0,
    45,
    0.95,
    0.5,
    0.0,
    60,
    0.95,
    0.5,
    0.0,
    75,
    0.95,
    0.5,
    0.0,
    90,
    0.95,
    0.5,
    0.0
]

# reset view to fit data
renderView1.ResetCamera(False)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# get opacity transfer function/opacity map for 'theta'
thetaPWF = GetOpacityTransferFunction('theta')
# Rescale transfer function
thetaPWF.RescaleTransferFunction(-90.0, 90.0)

# create a new 'Tensor Glyph'
tensorGlyph1 = TensorGlyph(registrationName='TensorGlyph1', Input=activeSource,
                           GlyphType='Sphere')
tensorGlyph1.Tensors = ['POINTS', 'tensors']
tensorGlyph1.Scalars = ['POINTS', 'theta']
renderView1.AxesGrid.Visibility = 1
tensorGlyph1.ExtractEigenvalues = 0
tensorGlyph1.ScaleFactor = 1

# show data in view
tensorGlyph1Display = Show(tensorGlyph1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
tensorGlyph1Display.Representation = 'Surface'
tensorGlyph1Display.ColorArrayName = ['POINTS', 'theta']
tensorGlyph1Display.LookupTable = thetaLUT
tensorGlyph1Display.SelectTCoordArray = 'None'
tensorGlyph1Display.SelectNormalArray = 'Normals'
tensorGlyph1Display.SelectTangentArray = 'None'
tensorGlyph1Display.OSPRayScaleArray = 'theta'
tensorGlyph1Display.OSPRayScaleFunction = 'PiecewiseFunction'
tensorGlyph1Display.SelectOrientationVectors = 'None'
tensorGlyph1Display.ScaleFactor = 6.865732884407044
tensorGlyph1Display.SelectScaleArray = 'theta'
tensorGlyph1Display.GlyphType = 'Arrow'
tensorGlyph1Display.GlyphTableIndexArray = 'theta'
tensorGlyph1Display.GaussianRadius = 0.34328664422035216
tensorGlyph1Display.SetScaleArray = ['POINTS', 'theta']
tensorGlyph1Display.ScaleTransferFunction = 'PiecewiseFunction'
tensorGlyph1Display.OpacityArray = ['POINTS', 'theta']
tensorGlyph1Display.OpacityTransferFunction = 'PiecewiseFunction'
tensorGlyph1Display.DataAxesGrid = 'GridAxesRepresentation'
tensorGlyph1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
tensorGlyph1Display.ScaleTransferFunction.Points = [
    -89.89864349365234, 0.0, 0.5, 0.0, 89.9757080078125, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
tensorGlyph1Display.OpacityTransferFunction.Points = [
    -89.89864349365234, 0.0, 0.5, 0.0, 89.9757080078125, 1.0, 0.5, 0.0]

# hide data in view
Hide(activeSource, renderView1)

# show color bar/color legend
tensorGlyph1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# reset view to fit data
renderView1.ResetCamera(False)


# create a new 'Tensor Glyph'
tensorGlyph2 = TensorGlyph(registrationName='TensorGlyph2', Input=activeSource,
                           GlyphType='Sphere')
tensorGlyph2.Tensors = ['POINTS', 'tensors']
tensorGlyph2.ExtractEigenvalues = 0
tensorGlyph2.Scalars = ['POINTS', 'phi']
tensorGlyph2.ScaleFactor = 1

# show data in view
tensorGlyph2Display = Show(tensorGlyph2, renderView1, 'GeometryRepresentation')

# get color transfer function/color map for 'phi'
phiLUT = GetColorTransferFunction('phi')
# Rescale transfer function
phiLUT.RescaleTransferFunction(0, 90.0)

# set the colormap
phiLUT.RGBPoints = [
    0,
    1.0,
    1.0,
    1.0,
    90,
    1.0,
    1.0,
    1.0
]

# get opacity transfer function/color map for 'phi'
phi_opacity = GetOpacityTransferFunction('phi')

phi_opacity.Points = [
    0,
    1.0,
    0.5,
    0.0,
    90,
    0.0,
    0.5,
    0.0
]


# trace defaults for the display properties.
tensorGlyph2Display.Representation = 'Surface'
tensorGlyph2Display.ColorArrayName = ['POINTS', 'phi']
tensorGlyph2Display.LookupTable = phiLUT
tensorGlyph2Display.SelectTCoordArray = 'None'
tensorGlyph2Display.SelectNormalArray = 'Normals'
tensorGlyph2Display.SelectTangentArray = 'None'
tensorGlyph2Display.OSPRayScaleArray = 'phi'
tensorGlyph2Display.OSPRayScaleFunction = 'PiecewiseFunction'
tensorGlyph2Display.SelectOrientationVectors = 'None'
tensorGlyph2Display.ScaleFactor = 6.865732884407044
tensorGlyph2Display.SelectScaleArray = 'phi'
tensorGlyph2Display.GlyphType = 'Arrow'
tensorGlyph2Display.GlyphTableIndexArray = 'phi'
tensorGlyph2Display.GaussianRadius = 0.34328664422035216
tensorGlyph2Display.SetScaleArray = ['POINTS', 'phi']
tensorGlyph2Display.ScaleTransferFunction = 'PiecewiseFunction'
tensorGlyph2Display.OpacityArray = ['POINTS', 'phi']
tensorGlyph2Display.OpacityTransferFunction = 'PiecewiseFunction'
tensorGlyph2Display.DataAxesGrid = 'GridAxesRepresentation'
tensorGlyph2Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
tensorGlyph2Display.ScaleTransferFunction.Points = [
    0.48617199063301086, 0.0, 0.5, 0.0, 89.98120880126953, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
tensorGlyph2Display.OpacityTransferFunction.Points = [
    0.48617199063301086, 0.0, 0.5, 0.0, 89.98120880126953, 1.0, 0.5, 0.0]

# hide data in view
Hide(activeSource, renderView1)

# show color bar/color legend
tensorGlyph2Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get opacity transfer function/opacity map for 'phi'
phiPWF = GetOpacityTransferFunction('phi')
# Rescale transfer function
phiPWF.RescaleTransferFunction(0, 90.0)

# set active source
SetActiveSource(tensorGlyph1)

# set active source
SetActiveSource(tensorGlyph2)

# Properties modified on phiLUT
phiLUT.EnableOpacityMapping = 1

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
