from rest_framework import serializers
from .models import Lead, Order


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    lead = serializers.PrimaryKeyRelatedField(queryset=Lead.objects.all())

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lead_id = representation.pop('lead')
        representation['lead'] = LeadSerializer(Lead.objects.get(id=lead_id)).data
        return representation
