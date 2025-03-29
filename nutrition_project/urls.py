from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Nutrition API project!")

urlpatterns = [
    path('', home),  # Home view for the empty path
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
