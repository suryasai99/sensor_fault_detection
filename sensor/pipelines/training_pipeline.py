from sensor.Entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig
from sensor.logger import logging
from sensor.exception import CustomException
from sensor.Entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
import os,sys
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation

class TrainPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)

    def start_data_ingestion(self) -> DataIngestionArtifact :
        try:
            logging.info('Data ingestion started')
            data_ingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f'Data ingestion finished and artifact: {data_ingestion_artifact}')
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)-> DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config = self.training_pipeline_config)
            data_validation = DataValidation(
                data_ingestion_artifact = data_ingestion_artifact,
                data_validation_config = data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()

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
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact = data_ingestion_artifact)
        except Exception as e:
            raise CustomException(e,sys)