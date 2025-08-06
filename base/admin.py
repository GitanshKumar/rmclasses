from django.contrib import admin

from .models import Course, Review, Standard, Registration
# Register your models here.
admin.site.register([Course, Review, Standard, Registration])