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


class Maze:
    def __init__(self, rows=4, columns=4):
        self.env=np.zeros((4,4))
        self.mousy = Agent(0,0)
        self.q = np.zeros((rows*columns, 4 ))

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

    def compute_possible_moves(self):
        a = self.mousy
        # possible moves for an agent is to move forward or backward in a 2d space.
        moves = [ a.vmove(1),
                  a.vmove(-1),
                  a.hmove(-1),
                  a.hmove(1)
                  ]
        # the following statement will return the list of moves that agent can move without hitting the wall
        return [m for m in moves if self.is_valid_new_agent(m) ]

    def do_a_move(self, a):
        assert self.is_valid_new_agent(a), "Mousy can't go there"
        self.mousy = a
        return 10 if self.has_won() else -0.1

    def has_won(self):
        a = self.mousy
        return self.env[a.i, a.j] == 1


    def visualize(self):
        # First we need to check if it is :in bounds:
        assert self.in_bounds(*(self.mousy.loc)), "Mousy is out of bounds" # * operator inside a function is used to unpack a tuple
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
    m = make_test_maze()
    final_score = 0
    # m.mousy = m.mousy.vmove(0)
    while not m.has_won():
        moves = m.compute_possible_moves()
        random.shuffle(moves)
        final_score += m.do_a_move(moves[0])
        print(moves[0])
        m.visualize3d()
        # m.mousy = moves[-1]
        # m.visualize()
        time.sleep(0.5)
if __name__=='__main__':
    main()