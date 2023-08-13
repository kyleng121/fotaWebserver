from rest_framework import serializers
from .models import Messages

class messagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'  # You can specify specific fields if needed