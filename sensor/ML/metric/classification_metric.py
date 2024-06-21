from sensor.Entity.artifact_entity import ClassificationMetricArtifact
from sensor.logger import logging
from sensor.exception import CustomException
import os,sys
from sklearn.metrics import(accuracy_score, 
                            precision_score, 
                            recall_score, 
                            f1_score, 
                            roc_auc_score,
                            roc_curve,
                            confusion_matrix)

def get_classification_score(y_true,y_pred)-> ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score(y_true,y_pred)
        model_recall_score = recall_score(y_true,y_pred)
        model_precision_score = precision_score(y_true,y_pred)

        classification_metric = ClassificationMetricArtifact(f1_score = model_f1_score,
                                            precision_score = model_precision_score, 
                                            recall_score = model_recall_score)
        
        return classification_metric
    
    except Exception as e:
        logging.info("error occured in get_classification score")
        raise CustomException(e,sys)