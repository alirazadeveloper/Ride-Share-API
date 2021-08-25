from rest_framework.parsers import MultiPartParser
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from .serializers import *
from .models import *
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from .jsonresponse import sentresponse
from .otpwork import otpgen
from rest_framework.permissions import AllowAny
import os
from urllib.parse import urlparse


class Needtoken(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'status': 'false', 'message': 'unauthorized', 'data': ''}
    default_code = 'not_authenticated'


class tokenexp(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'status': 'false',
                      'message': 'session token is expired', 'data': ''}
    default_code = 'not_authenticated'


class Is_User(BasePermission):
    def has_permission(self, request, view):
        try:
            request.headers["Authorization"]
        except Exception as e:
            raise Needtoken()
        if not request.headers["Authorization"]:
            raise Needtoken()
        auth_token = request.headers["Authorization"]
        global auth_user
        auth_user = token.objects.filter(token=auth_token)
        if len(auth_user) > 0:
            if auth_user[0].expire_on > timezone.now():
                return True
            else:
                raise tokenexp()
        else:
            raise Needtoken()

# user register view


class userregister(viewsets.ModelViewSet):
    http_method_names = ['post']
    permission_classes = [AllowAny, ]
    queryset = user.objects.all()
    serializer_class = user_registerSerilizer

    def create(self, request):
        try:
            User_registerdata = JSONParser().parse(request)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())

        try:
            Phone_number = user.objects.filter(
                phone_number=User_registerdata["phone_number"]
            )
        except Exception as e:
            return Response(sentresponse("false", "invalid key", "").response())

        if len(Phone_number) > 0:
            if Phone_number[0].is_verfied == True:
                return Response(sentresponse("false", "user already registered", "").response())
            return Response(sentresponse("false", "phone number already registered", "").response())

        try:
            Email = user.objects.filter(
                email=User_registerdata["email"]
            )
        except Exception as e:
            return Response(sentresponse("false", "invalid key", "").response())
        if len(Email) > 0:
            return Response(sentresponse("false", "email already registered", "").response())

        try:
            Id_num = user.objects.filter(
                id_num=User_registerdata["id_num"]
            )
        except Exception as e:
            return Response(sentresponse("false", "invalid key", "").response())

        if len(Id_num) > 0:
            return Response(sentresponse("false", "id num already registered", "").response())

        try:
            User_registerserializer = user_registerSerilizer(
                data=User_registerdata)
            if User_registerserializer.is_valid():
                otp = otpgen()
                User_registerserializer.save(otp=otp)
                User = user.objects.filter(
                    email=User_registerdata["email"])
                return Response(sentresponse("true", "please verify otp", {
                    "email": User[0].email,
                    "otp": f"{otp}"
                }).response())
            else:
                return Response(sentresponse("false", User_registerserializer.error_messages, "").response())
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())

# file upload views


class upload_image(viewsets.ModelViewSet):
    http_method_names = ['post']
    permission_classes = [AllowAny, ]
    queryset = Image.objects.all()
    parser_classes = [MultiPartParser, ]
    permission_classes = [AllowAny, ]
    serializer_class = imageSerializer

    def create(self, request):
        try:
            file = request.FILES.get('file_uploaded')
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        file_serializer = imageSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            if not file_serializer.data['image']:
                return Response(sentresponse("false", "file not provided", "").response())
            img_name = os.path.basename(
                urlparse(file_serializer.data['image']).path)
            return Response(sentresponse("true", "file uploaded", {
                "name": img_name,
                "image": "http://"+str(request.get_host())+str(file_serializer.data['image'])
            }).response())
        else:
            return Response(sentresponse("false", file_serializer.error_messages, "").response())
