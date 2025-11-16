from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Plan)
admin.site.register(Feature)
admin.site.register(UserSubscription)
