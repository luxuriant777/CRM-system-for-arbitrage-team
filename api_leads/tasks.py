from crm_arbitrage.celery import app
from .models import Lead
from django.db import transaction


@app.task
def process_lead(lead_data):
    try:
        with transaction.atomic():
            Lead.objects.create(**lead_data)
    except Exception as e:
        print("Error occurred while processing lead:", e)
