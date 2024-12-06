import os

SECRET_KEY = "a_very_secure_secret_key"
SQLALCHEMY_DATABASE_URI = "sqlite:////app/superset_home/superset.db"
ENABLE_PROXY_FIX = True

# Snowflake SQLAlchemy URI
SNOWFLAKE_URI = (
    f"snowflake://{os.getenv('SNOWFLAKE_USER')}:{os.getenv('SNOWFLAKE_PASSWORD')}@"
    f"{os.getenv('SNOWFLAKE_ACCOUNT')}/{os.getenv('SNOWFLAKE_DATABASE')}/"
    f"{os.getenv('SNOWFLAKE_SCHEMA')}?warehouse={os.getenv('SNOWFLAKE_WAREHOUSE')}"
)
