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

        self.train_images = []
        self.train_labels = []
        self.test_images = []
        self.test_labels = []

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
                    img = keras.preprocessing.image.load_img(imagePath)
                    if img is not None:                 
                        img = keras.preprocessing.image.img_to_array(img)
                        img = np.expand_dims(img, axis=0)

                        generateImage = dataGenerator.flow(img, batch_size=1, save_to_dir=savePath,
                        save_prefix="image", save_format="png")

                        for i in range(11):
                            generateImage.next()

    def createTrainingData(self, dataFolder: str, createPickles: bool = False):
        
        imagePaths = sorted(list(paths.list_images(dataFolder)))
        random.seed(42)
        random.shuffle(imagePaths)

        for img in imagePaths:
            image = cv2.imread(img)
            image = cv2.resize(image, (self.width, self.height))
            self.train_images.append(image)

            label = img.split(os.path.sep)[-2]
            self.train_labels.append(label)

        self.train_images = np.array(self.train_images, dtype="float") / 255.0
        self.train_labels = np.array(self.train_labels)

        (self.train_images, self.test_images, self.train_labels, self.test_labels) = train_test_split(self.train_images,
	    self.train_labels, test_size=0.25, random_state=42)

        if (createPickles):
            pickle_out = open("data/training/pickles/train_images.p","wb")
            pickle.dump(self.train_images, pickle_out)
            pickle_out.close()

            pickle_out = open("data/training/pickles/train_labels.p","wb")
            pickle.dump(self.train_labels, pickle_out)
            pickle_out.close()

            pickle_out = open("data/training/pickles/test_images.p","wb")
            pickle.dump(self.test_images, pickle_out)
            pickle_out.close()

            pickle_out = open("data/training/pickles/test_labels.p","wb")
            pickle.dump(self.test_labels, pickle_out)
            pickle_out.close()

    def training(self, modelPath: str, loadPickles: bool = False):

        if (loadPickles):
            self.train_images = pickle.load(open("data/training/pickles/train_images.p", "rb"))
            self.train_labels = pickle.load(open("data/training/pickles/train_labels.p", "rb"))
            self.test_images = pickle.load(open("data/training/pickles/test_images.p", "rb"))
            self.test_labels = pickle.load(open("data/training/pickles/test_labels.p", "rb"))
        else:
            if(len(self.train_images) == 0):
                print("No training data")
                return


        lb = LabelBinarizer()
        self.train_labels = lb.fit_transform(self.train_labels)
        self.test_labels = lb.transform(self.test_labels)
  

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

        #tensorboard --logdir data/training/logs/
        logName = "log{}".format(int(time.time()))
        tensorboard = keras.callbacks.TensorBoard(log_dir="data/training/logs/{}".format(logName))

        sgd = keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy',
                    optimizer='adam',
                    metrics=['accuracy'])

        reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2,
                  patience=5, min_lr=0.001)

        model.fit(self.train_images, self.train_labels, validation_data=(self.test_images, self.test_labels),
                epochs=15,
                batch_size=64,
                callbacks=[reduce_lr, tensorboard])

        model.save(modelPath+"/model")

        os.makedirs(modelPath+"/labelizer", exist_ok=True)
        pickle_out = open(modelPath+"/labelizer/labelizer.p","wb")
        pickle.dump(lb, pickle_out)
        pickle_out.close()


    def loadModel(self, modelPath: str):
    
        self.model = keras.models.load_model(modelPath+"/model")

        self.labelizer = pickle.load(open(modelPath +"/labelizer/labelizer.p", "rb"))


    def classify(self, image):

        image = cv2.resize(image, (self.width, self.height))

        image = image.astype("float")/255.0

        #image = image.flatten()

        #image = image.reshape((1, image.shape[0]))

        # time_s = time.perf_counter()
        image = np.expand_dims(image, axis=0)

        prediction_result = self.model.predict_on_batch(image)

        # print(time.perf_counter() - time_s)

        i = prediction_result.numpy().argmax(axis=1)[0]
        label = self.labelizer.classes_[i]


        return label, prediction_result
