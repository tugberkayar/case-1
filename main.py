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
    data: List[News] = FileOperations.get_data_from_file()
    stop_words: Set[str] = FileOperations.get_stop_words()
    split_news: Dict[Constants.Category, List[News]] = Logics.split_news_into_categories(data)
    category_news = split_news[Constants.Category(category_name)]
    word_counts: Dict[str, int] = Logics.count_words(category_news, stop_words)
    most_frequent_words: Dict[str, int] = Logics.filter_most_frequent_words(word_counts)
    FileOperations.write_most_frequent_words_to_file(category_name, most_frequent_words)


def merge_results_in_html_file_task():
    """ Compiles results to an HTML file."""
    FileOperations.merge_results_in_html_file()


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
