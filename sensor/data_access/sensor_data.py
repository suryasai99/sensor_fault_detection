from sensor.logger import logging
from sensor.exception import CustomException
import numpy as np
import pandas as pd
import sys

from sensor.configuration.mongo_DB_connection import MongoDBClient
from sensor.constant.database import *


class SensorData:
    """
    This class helps us to export entire mongodb record as pandas dataframe
    """

    def __init__(self):
        """
        establishing mongo db connection
        """
        try:
            logging.info("establishing mongo db connection")
            self.mongo_client = MongoDBClient(database_name = DATABASE_NAME)
            logging.info("mongo db connection successfull")

        except Exception as e:
            logging.info("problem occured during mongo db connection")
            raise CustomException(e,sys)
        
    def export_collection_as_dataframe(self,
                                       collection_name:str,
                                       database_name = None) ->pd.DataFrame:
        
        try:
            """
            export entire collection as dataframe:
            return pd.DataFrame of collection
            """
            logging.info("extracting data from database and collection ")
            if database_name is None:
                database_name = self.mongo_client.database_name
            collection = self.mongo_client.client[database_name][collection_name]

            logging.info("putting the collection in dataframe ")
            data = list(collection.find())
            df = pd.DataFrame(data)
            print(df.head())

            logging.info("Successfull insertion of data into dataframe ")

            if "_id" in list(df.columns):
                df = df.drop("_id", axis = 1)

            df.replace({"na": np.nan}, inplace = True)
            logging.info("The data export is successfull ")

            return df

        except Exception as e:
            logging.info("problem occured during export of collections ")
            raise CustomException(e,sys)