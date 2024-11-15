import os
import sys

from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from network_security.logging.logger import logging
from network_security.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from network_security.entity.config_entity import ModelTrainerConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.util.main_utils.utils import (
    evaluate_models,
    load_numpy_array_data,
    save_object,
)
from network_security.util.ml_utils.metric.classification_metric import (
    get_classification_score,
)
from network_security.util.ml_utils.model.estimator import NetworkModel


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact,
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_model(self, X_train, y_train, X_test, y_test) -> ModelTrainerArtifact:
        """
        This function trains a model based on the given training and testing datasets.

        It iterates over a predefined set of machine learning models, each with its own set of parameters.
        For each model, it performs a grid search to find the best parameters, trains the model using the training dataset,
        and evaluates the model's performance on both the training and testing datasets.
        The model with the best performance on the testing dataset is selected as the final trained model.

        :param X_train: The feature dataset for training.
        :param y_train: The target dataset for training.
        :param X_test: The feature dataset for testing.
        :param y_test: The target dataset for testing.
        :return: A ModelTrainerArtifact object containing the trained model file path and the train and test metric artifacts.
        """
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
            params = {
                "Decision Tree": {
                    "criterion": ["gini", "entropy", "log_loss"],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest": {
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                    # 'max_features':['sqrt','log2',None],
                    "n_estimators": [8, 16, 32, 128, 256]
                },
                "Gradient Boosting": {
                    # 'loss':['log_loss', 'exponential'],
                    "learning_rate": [0.1, 0.01, 0.05, 0.001],
                    "subsample": [0.6, 0.7, 0.75, 0.85, 0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
                "Logistic Regression": {},
                "AdaBoost": {
                    "learning_rate": [0.1, 0.01, 0.001],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
            }

            model_report: dict = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                param=params,
            )

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]
            y_train_pred = best_model.predict(X_train)

            classification_train_metric = get_classification_score(
                y_true=y_train,
                y_pred=y_train_pred,
            )

            y_test_pred = best_model.predict(X_test)

            classification_test_metric = get_classification_score(
                y_true=y_test,
                y_pred=y_test_pred,
            )

            preprocessor = (
                self.data_transformation_artifact.transformed_object_file_path
            )

            model_dir_path = os.path.dirname(
                self.model_trainer_config.trained_model_file_path
            )
            os.makedirs(model_dir_path, exist_ok=True)

            network_model = NetworkModel(
                preprocessor=preprocessor,
                model=best_model,
            )
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=network_model,
            )

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric,
            )

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_model_trainer(self):
        try:
            train_file_path = (
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_file_path = (
                self.data_transformation_artifact.transformed_test_file_path
            )

            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            model_trainer_artifact = self.train_model(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
            )
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
