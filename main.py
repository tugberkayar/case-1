import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from typing import Dict, List, Set

from src import Configs, Constants, FileOperations, Logics, News


def count_words_for_category(category_name: str):
    """ Task that counts most frequent words for a given category name, and writes it to a JSON file.
    It can be considered main function for a category.

    Args:
        category_name (str): Category.
    """
    logging.info(f"Calculation started for {category_name.lower()} category.")

    data: List[News] = FileOperations.get_data_from_file()
    logging.info(f"Data is loaded. News count: {len(data)}")

    stop_words: Set[str] = FileOperations.get_stop_words()
    logging.info(f"Stop words is loaded. Stop word count: {len(stop_words)}")

    category_news = [news for news in data if news.category == category]
    logging.info(f"{category_name.title()} news are filtered. Number of news in the category: {len(category_news)}")

    word_counts: Dict[str, int] = Logics.count_words(category_news, stop_words)
    logging.info(f"Words are counted. Number of distinct words: {len(word_counts)}")

    most_frequent_words: Dict[str, int] = Logics.filter_most_frequent_words(word_counts)
    logging.info(f"Most frequent words are filtered: {most_frequent_words}")

    FileOperations.write_most_frequent_words_to_file(category_name, most_frequent_words)
    logging.info("Most frequent words are written into a JSON file.")


def merge_results_in_html_file_task():
    """ Compiles results to an HTML file."""
    logging.info("Compilation has started.")

    FileOperations.merge_results_in_html_file()
    logging.info("All files are compiled into an HTML file.")


with DAG(dag_id="main_dag",
         start_date=datetime.utcnow(),
         description="Main DAG of the project") as dag:

    counter_tasks = []
    for category in Configs.PROCESSED_CATEGORIES:
        category_task = PythonOperator(
            task_id=f"{category.lower()}-counter",
            python_callable=count_words_for_category,
            op_kwargs={"category_name": category},
            dag=dag
        )
        counter_tasks.append(category_task)

    merge_to_html_task = PythonOperator(
        task_id="html-merger",
        python_callable=merge_results_in_html_file_task,
        dag=dag
    )
    for task in counter_tasks:
        task.set_downstream(merge_to_html_task)
