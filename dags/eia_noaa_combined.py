import os
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, RenderConfig
from dotenv import load_dotenv
from airflow.decorators import dag, task
from airflow.utils.dates import datetime, timedelta

from include.eia_data_functions import get_eia_data_from_api, merge_eia_data_to_snowflake
from include.noaa_data_funtions import merge_noaa_data_to_snowflake

dbt_env_path = os.path.join(os.environ['AIRFLOW_HOME'], 'dbt_project', 'dbt.env')
load_dotenv(dbt_env_path)

airflow_home = os.getenv('AIRFLOW_HOME')
PATH_TO_DBT_PROJECT = f'{airflow_home}/dbt_project'
PATH_TO_DBT_PROFILES = f'{airflow_home}/dbt_project/profiles.yml'


profile_config = ProfileConfig(
    profile_name="dbt_project",
    target_name="dev",
    profiles_yml_filepath=PATH_TO_DBT_PROFILES
)

@dag(
    dag_id='eia_noaa_combined_data',
    description="A dag that extracts data from eia.gov api and merges it into a snowflake table.",
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
    tags=["eia","noaa","dbt"],
)
def get_eia_and_noaa_data():
    
    @task()
    def extract_eia_data_task(ds):
        return get_eia_data_from_api(ds)
    
    @task()
    def update_eia_table_task(data):
        return merge_eia_data_to_snowflake(data)
    
    @task()
    def update_noaa_table_task(ds):
        return merge_noaa_data_to_snowflake(ds)
    
    dbt_build_models = DbtTaskGroup(
        group_id="eia_and_noaa_cosmos_dag",
        project_config=ProjectConfig(PATH_TO_DBT_PROJECT),
        profile_config=profile_config,
        render_config=RenderConfig(
            exclude=["path:seeds/*"],
        ),
    )

    data = extract_eia_data_task(ds="{{ ds }}")
    update_eia = update_eia_table_task(data)
    update_noaa = update_noaa_table_task(ds="{{ ds }}")
    
    [update_eia, update_noaa] >> dbt_build_models

dag_instance = get_eia_and_noaa_data()