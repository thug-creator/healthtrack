from django.contrib import admin
from .models import Measurement, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_systolic_min', 'target_systolic_max')

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'systolic', 'diastolic', 'pulse', 'is_normal')
    list_filter = ('timestamp',)
    search_fields = ('user__username',)