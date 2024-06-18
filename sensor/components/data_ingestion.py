from sensor.logger import logging
from sensor.exception import CustomException
from sensor.Entity.config_entity import DataIngestionConfig
from sensor.Entity.artifact_entity import DataIngestionArtifact
import os,sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sensor.data_access.sensor_data import SensorData

class DataIngestion:

    def __init__(self,data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

    def export_data_into_featurestore(self) -> pd.DataFrame:

        try:
            """
            Export mongodb collection record as dataframe into feature
            """
            logging.info("exporting data from mongoDB to feature store")
            sensor_data = SensorData()
            dataframe = sensor_data.export_collection_as_dataframe(collection_name = self.data_ingestion_config.collection_name)
            feature_store_filepath = self.data_ingestion_config.feature_store_file_path

            # creating folder
            logging.info(" creating folder")
            dir_path = os.path.dirname(feature_store_filepath)
            os.makedirs(dir_path, exist_ok = True)

            # saving the data
            logging.info("saving data to csv file")
            dataframe.to_csv(feature_store_filepath,
                             index = False,
                             header = True)
            logging.info("successfully exported data from mongoDB to feature store")

            return dataframe

        except Exception as e:
            logging.info("error while exporting data from mongoDB to feature store")
            raise CustomException(e,sys)
        

    def split_data_as_train_test(self,dataframe:pd.DataFrame) ->None:
        """
        Feature store data split into train and test
        """
        try:
            train_set,test_set = train_test_split(
                dataframe,
                test_size = self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("performed train test split on the dataframe")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok = True)

            logging.info("Exporting train and test file path")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index = False,
                header = True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index = False,
                header = True
            )

            logging.info("successfully exported train and test file path")

        except Exception as e:
            logging.info("Error in splitting train and test file")
            raise CustomException(e,sys)
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("initiating data ingestion")
            dataframe = self.export_data_into_featurestore() 
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path = self.data_ingestion_config.training_file_path,
                                  test_file_path = self.data_ingestion_config.testing_file_path)
            logging.info("data ingestion completed")
            return data_ingestion_artifact

            

        except Exception as e:
            logging.info("problem in data initiate_data_ingestion step")
            raise CustomException(e,sys)
        