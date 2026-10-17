from rest_framework import serializers


class ChatMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000)
    locale = serializers.ChoiceField(choices=['ar', 'en'], default='ar', required=False)
