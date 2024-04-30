from onlinerequest.models import Document
from onlinerequest.models import Request
from rest_framework import serializers

class RequestSerializer(serializers.ModelSerializer):
    document = serializers.CharField()

    class Meta:
        model = Request
        fields = ['id', 'description', 'files_required', 'document']  # Adjust fields as needed
