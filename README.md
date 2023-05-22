# Entrapeer Case 1

This project counts words in given news articles for given categories,
writes the most frequent words to an HTML file. It does it with a airflow workflow.

## How to Compile

1. Go to project folder from terminal.
2. Run `pip install -r requirmements.txt`
3. Go back parent directory. `cd ..`
4. Run `export AIRFLOW_HOME=$(pwd)`. In this way, when you run airflow, the files will appear in the parent directory of the project.
5. Run `airflow db init`
6. Checkout `airflow.cfg` file that should be appeared on the parent directory of the project. In this file, there is a variable called `dags_folder`. Set it to project directory, so that it detects the DAG of the project.
7. Run `airflow standalone`.
8. After the run is completed, go to http://localhost:8080/ in your web browser. The `main_dag` should be appeared on the list.
9. Click on it.
10. On the top right corner, you will see a button that resembles Play button. Click on it. Then Trigger the DAG.
11. After the completion, the output files must appear on `output/` folder of the project.