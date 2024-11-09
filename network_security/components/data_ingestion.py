from network_security.entity.artifact_entity import DataIngestionArtifact
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

# Configuration of the data ingestion
from network_security.entity.config_entity import DataIngestionConfig

import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(
        self,
        data_ingestion_config: DataIngestionConfig,
    ):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """
        This function reads the data from the MongoDB collection and returns it as a pandas DataFrame.

        Returns:
            pd.DataFrame: The pandas DataFrame containing the data from the MongoDB collection
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.tolist():
                df = df.drop(columns=["_id"], axis=1)

            df.replace("na", np.nan, inplace=True)

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        This function exports the given DataFrame into a CSV file in the feature store directory.

        Args:
            dataframe (pd.DataFrame): The DataFrame to be exported.

        Returns:
            pd.DataFrame: The same DataFrame that was exported.
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_name = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_name, exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """
        Splits the given DataFrame into training and testing sets based on the specified split ratio.

        Args:
            dataframe (pd.DataFrame): The DataFrame to be split.

        Returns:
            None: This function does not return anything. It directly exports the split dataframes to CSV files.
        """
        try:
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
            )
            logging.info("Performed Train Test split on the DataFrame")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True,
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True,
            )

            logging.info("Exported train and test file successfully")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        try:
            df = self.export_collection_as_dataframe()
            df = self.export_data_into_feature_store(df)
            self.split_data_as_train_test(df)
            dataIngestionArtifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )

            return dataIngestionArtifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
