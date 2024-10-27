# C:\Users\Admin\connect_website\collaborate\admin.py
from django.contrib import admin
from .models import Idea, UserProfile
from .models import IndividualProfile, BusinessProfile

admin.site.register(IndividualProfile)
admin.site.register(BusinessProfile)


# Register models for admin panel access
admin.site.register(Idea)
admin.site.register(UserProfile)
