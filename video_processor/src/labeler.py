import cv2
from imutils import paths
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input directory", default=".")
parser.add_argument("-o", "--output", help="Output directory", default=".")
args = parser.parse_args()

imagePaths = sorted(list(paths.list_images(args.input)))
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 500, 500)

image = cv2.imread(imagePaths[0])
cv2.imshow('image', image)
cv2.waitKey(0)

for img in imagePaths:
    cv2.waitKey(10)
    print(img)
    image = cv2.imread(img)
    cv2.imshow('image', image)
    cv2.waitKey(10)
    label = input("Label: ")
    basename = os.path.basename(img)
    os.makedirs(args.output+"/"+label+"/", exist_ok=True)
    os.rename(img, args.output+"/"+label+"/"+basename)
