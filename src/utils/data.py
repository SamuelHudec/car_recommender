import logging
import os

import pandas as pd
import requests

logger = logging.getLogger("Data_utils")


def data_fetcher(path: str) -> pd.DataFrame:
    if os.path.splitext(path)[1] == ".csv":
        return pd.read_csv(path)
    elif path.startswith("http://"):
        response = requests.get(path)
        return pd.DataFrame(response.json())
    else:
        logger.error("Can not fetch data. Check if path have correct format")


def data_dumper(data: pd.DataFrame, path: str):
    if os.path.splitext(path)[1] == ".csv":
        data.to_csv(path, index=False)
        logger.info(f"Data dump to directory: {path}")
    elif path.startswith("http://"):
        data_string = data.to_json(index=False)
        response = requests.put(path, json=data_string)
        logger.info(f"Data dump with message: {response.json()}")
    else:
        logger.error("Can not fetch data. Check if path have correct format")
