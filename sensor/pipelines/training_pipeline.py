from sensor.Entity.config_entity import(TrainingPipelineConfig,
                                        DataIngestionConfig,
                                        DataValidationConfig,
                                        DataTransformationConfig,
                                        ModelTrainerConfig,
                                        ModelEvaluationConfig,
                                        ModelPusherConfig)
                                        
from sensor.logger import logging
from sensor.exception import CustomException
from sensor.Entity.artifact_entity import(DataIngestionArtifact,
                                          DataValidationArtifact,
                                          DataTransformationArtifact,
                                          ModelTrainerArtifact,
                                          ModelEvaluationArtifact,
                                          ModelPusherArtifact)
import os,sys
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher


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
            logging.info('Data validation started')
            data_validation_config = DataValidationConfig(training_pipeline_config = self.training_pipeline_config)
            data_validation = DataValidation(
                data_ingestion_artifact = data_ingestion_artifact,
                data_validation_config = data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info('Data validation finished')

            return data_validation_artifact

        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            logging.info("Data transformation initiated")
            data_transformation_config = DataTransformationConfig(
                training_pipeline_config = self.training_pipeline_config,    
            )
            data_transformation = DataTransformation(
                data_validation_artifact = data_validation_artifact,
                data_transformation_config = data_transformation_config
            )
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data transformation successfull")

            return data_transformation_artifact
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_model_trainer(self,
                            data_transformation_artifact:DataTransformationArtifact):
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config = self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config,
                                         data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()

            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_model_evaluation(self,
                               data_validation_artifact:DataValidationArtifact,
                               model_trainer_artifact:ModelTrainerArtifact):
        try:
            model_eval_config = ModelEvaluationConfig(
                training_pipeline_config = self.training_pipeline_config
            )
            model_evaluation = ModelEvaluation(
                model_eval_config = model_eval_config,
                data_validation_artifact = data_validation_artifact,
                model_trainer_artifact = model_trainer_artifact
            )
            model_eval_artifact = model_evaluation.initiate_model_evaluation()

            return model_eval_artifact
        
        except Exception as e:
            raise CustomException(e,sys)

    def start_model_pusher(self,
                           model_eval_artifact:ModelEvaluationArtifact):
        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config = self.training_pipeline_config)
            model_pusher = ModelPusher(
                model_pusher_config = model_pusher_config,
                model_eval_artifact = model_eval_artifact
            )
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact = data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact = data_validation_artifact
            )
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            model_eval_artifact = self.start_model_evaluation(data_validation_artifact,
                                                              model_trainer_artifact)
            if not model_eval_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model")
            model_pusher_artifact = self.start_model_pusher(model_eval_artifact)

        except Exception as e:
            raise CustomException(e,sys)