import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import wandb
from tqdm import tqdm
import numpy as np
from collections import deque

import gym
from dataclasses import dataclass
from typing import Any
from random import sample, random

# Every reinforcement leanring problem consists of 4 important "entities"
@dataclass
class Sarsd: ## State, action, reward, next state
    state: Any
    action: int
    reward: float
    next_state: Any
    done: bool

class DQNAgent:
    def __init__(self, model):
        ### We have to account epsilon (for exploration)
        self.model = model

    def act(self, observations):
        # obs shape is (N, 4)
        q_vals = self.model(obeservations)

        return q_val.max(-1)[1]
# we try to learn a policy that will maximize the expected cumulative
# reward given a distribution of initial states.
# We learn the policy by interacting with the environment through trial and error,
# and use the data gathered in the process to improve our policy.
# But some RL algorithms can learn a policy from data that has been gathered by another policy
class ReplayBuffer:
    def __init__(self, buffer_size=100000):
        self.buffer_size = buffer_size
        self.buffer = deque(maxlen=buffer_size)

    def insert(self, sars):
        self.buffer.append(sars)
        #self.buffer = self.buffer[-self.buffer_size:]

    def sample(self, num_samples):
        assert num_samples <= len(self.buffer)
        return sample(self.buffer, num_samples)

class Model(nn.Module):
    def __init__(self, obs_shape, num_actions):
        super(Model, self).__init__()

        assert len(obs_shape) == 1, "This network only works for flat observations"
        self.obs_shape = obs_shape
        self.num_actions = num_actions

        # Careful of action function, we cannot use ReLU after the last layer because we need to account
        # negative rewards too, and with ReLU it wouldn't be possible for us.
        self.net = torch.nn.Sequential(
            torch.nn.Linear(obs_shape[0], 256),
            torch.nn.ReLU(),
            torch.nn.Linear(256, num_actions)
        )
        self.opt = optim.Adam(self.net.parameters(), lr=0.0001)

    def forward(self, x):
        return self.net(x)

def train_step(model, state_transitions, tgt, num_actions):

    ## For debugging
    #import ipdb; ipdb.set_trace()

    cur_states = torch.stack([torch.Tensor([s.state]) for s in state_transitions])
    rewards = torch.stack([torch.Tensor([s.reward])  for s in state_transitions])
    mask = torch.stack( ([torch.Tensor([0]) if s.done else torch.Tensor([1]) for s in state_transitions ]))  ## s.done returns a boolean value
    next_states = torch.stack([torch.Tensor([s.next_state]) for s in state_transitions])
    actions = [s.action for s in state_transitions ]

    with torch.no_grad():
        qvals_next = tgt(next_states).max(-1)[0]

    model.opt.zero_grad()
    qvals = model(cur_states)

    ## One hot because it will only give those values that are the agent took.
    one_hot_actions = F.one_hot(torch.LongTensor(actions), num_actions)

    # mask = 0, when the game has ended
    loss = ((rewards + mask[:, 0]*qvals_next - torch.sum(qvals*one_hot_actions, -1))**2).mean()
    loss.backward()
    model.opt.step()
    return loss


def update_target_model(m,tgt):
    tgt.load_state_dict(m.state_dict())

def main(test=False, chkpoint=None):
    if not test:
        wandb.init(project="dqn-tutorial", name="dqn-cartpole")

    # Exploration
    eps_min = 0.01
    eps_decay = 0.999995  ## over the period of time we should minimize the exploration


    # constraints
    min_rb_size = 10000
    sample_size = 2500
    env_steps_before_train = 100
    tgt_model_update = 150

    env = gym.make("CartPole-v1")
    last_observation = env.reset()
    rb = ReplayBuffer()
    steps_since_train = 0
    epochs_since_tgt = 0

    m = Model(env.observation_space.shape, env.action_space.n)
    if chkpoint is not None:
        m.load_state_dict(torch.load(chkpoint))
    tgt = Model(env.observation_space.shape, env.action_space.n)
    update_target_model(m, tgt)
    #qvals = m(torch.Tensor(observation))

    step_num = -1 * min_rb_size
    episode_rewards = []
    rolling_reward = 0

    tq = tqdm()
    try:
        while True:
            if test:
                env.render()
                time.sleep(0.05)
            tq.update(1)

            eps = eps_decay**(step_num)

            if test:
                eps = 0

            if random() <eps: # Explore
                action = env.action_space.sample()
            else:  # Exploit
                #import ipdb; ipdb.set_trace()
                action = m(torch.Tensor(last_observation)).max(-1)[-1].item()

            observation, reward, done, info = env.step(action)
            rolling_reward += reward

            rb.insert(Sarsd(last_observation, action, reward, observation, done))
            last_observation = observation

            if done:
                episode_rewards.append(rolling_reward)
                if test:
                    print(rolling_reward)
                rolling_reward = 0
                observation = env.reset()

            steps_since_train +=1
            step_num += 1

            if (not test) and len(rb.buffer) > min_rb_size and steps_since_train > env_steps_before_train:
                loss = train_step(m, rb.sample(sample_size), tgt, env.action_space.n)
                wandb.log({'loss': loss.detach().item(), 'eps': eps, 'avg_reward': np.mean(episode_rewards)}, step=step_num)
                #print(step_num, loss.detach().item())
                epochs_since_tgt += 1

                if epochs_since_tgt > tgt_model_update:
                    print(" Updating Target model")
                    update_target_model(m, tgt)
                    epochs_since_tgt = 0
                    torch.save(tgt.state_dict(), f"../../../models/rl/{step_num}.pth")
                steps_since_train = 0

    except KeyboardInterrupt:
        pass
    env.close()

if __name__ == '__main__':
    main()