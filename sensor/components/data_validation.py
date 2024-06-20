from sensor.logger import logging
from sensor.exception import CustomException
from sensor.Entity.config_entity import DataValidationConfig
from sensor.Entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
import os,sys
import pandas as pd
from sensor.utils.main_utils import read_yaml_file,write_yaml_file
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp

class DataValidation:

    def __init__(self,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys)

    def validate_number_of_columns(self,
                                   dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            logging.info('error occured during validating number of columns')
            raise CustomException(e,sys)

    def is_numerical_column_exist(self,
                                  dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self._schema_config['numerical_columns']
            dataframe.columns = dataframe.columns

            numerical_columns_present = True
            missing_numerical_columns = []

            for cols in numerical_columns:
                if cols not in dataframe.columns:
                    numerical_columns_present = False
                    missing_numerical_columns.append(cols)
            
            return numerical_columns_present
        
        except Exception as e:
            logging.info('error occured during validating numerical columns exists or not')
            raise CustomException(e,sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logging.info("error occured while reading data")
            raise CustomException(e,sys)

    def detect_dataset_drift(self,base_df, current_df, threshold = 0.05):
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column:
                    {"pvalue":float(is_same_dist.pvalue),
                     "drift_status":is_found}
                })
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # creating directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok = True)
            write_yaml_file(file_path = drift_report_file_path,
                            content = report)
            return status

        except Exception as e:
            logging.info("error occured while detecting drift")
            raise CustomException(e,sys)


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            error_message = ""
            # taking the train and test file paths     
            train_file_path = self.data_ingestion_artifact.trained_file_path 
            test_file_path = self.data_ingestion_artifact.test_file_path

            # reading the data
            # static method can be used by calling with class
            logging.info('reading csv file for training set')
            train_dataframe = DataValidation.read_data(train_file_path)
            logging.info('reading csv file for test set')
            test_dataframe = DataValidation.read_data(test_file_path)

            # validating number of columns for train and test data
            # validating for train data
            logging.info('validating number of columns for training data')
            status = self.validate_number_of_columns(dataframe = train_dataframe)
            if not status:
                error_message = f"{error_message} train dataframe does not contain all the columns"
            logging.info(f'validating number of columns for training data is completed')

            # validating for test data
            logging.info('validating number of columns for test data')
            status = self.validate_number_of_columns(dataframe = test_dataframe)
            if not status:
                error_message = f"{error_message} test dataframe does not contain all the columns"
            logging.info(f'status of validating number of columns for test data is:{status}')

            # validating numerical columns for training and test set
            logging.info('validating numerical columns for training set')
            status = self.is_numerical_column_exist(dataframe = train_dataframe)
            if not status:
                error_message = f"{error_message} Train dataframe does not contain all numerical columns"
            logging.info(f'validated numerical columns for training data and status is completed')

            logging.info('validating numerical columns for test set')
            status = self.is_numerical_column_exist(dataframe = test_dataframe)
            if not status:
                error_message = f"{error_message} Test dataframe does not contain all numerical columns"
            logging.info(f'validated numerical columns for test data and status is completed')

            if len(error_message)>0:
                raise Exception(error_message)
            
            # check data drift
            logging.info('checking the data drift for train and test data')
            status = self.detect_dataset_drift(base_df = train_dataframe,
                                               current_df = test_dataframe)
            logging.info(f'status of the data drift for train and test data is completed')

            data_validation_artifact = DataValidationArtifact(
                validation_status = status,
                valid_train_file_path = self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path = self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path = self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path = self.data_validation_config.invalid_test_file_path,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            logging.info("error occured in initiate_data_validation")
            raise CustomException(e,sys)