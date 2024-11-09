import json
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
import os
import sys

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi

ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from network_security.exception.exception import NetworkSecurityException
from network_security.logging import logger


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)

            data_json = list(json.loads(data.T.to_json()).values())
            # data_json = data.to_json(orient="records")
            return data_json

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collections):
        try:
            self.records = records
            self.database = database
            self.collections = collections

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collections]

            self.collection.insert_many(self.records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "MLSHUBH"
    COLLECTION = "NetworkData"
    networkDataOBJ = NetworkDataExtract()
    records = networkDataOBJ.csv_to_json_convertor(FILE_PATH)
    no_of_records = networkDataOBJ.insert_data_mongodb(records, DATABASE, COLLECTION)
