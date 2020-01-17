from django.contrib import admin
from .models import Airport, Flight, Passenger

# Register your models here.

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('city', 'code',)

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'duration')

admin.site.register(Passenger)