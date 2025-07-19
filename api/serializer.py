from rest_framework import serializers
from userauths.models import Profile,User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from datetime import datetime
from booking.models import Booking
from Transport.models import Transport
from django.utils import timezone

from Transport.models import Transport
from rest_framework import serializers

from rest_framework import serializers
from booking.models import Booking
from Transport.models import Transport


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username

        return token
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True , required=True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True , required=True)

    class Meta:
        model = User
        fields = ['full_name' , 'email' , 'password' , 'password2']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password" : "Password fields didnt match."})
        return attrs
    
    def create(self , validated_data):
        user = User.objects.create(
            full_name = validated_data['full_name'],
            email = validated_data['email']
        )
        email_username, _ = user.email.split("@")
        user.username = email_username
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'



class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'booking_date']

    def validate(self, data):
        request = self.context.get('request')
        user = request.user if request else None

        seat_number = data.get('seat_number')
        transport = data.get('transport')

        if not seat_number:
            raise serializers.ValidationError({"seat_number": "شماره صندلی الزامی است."})

        if transport.departure_time < timezone.now():
            raise serializers.ValidationError({"transport": "امکان رزرو سفرهای گذشته وجود ندارد."})

        if int(seat_number) > int(transport.total_seats):
            raise serializers.ValidationError({"seat_number": f"حداکثر شماره صندلی {transport.total_seats} است."})

        if not self.instance or (
            self.instance.transport != transport or self.instance.seat_number != seat_number
        ):
            if Booking.objects.filter(
                transport=transport,
                seat_number=seat_number,
                is_cancelled=False  # 🟢 این خط جدید اضافه شده
            ).exists():
                raise serializers.ValidationError({"seat_number": "این صندلی قبلاً رزرو شده است."})

        return data


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)