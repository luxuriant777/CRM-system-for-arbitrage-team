from rest_framework import serializers
from api_leads.serializers import LeadSerializer
from .models import Order
from api_leads.models import Lead


class OrderSerializer(serializers.ModelSerializer):
    lead = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_lead(self, obj):
        lead_id = obj.get("lead_id")
        lead = Lead.objects.get(id=lead_id)
        return LeadSerializer(lead).data

    def validate(self, data):
        lead_id = data.get("lead_id")
        if not Lead.objects.filter(id=lead_id).exists():
            raise serializers.ValidationError({"lead_id": "Order with the provided 'lead_id' does not exist."})
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lead_data = representation.pop("lead")
        representation["lead"] = lead_data
        return representation


class OrderListSerializer(serializers.ModelSerializer):
    lead = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_lead(self, obj):
        lead_id = obj.lead_id
        lead = Lead.objects.get(id=lead_id)
        return LeadSerializer(lead).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lead_data = representation.pop("lead")
        representation["lead"] = lead_data
        return representation
