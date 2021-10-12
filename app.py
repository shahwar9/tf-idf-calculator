from flask import Flask, request, jsonify

from common.utils import get_content_from_url
from handlers.tf import TermFrequencyCalculator

app = Flask(__name__)
port = 5100


@app.route("/tfidf")
def calculate_term_frequency():
    url = request.args.get("url", default="https://en.wikipedia.org/wiki/Main_Page", type=str)
    limit = request.args.get("limit", default=10, type=int)
    content = get_content_from_url(url)

    top_tf_results = calculate_tf(content, limit)

    return jsonify(top_tf_results)


def calculate_tf(text, limit):
    tf_mdl = TermFrequencyCalculator(models_dir="models")
    results = tf_mdl.get_tf(text, limit)

    return format_results(results)


def format_results(results):
    formatted_result = {"terms": []}

    for term, tfidf in results.items():
        formatted_result["terms"].append({"term": term, "tf-idf": tfidf})

    return formatted_result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
