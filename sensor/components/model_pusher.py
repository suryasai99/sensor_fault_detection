
from sensor.exception import CustomException
from sensor.logger import logging
from sensor.Entity.artifact_entity import ModelPusherArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from sensor.Entity.config_entity import ModelEvaluationConfig,ModelPusherConfig
import os,sys
from sensor.ML.metric.classification_metric import get_classification_score
from sensor.utils.main_utils import save_object,load_object,write_yaml_file

import shutil

class ModelPusher:

    def __init__(self,
                 model_pusher_config:ModelPusherConfig,
                 model_eval_artifact:ModelEvaluationArtifact):
        
        try:
            self.model_pusher_config =model_pusher_config
            self.model_eval_artifact = model_eval_artifact

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            logging.info("initiated model pusher")
            trained_model_path = self.model_eval_artifact.trained_model_path

            # creating model pusher directory to save model
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path), exist_ok = True)
            shutil.copy(src = trained_model_path,
                        dst = model_file_path)
            
            # saved model dir
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path), exist_ok = True)
            shutil.copy(src = trained_model_path,
                        dst = saved_model_path)
            
            # prepare artifact 
            model_pusher_artifact = ModelPusherArtifact(
                saved_model_path = saved_model_path, 
                model_file_path = model_file_path
            )
            logging.info("model pusher successfull")
            return model_pusher_artifact
            

        except Exception as e:
            logging.info("error occured in initiated model pusher")
            raise CustomException(e,sys)