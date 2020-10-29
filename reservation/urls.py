"""reservation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django_workshop.views import (
    main_page, AddRoom, ListRoom, DeleteRoom, modify_room, reserve_room, room_details
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name="menu"),
    path('room/new/', AddRoom.as_view()),
    path('room/', ListRoom.as_view(), name="room-list"),
    path('room/delete/<int:room_id>/', DeleteRoom.as_view()),
    path('room/modify/<int:room_id>/', modify_room),
    path('room/reserve/<int:room_id>/', reserve_room),
    path('room/<int:room_id>/', room_details),

]
