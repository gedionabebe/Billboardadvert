from django.contrib import admin
from .models import Billboard
from .models import Rent
from .models import Advertisement
from .models import Request


admin.site.register(Billboard)
admin.site.register(Rent)
admin.site.register(Advertisement)
admin.site.register(Request)
# Register your models here.
