import json

from typing import Any, Dict, List, Set

from .configs import Configs
from .models import News


class FileOperations:

    @staticmethod
    def get_data_from_file() -> List[News]:
        """ Reads input data from file and validates it into list of News objects.

        Returns:
            List[News]: List of news.
        """
        raw_data: str = FileOperations._read_file(Configs.DATA_FILE_NAME)
        data_objects: List[News] = FileOperations._convert_raw_data_to_objects(raw_data)
        return data_objects

    @staticmethod
    def get_stop_words() -> Set[str]:
        """ Reads stop words from input file.

        Returns:
            Set[str]: Set of stop words.
        """
        raw_stop_words: str = FileOperations._read_file(Configs.STOP_WORDS_FILE_PATH)
        stop_words: Set[str] = set(raw_stop_words.split("\n"))
        return stop_words

    @staticmethod
    def write_most_frequent_words_to_file(category: str, counts: Dict[str, int]):
        """ Writes most frequent words from given category to a JSON file.

        Args:
            category (str): Category string.
            counts (Dict[str, in]): Most frequent words dict.
        """
        file_name = Configs.COUNTS_OUTPUT_FILE_NAME.format(category=category.lower())
        with open(file_name, "w") as f:
            json.dump(counts, f)

    @staticmethod
    def _convert_raw_data_to_objects(raw_data: str) -> List[News]:
        """ Converts raw input data to list of News objects.

        Args:
            raw_data (str): Raw data string

        Returns:
            List[News]: List of News objects.
        """
        data_list: List[str] = raw_data.split("\n")[:-1]
        data_json: List[Dict[str, Any]] = [json.loads(d) for d in data_list]
        data_objects: List[News] = [News(**d) for d in data_json if d["category"] in Configs.PROCESSED_CATEGORIES]
        return data_objects

    @staticmethod
    def merge_results_in_html_file():
        """ Merges most frequent word JSON files into an HTML file."""
        most_frequent_words: Dict[str, Dict[str, int]] = {}
        for category in Configs.PROCESSED_CATEGORIES:
            category_result_file = Configs.COUNTS_OUTPUT_FILE_NAME.format(category=category)
            category_result: Dict[str, int] = json.loads(FileOperations._read_file(category_result_file))
            most_frequent_words[category] = category_result
        html_text = FileOperations._build_html_text(most_frequent_words)
        with open(Configs.HTML_OUTPUT_FILE_NAME, "w") as f:
            f.write(html_text)

    @staticmethod
    def _build_html_text(most_frequent_words: Dict[str, Dict[str, int]]) -> str:
        """ Converts most frequent word dict to an HTML text.

        Args:
            most_frequent_words (Dict[str, int]): Most frequent words dict.

        Returns:
            str: HTML text.
        """
        html_template: str = FileOperations._read_file(Configs.HTML_TEMPLATE_FILE_PATH)
        html_body: str = FileOperations._build_html_body(most_frequent_words)
        html_text: str = html_template.format(body_text=html_body)
        return html_text

    @staticmethod
    def _build_html_body(most_frequent_words: Dict[str, Dict[str, int]]) -> str:
        """ Converts most frequent word dict to an HTML body text.

        Args:
            most_frequent_words (Dict[str, int]): Most frequent words dict.

        Returns:
            str: HTML body text.
        """
        html_body = ""
        for category, words in most_frequent_words.items():
            category_body = f"<h1>{category}</h1>\n<p>"
            for word, count in words.items():
                category_body += f"{word}: {count}<br>"
            category_body += "</p>"
            html_body += category_body
        return html_body

    @staticmethod
    def _read_file(path: str) -> str:
        """ Reads given file path.

        Args:
            path (str): File path.

        Returns:
            str: Text in the file.

        Raises:
            FileNotFoundError.
        """
        with open(path) as f:
            data: str = f.read()
        return data
