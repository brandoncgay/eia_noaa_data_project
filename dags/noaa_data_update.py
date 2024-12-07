from airflow.decorators import dag, task
from airflow.utils.dates import datetime, timedelta

from include.noaa_data_funtions import merge_data_to_snowflake

@dag(
    description="A dag extracts data from noaa s3 and merges it into a snowflake table.",
    default_args={
        "owner": "Brandon Gay",
        "start_date": datetime(2024, 12, 1),
        "retries": 0,
        "execution_timeout": timedelta(hours=1),
    },
    start_date=datetime(2024, 12, 1),
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=True,
    template_searchpath='include',
    tags=["noaa"],
)
def get_noaa_data():
    
    @task
    def update_table_task(ds):
        return merge_data_to_snowflake(ds)
    
    update_table_task()

dag_instance = get_noaa_data()