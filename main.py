from sensor.configuration.mongo_DB_connection import MongoDBClient
from sensor.Entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
if __name__=='__main__':
    #mongodb_client = MongoDBClient()
    #print(mongodb_client.database.list_collection_names())

    training_pipeline_config = TrainingPipelineConfig()
    #data_ingestion_config = DataIngestionConfig(training_pipeline_config)
    #print(data_ingestion_config.__dict__)
    