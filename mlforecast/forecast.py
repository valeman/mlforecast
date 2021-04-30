# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/forecast.ipynb (unless otherwise specified).

__all__ = ['Forecast']

# Cell
from typing import Callable, Dict

import pandas as pd

from .core import predictions_flow, preprocessing_flow

# Cell
class Forecast:
    """Full pipeline encapsulation.

    Takes a model (scikit-learn compatible regressor) and a flow configuration."""

    def __init__(self, model, flow_config: Dict):
        self.model = model
        self.flow_config = flow_config

    def preprocess(self, data: pd.DataFrame, prep_fn: Callable = preprocessing_flow) -> pd.DataFrame:
        """Apply the transformations defined in the flow configuration."""
        self.ts, series_df = prep_fn(data, **self.flow_config)
        return series_df

    def fit(self, data: pd.DataFrame, prep_fn: Callable = preprocessing_flow, **kwargs) -> 'Forecast':
        """Perform the preprocessing and fit the model."""
        series_df = self.preprocess(data, prep_fn)
        X, y = series_df.drop(columns=['ds', 'y']), series_df.y.values
        del series_df
        self.model.fit(X, y, **kwargs)
        return self

    def predict(self, horizon: int, predict_fn: Callable = predictions_flow) -> pd.DataFrame:
        """Compute the predictions for the next `horizon` steps."""
        return predict_fn(self.ts, self.model, horizon)

    def __repr__(self):
        return f'Forecast(model={self.model}, flow_config={self.flow_config})'