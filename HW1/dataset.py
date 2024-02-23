import os
import cv2
import glob
from PIL import Image
from numpy import asarray

def loadImages(dataPath):
  """
  load all Images in the folder and transfer a list of tuples. The first 
  element is the numpy array of shape (m, n) representing the image. 
  The second element is its classification (1 or 0)
    Parameters:
      dataPath: The folder path.
    Returns:
      dataset: The list of tuples.
  """
  # Begin your code (Part 1)

  ''' Using cv2.imread to read in all the images from the face and non-face folder.
      the star symbol (*) will read in all the files despite its specific name.     '''
  image_face = [cv2.imread(file) for file in glob.glob(dataPath + '/face/*.pgm')]
  image_non = [cv2.imread(file) for file in glob.glob(dataPath + '/non-face/*.pgm')]

  ''' Insert the images and its label to the dataset list in pairs. '''
  dataset = []
  for img in image_face:
    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert image to gray scale
    pair = [0, 0]
    pair[0] = img_g
    pair[1] = 0 # set label of face to 0
    dataset.append(pair)

  for img in image_non:
    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert image to gray scale
    pair = [0, 0]
    pair[0] = img_g
    pair[1] = 1 # set label of face to 1
    dataset.append(pair)

  # End your code (Part 1)

  return dataset