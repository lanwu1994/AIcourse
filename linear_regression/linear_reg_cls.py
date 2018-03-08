import numpy


def cost(X, y, w):
    """
    Task: compute value of the cost function
    :param X: array of shape (n_samples, n_features), dataset of features
    :param y: array of shape (n_samples, n_targets), dataset of target values
    :param w: array of shape (n_features, n_targets), weight vector
    :return:
    Let's denote N = n_samples, m = n_features, k = n_targets.
    Suppose X = [[x_11, x_12, ..., x_1m]
                 [x_21, x_22, ..., x_2m]
                 ...
                 [x_N1, x_N2, ..., x_Nm]]

            y = [[y_11, y_12, ..., y_1k]
                 [y_21, y_22, ..., y_2k]
                 ...
                 [y_N1, y_N2, ..., y_Nk]]

            w = [[w_11, w_12, ..., w_1k]
                 [w_21, w_22, ..., w_2k]
                 ...
                 [w_m1, w_m2, ..., w_mk]]

    Then value of the cost function has consists of k parts.
    The form of the j-th part has the following format:

    cost_j = 1/N * [(x_11*w_1j + x_12*w_2j + ... + x_1m*w_mj - y_1j)^2 +
                    (x_21*w_1j + x_22*w_2j + ... + x_2m*w_mj - y_2j)^2 +
                    ... +
                    (x_N1*w_1j + x_N2*w_2j + ... + x_Nm*w_mj - y_Nj)^2]

    Then value of the cost function has the following value:
    cost = 1/k * (cost_1 + cost_2 + ... + cost_k)

    HINT: You can compute value of the cost function way easier by using
    vectorized operations with following numpy functions: np.mean, np.dot.

    NOTE: Your implementation will be tested with different values of N, m and k.
    Please, don't make any assumptions in the code about particular values for them.

    NOTE: Returned value should have 'float' type
    """

    ## STUDENT TASK ##
    # Task: Return the value of the cost function for given X, y and w.
    N = X.shape[0]
    m = X.shape[1]
    k = y.shape[1]
    cost=0

    for j in range(k):
        cost_j = numpy.mean((numpy.dot(X,w)-y)**2)
        cost = cost+cost_j

    cost = 1.0*cost/k
    return cost


def gradient(X, y, w):
    """
    Task: compute value of the gradient of cost function
    :param X: array of shape (n_samples, n_features), dataset of features
    :param y: array of shape (n_samples, n_targets), dataset of target values
    :param w: array of shape (n_features, n_targets), weight vector
    :return:
    Let's denote N = n_samples, m = n_features, k = n_targets.
    Suppose X = [[x_11, x_12, ..., x_1m]
                 [x_21, x_22, ..., x_2m]
                 ...
                 [x_N1, x_N2, ..., x_Nm]]

            y = [[y_11, y_12, ..., y_1k]
                 [y_21, y_22, ..., y_2k]
                 ...
                 [y_N1, y_N2, ..., y_Nk]]

            w = [[w_11, w_12, ..., w_1k]
                 [w_21, w_22, ..., w_2k]
                 ...
                 [w_m1, w_m2, ..., w_mk]]

    Gradient of cost function is the matrix of shape (n_features, n_targets).
    Let's denote g_ij as the value of gradient w.r.t w_ij.

    g_ij = 2/N * [(x_11*w_1j + x_12*w_2j + ... + x_1m*w_mj - y_1j)*x_1i +
                  (x_21*w_1j + x_22*w_2j + ... + x_2m*w_mj - y_2j)*x_2i +
                  ... +
                  (x_N1*w_1j + x_N2*w_2j + ... + x_Nm*w_mj - y_Nj)*x_N_i]

    Then gradient of the cost function is the following matrix:
    G = [[g_11, g_12, ..., g_1k],
         [g_21, g_22, ..., g_2k],
         ...
         [g_m1, g_m2, ..., g_mk]]

    HINT: You can compute gradient the cost function way easier by using
    vectorized operations with following numpy function: np.dot.

    NOTE: Your implementation will be tested with different values of N, m and k.
    Please, don't make any assumptions in the code about particular values for them.

    NOTE: Returned value should have numpy 'ndarray' type. If your implementation returns G,
    which is list of lists like [[..], [..], .., [..]], then return np.array(G) instead.
    """

    ## STUDENT TASK ##
    N = X.shape[0]
    m = X.shape[1]
    k = y.shape[1]
    G = []
    
    G = 2/N* numpy.dot(numpy.transpose(X),(numpy.dot(X,w)-y))

    return numpy.array(G)


def run_gradient_descent(X, y, epsilon=1e-7, alpha=0.01):
    """
    Run gradient descent
    :param X: array of shape (n_samples, n_features), dataset of features
    :param y: array of shape (n_samples, n_targets), dataset of target values
    :param epsilon: float, accuracy parameter
    :param alpha: float, size of the step for gradient descent
    :return: 2-tuple, (obtained weight vector, array of cost function values for each step)
    """

    # Initial weight vector of shape (n_features, n_targets)
    w = numpy.zeros((X.shape[1], y.shape[1]))

    # Value of the cost function for the current step
    current_cost_value = -numpy.inf

    # Value of the cost function for the previous step
    previous_cost_value = numpy.inf

    # Array to store values of cost function for each step
    cost_values = []

    # Implementation of the gradient descent algorithm
    # If the value of cost function changes a lot, then we need more iterations
    while numpy.abs(current_cost_value - previous_cost_value) >= epsilon:
        # Compute the gradient for the current weight vector w and data X, y.
        grad_value = gradient(X, y, w)

        # Remember the previous value of the cost function
        previous_cost_value = current_cost_value

        # Update value of the cost function for the current step
        current_cost_value = cost(X, y, w)

        # Store current cost function value in the array
        cost_values.append(current_cost_value)

        ## STUDENT TASK ##
        # Task: Update value of the weight vector with the following formula:
        # weight_vector = weight_vector - alpha * gradient_value
        w = w - alpha* grad_value

    return w, cost_values