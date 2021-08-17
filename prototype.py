import vtk
import cv2
import gui
import itk
import numpy as np
import data_transforms
import SimpleITK as sitk
import matplotlib.pyplot as plt
from myshow import myshow, myshow3d

"""
nodule0 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.269689294231892620436462818860.2.50000051251220000101.nrrd")
nodule0_mask1 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.269689294231892620436462818860.2.50000051251220000101Mask_1.nrrd")
nodule0_mask2 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.269689294231892620436462818860.2.50000051251220000101Mask_2.nrrd")
nodule0_mask3 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.269689294231892620436462818860.2.50000051251220000101Mask_3.nrrd")

nodule1 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.822128649427327893802314908658.42.50000051251220000101.nrrd")
nodule1_mask1 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.822128649427327893802314908658.42.50000051251220000101Mask_1.nrrd")
nodule1_mask2 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.822128649427327893802314908658.42.50000051251220000101Mask_2.nrrd")
nodule1_mask3 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.822128649427327893802314908658.42.50000051251220000101Mask_3.nrrd")

nodule2 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.217955041973656886482758642958.22.50000051251220000101.nrrd")
nodule2_mask1 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.217955041973656886482758642958.22.50000051251220000101Mask_1.nrrd")
nodule2_mask2 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.217955041973656886482758642958.22.50000051251220000101Mask_2.nrrd")
nodule2_mask3 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.217955041973656886482758642958.22.50000051251220000101Mask_3.nrrd")
"""
nodule3 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.100953483028192176989979435275.32.50000051251220000101.nrrd")
#nodule3_mask1 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.100953483028192176989979435275.32.50000051251220000101Mask_1.nrrd")
#nodule3_mask2 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.100953483028192176989979435275.32.50000051251220000101Mask_2.nrrd")
nodule3_mask3 = sitk.ReadImage("1.3.6.1.4.1.14519.5.2.1.6279.6001.100953483028192176989979435275.32.50000051251220000101Mask_3.nrrd")

imagearray = np.load("image.npy")
imagearray = imagearray.astype('float64')

maskarray = np.load("mask.npy")
maskarray = maskarray.astype('float64')

# Maskelemek için yazılmış emek kokan fonksiyon
def mask_image(image, mask):
    image_array = sitk.GetArrayFromImage(image)
    mask_array = sitk.GetArrayFromImage(mask)
    
    masked_array = image_array * mask_array
    masked_nodule = sitk.GetImageFromArray(masked_array)
    return masked_nodule

# Mask3 nodule 
#masked3_nodule0 = mask_image(nodule0, nodule0_mask3)
#masked3_nodule1 = mask_image(nodule1, nodule1_mask3)
#masked3_nodule2 = mask_image(nodule2, nodule2_mask3)
masked3_nodule3 = mask_image(nodule3, nodule3_mask3)

# Mask2 nodule 
#masked2_nodule0 = mask_image(nodule0, nodule0_mask2)
#masked2_nodule1 = mask_image(nodule1, nodule1_mask2)
#masked2_nodule2 = mask_image(nodule2, nodule2_mask2)
masked2_nodule3 = mask_image(nodule3, nodule3_mask2)


# Mask1 nodule 
#masked1_nodule0 = mask_image(nodule0, nodule0_mask1)
#masked1_nodule1 = mask_image(nodule1, nodule1_mask1)
#masked1_nodule2 = mask_image(nodule2, nodule2_mask1)
masked1_nodule3 = mask_image(nodule3, nodule3_mask1)

#myshow(masked_nodule0)


