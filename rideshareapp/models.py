from django.db import models

# Create your models here.
import uuid
import os
from .auth import generate_access_token
# Create your models here.

# token database


class token(models.Model):
    user_id = models.IntegerField(null=True, default=None)
    token = models.CharField(
        max_length=256, unique=True, null=True, default=None)
    expire_on = models.DateTimeField(null=True, default=None)


# user database

class user(models.Model):
    full_name = models.CharField(
        max_length=256, null=False)
    email = models.EmailField(
        max_length=70, blank=True, default=None, null=False, unique=True)
    phone_number = models.CharField(
        max_length=256, null=False, default=None, unique=True)
    password = models.CharField(max_length=256,  null=False)

    created_on = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.IntegerField(null=True, default=None)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.IntegerField(null=True, default=None)
    is_deleted = models.BooleanField(null=True, default=False)
    is_verfied = models.BooleanField(null=True, default=False)
    deleted_on = models.DateTimeField(auto_now_add=True, null=True)
    deleted_by = models.IntegerField(null=True, default=None)
    image = models.CharField(max_length=256,  null=True, default='')
    otp = models.CharField(max_length=256,  null=True, default='')

    def __str__(self):
        return self.full_name

    def getlogininfo(self):

        return {
            "access_token": generate_access_token(self)
        }


#  image upload database


def nameFile(instance, filename):
    imgname = str(uuid.uuid4().hex)
    filename, file_extension = os.path.splitext(str(filename))
    return imgname+file_extension
    # return '/'.join(['images', imgname+file_extension])


class Image(models.Model):
    image = models.ImageField(verbose_name=u"file_uploaded",
                              upload_to=nameFile, null=False, blank=True, default=None)
    name = models.CharField(
        max_length=256, null=True, default=None)
