import os

from loguru import logger
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

from common.utils import pre_process, get_paths, read_data, save_model


class InverseDocumentFrequencyCalculator:
    def __init__(self, cfg):
        self.cfg = cfg

    def create_idf_model(self):

        # Get absolute paths to all csv files present.
        data_paths = get_paths(self.cfg.dataset_dir)

        # Read content from csv files in one dataframe.
        # TODO: Data read can be a bottle neck in performance,
        #       can be performed in parallel.
        docs_df = read_data(data_paths)

        # Apply preprocessing to the data.
        # TODO: Bottleneck if there is loads of articles.
        docs_df["content"] = docs_df["content"].apply(lambda x: pre_process(x))
        pp_docs = docs_df["content"].tolist()

        self.train_idf(pp_docs)

    def train_idf(self, pre_processed_docs):
        # Calculate count vectorizer.
        cv = CountVectorizer(stop_words="english")
        word_count_vector = cv.fit_transform(pre_processed_docs)

        logger.info("Count Vectorizer model created.")
        logger.info("Top 10 vocabulary words: " f"{list(cv.vocabulary_.keys())[:10]}")

        save_model(cv, os.path.join(self.cfg.models_dir, self.cfg.cv_model_name))

        # Create tf-idf model
        tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
        tfidf_transformer.fit(word_count_vector)

        save_model(tfidf_transformer, os.path.join(self.cfg.models_dir, self.cfg.idf_model_name))

    def update_idf(self, new_dataset):
        raise NotImplementedError("IDF Update is not implemented yet.")
