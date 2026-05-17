from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required

from lavup.views.auth import login_identify, login_verify, logout_view, dashboard
from lavup.views.lavador import (
    main as lavador_main,
    agenda_iniciar, agenda_reagendar, agenda_transferir, agenda_cancelar, agenda_concluir,
)
from lavup.views.crud import (
    agenda, agenda_criar, agenda_editar, agenda_deletar,
    clientes, cliente_criar, cliente_editar, cliente_deletar,
    veiculos, veiculo_criar, veiculo_editar, veiculo_deletar,
    servicos, servico_criar, servico_editar, servico_deletar,
    usuarios, usuario_criar, usuario_editar, usuario_deletar,
    ordens, os_criar, os_editar, os_deletar,
    configuracoes
)

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
    path('agenda/criar/', login_required(agenda_criar, login_url='login'), name='agenda_criar'),
    path('agenda/<int:pk>/editar/', login_required(agenda_editar, login_url='login'), name='agenda_editar'),
    path('agenda/<int:pk>/deletar/', login_required(agenda_deletar, login_url='login'), name='agenda_deletar'),
    
    path('clientes/', login_required(clientes, login_url='login'), name='clientes'),
    path('clientes/criar/', login_required(cliente_criar, login_url='login'), name='cliente_criar'),
    path('clientes/<int:pk>/editar/', login_required(cliente_editar, login_url='login'), name='cliente_editar'),
    path('clientes/<int:pk>/deletar/', login_required(cliente_deletar, login_url='login'), name='cliente_deletar'),
    
    path('veiculos/', login_required(veiculos, login_url='login'), name='veiculos'),
    path('veiculos/criar/', login_required(veiculo_criar, login_url='login'), name='veiculo_criar'),
    path('veiculos/<int:pk>/editar/', login_required(veiculo_editar, login_url='login'), name='veiculo_editar'),
    path('veiculos/<int:pk>/deletar/', login_required(veiculo_deletar, login_url='login'), name='veiculo_deletar'),
    
    path('servicos/', login_required(servicos, login_url='login'), name='servicos'),
    path('servicos/criar/', login_required(servico_criar, login_url='login'), name='servico_criar'),
    path('servicos/<int:pk>/editar/', login_required(servico_editar, login_url='login'), name='servico_editar'),
    path('servicos/<int:pk>/deletar/', login_required(servico_deletar, login_url='login'), name='servico_deletar'),
    
    path('usuarios/', login_required(usuarios, login_url='login'), name='usuarios'),
    path('usuarios/criar/', login_required(usuario_criar, login_url='login'), name='usuario_criar'),
    path('usuarios/<int:pk>/editar/', login_required(usuario_editar, login_url='login'), name='usuario_editar'),
    path('usuarios/<int:pk>/deletar/', login_required(usuario_deletar, login_url='login'), name='usuario_deletar'),
    
    path('os/', login_required(ordens, login_url='login'), name='ordens'),
    path('os/criar/', login_required(os_criar, login_url='login'), name='os_criar'),
    path('os/<int:pk>/editar/', login_required(os_editar, login_url='login'), name='os_editar'),
    path('os/<int:pk>/deletar/', login_required(os_deletar, login_url='login'), name='os_deletar'),

    path('lavador/', login_required(lavador_main, login_url='login'), name='lavador_main'),
    path('lavador/agenda/<int:pk>/iniciar/', login_required(agenda_iniciar, login_url='login'), name='agenda_iniciar'),
    path('lavador/agenda/<int:pk>/reagendar/', login_required(agenda_reagendar, login_url='login'), name='agenda_reagendar'),
    path('lavador/agenda/<int:pk>/transferir/', login_required(agenda_transferir, login_url='login'), name='agenda_transferir'),
    path('lavador/agenda/<int:pk>/cancelar/', login_required(agenda_cancelar, login_url='login'), name='agenda_cancelar'),
    path('lavador/agenda/<int:pk>/concluir/', login_required(agenda_concluir, login_url='login'), name='agenda_concluir'),

    path('configuracoes/', login_required(configuracoes, login_url='login'), name='configuracoes'),
]
