import numpy as np

import plotly.graph_objs as go
import plotly.offline as py

from tqdm import tqdm_notebook as tqdm


class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):

        # Dimensions of the neural network
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Initialize weights with a normal distribution
        self.weights_input_to_hidden = np.random.normal(
            0.0, self.hidden_nodes ** -0.5, (self.hidden_nodes, self.input_nodes)
        )

        self.weights_hidden_to_output = np.random.normal(
            0.0, self.output_nodes ** -0.5, (self.output_nodes, self.hidden_nodes)
        )
        self.lr = learning_rate

    @staticmethod
    def activation_function(x):
        """ This is the sigmoid function """
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def activation_function_inverse(x):
        """ Inverse of the sigmoid function """
        return (1 - x) * x

    @staticmethod
    def MSE(prediction, y):
        """ Mean squared errors """
        return np.mean((prediction - y) ** 2)

    def forward_pass(self, inputs_list):
        """ Does one forward pass """

        # Convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T

        # Get values of the hiden layer
        hidden_layer = self.activation_function(np.dot(self.weights_input_to_hidden, inputs))

        # Get values of the last layer (no activation function)
        return np.dot(self.weights_hidden_to_output, hidden_layer)

    def train_one_time(self, inputs_list, targets_list):
        """ Does one run of the training process """

        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        # ----------------------------------------------------------------------------
        # 1. Forward pass
        hidden_layer = self.activation_function(np.dot(self.weights_input_to_hidden, inputs))

        # Get values of the last layer (no activation function)
        final_layer = np.dot(self.weights_hidden_to_output, hidden_layer)

        # ----------------------------------------------------------------------------
        # 2. Backward pass
        output_errors = (
            targets - final_layer
        )  # Output layer error is the difference between desired target and actual output.

        hidden_errors = np.dot(self.weights_hidden_to_output.T, output_errors)
        hidden_grad = self.activation_function_inverse(hidden_layer)  # hidden layer gradients

        # ----------------------------------------------------------------------------
        # 3. Update weights
        self.weights_hidden_to_output += self.lr * np.dot(output_errors, hidden_layer.T)
        self.weights_input_to_hidden += self.lr * np.dot(hidden_errors * hidden_grad, inputs.T)

    def predict(self, inputs_list):
        """ Does a prediction """
        # Convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T

        # Get values of the hiden layer
        hidden_layer = self.activation_function(np.dot(self.weights_input_to_hidden, inputs))

        # Get values of the last layer (no activation function)
        return np.dot(self.weights_hidden_to_output, hidden_layer)

    def train_network(self, epochs, data):
        """ Train N epochs """

        self.losses = {"train": [], "validation": []}

        for e in tqdm(range(epochs), desc="epochs"):

            # Go through a random batch of 128 records from the training data set
            batch = np.random.choice(data["x_train"].index, size=128)

            for record, target in zip(
                data["x_train"].ix[batch].values, data["y_train"].ix[batch]["cnt"]
            ):
                self.train_one_time(record, target)

            # Store losses to see the results
            self.losses["train"].append(
                self.MSE(self.predict(data["x_train"]), data["y_train"]["cnt"].values)
            )
            self.losses["validation"].append(
                self.MSE(self.predict(data["x_val"]), data["y_val"]["cnt"].values)
            )

        self.print_losses()

    def print_losses(self):
        """ show evolution of training and validation losses """
        py.iplot([go.Scatter(y=loss, name=name) for name, loss in self.losses.items()])
