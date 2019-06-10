""" Utilities """

import pickle


def store_model(model, filename="model.pickle"):
    """ Store a classifier as a pickle """

    with open(filename, "wb") as file:
        pickle.dump(model, file, protocol=pickle.HIGHEST_PROTOCOL)


def read_model(filename="model.pickle"):
    """ Store a classifier as a pickle """
    with open(filename, "rb") as file:
        return pickle.load(file)
