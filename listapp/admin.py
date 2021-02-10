from django.contrib import admin
from .models import Task
from .models import Tag
from .models import CustomUser


admin.site.register(CustomUser)
admin.site.register(Task)
admin.site.register(Tag)
