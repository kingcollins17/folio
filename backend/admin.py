from django.contrib import admin
from .models import ProfileInfo, SocialAccount

# Register your models here.
admin.site.register(ProfileInfo)
admin.site.register(SocialAccount)
