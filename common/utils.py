import re
import os
import pickle
import pandas as pd
import urllib
import json
import yaml

from types import SimpleNamespace
from typing import List, Any
from glob import glob
from loguru import logger
from bs4 import BeautifulSoup


def get_content_from_url(url):
    """
    Uses BeautifulSoup to extract content from the URL.

    :param url:
    :return: text (str)
    """
    f = urllib.request.urlopen(url)
    html_text = f.read()
    soup = BeautifulSoup(html_text, features="html.parser")
    text = soup.get_text()
    text = pre_process(text)

    return text


def save_model(model: Any, filename: str) -> None:
    """
    Saves the model based on the file name provided.

    :param model: Model from sklearn.
    :param filename: name of the file.
    :return: None
    """
    logger.info(f"Saving Model: {filename}")
    pickle.dump(model, open(filename, "wb"))


def get_paths(dataset_path: str) -> List[str]:
    """
    Returns all csv file paths within a directory.

    :param dataset_path: path to directory.
    :return: List of absolute paths to csv files.
    """
    return glob(os.path.join(dataset_path, "*.csv"))


def read_data(data_paths: List[str]) -> pd.DataFrame:
    """
    Reads data (only content) from list of paths and combines them in 1 dataframe.
    :param data_paths: List of paths to csv files.
    :return: pd.Dataframe containing all the data content.
    """
    logger.info(f"Reading data from csv files: {data_paths}")
    dataframes = [pd.read_csv(data_path, usecols=["content"]) for data_path in data_paths]

    logger.info("Concatenating dataframes from different files...")
    docs_df = pd.concat(dataframes)

    return docs_df


def pre_process(text: str) -> str:
    """
    Very light weight pre-processing on the content.

    This method is used to remove any numbers or unexpected
    patterns from the text.

    :param text:
    :return: preprocessed text.
    """
    text = text.lower()
    text = re.sub("", "", text)
    text = re.sub("(\\d|\\W)+", " ", text)
    text = re.sub(r"[^\x00-\x7f]", r" ", text)
    return text


def get_config(filename):
    """
    Utility method to return dot notation cfg object.

    :param filename: Name of the config file.
    :return: Dot notation cfg object.
    """
    config = yaml.safe_load(open(filename))
    app_cfg = json.loads(json.dumps(config), object_hook=lambda d: SimpleNamespace(**d))

    return app_cfg
