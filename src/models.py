from cached_property import cached_property
from dataclasses import dataclass
from datetime import datetime
from nltk.tokenize import word_tokenize
from typing import List

from .configs import Configs
from .constants import Constants


@dataclass
class News:
    link: str
    headline: str
    category: Constants.Category
    short_description: str
    authors: str
    date: datetime

    @cached_property
    def stemmed_tokens(self) -> List[str]:
        return [self._stemmer.stem(token) for token in self._tokens]

    @property
    def _article(self) -> str:
        return self.short_description

    @cached_property
    def _article_wout_punctuations(self) -> str:
        return "".join([char for char in self._article if char not in Configs.PUNCTUATION_SET])

    @cached_property
    def _tokens(self) -> List[str]:
        return word_tokenize(self._article_wout_punctuations)

    @property
    def _stemmer(self):
        return Configs.STEMMER
