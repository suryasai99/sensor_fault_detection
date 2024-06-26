import yaml
from sensor.logger import logging
from sensor.exception import CustomException
import os,sys
import numpy as np
import dill

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


def save_numpy_array_data(file_path:str,
                          array:np.array):
    """
    save numpy array data to file

    Args:
        file_path (str):location of file to save
        array (np.array): np.array data to save
    """

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok = True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise CustomException(e,sys)
    

def load_numpy_array_data(file_path:str) ->np.array:
    """
    load numpy array data from file

    Args:
        file_path (str): location of file to load

    Returns:
        np.array: numpy array loaded
    """

    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    
def save_object(file_path:str, obj:object)->None:
    try:
        logging.info("Entered the save object method of mainutils class")
        os.makedirs(os.path.dirname(file_path),exist_ok = True)
        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)
        logging.info("exited the save_object method of mainutils class")

    except Exception as e:
        raise CustomException(e,sys)
    
def load_object(file_path:str)->None:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exists")

        with open(file_path,'rb') as file_obj:
            return dill.load(file_obj)
            
        
    except Exception as e:
        raise CustomException(e,sys)