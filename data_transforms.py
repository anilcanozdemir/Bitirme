import itk
import vtk
import numpy as np
import SimpleITK as sitk
from vtk.util.numpy_support import numpy_to_vtk

def vtk_image_from_image(image):
    """
    Converts itk image to vtk image format.

    Parameters
    ----------
    image : itk.Image

    Returns
    -------
    vtk_image : vtk.Image

    """
    array = itk.array_view_from_image(image)

    vtk_image = vtk.vtkImageData()
    data_array = numpy_to_vtk(array.reshape(-1))
    data_array.SetNumberOfComponents(image.GetNumberOfComponentsPerPixel())
    data_array.SetName('Scalars')
    
    # Always set Scalars for (future?) multi-component volume rendering
    vtk_image.GetPointData().SetScalars(data_array)
    dim = image.GetImageDimension()
    spacing = [1.0,] * 3
    spacing[:dim] = image.GetSpacing()
    vtk_image.SetSpacing(spacing)
    origin = [0.0,] * 3
    origin[:dim] = image.GetOrigin()
    vtk_image.SetOrigin(origin)
    dims = [1,] * 3
    dims[:dim] = itk.size(image)
    vtk_image.SetDimensions(dims)
    
    # Todo: Add Direction with VTK 9
    if image.GetImageDimension() == 3:
        PixelType = itk.template(image)[1][0]
        if PixelType == itk.Vector:
            vtk_image.GetPointData().SetVectors(data_array)
        elif PixelType == itk.CovariantVector:
            vtk_image.GetPointData().SetVectors(data_array)
        elif PixelType == itk.SymmetricSecondRankTensor:
            vtk_image.GetPointData().SetTensors(data_array)
        elif PixelType == itk.DiffusionTensor3D:
            vtk_image.GetPointData().SetTensors(data_array)
            
    return vtk_image

def sitk_to_itk(sitk_image, image_dimension, index):
    """
    Create an itk image from the simpleitk image via numpy array

    Parameters
    ----------
    sitk_image : sitk.Image

    image_dimension : # dimension of input image
        
    index : [15] * image_dimension
        
    Returns
    -------
    itk_image : itk.Image
        DESCRIPTION.

    """
    itk_image = itk.GetImageFromArray(sitk.GetArrayFromImage(sitk_image), is_vector = sitk_image.GetNumberOfComponentsPerPixel()>1)
    itk_image.SetOrigin(sitk_image.GetOrigin())
    itk_image.SetSpacing(sitk_image.GetSpacing())   
    itk_image.SetDirection(itk.GetMatrixFromArray(np.reshape(np.array(sitk_image.GetDirection()), [image_dimension]*2)))
    print('ITK image value at {0}: {1}'.format(index, itk_image.GetPixel(index)))
    
    # Change the pixel value
    itk_image.SetPixel(index, 888)
    
    return itk_image
        
    
