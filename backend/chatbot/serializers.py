from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
class ChatInputSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=1000, required=True)

class ChatResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    status = serializers.CharField()
    
    
    
    
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('帳號或密碼錯誤')
            if not user.is_active:
                raise serializers.ValidationError('帳號已被停用')
            data['user'] = user
        else:
            raise serializers.ValidationError('請輸入帳號和密碼')
        
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','is_staff']