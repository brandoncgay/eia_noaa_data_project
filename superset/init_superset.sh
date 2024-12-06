#!/bin/bash

# Initialize the Superset database
superset db upgrade

# Create an admin user
superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname User \
  --email admin@example.com \
  --password admin

# Initialize Superset
superset superset init 

# Starting server
/bin/sh -c /usr/bin/run-server.sh

echo "Superset initialization completed!"
