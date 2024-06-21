import os
from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME

# defining common constant variables for training pipeline
TARGET_COLUMN = "class"
PIPELINE_NAME: str = "sensor"
ARTIFACT_DIR: str = "artifact"
FILE_NAME: str = "sensor.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"


PREPROCESSING_FILE_NAME = "preprocessing.pkl"
SCHEMA_FILE_PATH = os.path.join("config/schema.yaml")
SCHEMA_DROP_COLS = "drop_columns"

"""
    Data Ingestion constant with DATA_INGESTION variable name
"""
 

DATA_INGESTION_COLLECTION_NAME:str = "sensors"
DATA_INGESTION_DIR_NAME: str  = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2


"""
    Data validation constant with DATA_VALIDATION variable name

"""
DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_VALID_DIR = "validated"
DATA_VALIDATION_INVALID_DIR = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "report.yaml"


"""
    Data transformation constant with DATA_TRANSFORMATION variable name

"""
DATA_TRANSFORMATION_DIR_NAME = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "transformed_object"



"""
MOdel trainer related constant start with MODE TRAINER VAR NAME

"""

MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD:float = 0.05



"""
MOdel evaluation related constant start with MODE EVALUATION

"""
MODEL_EVALUATION_DIR_NAME:str = "model_evaluation"
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE:float = 0.02
MODEL_EVALUATION_REPORT_NAME:str = "report.yaml"