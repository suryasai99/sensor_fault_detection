import os,sys
import pandas as pd
import numpy as np

from sensor.logger import logging
from sensor.exception import CustomException
from sensor.Entity.config_entity import ModelEvaluationConfig
from sensor.Entity.artifact_entity import(DataValidationArtifact,
                                          ModelTrainerArtifact,
                                          ModelEvaluationArtifact)

from sensor.ML.model.estimator import SensorModel,ModelResolver
from sensor.utils.main_utils import(save_object,
                                    load_object,
                                    write_yaml_file)
from sensor.ML.metric.classification_metric import get_classification_score
from sensor.constant.training_pipeline import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder


class ModelEvaluation:

    def __init__(self,
                 model_eval_config:ModelEvaluationConfig,
                 data_validation_artifact: DataValidationArtifact,
                 model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            logging.info("initiating model evaluation")
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path
            valid_test_file_path = self.data_validation_artifact.valid_test_file_path

            # valid train and test dataframe
            logging.info("taking the train and test from validated file path")
            train_df = pd.read_csv(valid_train_file_path)
            test_df = pd.read_csv(valid_test_file_path)

            # concatenating train and test
            logging.info("concatenating train and test")
            df = pd.concat([train_df,test_df])

            # sepearting input and target column
            y_true = df[TARGET_COLUMN]
            df.drop(TARGET_COLUMN,axis=1,inplace=True)

            # applying label encoder to change categorical to numerical
            label_encoder = LabelEncoder()
            logging.info("label encoding on output")
            y_true = label_encoder.fit_transform(y_true)


            train_model_file_path = self.model_trainer_artifact.trained_model_file_path
            model_resolver = ModelResolver()

            is_model_accepted = True
            if not model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted = is_model_accepted,
                    improved_accuracy = None,
                    best_model_path = None,
                    trained_model_path = train_model_file_path,
                    train_model_metric_artifact = self.model_trainer_artifact.test_metric_artifact,
                    best_model_metric_artifact = None)
                
                logging.info(f"model evaluation artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact
            
            latest_model_path = model_resolver.get_best_model_path()
            latest_model = load_object(latest_model_path)
            train_model = load_object(train_model_file_path)

            y_trained_pred = train_model.predict(df)
            y_latest_pred = latest_model.predict(df)

            trained_metric = get_classification_score(y_true = y_true,
                                                      y_pred = y_trained_pred)
            latest_metric = get_classification_score(y_true = y_true,
                                                     y_pred = y_latest_pred)
            
            # comparing whether the difference between trained_metric & latest_metric exceeds the threshold or not

            improved_accuracy = trained_metric-latest_metric
            if self.model_eval_config.change_threshold<improved_accuracy:
                is_model_accepted = True
            else:
                is_model_accepted = False


            model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted = is_model_accepted,
                    improved_accuracy = improved_accuracy,
                    best_model_path = latest_model_path,
                    trained_model_path = train_model_file_path,
                    train_model_metric_artifact = trained_metric,
                    best_model_metric_artifact = latest_metric)
            
            model_eval_report = model_evaluation_artifact.__dict__()

            # saving the report
            write_yaml_file(self.model_eval_config.report_file_path,model_eval_report)    
            logging.info(f"model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact

        except Exception as e:
            logging.info("error occured in initiate_model_evaluation")
            raise CustomException(e,sys)
  