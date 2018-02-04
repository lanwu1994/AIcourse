import numpy

NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3

class Gridworld_det:
    """
    You are an agent on an MxN grid and your goal is to reach the terminal
    state at the top left or the bottom right corner.

    For example, a 5x5 grid could look as follows:

    T  .  .  .  .
    .  .  .  .  .
    .  x  o  o  o
    .  .  .  .  .
    .  .  .  .  T

    x is your position,  T is a terminal state, o is an obstacle.

    You can take actions in each direction (NORTH=0, SOUTH=1, WEST=2, EAST=3).
    Actions going off the edge or causing a collision with an obstacle leave
    you in your current state.

    You receive a reward of -1 at each step until you reach a terminal state
    in which you do receive a reward of 0.
    """

    def __init__(self, world_definition = None):
        if world_definition is None:
            self.world, self.rewards = Gridworld_det._create_example_world ("4x4_world")
        else:
            self.world, self.rewards = world_definition

        self.shape = self.world.shape
        self.MAX_Y = self.shape[0]
        self.MAX_X = self.shape[1]

        # State space
        self.nSp = numpy.prod (self.shape)
        self.S = [0 for _ in range(1,self.nSp)]      # S  ... set of all non-terminal states
        self.Sp = [0 for _ in range(self.nSp)]    # S+ ... set of all states, S \cup {T1, T2, ...}

        # Action space / set of actions
        self.A = [NORTH, SOUTH, WEST, EAST]
        self.nA = len (self.A)

        # Description of the process dynamics using a _deterministic_ model:
        # - Transition model:   T(.,.): S x A --> S
        # - Reward function:    R(.,.): S x A --> R
        self.T = {state:{} for state in range(self.nSp)} # transition
        self.R = {state:{} for state in range(self.nSp)} # reward

        for state in range (self.nSp):

            self.T[state] = {a : [] for a in self.A} # T[state][action] ~ T(s,a)
            self.R[state] = {a : [] for a in self.A} # R[state][action] ~ R(s,a)

            ## STUDENTS TASK ##
            # 'state' is a terminal state: 'T'
            if self._is_terminal (state):
                self.Sp.append (state)

                # state' = state: The robot does not move from a terminal state,
                #                 regardless of the chosen action.
                for action in self.A:
                    new_state_a = state

                    # Get the reward of the updated state from the world.
                    x, y = self._state2coord (new_state_a)
                    reward = self.rewards[self.world[y, x]] # NOTE: The world is stored as matrix
                                                            #       therefore we need to access it
                                                            #       (row,column).
                    #print(self.T[state][action])
                    self.T[state][action] = state
                    self.R[state][action] = reward
                    #print(self.T[state][action])


            # 'state' isn't a terminal state
            else:
                self.S.append (state)

                # state' = state + action: The robot moves to the updated state.
                for action in self.A:

                    new_state_a = self._update_state(state,action)
                  
                    # Get the reward of the updated state from the world.
                    x, y = self._state2coord(new_state_a)
                    
                    reward = self.rewards[self.world[y, x]] # NOTE: The world is stored as matrix
                                                            #       therefore we need to access it
                                                            #       (row,column).

                    self.T[state][action] = new_state_a
                    self.R[state][action] = reward

        self.Sp = self.Sp + self.S

    def _update_state (self, state, action):
        """
        Task: Update the current s state with an action a.

        NOTE: The origin of the gridworld is considered to be in the SOUTH-WEST
              corner:

           (0,0)  x
             +-------->
             |  T . . .
             |y . . . .
             |  . . . .
             V  . . . .

              For example if you wanna move to EAST you need do modify the current
              coordinates [x,y] + [1,0]. For SOUTH it would be [x,y] + [0,1].

        :param state: scalar, index of state s
        :param action: scalar, index of action a

        :return: scalar. index of the new state s'
        """
        if not action in self.A:
            raise ValueError ("Invalid action %d." % action)

        xy = numpy.array (self._state2coord (state), dtype = "int")
     
        # xy ... vector like [x, y]

        ## STUDENTS TASK ##
        if action == NORTH:
            new_xy = xy + [0,-1]
        elif action == SOUTH:
            new_xy = xy + [0,1]
        elif action == WEST:
            new_xy = xy + [-1,0]
        elif action == EAST:
            new_xy = xy + [1,0]

        if self._is_outside_at (new_xy):
            # If the updated state, would place the robot outside the world,
            # the robot remains in the current state s.

            return self._coord2state (xy)
        elif self._is_obstacle_at (new_xy):
            # If at the updated state s' an obstacle is placed, than the robot
            # cannot move there and remains in the current state s.

            return self._coord2state (xy)
        else:
            return self._coord2state (new_xy)


    @staticmethod
    def _create_example_world (type = "4x4_world"):
        """
        Function to create example grid-worlds.

        New worlds can be added here following the scheme of the
        already implemented examples.

        :param type: string, either "4x4_world", "obstacles" or YOUR_OWN_WORLD

        :return:
        """

        if type == "4x4_world":
            rewards = {"T": 0.0, ".": -1.0}
            world = numpy.array (
                [["T", ".", ".", "."],
                 [".", ".", ".", "."],
                 [".", ".", ".", "."],
                 [".", ".", ".", "T"]])

        elif type == "obstacles":
            rewards = {"T": 0.0, ".": -1.0, "o": -1.0}
            world = numpy.array (
                [[".", ".", ".", ".", ".", "."],
                 [".", "o", ".", ".", ".", "."],
                 [".", "o", "o", ".", ".", "."],
                 [".", ".", "o", ".", ".", "."],
                 [".", ".", "o", "o", "o", "o"],
                 [".", ".", ".", ".", ".", "T"]])

        elif type == "6x6_world_blocked":
            rewards = {"T": 0.0, ".": -1.0, "o": -1.0}
            world = numpy.array (
                [["T", ".", ".", ".", ".", "."],
                 [".", ".", ".", ".", ".", "."],
                 [".", ".", "o", "o", "o", "o"],
                 [".", ".", "o", ".", ".", "."],
                 [".", ".", "o", ".", ".", "."],
                 [".", ".", "o", ".", ".", "."]])

        elif type == "6x4_world_2":
            rewards = {"T": 0.0, ".": -1.0, "o": -1.0, "x": -5.0}
            world = numpy.array (
                [["T", ".", ".", "."],
                 ["x", "x", "x", "x"],
                 ["x", "x", ".", "x"],
                 ["x", "x", ".", "x"],
                 ["x", "x", ".", "x"],
                 [".", ".", ".", "."]])
        else:
            raise ValueError ("Invalid example world type: %s" % type)

        return world, rewards

    def _is_terminal (self, state):
        """
        Determine, whether the current state s is a terminal state with respect to the
        current world.

        :param state: integer, state signal
        :return: boolearn, true: state is a terminal state, false: else
        """

        x, y = self._state2coord (state)
        return self.world[y, x] == "T"

    def _is_outside_at (self, xy):

        """
        Task: Check whether the position is outside the world, i.e. a invalid one.

        :param state: tuple, states coordinates, (x, y)
        :return: boolean, true: coordinates outside, false: else
        """
        y, x = xy[1], xy[0]

        return y < 0 or x < 0 or y >= self.MAX_Y or x >= self.MAX_X

    def _is_obstacle_at (self, xy):
        """
        Is at the current position an obstacle placed?

        :param state: tuple, states coordinates, (x, y)
        :return: boolean, true: at coordinates is no obstacle, false: else
        """
        y, x = xy[1], xy[0]

        return self.world[y, x] == 'o'

    def _state2coord (self, state):
        """
        Inverse index map: i^{-1}(.,.): {0, 1, ..., K * L - 1} --> [K] x [L]

        :param state: integer, state signal
        :return: tuple, states coordinates, (x, y)
        """

        yx = numpy.unravel_index (state, self.shape, order ="C")

        return (yx[1], yx[0])

    def _coord2state (self, xy):
        """
        Bijective index map: i(.): [K] x [L] --> {0, 1, ..., K * L - 1}

        :param xy: tuple or array-like, coordinates to map
        :return: integer, state signal
        """

        return numpy.ravel_multi_index ((xy[1], xy[0]), self.shape, order = "C")

    def _action2str (self, action):
        """
        Convert the numerical action representation into a string.

        :param action: integer, a in A
        :return: string, verbal representation of the action.
        """

        if action == NORTH:
            astr = "NORTH"
        elif action == SOUTH:
            astr = "SOUTH"
        elif action == WEST:
            astr = "WEST"
        elif action == EAST:
            astr = "EAST"
        else:
            raise ValueError ("Invalid action %d." % action)

        return astr

# env = Gridworld_det()