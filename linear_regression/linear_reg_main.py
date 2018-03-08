import numpy as np
import matplotlib.pyplot as plt

from linear_reg_cls import cost, run_gradient_descent


# Read data from files
def load_X(filename):
    X = np.loadtxt(filename)
    # Add column of 1s
    X = np.hstack((np.ones((X.shape[0], 1)), X))
    return X


def load_y(filename):
    y = np.loadtxt(filename)
    return y


# X has the following shape: (n_samples, n_features)
X = load_X("data_x")

val_X = load_X("val_data_x")

# y has the following shape: (n_samples, n_targets)
# In this case n_targets=2, since we need to predict both "x" and "y" coordinates of rumba
y = load_y("data_y")

val_y = load_y("val_data_y")

def run():
    # Run gradient descent
    w, cost_values = run_gradient_descent(X, y)

    # Print out value of the cost function
    print("Cost function value: {}".format(cost_values[-1]))

    # Print out the weight vector
    print("Weight vector: \n {}".format(w))

    # Plot the value of the cost function for each step
    # Cost function value has to decrease
    plt.plot(cost_values)
    plt.xlabel("# of iteration")
    plt.ylabel("cost function value")
    plt.show()

    y_pred = X.dot(w)
    val_y_pred = val_X.dot(w)

    #error of prediction on data_x
    traning_error = np.round(cost(X,y,w),5)
    print("training error: {}".format(traning_error))
    validation_error = np.round(cost(val_X,val_y,w),5)
    print("validation error: {}".format(validation_error))



    # Fitted regression line shown in red
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].scatter(X[:, 1], y[:, 0])
    axarr[0].set_xlabel('Feature extracted from side camera')
    axarr[0].set_ylabel("X-coordinate")
    axarr[0].plot(X[:, 1], y_pred[:, 0], 'red')

    axarr[1].scatter(X[:, 2], y[:, 1])
    axarr[1].set_xlabel('Feature extracted from front camera')
    axarr[1].set_ylabel("Y-coordinate")
    axarr[1].plot(X[:, 2], y_pred[:, 1], 'red')

    plt.show()



if __name__ == "__main__":
    run()
    # w = np.ones((X.shape[1], y.shape[1]))
    # print(np.dot(np.transpose(X),(np.dot(X,w)-y)))

