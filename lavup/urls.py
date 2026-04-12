from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required

from lavup.views.auth import login_identify, login_verify, logout_view, dashboard
from lavup.views.crud import agenda, clientes, veiculos, veiculo_criar, veiculo_editar, veiculo_deletar, servicos, usuarios, configuracoes

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('', login_identify, name='login'),
    path('login/', login_identify, name='login_identify'),
    path('login/verificar/', login_verify, name='login_verify'),
    path('logout/', logout_view, name='logout'),

    # App
    path('dashboard/', login_required(dashboard, login_url='login'), name='dashboard'),
    path('agenda/', login_required(agenda, login_url='login'), name='agenda'),
    path('clientes/', login_required(clientes, login_url='login'), name='clientes'),
    path('veiculos/', login_required(veiculos, login_url='login'), name='veiculos'),
    path('veiculos/criar/', login_required(veiculo_criar, login_url='login'), name='veiculo_criar'),
    path('veiculos/<int:pk>/editar/', login_required(veiculo_editar, login_url='login'), name='veiculo_editar'),
    path('veiculos/<int:pk>/deletar/', login_required(veiculo_deletar, login_url='login'), name='veiculo_deletar'),
    path('servicos/', login_required(servicos, login_url='login'), name='servicos'),
    path('usuarios/', login_required(usuarios, login_url='login'), name='usuarios'),
    path('configuracoes/', login_required(configuracoes, login_url='login'), name='configuracoes'),
]
