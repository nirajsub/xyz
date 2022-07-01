from django.contrib import admin

from .models import *

admin.site.register(MainUser)
admin.site.register(Privilage)

admin.site.register(CustomerUser)
admin.site.register(CustomerHotelRegister)
admin.site.register(CustomerRecord)