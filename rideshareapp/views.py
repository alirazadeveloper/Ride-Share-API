import io
from django.db.models.fields import CharField, URLField
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import MultiPartParser,FileUploadParser,FormParser
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
from .FCMchat import sendPush


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
        if not str(request.headers["Authorization"]).strip():
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
            Phone_number = self.queryset.filter(
                phone_number=User_registerdata["phone_number"]
            )
        except Exception as e:
            return Response(sentresponse("false", "invalid key", "").response())
        if len(Phone_number) > 0:
            return Response(sentresponse("false", "phone number already registered", "").response())
        try:
            Email = self.queryset.filter(
                email=User_registerdata["email"]
            )
        except Exception as e:
            return Response(sentresponse("false", "invalid key", "").response())
        if len(Email) > 0:
            return Response(sentresponse("false", "email already registered", "").response())
        try:
            User_registerserializer = self.serializer_class(
                data=User_registerdata)
            if User_registerserializer.is_valid():
                otp = otpgen()
                User_registerserializer.save(otp=otp)
                # to = User_registerdata["phone_number"]
                # sentotp(to, otp)
                return Response(sentresponse("true", "please verify otp", {
                    "phone_number": User_registerdata["phone_number"],
                    "otp": f"{otp}"
                }).response())
            else:
                return Response(sentresponse("false", User_registerserializer.error_messages, "").response())
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())

# file upload views


class upload_file(viewsets.ModelViewSet):
    http_method_names = ['post']
    permission_classes = [AllowAny, ]
    queryset = fileupload.objects.all()
    parser_classes = [MultiPartParser,FileUploadParser,FormParser,]
    permission_classes = [AllowAny, ]
    serializer_class = fileSerializer

    def create(self, request):
        try:
            file = request.FILES.get('file_uploaded')
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        try:
            file_serializer = self.serializer_class(data=request.data)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        # try:
        if file_serializer.is_valid():
            file_serializer.save()
            if not file_serializer.data['filefield']:
                return Response(sentresponse("false", "file not provided", "").response())
            file_name = os.path.basename(
                urlparse(file_serializer.data['filefield']).path)
            return Response(sentresponse("true", "file uploaded", {
                "name": file_name,
                "file": "http://"+str(request.get_host())+str(file_serializer.data['filefield'])
            }).response())
        else:
            return Response(sentresponse("false", file_serializer.error_messages, "").response())
        # except Exception as e:
        #             return Response(sentresponse("false", "file size limit exceeded", "").response())    

# verify otp views


class verifyotp(viewsets.ModelViewSet):
    http_method_names = ['post']
    permission_classes = [AllowAny, ]
    queryset = user.objects.all()
    serializer_class = verifyotpSerilizer

    def create(self, request):
        try:
            User_registerdata = JSONParser().parse(request)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        User = self.queryset.filter(
            phone_number=User_registerdata["phone_number"])
        if len(User) > 0:
            if User[0].is_verfied == True:
                return Response(sentresponse("false", "user already verified", "").response())
            if str(User[0].otp) == str(User_registerdata['otp']):
                User[0].is_verfied = True
                User[0].save()
                return Response(sentresponse("true", "user registered successfully", "").response())
            else:
                return Response(sentresponse("false", "invalid otp", "").response())
        else:
            return Response(sentresponse("false", "invalid phone number", "").response())


# re-sent otp views


class resentotp(viewsets.ModelViewSet):
    http_method_names = ['post']
    permission_classes = [AllowAny, ]
    queryset = user.objects.all()
    serializer_class = resentotpSerilizer

    def create(self, request):
        try:
            resentotp_data = JSONParser().parse(request)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        try:
            User = self.queryset.filter(
                phone_number=resentotp_data['phone_number']
            )
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        if len(User) > 0:
            otp = otpgen()
            User[0].otp = otp
            User[0].save()
            # to = User[0].phone_number
            # sentotp(to, otp)
            return Response(sentresponse("true", "success", {
                "otp": f"{otp}"
            }).response())
        else:
            return Response(sentresponse("false", "invalid phone number", "").response())


# login views


class login(viewsets.ModelViewSet):
    http_method_names = ['post']
    permission_classes = [AllowAny, ]
    queryset = user.objects.all()
    serializer_class = loginSerilizer

    def create(self, request):
        try:
            User_logindata = JSONParser().parse(request)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())

        User = self.queryset.filter(
            email=User_logindata["email"])
        if len(User) == 0:
            return Response(sentresponse("false", "invalid email", "").response())
        Password = self.queryset.filter(
            password=User_logindata["password"])

        if len(Password) == 0:
            return Response(sentresponse("false", "invalid password", "").response())
        auth_token, exp = generate_access_token(User[0])
        if not str(User_logindata["fcm"]).strip():
            return Response(sentresponse("false", "invalid fcm", "").response())
        
        User[0].fcm = User_logindata["fcm"]
        User[0].save()
        try:
            token.objects.create(
                user_id=User[0].id, token=auth_token, expire_on=exp)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())

        return Response({
            "status": "true",
            "message": "login successfully",
            'data': {
                "access_token": auth_token
            }
        })

