import cv2
from imutils import paths
import argparse
import os
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input directory", default=".")
parser.add_argument("-o", "--output", help="Output directory", default=".")
args = parser.parse_args()

imagePaths = sorted(list(paths.list_images(args.input)))
cv2.namedWindow('image, +1, +2, +3, +4', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image, +1, +2, +3, +4', 1500, 500)

image = cv2.imread(imagePaths[0])
cv2.imshow('image, +1, +2, +3, +4', image)
cv2.waitKey(0)

firstImg = cv2.imread(imagePaths[0])
first = cv2.calcHist(firstImg, [0, 1, 2], None, [
                     8, 8, 8], [0, 256, 0, 256, 0, 256])


def f(imgPath):
    image = cv2.imread(imgPath)
    #hist = cv2.calcHist(image, [0, 1, 2], None, [
    #                 8, 8, 8], [0, 256, 0, 256, 0, 256])
    distance = np.linalg.norm(np.subtract(firstImg.flatten(), image.flatten()))
    #distance = cv2.compareHist(first,hist,cv2.HISTCMP_CORREL)
    return distance


sortedPaths = sorted(imagePaths, key=f)

last = ""
for (nth, img) in enumerate(sortedPaths):
    cv2.waitKey(10)
    print(img)
    image = cv2.imread(img)
    image1 = cv2.imread(sortedPaths[nth+1])
    image2 = cv2.imread(sortedPaths[nth+2])
    image3 = cv2.imread(sortedPaths[nth+3])
    image4 = cv2.imread(sortedPaths[nth+4])
    cv2.imshow('image, +1, +2, +3, +4',
               np.hstack([image, image1, image2, image3, image4]))
    cv2.waitKey(10)
    label = input("Label: ")
    if label == "":
        label = last
        print("Last assumed: "+str(last))
    else:
        last = label
    basename = os.path.basename(img)
    os.makedirs(args.output+"/"+label+"/", exist_ok=True)
    os.rename(img, args.output+"/"+label+"/"+basename)
