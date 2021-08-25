# import serializer from rest_framework
from rest_framework import serializers
from varname import nameof
# import model from models.py
from .models import *

# Create a model serializer


class user_registerSerilizer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    class Meta:
        model = user
        # fields = '__all__'
        fields = ("id", nameof(user.full_name),
                  nameof(user.phone_number),
                  nameof(user.address),
                  nameof(user.gender),
                  nameof(user.email),
                  nameof(user.id_num),
                  nameof(user.image),
                  )


class imageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = (
            nameof(Image.image),
            # nameof(Image.name)
        )
