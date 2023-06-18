from rest_framework import serializers
from api_prospects.serializers import ProspectSerializer
from .models import Order
from api_prospects.models import Prospect


class OrderSerializer(serializers.ModelSerializer):
    prospect = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_prospect(self, obj):
        prospect_id = obj.get("prospect_id")
        prospect = Prospect.objects.get(id=prospect_id)
        return ProspectSerializer(prospect).data

    def validate(self, data):
        prospect_id = data.get("prospect_id")
        if not Prospect.objects.filter(id=prospect_id).exists():
            raise serializers.ValidationError({"prospect_id": "Order with the provided 'prospect_id' does not exist."})
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        prospect_data = representation.pop("prospect")
        representation["prospect"] = prospect_data
        return representation


class OrderListSerializer(serializers.ModelSerializer):
    prospect = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_prospect(self, obj):
        prospect_id = obj.prospect_id
        prospect = Prospect.objects.get(id=prospect_id)
        return ProspectSerializer(prospect).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        prospect_data = representation.pop("prospect")
        representation["prospect"] = prospect_data
        return representation
