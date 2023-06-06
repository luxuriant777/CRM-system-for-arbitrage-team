from rest_framework import serializers
from .models import Lead, Order


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    lead = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_lead(self, obj):
        lead_id = obj.get('lead_id')
        lead = Lead.objects.get(id=lead_id)
        return LeadSerializer(lead).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lead_data = representation.pop('lead')
        representation['lead'] = lead_data
        return representation


class OrderListSerializer(serializers.ModelSerializer):
    lead = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_lead(self, obj):
        lead_id = obj.lead_id
        lead = Lead.objects.get(id=lead_id)
        return LeadSerializer(lead).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lead_data = representation.pop('lead')
        representation['lead'] = lead_data
        return representation
