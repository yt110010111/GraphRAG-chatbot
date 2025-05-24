from rest_framework import serializers

class ChatInputSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=1000, required=True)

class ChatResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    status = serializers.CharField()