def render(vtk_img):
    colors = vtk.vtkNamedColors()
    
    colors.SetColor("BkgColor", [0, 0, 0, 0])
    #51, 77, 102, 255
    
    
    # Create the renderer, the render window, and the interactor. The renderer
    # draws into the render window, the interactor enables mouse- and
    # keyboard-based interaction with the scene.
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    
    # The following reader is used to read a series of 2D slices (images)
    # that compose the volume. The slice dimensions are set, and the
    # pixel spacing. The data Endianness must also be specified. The reader
    # uses the FilePrefix in combination with the slice number to construct
    # filenames using the format FilePrefix.%d. (In this case the FilePrefix
    # is the root name of the file: quarter.)
    
    # The volume will be displayed by ray-cast alpha compositing.
    # A ray-cast mapper is needed to do the ray-casting.
    volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
    volumeMapper.SetInputData(vtk_img)
    
    # The color transfer function maps voxel intensities to colors.
    # It is modality-specific, and often anatomy-specific as well.
    # The goal is to one color for flesh (between 500 and 1000)
    # and another color for bone (1150 and over).
    volumeColor = vtk.vtkColorTransferFunction()
    volumeColor.AddRGBPoint(0, 127.0, 0.0, 0.0) #akciğer
    volumeColor.AddRGBPoint(500, 20.0, 20.5, 20.3) #bronşlar
    volumeColor.AddRGBPoint(1000, 1.0, 0.5, 0.3)
    volumeColor.AddRGBPoint(1150, 1.0, 0.0, 0.9)
    
    # The opacity transfer function is used to control the opacity
    # of different tissue types.
    volumeScalarOpacity = vtk.vtkPiecewiseFunction()
    volumeScalarOpacity.AddPoint(0, 0.05)
    volumeScalarOpacity.AddPoint(500, 1.0)
    volumeScalarOpacity.AddPoint(1000, 1.0)
    volumeScalarOpacity.AddPoint(1150, 1.0)
    
    # The gradient opacity function is used to decrease the opacity
    # in the "flat" regions of the volume while maintaining the opacity
    # at the boundaries between tissue types.  The gradient is measured
    # as the amount by which the intensity changes over unit distance.
    # For most medical data, the unit distance is 1mm.
    volumeGradientOpacity = vtk.vtkPiecewiseFunction()
    volumeGradientOpacity.AddPoint(0, 0.0)
    volumeGradientOpacity.AddPoint(90, 0.5)
    volumeGradientOpacity.AddPoint(100, 1.0)
    
    # The VolumeProperty attaches the color and opacity functions to the
    # volume, and sets other volume properties.  The interpolation should
    # be set to linear to do a high-quality rendering.  The ShadeOn option
    # turns on directional lighting, which will usually enhance the
    # appearance of the volume and make it look more "3D".  However,
    # the quality of the shading depends on how accurately the gradient
    # of the volume can be calculated, and for noisy data the gradient
    # estimation will be very poor.  The impact of the shading can be
    # decreased by increasing the Ambient coefficient while decreasing
    # the Diffuse and Specular coefficient.  To increase the impact
    # of shading, decrease the Ambient and increase the Diffuse and Specular.
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(volumeColor)
    volumeProperty.SetScalarOpacity(volumeScalarOpacity)
    volumeProperty.SetGradientOpacity(volumeGradientOpacity)
    volumeProperty.SetInterpolationTypeToLinear()
    volumeProperty.ShadeOn()
    volumeProperty.SetAmbient(0.2)
    volumeProperty.SetDiffuse(1.0)
    volumeProperty.SetSpecular(1.0)
    
    # The vtkVolume is a vtkProp3D (like a vtkActor) and controls the position
    # and orientation of the volume in world coordinates.
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    
    # Finally, add the volume to the renderer
    ren.AddViewProp(volume)
    
    # Set up an initial view of the volume.  The focal point will be the
    # center of the volume, and the camera position will be 400mm to the
    # patient's left (which is our right).
    camera = ren.GetActiveCamera()
    c = volume.GetCenter()
    camera.SetViewUp(0, 0, -1)
    camera.SetPosition(c[0], c[1] - 400, c[2])
    camera.SetFocalPoint(c[0], c[1], c[2])
    camera.Azimuth(30.0)
    camera.Elevation(30.0)
    
    # Set a background color for the renderer
    ren.SetBackground(colors.GetColor3d("BkgColor"))
    
    # Increase the size of the render window
    renWin.SetSize(640, 480)
    
    # Interact with the data.
    iren.Start()

image = sitk.GetImageFromArray(imagearray)
mask = sitk.GetImageFromArray(maskarray)

masked_image = mask_image(image, mask)
#myshow(masked_image)


deneme = masked_image
sitk_image = deneme
image_dimension = 3
index = [15]*image_dimension

itk_image = data_transforms.sitk_to_itk(sitk_image, image_dimension, index)

# Rendering
vtk_img = data_transforms.vtk_image_from_image(itk_image)
render(vtk_img)

