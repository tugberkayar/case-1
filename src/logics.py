from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple

from .configs import Configs
from .constants import Constants
from .models import News


class Logics:

    @staticmethod
    def count_words(news: List[News], stop_words: Set[str]) -> Dict[str, int]:
        """ Counts words in given list of news article, discarding the stop words.

        Args:
            news (List[News]): List of news.
            stop_words (Set[str]): Set of stop words.

        Returns:
            Dict[str, int]: Word counts.
        """
        all_words: List[str] = []
        for n in news:
            all_words += n.stemmed_tokens
        all_words_wout_stop_words: List[str] = [word for word in all_words
                                                if not Logics._is_word_excluded(word, stop_words)]

        counter = Counter(all_words_wout_stop_words)
        return dict(counter)

    @staticmethod
    def filter_most_frequent_words(counts: Dict[str, int]) -> Dict[str, int]:
        """ Sorts given word counts, and keeps only the most recurrent words up to cutoff word count.

        Args:
            counts Dict[str, in]: Word counts.

        Returns:
            Dict[str, int]: Word counts, only the most appeared words.
        """
        sorted_counts: List[Tuple[str, int]] = sorted(counts.items(), key=lambda item: item[1], reverse=True)
        most_frequent_words: List[Tuple[str, int]] = sorted_counts[:Configs.MOST_FREQUENT_WORDS_CUTOFF]
        most_frequent_words_dict: Dict[str, int] = {word: count for word, count in most_frequent_words}
        return most_frequent_words_dict

    @staticmethod
    def split_news_into_categories(all_news: List[News]) -> Dict[Constants.Category, List[News]]:
        """ Split news into categories, Keeps only the ones that will be processed.

        Args:
            all_news (List[News]): List of news.

        Returns:
            Dict[Constant.Category, List[News]]: News divided into categories.
        """
        split_news: Dict[Constants.Category, List[News]] = defaultdict(list)
        for news in all_news:
            split_news[news.category].append(news)
        return split_news

    @staticmethod
    def _is_word_excluded(word: str, stop_words: Set[str]) -> bool:
        """ Decides whether a word should be excluded from counter or not.

        Args:
            word (str): Word.
            stop_words (Set[str]): Stop words.

        Returns:
            bool: The decision.
        """
        return (word in stop_words or
                word.isnumeric())
