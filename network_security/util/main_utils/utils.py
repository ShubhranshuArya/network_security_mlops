import os
import pickle
import sys
import numpy as np
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import yaml

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging


def read_yaml_file(file_path) -> dict:
    """
    This function reads a YAML file and returns its content as a dictionary.

    :param file_path: The path to the YAML file.
    :return: A dictionary containing the content of the YAML file.
    """

    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise NetworkSecurityException(e, sys)


def write_yaml_file(
    file_path: str,
    content: object,
    replace: bool = False,
) -> None:
    """
    This function writes a dictionary into a YAML file.

    :param file_path: The path to the YAML file.
    :param data: A dictionary to be written into the YAML file.
    :return: None
    """

    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            return yaml.dump(content, file)

    except Exception as e:
        raise NetworkSecurityException(e, sys)


def save_numpy_array_data(file_path: str, array: np.ndarray):
    """
    This function saves a numpy array into a file.

    :param file_path: The path to the file where the numpy array will be saved.
    :param array: The numpy array to be saved.
    :return: None
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def load_numpy_array_data(file_path: str) -> np.ndarray:
    """
    This function loads a numpy array from a file.

    :param file_path: The path to the file where the numpy array is saved.
    :return: The loaded numpy array.
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def save_object(file_path: str, obj: object):
    """
    This function saves an object into a file.

    :param file_path: The path to the file where the object will be saved.
    :param obj: The object to be saved.
    :return: None
    """
    try:
        logging.info(f"Entered the save_object method of MainUtils class")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info(f"Exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def load_object(file_path: str) -> object:
    """
    This function loads an object from a file.

    :param file_path: The path to the file where the object is saved.
    :return: The loaded object.
    """
    try:
        if not os.path.exists(file_path):
            return Exception(f"The file: {file_path} does not exist")
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, param) -> dict:
    """
    Evaluates multiple machine learning models on given training and testing datasets.

    This function iterates over a dictionary of models and their corresponding parameters.
    For each model, it performs a grid search for the best parameters, trains the model,
    and predicts on both the training and testing datasets.
    The R-squared score is calculated for both predictions and stored in a report dictionary.
    """
    try:
        report: dict = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            gs_best = GridSearchCV(model, para, cv=5)
            gs_best.fit(X_train, y_train)

            model.set_params(**gs_best.best_params_)
            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report
    except Exception as e:
        raise NetworkSecurityException(e, sys)
