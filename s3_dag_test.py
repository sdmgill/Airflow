"""
S3 Sensor Connection Test
"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.sensors import S3KeySensor
from airflow.operators import SimpleHttpOperator, HttpSensor
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 8, 16),
    'email': ['sean.gill@portsamerica.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('s3_dag_test', default_args=default_args, schedule_interval= '0 0 * * *')

t1 = BashOperator(
    task_id='bash_test',
    bash_command='echo "hello, it should work" > s3_conn_test.txt',
    dag=dag)

sensor = S3KeySensor(
    task_id='check_s3_for_file_in_s3',
    bucket_key='file-to-watch-*',
    wildcard_match=True,
    bucket_name='pa-airflow',
    aws_conn_id='s3_conn',
    timeout=18*60*60,
    poke_interval=120,
    dag=dag)

t1.set_upstream(sensor)