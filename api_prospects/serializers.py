from rest_framework import serializers
from .models import Prospect


class ProspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prospect
        fields = "__all__"
