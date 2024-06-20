import os
from datetime import datetime
from sensor.constant.training_pipeline import *

# class for creating folder with timestamp
class TrainingPipelineConfig:
    def __init__(self, timestamp = datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name: str = PIPELINE_NAME
        self.artifact_dir:str = os.path.join(ARTIFACT_DIR, 
                                             timestamp)
        self.timestamp: str = timestamp


class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir:str = os.path.join(
            training_pipeline_config.artifact_dir, 
            DATA_INGESTION_DIR_NAME
        )

        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir, 
            DATA_INGESTION_FEATURE_STORE_DIR, 
            FILE_NAME
        )

        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir, 
            DATA_INGESTION_INGESTED_DIR, 
            TRAIN_FILE_NAME
        )

        self.testing_file_path:str = os.path.join(
            self.data_ingestion_dir, 
            DATA_INGESTION_INGESTED_DIR, 
            TEST_FILE_NAME
        )

        self.train_test_split_ratio:float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

        self.collection_name: str = DATA_INGESTION_COLLECTION_NAME


class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):

        # creating data validation folder
        self.data_validation_dir:str = os.path.join(training_pipeline_config.artifact_dir, 
                                                    DATA_VALIDATION_DIR_NAME)

        # folder for valid data
        self.valid_data_dir:str = os.path.join(self.data_validation_dir, 
                                               DATA_VALIDATION_VALID_DIR)
        
        # folder for invalid data
        self.invalid_data_dir:str = os.path.join(self.data_validation_dir,
                                                 DATA_VALIDATION_INVALID_DIR)
        
        # file path for valid train
        self.valid_train_file_path:str = os.path.join(self.valid_data_dir,
                                                      TRAIN_FILE_NAME)
        
        # file path for valid test
        self.valid_test_file_path:str = os.path.join(self.valid_data_dir,
                                                TEST_FILE_NAME)
        
        # file path for invalid train
        self.invalid_train_file_path:str = os.path.join(self.invalid_data_dir,
                                                   TRAIN_FILE_NAME)

        # file path for valid test
        self.invalid_test_file_path:str = os.path.join(self.invalid_data_dir,
                                                  TEST_FILE_NAME)
        
        # file path for drift report
        self.drift_report_file_path:str = os.path.join(
            self.data_validation_dir,
            DATA_VALIDATION_DRIFT_REPORT_DIR,
            DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )


class DataTransformationConfig:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        self.data_transformation_dir:str = os.path.join(
            training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME
        )

        self.transformed_train_file_path:str = os.path.join(
            self.data_transformation_dir,
            DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            TRAIN_FILE_NAME.replace("csv","npy")
        )

        self.transformed_test_file_path:str = os.path.join(
            self.data_transformation_dir,
            DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            TEST_FILE_NAME.replace("csv","npy")
        )

        self.transformed_object_file_path = os.path.join(
            self.data_transformation_dir,
            DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            PREPROCESSING_FILE_NAME
        )

