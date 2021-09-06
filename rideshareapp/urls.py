# basic URL Configurations
from django.urls import include, path
# import routers
from rest_framework import routers

# import everything from views
from .views import *

# define the router
router = routers.SimpleRouter()

# define the router path and viewset to be used
router.register(r'resentotp', resentotp)
router.register(r'verifyotp', verifyotp)
router.register(r'signup', userregister)
router.register(r'fileupload', upload_file)
router.register(r'login', login)
router.register(r'forgetpassword', forgetpassword)
router.register(r'getuser', usergetbyid)
router.register(r'updateprofile', updateprofile)
router.register(r'deletebyid', deletebyid)
router.register(r'addcar', addcar)
router.register(r'updatecar', updatecar)
router.register(r'addtrip', addtrip)
router.register(r'gettrip', gettrip)
router.register(r'feedback', feedback)

# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
]
