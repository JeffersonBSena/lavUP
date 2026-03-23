from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required

from lavup.views.auth import login_identify, login_verify, logout_view, dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('', login_identify, name='login'),
    path('login/', login_identify, name='login_identify'),
    path('login/verificar/', login_verify, name='login_verify'),
    path('logout/', logout_view, name='logout'),

    # App
    path('dashboard/', login_required(dashboard, login_url='login'), name='dashboard'),
]
