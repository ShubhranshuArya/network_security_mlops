import os
import sys
from scipy.stats import ks_2samp
import pandas as pd
from network_security.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
)
from network_security.entity.config_entity import DataValidationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from network_security.util.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        """
        Reads a CSV file and returns its content as a pandas DataFrame.

        :param file_path: The path to the CSV file.
        :return: A pandas DataFrame containing the content of the CSV file.
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Validates if the number of columns in the dataframe matches the expected number based on the schema configuration.

        :param dataframe: The pandas DataFrame to be validated.
        :return: True if the number of columns matches the expected number, False otherwise.
        """
        try:
            status = len(dataframe.columns) == len(self.schema_config)
            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(
        self,
        train_df: pd.DataFrame,
        test_df: pd.DataFrame,
        threshold: float = 0.05,
    ) -> bool:
        """
        Detects dataset drift between the training and test dataframes.

        :param train_df: The pandas DataFrame of the training data.
        :param test_df: The pandas DataFrame of the test data.
        :param threshold: The threshold for the Kolmogorov-Smirnov test. Default is 0.05.
        :return: True if no drift is detected, False if drift is detected.
        """
        try:
            status = True
            report = {}
            for column in train_df.columns:
                d1 = train_df[column]
                d2 = test_df[column]
                _, p_value = ks_2samp(d1, d2)

                if p_value < threshold:
                    status = False
                    isFound = True
                else:
                    isFound = False

                report.update(
                    {
                        column: {
                            "p_value": float(p_value),
                            "drift_status": isFound,
                        }
                    }
                )
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # Check & Create Drift Report Directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)

            write_yaml_file(file_path=drift_report_file_path, content=report)

            # return status

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationConfig:

        try:
            training_file_path = self.data_ingestion_artifact.trained_file_path
            testing_file_path = self.data_ingestion_artifact.test_file_path

            # Read the data
            train_dataframe = DataValidation.read_data(training_file_path)
            test_dataframe = DataValidation.read_data(testing_file_path)

            # Validate number of columns
            status = self.validate_number_of_columns(train_dataframe)

            if not status:
                error_message = f"Number of columns in training data: {len(train_dataframe.columns)} does not match with number of columns in schema: {len(self.schema_config.keys())}"

            status = self.validate_number_of_columns(test_dataframe)

            if not status:
                error_message = f"Number of columns in testing data: {len(train_dataframe.columns)} does not match with number of columns in schema: {len(self.schema_config.keys())}"

            # Check for drift
            status = self.detect_dataset_drift(train_dataframe, test_dataframe)
            dir_path = os.path.dirname(
                self.data_validation_config.valid_train_file_path
            )
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True,
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True,
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
