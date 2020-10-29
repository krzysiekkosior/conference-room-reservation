from django.shortcuts import render, redirect
from django.views import View
from .models import Room, Reservation
from datetime import datetime


def main_page(request):
    return render(request, 'main.html')


class AddRoom(View):
    def get(self, request):
        return render(request, 'add_room.html')

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        if request.POST.get('projector'):
            projector = True
        else:
            projector = False
        if name == "":
            return render(request, 'add_room.html', {'message': 'Enter room name.'})
        if Room.objects.filter(name=name).count() != 0:
            return render(request, 'add_room.html', {'message': 'Room already exists!'})
        Room.objects.create(name=name, capacity=capacity, projector=projector)
        return redirect('menu')


class ListRoom(View):
    def get(self, request):
        rooms = Room.objects.all().order_by('id')
        if Room.objects.all().count() == 0:
            response = 'No room avaible!'
            context = {'no_room': response}
            return render(request, 'list_room.html', context)
        context = {'rooms': rooms}
        return render(request, 'list_room.html', context)


class DeleteRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        room.delete()
        return redirect('room-list')


def modify_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == 'GET':
        return render(request, 'modify_room.html', {'room': room})
    else:
        mod_name = request.POST.get('name')
        mod_capacity = request.POST.get('capacity')
        if request.POST.get('projector'):
            mod_projector = True
        else:
            mod_projector = False
        if mod_name == "":
            return render(request, 'modify_room.html', {'room': room,
                                                        'message': 'Enter room name.'})
        if room.name != mod_name and Room.objects.filter(name=mod_name).count() != 0:
            return render(request, 'modify_room.html', {'room': room,
                                                        'message': 'Room with this name '
                                                                   'already exists!'})
        room.name = mod_name
        room.capacity = int(mod_capacity)
        room.projector = mod_projector
        room.save()
        return redirect('room-list')


def reserve_room(request, room_id):
    room = Room.objects.get(id=room_id)
    reservations = Reservation.objects.filter(room_id=room_id).order_by('date')

    if request.method == 'GET':
        return render(request, 'reserve_room.html', {'room': room,
                                                     'reservations': reservations})
    else:
        comment = request.POST.get('comment')
        str_date = request.POST.get('date')
        date = datetime.strptime(str_date, '%Y-%m-%d')
        now = datetime.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if date < today:
            return render(request, 'reserve_room.html', {'room': room,
                                                         'reservations': reservations,
                                                         'message': "Date is in the past."})
        try:
            Reservation.objects.create(date=date, room=room, comment=comment)
        except:
            return render(request, 'reserve_room.html', {'room': room,
                                                         'reservations': reservations,
                                                         'message': "Already reserved"})
        return redirect('room-list')


def room_details(request, room_id):
    room = Room.objects.get(id=room_id)
    reservations = Reservation.objects.filter(room_id=room_id).order_by('date')
    context = {'room': room,
               'reservations': reservations}
    if request.method == 'GET':
        return render(request, 'room_details.html', context)
