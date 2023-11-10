import logging

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config.data import ID_COLUMN
from src.config.retriever import (
    CATEGORICAL_FEATURES,
    CATEGORICAL_IMPUTER_STRATEGY,
    DISTANCE_METRIC,
    N_CANDIDATES,
    NUMERIC_FEATURES,
    NUMERIC_IMPUTER_STRATEGY,
)

logger = logging.getLogger("train_and_retrieve_candidates")


class RetrieverKNN:
    """
    Class includes train and predict, this can be split into two processes. In case of new products not necessary
    ro run training.
    training, dumping model and predict
    loading model and predict
    """

    def __init__(self, train_data: pd.DataFrame) -> None:
        self.train_data = train_data
        self.encoder = self._data_encoder()
        self.model = NearestNeighbors(n_neighbors=N_CANDIDATES, metric=DISTANCE_METRIC)

    def _data_encoder(self) -> ColumnTransformer:
        numeric_transformer = Pipeline(
            steps=[("imputer", SimpleImputer(strategy=NUMERIC_IMPUTER_STRATEGY)), ("scaler", StandardScaler())]
        )

        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy=CATEGORICAL_IMPUTER_STRATEGY)),
                ("encoder", OneHotEncoder(handle_unknown="ignore")),
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, NUMERIC_FEATURES),
                ("cat", categorical_transformer, CATEGORICAL_FEATURES),
            ]
        )
        return preprocessor

    def _convert_model_ids_to_item_ids(self, data: pd.DataFrame) -> pd.DataFrame:
        # TODO: this is bottle neck, make it faster
        data = pd.DataFrame(data).reset_index()
        indices = self.train_data[ID_COLUMN].reset_index()
        indices_dict = dict(zip(indices.index, indices.item_id))
        return data.replace(indices_dict)

    def _parse_data_for_output(self, data: pd.DataFrame) -> pd.DataFrame:
        cols_to_iter = data.columns.to_list()
        cols_to_iter.remove("index")

        to_concat = list()
        for col in cols_to_iter:
            new_df = pd.DataFrame()
            new_df[ID_COLUMN] = data["index"]
            new_df[f"reco_id"] = data[col]
            new_df[f"reco_rank"] = col
            to_concat.append(new_df)
        return pd.concat(to_concat)

    def forward(self) -> pd.DataFrame:
        # have to split into preprocess and model becase knn have no predict or other conventions to use in pipe
        # TODO: wrap NearestNeighbors to class with conventions follow sklearn pipeline
        X_trans = self.encoder.fit_transform(self.train_data)
        logger.info("Training started")
        self.model.fit(X_trans)
        logger.info(f"Training with parameters {self.model.get_params()}")

        candidates = self.model.kneighbors(return_distance=False)
        candidates = self._convert_model_ids_to_item_ids(candidates)
        candidates = self._parse_data_for_output(candidates)
        logger.info(f"Retriever DONE")
        return candidates
