import re
import os
import pickle
import pandas as pd
import urllib

from typing import List, Any
from glob import glob
from loguru import logger
from bs4 import BeautifulSoup


def get_content_from_url(url):
    f = urllib.request.urlopen(url)
    html_text = f.read()
    soup = BeautifulSoup(html_text, features="html.parser")
    text = soup.get_text()
    text = pre_process(text)

    return text


def save_model(model: Any, filename: str) -> None:
    logger.info(f"Saving Model: {filename}")
    pickle.dump(model, open(filename, "wb"))


def get_paths(dataset_path: str) -> List[str]:
    return glob(os.path.join(dataset_path, "*.csv"))


def read_data(data_paths: List[str]) -> pd.DataFrame:
    logger.info(f"Reading data from csv files: {data_paths}")
    dataframes = [pd.read_csv(data_path, usecols=["content"]) for data_path in data_paths[:1]]

    logger.info("Concatenating dataframes from different files...")
    docs_df = pd.concat(dataframes)

    return docs_df


def pre_process(text: str) -> str:
    text = text.lower()
    text = re.sub("", "", text)
    text = re.sub("(\\d|\\W)+", " ", text)
    text = re.sub(r"[^\x00-\x7f]", r" ", text)
    return text
