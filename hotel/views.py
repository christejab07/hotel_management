from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Room, Reservation, Customer
from .forms import ReservationForm, CustomerForm, RoomForm
from django.utils.timezone import now


def index(request):
    return render(request, "hotel/index.html")


def view_rooms(request):
    reservations = Reservation.objects.filter(
        check_out__lt=now().date()
    )  # Convert now to date

    for reservation in reservations:
        reservation.room.is_available = True
        reservation.room.save()  # Mark rooms as available
        reservation.delete()  # Delete expired reservations

    # Fetch only available rooms
    rooms = Room.objects.filter(is_available=True)
    return render(request, "hotel/view_rooms.html", {"rooms": rooms})


def room_list(request):
    # Check for expired reservations and update room availability
    reserved = Reservation.objects.all()

    for reservation in reserved:
        if reservation.check_out < now().date():  # Convert now to date
            reservation.room.is_available = True
            reservation.room.save()  # Mark the room as available again
            reservation.delete()  # Remove expired reservation

    # After handling expired reservations, fetch all current reservations
    reservations = Reservation.objects.all()

    return render(request, "hotel/reserved_list.html", {"reservations": reservations})


def customer_register(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/customers/")
    else:
        form = CustomerForm()
    return render(request, "hotel/customer.html", {"form": form})


def book_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data.get("check_in")
            check_out = form.cleaned_data.get("check_out")
            today = now().date()

            # Allow today's date for check-in but prevent past dates
            if check_in < today:
                form.add_error("check_in", "Check-in date cannot be in the past.")
            if check_out < today:
                form.add_error("check_out", "Check-out date cannot be in the past.")
            if check_out <= check_in:
                form.add_error("check_out", "Check-out date must be after Check-in date.")

            # Save reservation only if there are no errors
            if not form.errors:
                room.is_available = False
                room.save()
                reservation = form.save(commit=False)
                reservation.room = room
                reservation.save()
                return HttpResponseRedirect("/list")
    else:
        form = ReservationForm()
    return render(request, "hotel/book_room.html", {"form": form, "room": room})


def create_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                "/view-rooms"
            )  # Redirect to view rooms after creating
    else:
        form = RoomForm()

    return render(request, "hotel/create_room.html", {"form": form})


def list_customers(request):
    customers = Customer.objects.all()  # Query all customers
    return render(request, "hotel/list_customers.html", {"customers": customers})

def chart_view(request):
    rooms = Room.objects.all()
    room_labels = [room.room_number for room in rooms]
    reservations = [Reservation.objects.filter(room=room).count() for room in rooms]

    return render(request, 'hotel/charts.html', {
        'room_labels': room_labels,
        'reservations': reservations
    })