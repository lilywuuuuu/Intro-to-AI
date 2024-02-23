import os
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)

    with open(dataPath) as f:
      lines = f.readlines() # Read in all the lines in the given .txt file
    
    ''' Read in the .txt file '''
    files = []
    cords = []
    count = 0
    num = 0
    file_index = -1
    for line in lines:
      if count == num: # Read in file name and the number of faces
        sep = line.split(" ") # Separate the file name and the number
        files.append(sep[0])
        num = int(sep[1])
        count = 0
        file_index += 1
        cords.append([])
      else: # Read in all the cords 
        count += 1
        sep = line[:-1].split(" ") # Neglect the '\n' sign using splice [:-1]
        c = []
        for i in range(4):
          c.append(int(sep[i])) # Append the cords into c
        cords[file_index].append(c) # Append c to cords[]

    ''' Use the cords and classifer to detect faces. '''
    for i in range(len(files)):
      plt.axis("off")
      image = cv2.imread("data/detect/"+ files[i]) # Read the corresponding image
      img_g = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert the image to grayscale
      imgplot = plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)) # Show the image in grayscale

      rect = []
      for cord in cords[i]:
        cropped = img_g[cord[1]:cord[1]+cord[3], cord[0]:cord[0]+cord[2]] # Crop the image into the right coordinates
        resized = cv2.resize(cropped, (19, 19), interpolation = cv2.INTER_AREA) # Resize the cropped image to 19x19
        face = clf.classify(resized) # Classify the face, 1 is face, 0 is not 
        if face: # Draw green box if it is face
          rect.append(plt.Rectangle((cord[0], cord[1]), cord[2], cord[3], linewidth=1, edgecolor='g', facecolor='none'))
        else: # Draw red box if it is not face
          rect.append(plt.Rectangle((cord[0], cord[1]), cord[2], cord[3], linewidth=1, edgecolor='r', facecolor='none'))
      
      for r in rect:
        plt.gca().add_patch(r) # Show the boxes on the image
      
      plt.show() 

    # End your code (Part 4)