import numpy

# DO NOT MODIFY INTERFACES or RETURN-VALUES. This would maybe break compatibility
# with the testing framework,

def calculate_value_for_action_det (env, state, V, discount_factor):
    """
    Function to calculate the value for all actions in a given state.

    :param env: Instance of the Gridworld_det class.
    :param state: scalar, index of the current state s
    :param V: array-like, shape = (nSp,), vector containing the
              current value-function estimate.
    :param discount_factor: scalar, discount factor \gamma

    :return: array-like, shape = (nA,), vector containing the
             value for each action.
    """

    ## STUDENT TASK ##
    # Pre-define a vector A to store all the values.
    A = numpy.zeros (env.nA)
    
    # Calculate value for each action a in A
    for action in range(len(A)):

        # Get the reward from the reward function R(s,a) of the environment
        # x, y = env._state2coord(state)
        # reward = env.rewards[env.world[y, x]]
        reward=env.R[state][action]
        
       
        # Get the new state from the transition model T(s,a) of the environment
        new_state_a = env.T[state][action]
        
       
        # Calculate R(s,a) + \gamma * v(T(s,a))
        A[action] = reward+discount_factor*V[new_state_a]
        

    return A

def value_iteration (env, theta = 0.0001, discount_factor = 0.9, verbose = True):
    """
    Implementation of the value-iteration algorithm.

    :param env: env: Instance of the Gridworld_det class.
    :param theta: scalar, convergence threshold
    :param discount_factor: scalar, discount factor \gamma

    :return: array-like, shape = (nSp,), vector containing the
             value-function estimate.
    """

    ## STUDENT TASK ##
    # Initialize value function V(s) for each state s in S+.
    # Note: Use a numpy array of the correct length to store all V(s) values, e.g. numpy.zeros
    V = numpy.zeros (env.nSp)

    k = 0

    while True:
        # Stopping condition
        delta = 0

        ## STUDENT TASK ##
        # Update for each state s in S the value function V(s), according to the
        # value-iteration algorithm (see exercise description).
        for s in env.S: # for ...
            # Save the old value V(s)
            v = V[s]

            # Calculate: R(s,a) + \gamma * v(T(s,a)) for each a in A.
            # NOTE: The helper-function 'calculate_value_for_action_det'
            #       does that for you and stores each the result into
            #       a vector:
            #           [R(s,a_1) + \gamma * v(T(s,a_1)),
            #            R(s,a_2) + \gamma * v(T(s,a_2)),
            #            ...]
            A = calculate_value_for_action_det (env, s, V, discount_factor)

            # Find the best action from 'A' and assign its value to V(s) (update)
            V[s] = max(A)

            # Update the delta as max(delta, |V(s)-v|)
            delta = max(delta,abs(V[s]-v))

        # Plot the value-function in each iteration
        if verbose:
            print ("Reshaped Grid Value Function:")
            print (V.reshape (env.shape))
            print ("")

        k += 1

        # Check if we can stop
        if delta < theta:
            break
    if verbose:
        print ("Iterations (value iteration): %d" % k)

    return V

def extract_deterministic_policy (env, V, discount_factor = 0.9):
    """
    Find the optimal deterministic policy using a greedy strategy.

    If two actions 'a_1' and 'a_2' have the same value for a certain
    state 's', the first depending on the order of the action indices
    is chosen.

    :param env: env: Instance of the Gridworld_det class.
    :param V: array-like, shape = (nSp,), vector containing the
              value-function estimate.
    :param discount_factor: scalar, discount factor \gamma

    :return: (policy, Q)-tuple
        policy: array-like, shape = (nSp,), optimal action action 'a'
                in state 's'.
        Q: array-like, shape = (nSp, nA), Q-value of the action
           'a' in state 's'.
    """

    # Deterministic policy \pi(.): S --> A
    #   policy[s] ... optimal action in state 's'
    policy = numpy.zeros (env.nSp)

    # Q is the action-value-function. This function is used
    # for the rendering of the optimal policy.
    # Q is represented as two-dimensional matrix
    #   Q[s,a] ... V(s) for all a in A
    Q = numpy.zeros ([env.nSp, env.nA])

    ## STUDENT TASK ##
    for s in env.S:
        # Calculate: R(s,a) + \gamma * v(T(s,a)) for each a in A.
        # NOTE: The helper-function 'calculate_value_for_action_det'
        #       does that for you and stores each the result into
        #       a vector:
        #           [R(s,a_1) + \gamma * v(T(s,a_1)),
        #            R(s,a_2) + \gamma * v(T(s,a_2)),
        #            ...]
        A = calculate_value_for_action_det (env, s, V, discount_factor)
        # print(A)

        # Get the _index_ of the (first) best action, e.g. using 'numpy.argmax'.
        best_action = numpy.argmax(A)

        assert (best_action in env.A) # It will throw an error, if the action index
                                      # is not in A.

        # Always the best action should be chosen for each state 's'.
        policy[s] = best_action
        Q[s, :] = A
    
    #print(Q[1,2])
    return policy, Q


# if __name__ == '__main__':
#     calculate_value_for_action_det (env, state, V, discount_factor)