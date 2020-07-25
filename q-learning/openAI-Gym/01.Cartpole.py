import gym
import time

env = gym.make("CartPole-v1")
overservation = env.reset()

for i in range(1000):
    env.render()
    time.sleep(0.1)

    ## for info about action space and following variables/
    # Switch to next line using "n"
    import ipdb; ipdb.set_trace()
    action = env.action_space.sample()
    # env.action_space to get number of actions
    # env.observation_space.shape to get shape of observation
    observation, reward, done, info = env.step(action)

    if done:
        observation = env.reset()
env.close()