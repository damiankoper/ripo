import numpy as np
import random
import pickle
import cv2
import os
import pickle
from tensorflow import keras
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from imutils import paths
import time

class Classification:
    def __init__(self, width: int = 50, height: int = 50, depth: int = 3):    

        self.model = None
        self.labelizer = None

        self.width = width
        self.height = height
        self.depth = depth

    def genAugmentedDataSet(self, dataFolder: str, newDataFolder: str):

            dataGenerator = keras.preprocessing.image.ImageDataGenerator(
                rotation_range=90,
                width_shift_range=0.05,
                height_shift_range=0.05,
                shear_range=0.5,
                horizontal_flip=True,
                vertical_flip=True,
                fill_mode="nearest")
            
            for label in os.listdir(dataFolder):
                labelPath = os.path.join(dataFolder, label)
                savePath = os.path.join(newDataFolder, label)
                for image in os.listdir(labelPath):
                    imagePath = os.path.join(labelPath, image)
                    print(imagePath)
                    img = keras.preprocessing.image.load_img(imagePath)
                    if img is not None:                 
                        img = keras.preprocessing.image.img_to_array(img)
                        img = np.expand_dims(img, axis=0)

                        generateImage = dataGenerator.flow(img, batch_size=1, save_to_dir=savePath,
                        save_prefix="image", save_format="jpg")

                        for i in range(101):
                            generateImage.next()

    def createTrainingData(self, dataFolder: str):
        
        train_images = []
        train_labels = []

        imagePaths = sorted(list(paths.list_images(dataFolder)))
        random.seed(42)
        random.shuffle(imagePaths)

        for img in imagePaths:
            image = cv2.imread(img)
            image = cv2.resize(image, (self.width, self.height))
            train_images.append(image)

            label = img.split(os.path.sep)[-2]
            train_labels.append(label)

        train_images = np.array(train_images, dtype="float") / 255.0
        train_labels = np.array(train_labels)

        (train_images, test_images, train_labels, test_labels) = train_test_split(train_images,
	    train_labels, test_size=0.25, random_state=42)

        pickle_out = open("data/training/pickles/train_images.p","wb")
        pickle.dump(train_images, pickle_out)
        pickle_out.close()

        pickle_out = open("data/training/pickles/train_labels.p","wb")
        pickle.dump(train_labels, pickle_out)
        pickle_out.close()

        pickle_out = open("data/training/pickles/test_images.p","wb")
        pickle.dump(test_images, pickle_out)
        pickle_out.close()

        pickle_out = open("data/training/pickles/test_labels.p","wb")
        pickle.dump(test_labels, pickle_out)
        pickle_out.close()

    def training(self, modelPath: str):

        train_images = pickle.load(open("data/training/pickles/train_images.p", "rb"))
        train_labels = pickle.load(open("data/training/pickles/train_labels.p", "rb"))
        test_images = pickle.load(open("data/training/pickles/test_images.p", "rb"))
        test_labels = pickle.load(open("data/training/pickles/test_labels.p", "rb"))

        lb = LabelBinarizer()
        train_labels = lb.fit_transform(train_labels)
        test_labels = lb.transform(test_labels)
  

        # model = keras.models.Sequential()
        # model.add(keras.layers.Dense(32, input_shape=((self.width*self.height*self.depth),), activation='relu'))
        # model.add(keras.layers.Dense(len(lb.classes_), activation='softmax'))
        
        # model.compile(optimizer='rmsprop',
        #             loss='categorical_crossentropy',
        #             metrics=['accuracy'])

        # model.fit(train_images, train_labels, validation_data=(test_images, test_labels), epochs=100, batch_size=32)


        # model = keras.models.Sequential()
        # model.add(keras.layers.Dense(128, activation='relu', input_shape=((self.width*self.height*self.depth),)))
        # model.add(keras.layers.Dropout(0.1))
        # model.add(keras.layers.Dense(64, activation='relu'))
        # model.add(keras.layers.Dropout(0.1))
        # model.add(keras.layers.Dense(len(lb.classes_), activation='softmax'))

        model = keras.models.Sequential()

        model.add(keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(50, 50, 3)))
        model.add(keras.layers.Conv2D(32, (3, 3), activation='relu'))
        model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
        model.add(keras.layers.Dropout(0.25))

        model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
        model.add(keras.layers.Dropout(0.25))

        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dense(256, activation='relu'))
        model.add(keras.layers.Dense(len(lb.classes_), activation='softmax'))

        sgd = keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy',
                    optimizer=sgd,
                    metrics=['accuracy'])

        model.fit(train_images, train_labels, validation_data=(test_images, test_labels),
                epochs=5,
                batch_size=32)

        model.save(modelPath)

        pickle_out = open("data/training/pickles/labelizer.p","wb")
        pickle.dump(lb, pickle_out)
        pickle_out.close()


    def loadModel(self, modelPath: str):
    
        self.model = keras.models.load_model(modelPath)

        self.labelizer = pickle.load(open("data/training/pickles/labelizer.p", "rb"))


    def classify(self, image):

        image = cv2.resize(image, (self.width, self.height))

        image = image.astype("float")/255.0

        #image = image.flatten()

        #image = image.reshape((1, image.shape[0]))

        #time_s = time.perf_counter()
        image = np.expand_dims(image, axis=0)

        prediction_result = self.model.predict_on_batch(image)

        #print(time.perf_counter() - time_s)

        i = prediction_result.numpy().argmax(axis=1)[0]
        label = self.labelizer.classes_[i]


        return label, prediction_result
