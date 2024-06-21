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

        # creating folder for data transformation
        self.data_transformation_dir:str = os.path.join(
            training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME
        )

        # file path for train data
        self.transformed_train_file_path:str = os.path.join(
            self.data_transformation_dir,
            DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            TRAIN_FILE_NAME.replace("csv","npy")
        )
 
        # file path for test data
        self.transformed_test_file_path:str = os.path.join(
            self.data_transformation_dir,
            DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            TEST_FILE_NAME.replace("csv","npy")
        )

        # file path for preprocessing model
        self.transformed_object_file_path = os.path.join(
            self.data_transformation_dir,
            DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            PREPROCESSING_FILE_NAME
        )

class ModelTrainerConfig:
    def __init__(self,
               training_pipeline_config:TrainingPipelineConfig):
        
        # creating folder for model training
        self.model_trainer_dir:str = os.path.join(
            training_pipeline_config.artifact_dir,
            MODEL_TRAINER_DIR_NAME
        )

        # file path to save the trained model
        self.trained_model_file_path:str = os.path.join(
            self.model_trainer_dir,
            MODEL_TRAINER_TRAINED_MODEL_DIR,
            MODEL_TRAINER_TRAINED_MODEL_NAME
        )
        
        # expected accuracy
        self.expected_accuracy:float = MODEL_TRAINER_EXPECTED_SCORE

        self.overfitting_underfitting_threshold = MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD

class ModelEvaluationConfig:

    def __init__(self, 
                 training_pipeline_config:TrainingPipelineConfig):
        
        # directory name
        self.model_evaluation_dir:str = os.path.join(
            training_pipeline_config.artifact_dir,
            MODEL_EVALUATION_DIR_NAME
        )

        # report file path
        self.report_file_path = os.path.join(
            self.model_evaluation_dir,
            MODEL_EVALUATION_REPORT_NAME
        )

        # threshold score to compare with the previous model
        self.change_threshold = MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE


class ModelPusherConfig:

    def __init__(self, 
                 training_pipeline_config:TrainingPipelineConfig):
        
        # directory name
        self.model_evaluation_dir:str = os.path.join(
            training_pipeline_config.artifact_dir,
            MODEL_PUSHER_DIR_NAME
        )

        # file path for the saved model
        self.model_file_path = os.path.join(self.model_evaluation_dir,
                                            MODEL_FILE_NAME)
        

        timestamp = round(datetime.now().timestamp())
        self.saved_model_path = os.path.join(
            SAVED_MODEL_DIR,
            f"{timestamp}",
            MODEL_FILE_NAME
        )
        
    

