import numpy as np
import imutils
import cv2

def Mask3(image):
    '''
    Gerekli fonksiyonları çağırarak maskelemeyi gerçekleştirir.

    Parameters
    ----------
    image : Image
        Grayscale image.

    Returns
    -------
    image : Image
        Grayscale image.

    '''
    image=drawBiggestContour(image)
    (image,FrameList)=getContorsFrame(image)
    image=walkAndMask(image,FrameList)
    image=walkinFrameList(image,FrameList)
    return image

def drawBiggestContour(image):
    '''
    Resimdeki en büyük nesneyi kontür yöntemi yardımıyla işaretler.

    Parameters
    ----------
    image : Image
        Grayscale image.

    Returns
    -------
    image : TYPE
        BGRscale image.

    '''
    image=cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    lower = np.array([0, 0, 0])
    upper = np.array([15, 15, 15])
    shapeMask = cv2.inRange(image, lower, upper)
    cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    biggestContour=0;
    for i in range(0,len(cnts)):
        if len(cnts[i])>biggestContour:
            biggestContour=len(cnts[i])
    for c in cnts:
        if len(c)==biggestContour:
             cv2.drawContours(image, [c], -1, (0, 255, 0), 0)
    return image

def getContorsFrame(image):
    '''
    Kontürlenen resimdeki nesnenin çerçevesini liste halinde alır

    Parameters
    ----------
    image : Image
        BGR scale image.

    Returns
    -------
    image : Image
        Grayscale image.
    FrameList : List
        Çerçeve listesi.

    '''
    FrameList=[]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    for i in range(0,len(image)):
        for j in range(0,len(image[1])):
            if image[i][j]==150:
                FrameList.append((i,j))
                image[i][j]=0
    return (image,FrameList)

def walkAndMask(image,FrameList):
    '''
    Pikselleri dolaşarak maskeleme yapar.

    Parameters
    ----------
    image : Image
        GrayScale image.
    FrameList : List
        Çerçeve listesi.

    Returns
    -------
    image : Image
         GrayScale image.

    '''
    for i in range(0,len(image)):
        for j in range(0,len(image[1])):
            if (i,j) in FrameList:
                break
            else:
                image[i][j]=0
                
    for i in range(0,len(image)):
        for j in range(len(image[1])-1,0,-1):
            if (i,j) in FrameList:
                break
            else:
                image[i][j]=0
                
    for j in range(0,len(image[1])):
        for i in range(0,len(image)):
            if (i,j) in FrameList:
                break
            else:
                image[i][j]=0
                
    for j in range(0,len(image[1])):
        for i in range(len(image)-1,0,-1):
            if (i,j) in FrameList:
                break
            else:
                image[i][j]=0
    return image

def walkinFrameList (image,FrameList):
    '''
    Çercevenin etrafını dolaşarak  maskeler.

    Parameters
    ----------
    image : Image
        DESCRIPTION.
    FrameList : TYPE
        DESCRIPTION.

    Returns
    -------
    image : TYPE
        DESCRIPTION.

    '''
    for k in range(0,len(FrameList)):
        (x,y)=FrameList[k]
        for i in range(x,len(image)):
            if image[i][y]==0 or i in FrameList:
                break
            else:
                image[i][y]=0
        for i in range(x-1,0,-1):
            if image[i][y]==0 or i in FrameList:
                break
            else:
                image[i][y]=0
        for i in range(y,len(image[1])):
            if image[x][i]==0 or i in FrameList:
                break
            else:
                image[x][i]=0
        for i in range(y-1,0,-1):
            if image[x][i]==0 or i in FrameList:
                break
            else:
                image[x][i]=0
        
    return image

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        