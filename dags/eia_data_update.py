from airflow.decorators import dag, task
from airflow.utils.dates import datetime, timedelta

from include.eia_data_functions import get_eia_data_from_api, merge_eia_data_to_snowflake

@dag(
    dag_id='get_eia_data',
    description="A dag that extracts data from eia.gov api and merges it into a snowflake table.",
    default_args={
        "owner": "Brandon Gay",
        "start_date": datetime(2024, 1, 1),
        "retries": 0,
        "execution_timeout": timedelta(hours=1),
    },
    start_date=datetime(2024, 1, 1),
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=True,
    template_searchpath='include',
    tags=["eia"],
)
def get_eia_data():
    
    @task()
    def extract_data_task(ds):
        return get_eia_data_from_api(ds)
    
    @task
    def update_table_task(data):
        return merge_eia_data_to_snowflake(data)
    

    data = extract_data_task()
    update_table_task(data)

dag_instance = get_eia_data()