from crm_arbitrage.celery import app
from .models import Prospect
from django.db import transaction


@app.task
def process_prospect(prospect_data):
    try:
        with transaction.atomic():
            Prospect.objects.create(**prospect_data)
    except Exception as e:
        print("Error occurred while processing the prospect:", e)
