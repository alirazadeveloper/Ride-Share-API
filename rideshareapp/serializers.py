# import serializer from rest_framework
from rest_framework import serializers
from varname import nameof
# import model from models.py
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


class imageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = (
            nameof(Image.image),
            # nameof(Image.name)
        )


class loginSerilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user
        # fields = '__all__'
        fields = ("id",
                  nameof(user.email),
                  nameof(user.password),
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
