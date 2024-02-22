
from django.contrib import admin
from django.urls import path, include
from reconfacial1.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Add this line for the root URL
    path('reconfacial1/', include('reconfacial1.urls')),
]
