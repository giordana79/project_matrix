from flask import Flask
from celery import Celery
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from app import tasks
# Importa le route definite in app/routes.py
from app import routes 



