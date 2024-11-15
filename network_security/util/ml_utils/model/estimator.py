import sys
from network_security.exception.exception import NetworkSecurityException


class NetworkModel:
    def __init__(self, preprocessor, model):
        self.preprocessor = preprocessor
        self.model = model

    def predict(self, X):
        try:
            X_transformed = self.preprocessor.transform(X)
            return self.model.predict(X_transformed)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
