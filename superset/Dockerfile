FROM apache/superset:latest

# Install Snowflake connector for Python
USER root
RUN pip install snowflake-sqlalchemy

# Copy the initialization script
COPY init_superset.sh /app/init_superset.sh
COPY superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
# Run the initialization script
ENTRYPOINT ["/app/init_superset.sh"]


