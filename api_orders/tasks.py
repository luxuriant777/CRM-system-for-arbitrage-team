from crm_arbitrage.celery import app
from .models import Order
from django.db import transaction


@app.task
def process_order(order_data):
    try:
        with transaction.atomic():
            Order.objects.create(**order_data)
    except Exception as e:
        print("Error occurred while processing order:", e)
