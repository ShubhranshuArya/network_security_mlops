import sys

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from network_security.logging.logger import logging
from network_security.constants.training_pipeline import (
    DATA_TRANSFORMATION_IMPUTER_PARAMS,
    TARGET_COLUMN,
)
from network_security.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)
from network_security.entity.config_entity import DataTransformationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.util.main_utils.utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(
        self,
        data_transformation_config: DataTransformationConfig,
        data_validation_artifact: DataValidationArtifact,
    ):
        try:
            self.data_transformation_config: DataTransformationConfig = (
                data_transformation_config
            )
            self.data_validation_artifact: DataValidationArtifact = (
                data_validation_artifact
            )
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

    def get_data_transformer_object(self) -> pd.DataFrame:
        """
        Generates a data transformer object using KNNImputer for handling missing values.

        Returns:
            Pipeline: A pipeline object containing the KNNImputer for data transformation.
        """
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor: Pipeline = Pipeline(steps=[("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info(
            "Entered initiate_data_transformation method of DataTransformation class"
        )
        try:
            logging.info("Initiated data transformation")

            train_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_train_file_path
            )
            test_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_test_file_path
            )

            # training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)

            target_feature_train_df = train_df[TARGET_COLUMN].replace(-1, 0)

            # testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)

            target_feature_test_df = test_df[TARGET_COLUMN].replace(-1, 0)

            # data transformer object
            preprocessor = self.get_data_transformer_object()

            preprocessor_object = preprocessor.fit(input_feature_train_df)

            transformed_input_train_features = preprocessor_object.transform(
                input_feature_train_df
            )

            transformed_input_test_features = preprocessor_object.transform(
                input_feature_test_df
            )

            train_arr = np.c_[
                transformed_input_train_features,
                np.array(target_feature_train_df),
            ]

            test_arr = np.c_[
                transformed_input_test_features,
                np.array(target_feature_test_df),
            ]

            # Save the transformed train and test arrays
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                train_arr,
            )

            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                test_arr,
            )

            # Save the preprocessor object
            save_object(
                file_path="final_models/model.pkl",
                obj=preprocessor_object,
            )

            save_object(
                file_path="final_models/preprocessor.pkl",
                obj=preprocessor_object,
            )

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
            )
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