# forget password views


class forgetpassword(viewsets.ModelViewSet):
    http_method_names = ['post']
    permission_classes = [Is_User, ]
    queryset = user.objects.all()
    serializer_class = forgetpassSerilizer

    def create(self, request):
        try:
            passwordreset_data = JSONParser().parse(request)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        try:
            User = self.queryset.filter(
                phone_number=passwordreset_data['phone_number']
            )
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        if len(User) > 0:
            # to = User[0].phone_number
            # sentotp(to, otp)
            User[0].password = passwordreset_data['new_password']
            User[0].save()
            return Response(sentresponse("true", "password updated", "").response())
        else:
            return Response(sentresponse("false", "invalid phone number", "").response())


# user get by id views


class usergetbyid(viewsets.ModelViewSet):
    http_method_names = ['get']
    permission_classes = [Is_User, ]
    queryset = user.objects.all()
    serializer_class = user_getSerilizer

    def list(self, request):
        User = self.queryset.filter(is_deleted=False)
        page = self.paginate_queryset(User)
        serializer = self.serializer_class(page, many=True)
        data = JSONRenderer().render(serializer.data)
        data = JSONParser().parse(io.BytesIO(data))
        res_list = []
        for res in data:
            if res["image"]:
                res["image"] = "http://" +\
                    str(request.get_host())+"/media/"+str(res["image"])
                res_list.append(res)
            else:
                res["image"] = ""
                res_list.append(res)
        return Response(sentresponse("true", "success", res_list).response())

    def retrieve(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
        except:
            return Response(sentresponse("false", "invalid id", "").response())
        if user.is_deleted == True:
            return Response(sentresponse("false", "invalid id", "").response())
        serializer = self.serializer_class(user)
        data = JSONRenderer().render(serializer.data)
        data = JSONParser().parse(io.BytesIO(data))
        if data["image"]:
            data["image"] = "http://" +\
                str(request.get_host())+"/media/"+data["image"]
        else:
            data["image"] = ""
        return Response(sentresponse("true", "success", data).response())


# update user profile view


class updateprofile(viewsets.ModelViewSet):
    http_method_names = ['put']
    permission_classes = [Is_User, ]
    queryset = user.objects.all()
    serializer_class = user_getSerilizer

    def update(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
        except:
            return Response(sentresponse("false", "invalid id", "").response())
        if user.is_deleted == True:
            return Response(sentresponse("false", "invalid id", "").response())
        try:
            User_registerdata = JSONParser().parse(request)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        try:
            User_registerserializer = self.serializer_class(user,
                                                            data=User_registerdata, partial=True)
            if User_registerserializer.is_valid():
                User_registerserializer.save()
                return Response(sentresponse("true", "profile updated successfully", "").response())
            else:
                return Response(sentresponse("false", User_registerserializer.error_messages, "").response())
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())


# delete user by id view

class deletebyid(viewsets.ModelViewSet):
    http_method_names = ['delete']
    permission_classes = [Is_User, ]
    queryset = user.objects.all()
    serializer_class = user_getSerilizer

    def destroy(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
        except:
            return Response(sentresponse("false", "invalid id", "").response())
        if user.is_deleted == True:
            return Response(sentresponse("false", "invalid id", "").response())
        else:
            user.is_deleted = True
            user.save()
        return Response(sentresponse("true", "user deleted successfully", "").response())


# car api view


class addcar(viewsets.ModelViewSet):
    http_method_names = ['post']
    permission_classes = [Is_User, ]
    queryset = car.objects.all()
    serializer_class = carSerilizer

    def create(self, request):
        try:
            car_data = JSONParser().parse(request)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        try:
            car_serializer = self.serializer_class(data=car_data)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        if car_serializer.is_valid():
            car_serializer.save()
            return Response(sentresponse("true", "car added successfully", "").response())
        else:
            return Response(sentresponse("false", car_serializer.error_messages, "").response())
        
# update car api view


class updatecar(viewsets.ModelViewSet):
    http_method_names = ['put']
    permission_classes = [Is_User, ]
    queryset = car.objects.all()
    serializer_class = updatecarSerilizer
    

    def update(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
        except:
            return Response(sentresponse("false", "invalid id", "").response())
        try:
            car_data = JSONParser().parse(request)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        try:
            car_serializer = self.serializer_class(user,data=car_data, partial=True)
            if car_serializer.is_valid():
                car_serializer.save()
                return Response(sentresponse("true", "car updated successfully", "").response())
            else:
                return Response(sentresponse("false", car_serializer.error_messages, "").response())
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())

# add trip view

class addtrip(viewsets.ModelViewSet):
    http_method_names = ['post']
    permission_classes = [Is_User, ]
    queryset = trip.objects.all()
    serializer_class = tripSerilizer

    def create(self, request):
        try:
            trip_data = JSONParser().parse(request)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        try:
            trip_serializer = self.serializer_class(data=trip_data)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        try:
            if trip_serializer.is_valid():
                trip_serializer.save()
                return Response(sentresponse("true", "trip added successfully", "").response())
            else:
                return Response(sentresponse("false", trip_serializer.error_messages, "").response())
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())

# get all trip

class gettrip(viewsets.ModelViewSet):
    http_method_names = ['get']
    permission_classes = [Is_User, ]
    queryset = trip.objects.all()
    serializer_class = gettripSerilizer

    def list(self, request):
        trip_data = self.queryset.filter(is_deleted=False).order_by("-created_on")
        page = self.paginate_queryset(trip_data)
        trip_serializer = self.serializer_class(page, many=True)
        return Response(sentresponse("true", "success", trip_serializer.data).response())
    
    def retrieve(self, request, pk=None):
        try:
            trip_data = self.queryset.get(pk=pk)
        except:
            return Response(sentresponse("false", "invalid id", "").response())
        if trip_data.is_deleted == True:
            return Response(sentresponse("false", "invalid id", "").response())
        trip_serializer = self.serializer_class(trip_data)
        return Response(sentresponse("true", "success",trip_serializer.data).response())

# feedback view

class feedback(viewsets.ModelViewSet):
    http_method_names = ['post','get']
    permission_classes = [Is_User, ]
    queryset = feedback.objects.all()
    serializer_class = feedbackSerilizer
    
    def create(self, request):
        try:
            feedback_data = JSONParser().parse(request)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        try:
            feedback_serializer = self.serializer_class(data=feedback_data)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        if feedback_serializer.is_valid():
            feedback_serializer.save()
            return Response(sentresponse("true", "feedback submit successfully", "").response())
        else:
            return Response(sentresponse("false", feedback_serializer.error_messages, "").response())
        
    def retrieve(self, request, pk=None,*args, **kwargs):
        try:
            feedback_data = self.queryset.get(pk=pk)
        except:
            return Response(sentresponse("false", "invalid id", "").response())
        feedback_serializer = self.serializer_class(feedback_data)
        return Response(sentresponse("true", "success",feedback_serializer.data).response())
    
    def list(self, request):
        feedback_data = self.queryset.all()
        page = self.paginate_queryset(feedback_data)
        feedback_serializer = self.serializer_class(page, many=True)
        return Response(sentresponse("true", "success", feedback_serializer.data).response())


# chat view

class sendmessage(viewsets.ModelViewSet):
    """
    Chat Documentation
    ---
        type field must enum
        - text message : 1
          voice message : 2
          image message : 3
          video message : 4
          other file message : 5
    
    """
    http_method_names = ['post']
    permission_classes = [Is_User, ]
    queryset = chat.objects.all()
    serializer_class = chatSerilizer

    def create(self, request):
        try:
            message_data = JSONParser().parse(request)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        if str(message_data['type'])=='1':
            User = user.objects.filter(pk=int(message_data['receiverid']))
            try:
                sendPush("RideShare",str(message_data['message']),registration_token=str(User[0].fcm))
            except Exception as e:
                return Response(sentresponse("false", e.args[0], "").response())
            try:
                message_serializer = self.serializer_class(data=message_data)
            except Exception as e:
                return Response(sentresponse("false", e.args[0], "").response())
            if message_serializer.is_valid():
                message_serializer.save()
                return Response(sentresponse("true", "message sent successfully", "").response())
            else:
                return Response(sentresponse("false", message_serializer.error_messages, "").response())
        elif str(message_data['type'])=='2':
            return Response(sentresponse("true", "message sent successfully", "").response())
        else:
            return Response(sentresponse("false", "invalid type", "").response())
        

# update fcm token
class updatefcm(viewsets.ModelViewSet):
    http_method_names = ['put']
    permission_classes = [Is_User, ]
    queryset = user.objects.all()
    serializer_class = updatefcmSerilizer
    
    def update(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
        except:
            return Response(sentresponse("false", "invalid id", "").response())
        try:
            fcm_data = JSONParser().parse(request)
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())
        try:
            fcm_serializer = self.serializer_class(user,data=fcm_data, partial=True)
            if fcm_serializer.is_valid():
                fcm_serializer.save()
                return Response(sentresponse("true", "fcm updated successfully", "").response())
            else:
                return Response(sentresponse("false", fcm_serializer.error_messages, "").response())
        except Exception as e:
            return Response(sentresponse("false", e.args[0], "").response())




