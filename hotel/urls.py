from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.customer_register, name="customer_register"),
    path("list/", views.room_list, name="room_list"),
    path("view-rooms/", views.view_rooms, name="view_rooms"),
    path("book/<int:room_id>/", views.book_room, name="book_room"),
    # path('all/',  views.AllRooms.as_view())
    path("create-room/", views.create_room, name="create_room"),
    path("customers/", views.list_customers, name="list_customers"),
    path('charts/', views.chart_view, name='charts'),
]
