from sensor.logger import logging
from sensor.exception import CustomException
from sensor.Entity.config_entity import DataIngestionConfig
from sensor.Entity.artifact_entity import DataIngestionArtifact
import os,sys
import pandas as pd


class DataTransformation:

    def __init__(self):
        pass


    def data_transformation_initiated(self):
        try:
            logging.info("")
            # To read the dataframe
            


        except Exception as e:
            raise CustomException(e,sys)