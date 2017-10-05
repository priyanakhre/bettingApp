from django.contrib import admin

from .models import User
from .models import Bet
from .models import Response

# Register your models here.
admin.site.register(User)
admin.site.register(Bet)
admin.site.register(Response)