# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import tensorflow_addons as tfa
import SimpleITK as sitk
import Masks
import cv2 as cv


# Image size that we are going to use
IMG_SIZE = 512
# Our images are RGB (3 channels)
N_CHANNELS =1
# Scene Parsing has 150 classes + `not labeled`
N_CLASSES = 2

def parse_image(img_path: str) -> dict:
    """Load an image and its annotation (mask) and returning
    a dictionary.

    Parameters
    ----------
    img_path : str
        Image (not the mask) location.

    Returns
    -------
    dict
        Dictionary mapping an image and its annotation.
    """
    image = tf.io.read_file(img_path)
    image = tf.io.decode_png(image,channels=1)
    image = tf.image.convert_image_dtype(image, tf.uint8)

    # For one Image path:
    # .../trainset/images/training/ADE_train_00000001.jpg
    # Its corresponding annotation path is:
    # .../trainset/annotations/training/ADE_train_00000001.png
    mask_path = tf.strings.regex_replace(img_path, "resimler", "maskeler")
    mask_path = tf.strings.regex_replace(mask_path, ".png", "Mask_3.png")
    mask = tf.io.read_file(mask_path)
    # The masks contain a class index for each pixels
    mask = tf.io.decode_png(mask,channels=1)
    # In scene parsing, "not labeled" = 255
    # But it will mess up with our N_CLASS = 150
    # Since 255 means the 255th class
    # Which doesn't exist
    # mask = tf.where(mask == 255, np.dtype('uint8').type(0), mask)
    # Note that we have to convert the new value (0)
    # With the same dtype than the tensor itself

    return {'image': image, 'segmentation_mask': mask}

def load_image_test(datapoint) :
    """Normalize and resize a test image and its annotation.

    Notes
    -----
    Since this is for the test set, we don't need to apply
    any data augmentation technique.

    Parameters
    ----------
    datapoint : dict
        A dict containing an image and its annotation.

    Returns
    -------
    tuple
        A modified image and its annotation.
    """
    input_image = datapoint
    

    input_image = normalize(input_image)

    return input_image
def normalize(input_image: tf.Tensor) -> tuple:
    """Rescale the pixel values of the images between 0.0 and 1.0
    compared to [0,255] originally.

    Parameters
    ----------
    input_image : tf.Tensor
        Tensorflow tensor containing an image of size [SIZE,SIZE,3].
    input_mask : tf.Tensor
        Tensorflow tensor containing an annotation of size [SIZE,SIZE,1].

    Returns
    -------
    tuple
        Normalized image and its annotation.
    """
    input_image = tf.cast(input_image, tf.float32) / 255.0
    return input_image

@tf.function



def create_mask(pred_mask: tf.Tensor) -> tf.Tensor:
    """Return a filter mask with the top 1 predicitons
    only.

    Parameters
    ----------
    pred_mask : tf.Tensor
        A [IMG_SIZE, IMG_SIZE, N_CLASS] tensor. For each pixel we have
        N_CLASS values (vector) which represents the probability of the pixel
        being these classes. Example: A pixel with the vector [0.0, 0.0, 1.0]
        has been predicted class 2 with a probability of 100%.

    Returns
    -------
    tf.Tensor
        A [IMG_SIZE, IMG_SIZE, 1] mask with top 1 predictions
        for each pixels.
    """
    # pred_mask -> [IMG_SIZE, SIZE, N_CLASS]
    # 1 prediction for each class but we want the highest score only
    # so we use argmax
    pred_mask = tf.argmax(pred_mask, axis=-1)
    # pred_mask becomes [IMG_SIZE, IMG_SIZE]
    # but matplotlib needs [IMG_SIZE, IMG_SIZE, 1]
    pred_mask = tf.expand_dims(pred_mask, axis=-1)
    return pred_mask
 
def predict_nrrd(image):
    model=load_model("best_model.h5")   
    np_image = Masks.reScaleas255(image)
    np_image = sitk.GetArrayFromImage(np_image)
    predict_array =[]
    remainder = len(np_image)%5
    length =int(len(np_image)/5)
    
    for i in range(0,length):
        print(i)
        imagearray=[]
        for j in range(0,5):
            dicts = np_image[j+(i*5)]
            image_deneme = np.array(dicts)
            image=load_image_test(dicts)
            imagearray.append(image)
            
            
        imagearray=np.array(imagearray)
    
        imagearray.shape
    
        one_img_batch = imagearray
        inference = model.predict(one_img_batch)
        pred_mask = create_mask(inference)
        predict_array.append(np.array(pred_mask[0]).reshape((512,512)))
        predict_array.append(np.array(pred_mask[1]).reshape((512,512)))
        predict_array.append(np.array(pred_mask[2]).reshape((512,512)))
        predict_array.append(np.array(pred_mask[3]).reshape((512,512)))
        predict_array.append(np.array(pred_mask[4]).reshape((512,512)))
        
    for i in range(0,remainder):
        xd = len(np_image)-remainder
        imagearray=[]
        
        dicts = np_image[xd+i]
        image_deneme = np.array(dicts)  
        image=load_image_test(dicts)
        for j in range(0,5):    
            imagearray.append(image)
            
            
        imagearray=np.array(imagearray)
        imagearray.shape
    
        one_img_batch = imagearray
        inference = model.predict(one_img_batch)
        pred_mask = create_mask(inference)
        predict_array.append(np.array(pred_mask[0]).reshape((512,512)))
    
    predict_array = np.array(predict_array)
    predict_array = predict_array*255
    predict_sitk =sitk.GetImageFromArray(predict_array)
    
  
    return predict_sitk
