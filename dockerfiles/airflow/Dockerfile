FROM apache/airflow:2.8.0-python3.9 as development
COPY requirements.txt /tmp


RUN pip install -U jupyter-core --user
RUN pip install -U jupyter --user
RUN pip install --no-cache-dir -r /tmp/requirements.txt


RUN chmod -R 775 /home/airflow/.local/share/jupyter
