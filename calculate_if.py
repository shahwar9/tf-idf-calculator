from handlers.tf import TermFrequencyCalculator


def main(model_file):
    tf_mdl = TermFrequencyCalculator(models_dir=model_file)

    tf_mdl.get_tf("obama calculated this document republicans")


if __name__ == "__main__":
    main("models")
