from sensor.Entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from sensor.logger import logging
from sensor.exception import CustomException
import os,sys



class TrainPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig
        self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)

    def start_data_ingestion(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
    
    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)

    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
        
    def run_pipeline(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)