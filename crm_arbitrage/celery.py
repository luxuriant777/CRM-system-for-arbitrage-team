from celery import Celery
import os

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm_arbitrage.settings")

app = Celery("crm_arbitrage")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
