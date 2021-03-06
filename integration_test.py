import json
from types import SimpleNamespace
from flask import Flask, request, jsonify

from handlers.tf import TermFrequencyCalculator
from handlers.idf import InverseDocumentFrequencyCalculator
from common.utils import pre_process


def create_idf(cfg, docs):
    pp_docs = [pre_process(text) for text in docs]
    idf = InverseDocumentFrequencyCalculator(cfg)
    idf.train_idf(pp_docs)


def calculate_term_frequency(cfg, content):
    tf_mdl = TermFrequencyCalculator(cfg)
    return tf_mdl.get_tf(content, limit=5)


if __name__ == "__main__":
    # Create config to save test models.
    config = {
        "models_dir": "models",
        "cv_model_name": "test-cv.pkl",
        "idf_model_name": "test-idf.pkl"
    }
    app_cfg = json.loads(json.dumps(config), object_hook=lambda d: SimpleNamespace(**d))

    # Create a test dataset
    docs = [
        "the house had a tiny little mouse",
        "the cat saw the mouse",
        "the mouse ran away from the house",
        "the cat finally ate the mouse",
        "the end of the mouse story"
    ]

    # Step 1: Create small IDF Model
    create_idf(app_cfg, docs)

    # Let us make first document to get Term Frequency.
    test_document = docs[0]

    # Step 2: Use IDF model to calculate term frequency.
    results = calculate_term_frequency(app_cfg, test_document)

    # Check if the values generated by models are expected values.
    assert results["tiny"] == 0.589
    assert results["little"] == 0.589
    assert results["house"] == 0.476
    assert results["mouse"] == 0.281

    print("***********************************")
    print("*     Integration Tests Passed    *")
    print("***********************************")

