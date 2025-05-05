from rest_framework import serializers
from .models import Ticket
from .models import User
import uuid



        
      
          
          
    
          

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2','is_staff']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 before creating user
        user = User.objects.create_user(**validated_data)  # This hashes the password
        return user


"""class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['id', 'ticketNumber', 'status', 'assignedUser','additionDate']"""

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id','ticketNumber', 'ticketDescription', 'status', 'assignedUser', 'additionDate']
        read_only_fields = ['id','ticketNumber', 'assignedUser', 'additionDate']

    def create(self, validated_data):
        validated_data['assignedUser'] = None
        if validated_data['status'] == '' or validated_data['status'] == 'None':
            validated_data['status'] = 'new'
        validated_data['ticketNumber'] = "TK"+str(uuid.uuid4())[:8]  
        return super().create(validated_data)