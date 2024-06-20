import os,sys
import pandas as pd
import numpy as np

from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler,LabelEncoder
from sklearn.pipeline import Pipeline


from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.logger import logging
from sensor.exception import CustomException
from sensor.Entity.config_entity import DataTransformationConfig
from sensor.Entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
#from sensor.ml.model.estimator import TargetValueMapping
from sensor.utils.main_utils import save_numpy_array_data,save_object

class DataTransformation:

    def __init__(self,
                 data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        """
        Args:
            data_validation_artifact (DataValidationArtifact): output of data validation artifact stage
            data_transformation_config (DataTransformationConfig): configuration for data transformation
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            logging.info("error occured in initializing of DataTransformation class ")
            raise CustomException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logging.info("error occured while reading the data")
            raise CustomException(e,sys)
        
    @classmethod    
    def get_data_transformer_object(cls)->Pipeline:
        try:
            robust_scaler = RobustScaler()
            simple_imputer = SimpleImputer(strategy = 'mean')

            logging.info("creating pipeline")

            preprocessor = Pipeline(
                steps = [
                    ('robust_scaler',robust_scaler),  # robust scaling of the data
                    ("simple_imputer",simple_imputer) # replacing missing value with mean
                ]
            )
            logging.info("created pipeline successfully")
            return preprocessor
         
        except Exception as e:
            logging.info("error occured in get_data_transformer_object pipeline")
            raise CustomException(e,sys)

    def initiate_data_transformation(self):
        try:
            logging.info(" reading of train data")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)

            logging.info(" reading of train data")
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # data transformation pipeline
            preprocessor = self.get_data_transformer_object()

            # dividing dependent and independent features from train and test
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis = 1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis = 1)
            target_feature_test_df = test_df[TARGET_COLUMN]

            # label encoding dependent features
            label_encoder = LabelEncoder()

            logging.info("label encoding train dependent features")
            target_feature_train_df = label_encoder.fit_transform(target_feature_train_df)
            logging.info("label encoding test dependent features")
            target_feature_test_df = label_encoder.fit_transform(target_feature_test_df)

            # transforming input features
            logging.info("transforming train independent features")
            transformed_input_train_feature = preprocessor.fit_transform(input_feature_train_df)
            logging.info("transforming test independent features")
            transformed_input_test_feature = preprocessor.fit_transform(input_feature_test_df)

            # sampling the imbalanced data with smote+tomek
            smt = SMOTETomek(sampling_strategy = 'minority')

            logging.info("sampling the train data")
            input_feature_train_final,target_feature_train_final = smt.fit_resample(
                transformed_input_train_feature,target_feature_train_df
            )
            logging.info("sampling the test data")
            input_feature_test_final,target_feature_test_final = smt.fit_resample(
                transformed_input_test_feature, target_feature_test_df
            )

            # concatenating independent and dependent features of train
            logging.info("concatenating independent and dependent features of train")
            train_arr = np.c_(input_feature_train_final,
                              target_feature_train_final)

            # concatenating independent and dependent features of test
            logging.info("concatenating independent and dependent features of test")
            test_arr = np.c_(input_feature_test_final, 
                             target_feature_test_final)
            
            # save numpy array data
            logging.info("saving the training array")
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,
                                  array = train_arr )
            
            logging.info("saving the test array")
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,
                                  array = test_arr)
            
            # saving the preprocessor object
            logging.info("saving the preprocessor object")
            save_object(self.data_transformation_config.transformed_object_file_path, 
                        preprocessor)
            
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )

            logging.info(f"Data transformation artifact:{data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e,sys)