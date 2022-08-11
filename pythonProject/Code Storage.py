import cv2, numpy as np
from PIL import ImageGrab
import matplotlib.pyplot as plt
import pickle
import CarView, ImageOrientationDetection
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, AveragePooling2D, Reshape, MaxPool2D, Conv2D, Softmax
def codeStorage():

    def loadNTrainImageOrientation():

        OrientationChecker = ImageOrientationDetection.TrainImage()
        OrientationChecker.collectData()
        model = OrientationChecker.train()
        model.save(r'F:\3rd Year Project\OrientationModel.h5', overwrite=True)
        model = OrientationChecker.getModel()



    # min = 255
    # max = 255

    testView = CarView.CarView()
    carViewEdge = testView.getView()
    # carViewEdge = np.array(cv2.Canny(np.array(ImageGrab.grab(bbox=(0, 130, 400, 400))), 60, 155)).astype('float32')
    xVal = 280
    yVal = 280
    model = Sequential()
    model.add(Reshape(input_shape=(1, xVal, yVal), target_shape=(xVal, yVal, 1)))
    model.add(MaxPool2D(pool_size=(20, 20), strides=(20, 20), padding='same', input_shape=(xVal, yVal, 1)))
    # model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
    bac = carViewEdge[None][:, :, None]
    output = (model(bac)).eval(session=tf.compat.v1.Session())
    output = np.reshape(output, (output.shape[1], output.shape[2]))
    for i in output:
        print(i)

    # cv2.imwrite(r'F:\3rd Year Project\s' + str(min) + 'x' + str(max) + 'Img.PNG', carViewEdge)
    # for y in range(0, output.shape[0]):
    # for x in range(0, output.shape[1]):
    # if(output[y][x]<100):
    # output[y][x] = 0
    # cv2.imshow('image', carViewEdge)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imshow('image', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    def filterMake():
        output = []
        step = 2
        filterSize = 8
        for y in range(0, carViewEdge.shape[0] - filterSize - 1, step):
            toAdd = []
            for x in range(0, carViewEdge.shape[1] - filterSize - 1, step):
                tempCollection = []
                for i in range(0, filterSize):
                    for z in range(0, filterSize):
                        tempCollection.append(carViewEdge[y + i][x + z])
                toAdd.append(int(np.mean(tempCollection)))
            output.append(toAdd)
        print("done")

    def getDistanceToEdges(self):
        distances = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(self.xCoord - 25, 0):
            distances[5] = distances[5] + 1
            if (self.carViewEdge[i][self.yCoord] == 255):
                break
        print("distance between distances is: ", distances[5])

    while (False):
        carViewEdge = np.array(
            cv2.Canny(np.array(ImageGrab.grab(bbox=(0, 0, 960, 540))), 100, 200))
        cv2.imshow('image', carViewEdge)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    if (False):
        carViewEdge = np.array(cv2.Canny(np.array(ImageGrab.grab(bbox=(0, 0, 960, 540))), 100, 200))
        print(carViewEdge.shape)
        env = MachineModel.RacingEnvironment()
        # Testing
        test = MachineModel.neuralModel()
        test.build()
        print(test.summary())
        episodes = 10
        for episode in range(1, episodes + 1):
            # state = env.reset()
            done = False
            score = 0
            while not done:
                action = random.choice([0, 1, 2, 3])
                n_state, reward, done, info = env.step(action)
                score = score + reward
            print(score)
    test = MiniMapTracker.MiniMapTracker()
    while (False):
        test.returnPosDifference()