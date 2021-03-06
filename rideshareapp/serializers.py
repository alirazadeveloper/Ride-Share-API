# import serializer from rest_framework
from rest_framework import serializers
from varname import nameof
from .models import *

# Create a model serializer


class user_registerSerilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user
        # fields = '__all__'
        fields = ("id", nameof(user.full_name),
                  nameof(user.phone_number),
                  nameof(user.email),
                  nameof(user.password),
                  nameof(user.image),
                  )


class user_getSerilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user
        # fields = '__all__'
        fields = ("id", nameof(user.full_name),
                  nameof(user.phone_number),
                  nameof(user.email),
                  nameof(user.password),
                  nameof(user.image),
                  nameof(user.eduction),
                  nameof(user.job_info),
                  )


class verifyotpSerilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user
        # fields = '__all__'
        fields = ("id", nameof(user.phone_number),
                  nameof(user.otp),
                  )


class resentotpSerilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user
        # fields = '__all__'
        fields = ("id", nameof(user.phone_number),
                  )

    
class fileSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = fileupload
        fields = (
            nameof(fileupload.filefield),
        )

    

class loginSerilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user
        # fields = '__all__'
        fields = ("id",
                  nameof(user.email),
                  nameof(user.password),
                  nameof(user.fcm),
                  )


class forgetpassSerilizer(serializers.HyperlinkedModelSerializer):
    new_password = serializers.CharField(source='password')

    class Meta:
        model = user
        # fields = '__all__'
        fields = ("id",
                  nameof(user.phone_number),
                  "new_password",
                  )


class car_pics(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = carpics
        fields = ("id", nameof(carpics.filename),
                  )


class carSerilizer(serializers.HyperlinkedModelSerializer):
    pictures = car_pics(many=True)

    class Meta:
        model = car
        # fields = '__all__'
        fields = ("id", nameof(car.user_id),
                  nameof(car.conveyance),
                  nameof(car.model),
                  nameof(car.seats),
                  "pictures"
                  )
    def create(self, validated_data):
        car_pics_data = validated_data.pop('pictures')
        cardata = car.objects.create(**validated_data) 
        for car_pics_data in car_pics_data:
            carpics.objects.create(                
                pictures=cardata, **car_pics_data)
        return cardata 
    
    def update(self, instance, validated_data):
        user = instance
        user.__dict__.update(validated_data)
        user.save()
        return user

# class updatecarSerilizer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = car
#         # fields = '__all__'
#         fields = ("id",
#                   nameof(car.seats),
#                   )
class updatefcmSerilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user
        # fields = '__all__'
        fields = ("id",
                  nameof(user.fcm),
                  )


class tripSerilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = trip
        # fields = '__all__'
        fields = ("id", nameof(trip.user_id),
                  nameof(trip.pickup),
                  nameof(trip.dropup),
                  nameof(trip.date),
                  nameof(trip.time),
                  )
        
class feedbackSerilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = feedback
        # fields = '__all__'
        fields = ("id", nameof(feedback.user_id),
                  nameof(feedback.message),
                  nameof(feedback.stars),
                  )
        
        
class gettripSerilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = trip
        # fields = '__all__'
        fields = ("id", nameof(trip.user_id),
                  nameof(trip.pickup),
                  nameof(trip.dropup),
                  nameof(trip.date),
                  nameof(trip.time),
                  nameof(trip.created_on),
                  )
        
        
class chatSerilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = chat
        # fields = '__all__'
        fields = ("id", nameof(chat.senderid),
                  nameof(chat.receiverid),
                  nameof(chat.type),
                  nameof(chat.message),
                  )