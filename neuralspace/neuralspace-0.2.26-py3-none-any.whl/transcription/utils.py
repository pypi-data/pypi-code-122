import yaml

from neuralspace.transcription.constants import (
    DOMAIN,
    LANGUAGE_MODEL_MAP_PATH,
    SAMPLE_RATE,
    SUBURL,
)


def get_sample_rate_and_suburl_from_language(language: str, specialization: str):
    sub_url = None
    sample_rate = None
    with open(LANGUAGE_MODEL_MAP_PATH) as f:
        model_map = yaml.safe_load(f)
    language_models = model_map.get(language, None)
    for model in language_models:
        if model[DOMAIN] == specialization:
            sub_url = model.get(SUBURL, None)
            sample_rate = model.get(SAMPLE_RATE, None)

    return sub_url, sample_rate
