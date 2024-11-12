import os
import pickle
import sys
import numpy as np
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
