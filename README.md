# Django Template
## Info
- Python version: `3.12.0`
Django template project with postgres

## Services
1. `cd docker`
2. `COMPOSE_PROJECT_NAME=django_template docker-compose -f docker-compose.services.yml up -d`

## Run project:
1. `python -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python manage.py runserver`

## Docker Build:
1. `docker-compose build`
2. `docker-compose up -d`