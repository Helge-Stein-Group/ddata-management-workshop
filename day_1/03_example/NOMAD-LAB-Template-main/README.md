# NOMAD-LAB Template For Parsing Battery Cycling Data

1. Pull the repository.
2. Add the folder "battery-cycle-parser" as the environment variable "PYTHONPATH"
3. Run chown -R 1000:1000 battery-cycle-parser
4. Add environment variable COMPOSE_FILE=docker-compose.yaml:docker-compose.plugins.yaml
5. docker compose up -d
