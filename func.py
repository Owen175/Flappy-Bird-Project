import cv2, numpy as np

img1 = cv2.imread('out.png')
img2 = cv2.imread('out.png')

h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]

#create empty matrix
vis = np.zeros((max(h1, h2), w1+w2,3), np.uint8)

#combine 2 images
vis[:h1, :w1,:3] = img1
vis[:h2, w1:w1+w2,:3] = img2

cv2.imwrite('out.png',vis)