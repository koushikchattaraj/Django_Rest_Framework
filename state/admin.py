from django.contrib import admin
from django.db import models
from state.models import State

# admin.site.register(State)
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['id','name']


