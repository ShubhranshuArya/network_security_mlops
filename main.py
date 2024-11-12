import logging
import sys
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_transformation import DataTransformation
from network_security.components.data_validation import DataValidation
from network_security.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    TrainingPipelineConfig,
)
from network_security.exception.exception import NetworkSecurityException


if __name__ == "__main__":

    try:
        training_pipeline_config = TrainingPipelineConfig()

        # Implement Data Ingestion
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Data Ingestion started")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed")

        # Implement Data Validation
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(
            data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config=data_validation_config,
        )
        logging.info("Initiate Data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation completed")

        # Implement Data Transformation
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(
            data_transformation_config=data_transformation_config,
            data_validation_artifact=data_validation_artifact,
        )
        logging.info("Initiate Data Transformation")
        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )
        logging.info("Data Transformation completed")
        print(data_transformation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
