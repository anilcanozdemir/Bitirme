import SimpleITK as sitk
import Mask3filter as mask

def Mask1filtering(imageName):   
    '''
    

    Parameters
    ----------
    imageName : string
        imageName

    Returns
    -------
    None.

    '''
    image = sitk.ReadImage(imageName)
    name_template= imageName[:len(imageName) - 5]
    image=binaryThreshold(image)
    image=erode(image)
    image=dilate(image)
    mask1Write(image, name_template)

def Mask2filtering(imageName):   
    '''
    

    Parameters
    ----------
    imageName : string
        imageName

    Returns
    -------
    None.

    '''
    name_template= imageName[:len(imageName) - 5]
    Mask1 = sitk.ReadImage(name_template+'Mask_1.nrrd')
    Mask3 = sitk.ReadImage(name_template+'Mask_3.nrrd')
    nda1 = sitk.GetArrayFromImage(Mask1)
    nda3 = sitk.GetArrayFromImage(Mask3)
    nda2 = nda1
    for i in range(0,len(nda1)):
        nda2[i]=nda1[i]*nda3[i]
    
    image = sitk.GetImageFromArray(nda2)
    mask2Write(image, name_template)

def Mask3filtering(imageName):
    '''
    Gerekli fonksiyonları çağırarak maskelemeyi yapar ve yazar.
    
    Parameters
    ----------
    imageName : String
        Imagename.

    Returns
    -------
    None.

    '''
    image = sitk.ReadImage(imageName)
    name_template= imageName[:len(imageName) - 5]
    image=binaryThreshold(image)
    image=erode(image)
    image=dilate(image)
    image=holeFilling(image)
    image=mask3Usage(image)
    image = sitk.GetImageFromArray(image)
    mask3Write(image,name_template)
    
def reScaleas255(image):
    '''
    Resmi tekrar boyutlandırır.
    
    Parameters
    ----------
    image : Image
        

    Returns
    -------
    image_255 : Image
        Tekrar boyutlandırılmış image.

    '''
    image_255=sitk.Cast(sitk.RescaleIntensity(image), sitk.sitkUInt8)
    return image_255    
def binaryThreshold(image):
    '''
    BinaryThreshold filtresi uygular.

    Parameters
    ----------
    image : Image
        

    Returns
    -------
    segmentated : Image
        BinaryThreshold filtresi uygulanmış image.

    '''
    
    
    binaryThreshold = sitk.BinaryThresholdImageFilter()
    binaryThreshold.SetLowerThreshold(-4000)
    binaryThreshold.SetUpperThreshold(-400)
    binaryThreshold.SetInsideValue(1)
    binaryThreshold.SetOutsideValue(0)
    segmentated = binaryThreshold.Execute(image)

    return segmentated

def erode(image):
    '''
    Erode filtresi uygular.

    Parameters
    ----------
    image : Image
        

    Returns
    -------
    erode : Image
        Erode filtresi uygulanmış image..

    '''
    erosion = sitk.ErodeObjectMorphologyImageFilter()
    erode = erosion.Execute(image)
    return erode

def dilate(image):
    '''
    Dilate filtresi uygular.

    Parameters
    ----------
    image : Image
        

    Returns
    -------
    dilation : Image
         Dilation filtresi uygulanmış image..

    '''
    dilate = sitk.DilateObjectMorphologyImageFilter()
    dilation = dilate.Execute(image)
    return dilation

def holeFilling(image):
    '''
    HoleFilling filtresi uygular.

    Parameters
    ----------
    image : Image
        

    Returns
    -------
    hole_filling : Image
        HoleFilling filtresi uygulanmış image.
        
    '''
    hole = sitk.VotingBinaryIterativeHoleFillingImageFilter()
    hole.SetRadius(2)
    hole.SetMaximumNumberOfIterations(700)
    hole_filling = hole.Execute(image)
    return hole_filling
def mask3Usage(image):
    '''
    Verilen resime Maskeleme gerçekleştirir .

    Parameters
    ----------
    image : Image
        

    Returns
    -------
    nda_mask : TYPE
        DESCRIPTION.

    '''
    nda = sitk.GetArrayFromImage(image)
    nda_mask =[]
    for i in range(0,len(nda)):
        scaled_image=nda[i]*255
        nda_temp=mask.Mask3(scaled_image)
        nda_mask.append(nda_temp/255)
    return nda_mask

def mask1Write(image,name_template):
    '''
    Oluşturulan maskeyi yazar.

    Parameters
    ----------
    image : Image
        DESCRIPTION.
    name_template : string
        Verilecek isim.

    Returns
    -------
    None.

    '''
    
    outputImageFileName = name_template + "Mask_1.nrrd"
    writer = sitk.ImageFileWriter()
    writer.SetFileName(outputImageFileName)
    writer.Execute(image)
    
def mask2Write(image,name_template):
    '''
    Oluşturulan maskeyi yazar.

    Parameters
    ----------
    image : Image
        DESCRIPTION.
    name_template : string
        Verilecek isim.

    Returns
    -------
    None.

    '''
    
    outputImageFileName = name_template + "Mask_2.nrrd"
    writer = sitk.ImageFileWriter()
    writer.SetFileName(outputImageFileName)
    writer.Execute(image)

def mask3Write(image,name_template):
    '''
    Oluşturulan maskeyi yazar.

    Parameters
    ----------
    image : Image
        DESCRIPTION.
    name_template : string
        Verilecek isim.

    Returns
    -------
    None.

    '''
    
    outputImageFileName = name_template + "Mask_3.nrrd"
    writer = sitk.ImageFileWriter()
    writer.SetFileName(outputImageFileName)
    writer.Execute(image)

