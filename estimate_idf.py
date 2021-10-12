from handlers.idf import InverseDocumentFrequencyCalculator


def main(dataset_path):
    idf = InverseDocumentFrequencyCalculator(models_dir="models")
    idf.train_idf(dataset_path=dataset_path)


if __name__ == "__main__":
    main("/Users/shahwar/repos/tf-idf-calculator/dataset")
