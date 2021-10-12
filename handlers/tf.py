import pickle
import os

from common.utils import pre_process


class TermFrequencyCalculator:
    def __init__(self, cfg):
        self.cfg = cfg
        try:
            idf_path = os.path.join(self.cfg.models_dir, self.cfg.idf_model_name)
        except FileNotFoundError:
            print(f"Model file not found: {idf_path}")

        try:
            cv_path = os.path.join(self.cfg.models_dir, self.cfg.cv_model_name)
        except FileNotFoundError:
            print(f"Model file not found: {cv_path}")

        self.idf = pickle.load(open(idf_path, "rb"))
        self.cv = pickle.load(open(cv_path, "rb"))
        self.tfidf_vector = None

    def get_tf(self, text, limit):

        text = pre_process(text)

        self.tfidf_vector = self.idf.transform(self.cv.transform([text]))

        sorted_items = self.sort_vectors()

        results = self.extract_top(sorted_items, limit)

        return results

    def extract_top(self, sorted_items, limit):

        feature_names = self.cv.get_feature_names()

        sorted_items = sorted_items[:limit]

        score_vals = []
        feature_vals = []

        for idx, score in sorted_items:
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

        results = {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]] = score_vals[idx]

        return results

    def sort_vectors(self):
        coo_matrix = self.tfidf_vector.tocoo()
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
