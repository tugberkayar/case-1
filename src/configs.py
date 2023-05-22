import os

from nltk.stem import SnowballStemmer
from string import punctuation
from typing import Set

from .constants import Constants

abs_directory_path = os.path.dirname(os.path.abspath(__file__))


class Configs:
    PROCESSED_CATEGORIES: Set[str] = {
        Constants.Category.POLITICS.value,
        Constants.Category.WELLNESS.value,
        Constants.Category.ENTERTAINMENT.value,
        Constants.Category.TRAVEL.value,
    }

    # Input configs
    DATA_FILE_NAME = abs_directory_path + "/data/data.json"
    STOP_WORDS_FILE_PATH = abs_directory_path + "/data/stopwords.txt"

    # NLP Configs
    STEMMER = SnowballStemmer(language="english")
    MOST_FREQUENT_WORDS_CUTOFF = 10
    PUNCTUATION_SET = set(punctuation).union(set("’”“"))

    # Output Configs
    OUTPUT_DIR = abs_directory_path + "/output"
    COUNTS_OUTPUT_FILE_NAME = OUTPUT_DIR + "/{category}_counts.json"
    HTML_TEMPLATE_FILE_PATH = abs_directory_path + "/data/html_template.txt"
    HTML_OUTPUT_FILE_NAME = OUTPUT_DIR + "/results.html"
