# -*- coding: utf-8 -*-
"""
Created on Tue May  4 01:01:47 2021

@author: white
"""


import SimpleITK as sitk
import Masks
import numpy as np
import Mask3filter as mask
from keras.models import load_model

def Unetpredict(unetmodel : str, nrrdfilename : str):
    unetmodel=load_model(unetmodel)
    imageinput=sitk.ReadImage(nrrdfilename)
    imageinput=Masks.reScaleas255(imageinput)
    imageinput = sitk.GetArrayFromImage(imageinput)
    masked_image=[]
    predicted_image=[]
    for i in range(0,len(imageinput)):
        pred=unetmodel.predict(np.asarray([imageinput[i]]) ).reshape((512,512))
        for j in range(0,len(pred)):
            for k in range(0,len(pred[0])):
                if pred[j][k]>=127:
                    pred[j][k]=255
                else:
                    pred[j][k]=0
        
        masked_image.append(pred)
    for i in range(0,len(masked_image)):
      for j in range(512):
        for k in range(512):
          if masked_image[i][j][k]==255:
            masked_image[i][j][k]=0
          else:
            masked_image[i][j][k]=255
    for i in range(0,len(masked_image)):
      predicted_image.append(mask.Mask3(masked_image[i].astype(np.uint8)))
    return sitk.GetImageFromArray(predicted_image*imageinput*(1/255))