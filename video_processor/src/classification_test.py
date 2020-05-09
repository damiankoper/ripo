import cv2
from .processors.Classification import Classification

if __name__ == "__main__":

    c = Classification()

    #c.genAugmentedDataSet("data/training/trimmed_data", "data/training/augmented_data")

    #c.createTrainingData("data/training/dataset/augmented_data", True)

    #c.training("data/training/trained_model", "data/training/pickles")

    c.loadModel("data/training/trained_model")


    im0 = cv2.imread("data/training/tests/test/0.png")
    im1 = cv2.imread("data/training/tests/test/1.png")
    im2 = cv2.imread("data/training/tests/test/2.png")
    im3 = cv2.imread("data/training/tests/test/3.png")
    im4 = cv2.imread("data/training/tests/test/4.png")
    im5 = cv2.imread("data/training/tests/test/5.png")
    im6 = cv2.imread("data/training/tests/test/6.png")
    im7 = cv2.imread("data/training/tests/test/7.png")
    im8 = cv2.imread("data/training/tests/test/8.png")
    im9 = cv2.imread("data/training/tests/test/9.png")
    im10 = cv2.imread("data/training/tests/test/10.png")
    im11 = cv2.imread("data/training/tests/test/11.png")
    im12 = cv2.imread("data/training/tests/test/12.png")
    im13 = cv2.imread("data/training/tests/test/13.png")
    im14 = cv2.imread("data/training/tests/test/14.png")
    im15 = cv2.imread("data/training/tests/test/15.png")
    

    im11_w_ruchu_1 = cv2.imread("data/training/tests/test/11_w_ruchu_1.png")

    im11_w_ruchu_2 = cv2.imread("data/training/tests/test/11_w_ruchu_2.png")

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



    im0 = cv2.imread("data/training/tests/test2/0.png")
    im1 = cv2.imread("data/training/tests/test2/1.png")
    im2 = cv2.imread("data/training/tests/test2/2.png")
    im3 = cv2.imread("data/training/tests/test2/3.png")
    im4 = cv2.imread("data/training/tests/test2/4.png")
    im5 = cv2.imread("data/training/tests/test2/5.png")
    im6 = cv2.imread("data/training/tests/test2/6.png")
    im7 = cv2.imread("data/training/tests/test2/7.png")
    im8 = cv2.imread("data/training/tests/test2/8.png")
    im9 = cv2.imread("data/training/tests/test2/9.png")
    im10 = cv2.imread("data/training/tests/test2/10.png")
    im11 = cv2.imread("data/training/tests/test2/11.png")
    im12 = cv2.imread("data/training/tests/test2/12.png")
    im13 = cv2.imread("data/training/tests/test2/13.png")
    im14 = cv2.imread("data/training/tests/test2/14.png")
    im15 = cv2.imread("data/training/tests/test2/15.png")

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