import cv2
from .processors.Classification import Classification

if __name__ == "__main__":

    c = Classification()

    c.createTrainingData("data/training/data")

    c.training("data/training/model")

    c.loadModel("data/training/model")


    im = cv2.imread("data/training/test/8.png")
    im2 = cv2.imread("data/training/test/16.png")
    im3 = cv2.imread("data/training/test/01.png")


    c.classify(im)
    c.classify(im2)
    c.classify(im3)






