from network_security.constants import training_pipeline
import os
from datetime import datetime


class TrainingPipelineConfig:
    """
    This class represents the configuration for the training pipeline.
    It includes properties such as pipeline name, artifact directory, and timestamp.
    The timestamp is used to create a unique directory for each pipeline run.
    """

    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name: str = training_pipeline.PIPELINE_NAME
        self.artifact_name: str = training_pipeline.ARTIFACT_DIR
        self.artifact_dir: str = os.path.join(self.artifact_name, timestamp)
        self.model_dir: str = os.path.join("final_models")
        self.timestamp: str = timestamp


class DataIngestionConfig:
    """
    This class represents the configuration for data ingestion in the training pipeline.
    It includes properties such as data ingestion directory, feature store file path, training file path,
    testing file path, train-test split ratio, collection name, and database name.
    These properties are used to manage the data ingestion process in the pipeline.
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME,
        )
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME,
        )
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME,
        )
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME,
        )
        self.train_test_split_ratio: float = (
            training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        )
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME


class DataValidationConfig:
    """
    This class represents the configuration for data validation in the training pipeline.
    It includes properties such as data validation directory, valid data directory, invalid data directory,
    valid and invalid train and test file paths, and drift report file path.
    These properties are used to manage the data validation process in the pipeline.
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME,
        )
        self.valid_data_dir: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_VALID_DIR,
        )
        self.invalid_data_dir: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_INVALID_DIR,
        )
        self.valid_train_file_path: str = os.path.join(
            self.valid_data_dir,
            training_pipeline.TRAIN_FILE_NAME,
        )
        self.valid_test_file_path: str = os.path.join(
            self.valid_data_dir,
            training_pipeline.TEST_FILE_NAME,
        )
        self.invalid_train_file_path: str = os.path.join(
            self.invalid_data_dir,
            training_pipeline.TRAIN_FILE_NAME,
        )
        self.invalid_test_file_path: str = os.path.join(
            self.invalid_data_dir,
            training_pipeline.TEST_FILE_NAME,
        )

        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )


class DataTransformationConfig:
    """
    This class represents the configuration for data transformation in the training pipeline.
    It includes properties such as data transformation directory, transformed train and test file paths,
    and transformed object file path.
    These properties are used to manage the data transformation process in the pipeline.
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_TRANSFORMATION_DIR_NAME,
        )
        self.transformed_train_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),
        )
        self.transformed_test_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy"),
        )
        self.transformed_object_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME,
        )


class ModelTrainerConfig:
    """
    This class represents the configuration for the model trainer in the training pipeline.
    It includes properties such as model trainer directory, trained model file path,
    expected accuracy, and overfitting/underfitting threshold.
    These properties are used to manage the model training process in the pipeline.
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.MODEL_TRAINER_DIR_NAME,
        )

        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir,
            training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME,
            training_pipeline.MODEL_FILE_NAME,
        )

        self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE

        self.overfitting_underfitting_threshold: float = (
            training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD
        )
