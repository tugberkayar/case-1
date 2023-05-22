import os

from .configs import Configs
from .constants import Constants
from .file_operations import FileOperations
from .logics import Logics
from .models import News

__all__ = [
    "Configs",
    "Constants",
    "FileOperations",
    "Logics",
    "News",
]

import nltk
nltk.download("punkt")
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

os.makedirs(Configs.OUTPUT_DIR, exist_ok=True)
