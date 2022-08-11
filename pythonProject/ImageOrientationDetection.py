from tensorflow.keras.layers import Dense, Flatten, AveragePooling2D, Reshape, MaxPool2D, Conv2D, Softmax
from tensorflow.keras.models import Sequential
from tensorflow.keras import optimizers, losses, metrics
import matplotlib.pyplot as plt
from tensorflow.python.keras.models import load_model
import CarView
from mlxtend.plotting import plot_confusion_matrix
from sklearn.metrics import confusion_matrix
import numpy as np

#A class that trains and returns its local model on image orientation
class TrainImage():

    #This method goes through the process of collecting screenshots of the car and the label of its orientation
    def collectData(self):
        print("starting data collection")
        #Sets up all of the attributes for training
        self.collecting = True
        #Gets a car view model
        self.testView = CarView.CarView()
        self.training = []
        self.orientationToSave = 0
        self.SavedOrientationsLabels = []

        #Whilst doing the collecting process
        while (self.collecting):
            #Shows the orientation the capture should be
            print("rotation should be: ", self.orientationToSave)
            #Input allows for delaying the screenshot process (to allow to get into position) or to stop
            cont = input("press to continue")
            #if input = n, stop
            if(cont ==  "n"):
                collecting = False
            #add to the training
            self.training.append(self.testView.getView())
            #saving orientation
            self.SavedOrientationsLabels.append(self.orientationToSave / 30)
            #Caps the orientation at maximum angle
            if(self.orientationToSave==360):
                self.orientationToSave = 0
            else:
                self.orientationToSave = self.orientationToSave + 30

        #Converts and saves the orientations
        self.training = np.array(self.training)
        np.save(r'F:\3rd Year Project\SavedOrientations2.npy', self.training)
        print("saved the orientations")

        #Converts and saves the orientation labels
        self.SavedOrientationsLabels = np.array(self.SavedOrientationsLabels.astype('int32'))
        np.save(r'F:\3rd Year Project\SavedOrientationsLabel2.npy', self.SavedOrientationsLabels)
        print("saved the labels as well")

    #Creates and compiles a neural model that will be used for machine orientation
    def getModel(self):
        model = Sequential()
        model.add(Conv2D(filters=6, kernel_size=(5, 5), strides=(1, 1), activation='elu', padding="same", input_shape=(50,50,3)))
        model.add(AveragePooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'))
        model.add(Conv2D(filters=16, kernel_size=(5, 5), strides=(1, 1), activation='elu', padding='valid'))
        model.add(AveragePooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'))
        model.add(Flatten())
        model.add(Dense(units=3800, activation='tanh'))
        model.add(Dense(units=900, activation='tanh'))
        model.add(Dense(units=324, activation='tanh'))
        model.add(Dense(units=108, activation='tanh'))
        model.add(Dense(units=12, activation='tanh'))
        model.add(Softmax())

        #Compiles the model
        model.compile(optimizer=optimizers.SGD(learning_rate=0.003),
                      loss=losses.SparseCategoricalCrossentropy(),
                      metrics=[metrics.CategoricalAccuracy()])
        return model

    #simply gets the trained neural model and returns it
    def loadModel(self):
        model = load_model(r'F:\3rd Year Project\OrientationModel.h5')
        return model

    def train(self):
        #Sets up a model
        self.model = self.getModel()
        self.SavedOrientations = np.load(r'F:\3rd Year Project\SavedOrientations2.npy')
        self.SavedOrientations = self.SavedOrientations.astype('float32')
        self.SavedOrientationsLabels = np.load(r'F:\3rd Year Project\SavedOrientationsLabel2.npy')
        self.SavedOrientationsLabels = self.SavedOrientationsLabels.astype('int32')
        print(self.SavedOrientations.shape)
        print(self.SavedOrientationsLabels.shape)
        self.order = np.random.permutation(len(self.SavedOrientations))
        self.SavedOrientations, self.SavedOrientationsLabels = self.SavedOrientations[self.order], self.SavedOrientationsLabels[self.order]
        # Dividing up the array
        self.arraySize = self.SavedOrientations.shape[0]
        self.split_point = int(self.arraySize * 0.8)

        # Divide the dataset into the two sets, training and test as a 70% split
        self.trnImage1 = np.array(self.SavedOrientations[:self.split_point, :])
        self.trnLabel1 = np.array(self.SavedOrientationsLabels[:self.split_point])
        self.trnImage2 = np.array(self.SavedOrientations[self.split_point:, :])
        self.trnLabel2 = np.array(self.SavedOrientationsLabels[self.split_point:])

        history = self.model.fit(self.trnImage1, self.trnLabel1, epochs=25, validation_split=0.2, verbose=1, batch_size=8, use_multiprocessing=True)

        print(self.model.summary())

        loss, accuracy = self.model.evaluate(self.trnImage2, self.trnLabel2, verbose=0)
        print("loss = ", loss)
        print("accuracy = ", accuracy)

        # Creation of a confusion matrix: (note: might not work after latest update)
        baseNeuralPredictions = self.model.predict_classes(self.trnImage2)
        baseNeuralMatrix = confusion_matrix(self.trnLabel2, baseNeuralPredictions)
        plot_confusion_matrix(conf_mat=baseNeuralMatrix)


        plt.figure(figsize=[10, 5])
        plt.subplot(121)
        plt.plot(history.history['categorical_accuracy'])
        plt.plot(history.history['val_categorical_accuracy'])
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend(['Training Accuracy',
                    'Validation Accuracy'])
        plt.title('Accuracy Curves')

        plt.subplot(122)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend(['Training Loss',
                    'Validation Loss'])
        plt.title('Loss Curves')
        plt.show()

        return self.model

