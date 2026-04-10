from django.shortcuts import render


def agenda(request):
    """Página de agendamentos."""
    return render(request, 'agenda.html')


def clientes(request):
    """Página de clientes."""
    return render(request, 'clientes.html')


def veiculos(request):
    """Página de veículos."""
    return render(request, 'veiculos.html')


def servicos(request):
    """Página de serviços."""
    return render(request, 'servicos.html')


def usuarios(request):
    """Página de usuários."""
    return render(request, 'usuarios.html')


def configuracoes(request):
    """Página de configurações."""
    return render(request, 'configuracoes.html')
