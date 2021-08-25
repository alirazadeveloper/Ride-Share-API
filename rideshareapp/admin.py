from django.contrib import admin
from .models import *
admin.site.site_header = "RideShare Admin"
# Register your models here.


class RideshareappAdmin(admin.ModelAdmin):
    search_fields = ['full_name']


admin.site.register(
    user, RideshareappAdmin
)
admin.site.register(
    token
)
admin.site.register(
    Image
)
