import yaml
import json
from types import SimpleNamespace

from handlers.idf import InverseDocumentFrequencyCalculator
from common.utils import get_config


def main(cfg):
    idf = InverseDocumentFrequencyCalculator(cfg)
    idf.create_idf_model()


if __name__ == "__main__":
    app_cfg = get_config("config.yaml")
    main(app_cfg)
