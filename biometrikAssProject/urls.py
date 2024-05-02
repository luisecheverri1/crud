
from django.contrib import admin
from django.urls import path, include
from reconfacial1.views import MyLoginView, admin_view, home, login_view
from reconfacial1.views import ProfileView 
urlpatterns = [
     # Login
    path('login/', MyLoginView.as_view(template_name='home.html'), name='login'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Add this line for the root URL
    path('reconfacial1/', include('reconfacial1.urls')),
    path('administrador/', admin_view, name='administrador'),
    path('login/', login_view, name='login'),
]
