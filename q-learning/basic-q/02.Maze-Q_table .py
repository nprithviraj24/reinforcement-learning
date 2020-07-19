
import numpy as np
import random
import time
from threeviz.api import plot_line_seg, plot_3d, plot_pose


"""
States
    - 0 means free
    - negative 1 means NOT traversable
    - 1 means goal
"""
# Agent class and his position
class Agent:
    def __init__(self, i=0, j=0): # Agent object has two defined main defined attributes, it's position in 2D space
        self.i = i
        self.j = j
    @property
    def loc(self):
        return (self.i, self.j)

    def vmove(self, direction):
        direction = 1 if direction >0 else -1
        return Agent(self.i+direction, self.j )

    def hmove(self, direction):
        direction = 1 if direction >0 else -1
        return Agent(self.i, self.j+direction)

    def __repr__(self):  # this is a function that returns a printable representation of the given object
        return str(self.loc)

class QLearning:
    def __init__(self, num_states, num_actions, lr=0.1, discount_factor=1.0):
        self.q = np.zeros((num_states, num_actions))
        self.a = lr
        self.g = discount_factor

    def update(self, st, at, rt, st1):
        q = self.q
        a = self.a
        g = self.g
        q[st, at] = (1-a)*q[st, at] + a*(rt+ g*np.max(q[st1]))
        # at - action, q[st] - current_state, a - lr, g - discount factor, q[st1] - next state

class Maze:
    def __init__(self, rows=4, columns=4):
        self.env=np.zeros((4,4))
        self.mousy = Agent(0,0)

    def state_for_agent(self, a):
        nr, nc = self.env.shape
        return a.i*nc + a.j

    def in_bounds(self, i, j):
        nr, nc = self.env.shape # Takes the actual shape of the maze
        return i>=0 and i<nr and j>=0 and j<nc
        # returns a boolean value. True if all of the values satisfy

    def agent_in_bounds(self, a):
        return self.in_bounds(a.i, a.j)

    # this function calculated the position where agent lives in order to make legitimate moves
    def agent_doesnt_die(self, a):
        return not self.env[a.i, a.j] == -1

    def is_valid_new_agent(self, a):
        return self.agent_in_bounds(a) and self.agent_doesnt_die(a)

    @property
    def all_actions(self):
        a = self.mousy
        return [ a.vmove(1),  # 0
                  a.vmove(-1), # 1
                  a.hmove(-1), # 2
                  a.hmove(1)   # 3
                  ]

    def compute_possible_moves(self):
        moves = self.all_actions
        # possible moves for an agent is to move forward or backward in a 2d space.
        # the following statement will return the list of moves that agent can move without hitting the wall
        return [(m, ii) for ii, m in enumerate(moves) if self.is_valid_new_agent(m) ]

    def do_a_move(self, a):
        assert self.is_valid_new_agent(a), "Mousy can't go there"
        self.mousy = a
        return 10 if self.has_won() else -0.1

    def has_won(self):
        a = self.mousy
        return self.env[a.i, a.j] == 1


    def visualize(self):
        # First we need to check if it is :in bounds:
        assert self.in_bounds(*self.mousy.loc), "Mousy is out of bounds"
        # * operator inside a function is used to unpack a tuple
        e = self.env.copy()
        m = self.mousy
        e[m.i, m.j] = 6
        print(e)

    def visualize3d(self):
        # First we need to check if it is :in bounds:
        nr, nc = self.env.shape
        z = 0.1
        a = self.mousy
        # plot_3d(x)
        plot_line_seg(0,0,z, nr,0,z, 'e1', size=0.2, color='red')
        plot_line_seg(0, 0, z, 0, nc, z, 'e2', size=0.2, color='red')
        plot_line_seg(0,nc,z, nr,nc,z, 'e3', size=0.2, color='red')
        plot_line_seg(nr,0,z, nr,nc,z, 'e4', size=0.2, color='red')
        plot_3d(*get_midpoint_for_loc(a.i,a.j), z, 'mousy', color='blue', size=1)
        plot_3d(*get_midpoint_for_loc(3,3), z, 'goal', color='green', size=1)
        xarr, yarr = np.where(self.env==-1)
        plot_3d(xarr+0.5, yarr+0.5, [z]*len(xarr), 'obstacles', size=1.0 )


def get_midpoint_for_loc(i,j):
    return i+0.5, j+0.5

def make_test_maze():
    m = Maze()
    e = m.env
    e[3,3] = 1  # this is our goal state
    e[0, 1:3] = -1  # these are some of the places our agent is not expected to go
    e[1,2:] = -1
    e[3, 0:2] = -1
    return m

def main():
    q = QLearning(16,4)
    for i in range(50):
        #print(i, end=" ")
        final_score = 0
        m = make_test_maze()
        while not m.has_won():
        # list me all the moves possible for the agent
           moves = m.compute_possible_moves();
        # shuffle the moves
           random.shuffle(moves)
        # move: tuple, move_idx: bottom(0), top(1), left (2), right(3)
           move, move_idx = moves[0]
           #print(move)
           at = move_idx
           st = m.state_for_agent(m.mousy)

           score = m.do_a_move(move)
           rt = score
           #print(score)
           #lm = m.mousy()  #last action of the agent
           st1 = m.state_for_agent(m.mousy)

           q.update(st, at, rt, st1)
    print(q.q)

    test_maze = make_test_maze()
    test_maze.visualize3d()
    while not test_maze.has_won():
        time.sleep(0.5)
        # Pick the state of the agent
        st = test_maze.state_for_agent(test_maze.mousy)

        # Select the action that has the highest action value
        a_idx = np.argmax(q.q[st])

        # Tell our agent to make a move
        test_maze.do_a_move(test_maze.all_actions[a_idx]);
        test_maze.visualize3d()
    m.visualize3d()
if __name__=='__main__':
    main()