import yaml
from sensor.logger import logging
from sensor.exception import CustomException
import os,sys

def read_yaml_file(file_path:str)->dict:
    try:
        logging.info("reading yaml file")
        with open(file_path,'rb') as yaml_file:
            logging.info("successfully opened yaml file")
            return yaml.safe_load(yaml_file)
    except Exception as e:
        logging.info("error occured while reading yaml file")
        raise CustomException(e,sys)
    
def write_yaml_file(file_path:str,
                    content:object,
                    replace:bool = False)->None:
    try:
        logging.info("writing yaml file")
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok = True)
        with open(file_path, "w") as file:
            yaml.dump(content,file)

    except Exception as e:
        logging.info("error occured while writing yaml file")
        raise CustomException(e,sys)