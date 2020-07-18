import gym
import time

#env = gym.make("CartPole-v1")
#overservation = env.reset()
import gym
env = gym.make('SpaceInvaders-v0')
env.reset()
env.render()