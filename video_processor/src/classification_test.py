import cv2
from .processors.Classification import Classification

if __name__ == "__main__":

    c = Classification()

    c.createTrainingData("data/training/data")

    c.training("data/training/model")

    c.loadModel("data/training/model")


    im0 = cv2.imread("data/training/test/0.png")
    im1 = cv2.imread("data/training/test/1.png")
    im2 = cv2.imread("data/training/test/2.png")
    im3 = cv2.imread("data/training/test/3.png")
    im4 = cv2.imread("data/training/test/4.png")
    im5 = cv2.imread("data/training/test/5.png")
    im6 = cv2.imread("data/training/test/6.png")
    im7 = cv2.imread("data/training/test/7.png")
    im8 = cv2.imread("data/training/test/8.png")
    im9 = cv2.imread("data/training/test/9.png")
    im10 = cv2.imread("data/training/test/10.png")
    im11 = cv2.imread("data/training/test/11.png")
    im12 = cv2.imread("data/training/test/12.png")
    im13 = cv2.imread("data/training/test/13.png")
    im14 = cv2.imread("data/training/test/14.png")
    im15 = cv2.imread("data/training/test/15.png")
    

    im11_w_ruchu_1 = cv2.imread("data/training/test/11_w_ruchu_1.png")

    im11_w_ruchu_2 = cv2.imread("data/training/test/11_w_ruchu_2.png")

    label, result = c.classify(im0)
    print(label)

    label, result = c.classify(im1)
    print(label)

    label, result = c.classify(im2)
    print(label)

    label, result = c.classify(im3)
    print(label)

    label, result = c.classify(im4)
    print(label)

    label, result = c.classify(im5)
    print(label)

    label, result = c.classify(im6)
    print(label)

    label, result = c.classify(im7)
    print(label)

    label, result = c.classify(im8)
    print(label)

    label, result = c.classify(im9)
    print(label)

    label, result = c.classify(im10)
    print(label)

    label, result = c.classify(im11)
    print(label)

    label, result = c.classify(im12)
    print(label)

    label, result = c.classify(im13)
    print(label)

    label, result = c.classify(im14)
    print(label)

    label, result = c.classify(im15)
    print(label)

    print("Test dla dwóch 11 w ruchu")

    label, result = c.classify(im11_w_ruchu_1)
    print(label)


    label, result = c.classify(im11_w_ruchu_2)
    print(label)


