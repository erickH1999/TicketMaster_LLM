"""
URL configuration for TicketMaster_LLM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from TicketMaster import views
from TicketMaster.views import chat_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.results, name="results"),
    path("", views.get_events, name="get_events"),
    path('view_favorites/', views.view_fav, name='view_favorites'),
    path('update/<int:event_id>', views.update_fav, name='delete_fav'),
    path('delete_fav/', views.delete_fav, name='delete_fav'),
    path('createfav/', views.create_fav, name='create_fav'),
    path('chat/', chat_view, name='chat_view'),
]
