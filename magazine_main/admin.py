from django.contrib import admin

from .models import Item, Borrowed

admin.site.register(Item)
admin.site.register(Borrowed)
