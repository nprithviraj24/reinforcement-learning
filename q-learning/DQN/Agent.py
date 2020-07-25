import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import gym
from dataclasses import dataclass

# Every reinforcement leanring problem consists of 4 important "entities"
@dataclass
class Sarsd: ## State, action, reward, next state
    state: 'typing.Any'
    action: int
    reward: float
    next_state: 'typing.Any'
    done: bool

class DQNAgent:
    def __init__(self, model):
        ### We have to account epsilon (for exploration)
        self.model = model

    def act(self, observations):
        # obs shape is (N, 4)
        q_vals = self.model(obeservations)

        return q_val.max(-1)
# we try to learn a policy that will maximize the expected cumulative
# reward given a distribution of initial states.
# We learn the policy by interacting with the environment through trial and error,
# and use the data gathered in the process to improve our policy.
# But some RL algorithms can learn a policy from data that has been gathered by another policy
class ReplayBuffer:
    def __init__(self, buffer_size=100000):
        self.buffer_size = buffer_size
        self.buffer = []

    def insert(self, sars):
        self.buffer.append(sars)
        self.buffer = self.buffer[-self.buffer_size:]

    def sample(self, num_samples):
        assert num_samples <= len(sel.buffers)
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
        self.opt = optim.Adam(lr=0.0001)

    def forward(self, x):
        return self.net(x)

def train_step(model, state_transitions, tgt, num_actions):
    cur_states = torch.stack([s.state for s in state_transtions])
    rewards = torch.stack([s.reward for s in state_transitions])
    mask = torch.stack([0 if s.done else 1 for s in state_transitions ])
    next_states = torch.stack([0 if s.done else 1 for s in state_transitions ])
    actions = torch.stack([s.action for s in state_transitions ])

    with torch.no_grad():
        qvals_next = tgt(next_states).max(-1)

    qvals = model(cur_states)


def update_target_model(m,tgt):
    tgt.lead_state_dict(m.state_dict())

if __name__ == '__main__':
    env = gym.make("CartPole-v1")
    last_observation = env.reset()
    rb = ReplayBuffer()
    m = Model(env.observation_space.shape, env.action_space.n)
    tgt = Model(env.observation_space.shape, env.action_space.n)
    #qvals = m(torch.Tensor(observation))

    try:
        while True:
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            rb.insert (Sarsd(last_observation, action, reward, observation, done))
            last_observation = observation

            if done:
                last_observation = env.reset()

            if len(rb.buffer) > 5000:
                import ipdb; ipdb.set_trace()
    except KeyboardInterrupt:
        pass
    env.close()