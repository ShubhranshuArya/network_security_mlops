import os
import sys
import yaml

from network_security.exception.exception import NetworkSecurityException


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
