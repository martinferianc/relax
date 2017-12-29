import cv2
import numpy as np

def preprocess_image(img, edge_method="Laplacian"):
      gray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
      # Perform an initial edge detecion
      if edge_method == "Laplacian":
          edges = cv2.Laplacian(gray,cv2.CV_64F)
      elif edge_method == "Canny":
          edges = cv2.Canny(gray,100,200)

      # Convert edge strenghts into probabilities with a normalized matrix
      x,y = edges.shape
      image = np.copy(edges)
      mi = np.amin(image)
      for i in range(x):
          for j in range(y):
              image[i,j]-=mi
      mx = np.amax(image)
      for i in range(x):
          for j in range(y):
              image[i,j]/=mx
      return image,gray,edges

def postprocess_image(img):
      x,y = img.shape
      for i in range(x):
          for j in range(y):
              img[i,j]*=255
      return img
