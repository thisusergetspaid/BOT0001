import pandas as pd

from sklearn.ensemble import (
    RandomForestClassifier
)

class Predictor:

    def __init__(self):

        self.model = (
            RandomForestClassifier()
        )

    def train(
        self,
        x,
        y
    ):
        self.model.fit(x, y)

    def predict(
        self,
        features
    ):
        return self.model.predict_proba(
            features
        )