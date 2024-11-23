from django.contrib import admin
from .models import Room, Customer, Reservation

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_number", "room_type", "price", "is_available")
    search_fields = ("room_number", "room_type")
    list_filter = ("is_available", )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone_number")
    search_fields = ("first_name", "last_name", "email")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("room", "customer", "check_in", "check_out", "status", "created_at")
    list_filter = ("status", "check_in", "check_out")
    search_fields = ("customer__first_name", "customer__last_name")
    date_hierarchy = "check_in"  # for filtering by date
