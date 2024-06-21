import os,sys
import pandas as pd
import numpy as np

from sensor.logger import logging
from sensor.exception import CustomException
from sensor.Entity.config_entity import ModelTrainerConfig
from sensor.Entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from sensor.ML.model.estimator import SensorModel
from sensor.utils.main_utils import load_numpy_array_data,save_object,load_object
from sensor.ML.metric.classification_metric import get_classification_score
from xgboost import XGBClassifier



class ModelTrainer:
    def __init__(self, 
                 model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise CustomException(e,sys)
        
    def train_model(self, x_train, y_train):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x_train,y_train)
            return xgb_clf
        except Exception as e:
            logging.info('error occured in xg boost model while training')
            raise CustomException(e,sys)
    
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            # file paths of train and test
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            logging.info("loading the numpy array train and test file")
            train_arr = load_numpy_array_data(train_file_path) # loading the numpy array train file
            test_arr = load_numpy_array_data(test_file_path) # loading the numpy array test file

            logging.info("splitting train and test file into dependent and independent features")
            x_train,x_test,y_train,y_test = (
                train_arr[:,:-1],
                test_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,-1]
            )

            # fitting model to x_train and y_train
            model = self.train_model(x_train,y_train)

            # predicting for x_train as well
            y_train_pred = model.predict(x_train)

            # metrics for predicting x_train
            classification_train_metric = get_classification_score(
                y_true = y_train,
                y_pred = y_train_pred
            )

            if classification_train_metric.f1_score<=self.model_trainer_config.expected_accuracy:
                raise Exception("model is not good further experiment required")

            # predicting values for x_test
            y_test_pred = model.predict(x_test)

            # metrics for predicting x_test
            classification_test_metric = get_classification_score(
                y_true = y_test,
                y_pred = y_test_pred
            )

            # Test to find whether our model is overfitting or underfitting
            diff = abs(classification_train_metric.f1_score - classification_test_metric.f1_score)

            if diff > self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception("Model is either overfitting or underfitting..more experimentation required")
                        
            preprocessor = load_object(
                file_path = self.data_transformation_artifact.transformed_object_file_path
            )

            sensor_model = SensorModel(preprocessor = preprocessor,
                                       model = model)
            
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok = True)


            # saving the entire model(preprocessor+model)
            save_object(
                self.model_trainer_config.trained_model_file_path,
                obj = sensor_model
            )

            # model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path = self.model_trainer_config.trained_model_file_path,
                train_metric_artifact = classification_train_metric,
                test_metric_artifact = classification_test_metric
            )

            logging.info(f"Model trainer artifact {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e,sys)