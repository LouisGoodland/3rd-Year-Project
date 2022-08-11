import GameController, MachineModel, Utility, ImageOrientationDetection
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

#This is simply the main class that is ran
#It sets up a machine model along with the accompying environment to perform reinforcement learning
#or utilise the machine model
model = load_model(r'F:\3rd Year Project\OrientationModel.h5')

#If I am retraining the image orientation model
trainingOrientationModel = False
if(trainingOrientationModel):
    imageTrainer = ImageOrientationDetection.TrainImage()
    imageTrainer.collectData()
    imageTrainer.train()

#Sets up all of the attributes that will be used for the environment
env = MachineModel.RacingEnvironment()
states = env.observation_space.shape
actions = env.action_space.n
model = MachineModel.neuralModel()

#Collects a DQN agent that will play the game
policy = BoltzmannQPolicy()
memory = SequentialMemory(limit=50000000, window_length=1)
dqn = DQNAgent(model=model, memory=memory, policy=policy, nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-3)
dqn.compile(Adam(lr=0.001), metrics=['mae'])

#Variables that will be changed to determine how I am using the program and what progress I have already made
learning = True
iteratorInt = 55
continuation = True

#If I have already made progress, load up the previous work I have done
if(continuation):
    dqn.load_weights(r'F:\3rd Year Project\MachineModelCheckpoints\LearningModel' + str(iteratorInt) + '.h5f')
    iteratorInt = iteratorInt + 1

#If I am training the model
if(learning):
    while(True):
        #runs a 4000 step iteration
        dqn.fit(env, nb_steps=8000, nb_max_start_steps= 5, visualize=False, verbose=1)
        #saves the weights
        dqn.save_weights(r'F:\3rd Year Project\MachineModelCheckpoints\LearningModel' + str(iteratorInt) + '.h5f', overwrite=True)
        #saves the utility data
        Utility.firstTimeSetUp = False
        Utility.save(iteratorInt)
        #removes any keyboard presses
        GameController.offKeys()
        #iterates to the next learning cycle
        iteratorInt = iteratorInt + 1
#If I am testing the model
else:
    #load and test the machine model
    dqn.load_weights(r'F:\3rd Year Project\LearningModel.h5f')
    dqn.test(env, nb_episodes=10000, visualize=False)






