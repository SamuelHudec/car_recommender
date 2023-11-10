import logging
import warnings
from typing import Tuple

import numpy as np
import pandas as pd

from src.config.data import ID_COLUMN, SPLIT_COLUMNS, SPLIT_PATTERNS, TRAINING_COLUMNS
from utils.data import data_fetcher

# Filter out FutureWarnings
warnings.simplefilter(action="ignore", category=FutureWarning)

logger = logging.getLogger("preproces_training_data")


class GetTrainingDataKNN:
    """
    I propose to write separate preprocess for each retriever we plan to use
    here you can find a lot hard coding what can or can not be unify
    TODO: write base class with fixed commons, in and outs
    TODO: extreme values
    """

    def __init__(self, path_to_data: str) -> None:
        self.data = data_fetcher(path=path_to_data)
        self.training_columns = TRAINING_COLUMNS
        self._check_and_log_stats()
        self.training_columns.append(ID_COLUMN)

    def _check_and_log_stats(self):
        # for some stats are questionable if not rise an exception
        logger.info(f"Data shape: {self.data.shape}")
        duplicates = self.data.drop_duplicates().shape[0] - self.data.shape[0]
        if duplicates > 0:
            logger.info(f"Number of duplicates: {duplicates}")
            self.data = self.data.drop_duplicates()
        missed_columns = [i for i in (set(self.training_columns) - set(self.data.columns))]
        if len(missed_columns) > 0:
            logger.error(f"The following training columns are missing in dataset: {missed_columns}")
        logger.info(f"Total number of nans: {self.data.isna().sum()}")
        if ID_COLUMN not in self.data.columns.tolist():
            raise ValueError("ID column are not in loaded dataset")

    def _split_data_by_at(self, column: str) -> None:
        # in production version check if it covers certain patterns or common by row not column
        if (self.data[column].str.contains("@").all()) & (column in self.data.columns):
            self.data[[f"{column}_left", f"{column}_right"]] = self.data[column].str.split("@", expand=True)
            # add new columns and delete old
            self.training_columns.append(f"{column}_left")
            self.training_columns.append(f"{column}_right")
            self.training_columns.remove(column)
        else:
            logger.error(f"Column {column} cant be split by @ or not in dataset")

    def _parse_by_pattern(self, column: str, pattern: str) -> None:
        if column in self.data.columns:
            self.data[column] = self.data[column].str.replace(" ", "")
            self.data[column] = self.data[column].str.lower()
            self.data[column] = self.data[column].str.replace(pattern, "")
            self.data[column] = self.data[column].replace("", np.nan)
            try:
                self.data[column] = self.data[column].astype(float)
            except ValueError:
                logger.error(f"Column {column} cant be cast as float")

    def _handle_split_columns(self):
        # TODO: parametrize
        for col in SPLIT_COLUMNS:
            self._split_data_by_at(col)
        for col, pat in SPLIT_PATTERNS.items():
            self._parse_by_pattern(col, pat)

    def _handle_fuel_type(self):
        # TODO: parametrize
        for type in ["CNG", "LPG", "CNG + CNG", "Petrol + CNG", "Petrol + LPG"]:
            self.data.loc[self.data["Fuel Type"] == type, "Fuel Type"] = "GAS"
        for type in ["Electric", "Hybrid"]:
            self.data.loc[self.data["Fuel Type"] == type, "Fuel Type"] = "ELC"

    def forward(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        # important is to fix outputs from each pipline element
        self._handle_split_columns()
        self._handle_fuel_type()
        logger.info(f"Preprocess DONE")
        return self.data[self.training_columns], self.data
