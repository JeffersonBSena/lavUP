from django.shortcuts import render, redirect, get_object_or_404

from lavup.models.fabricante import Fabricante
from lavup.models.tamanho import Tamanho
from lavup.models.veiculo import Veiculo


def agenda(request):
    """Página de agendamentos."""
    return render(request, 'agenda.html')


def agenda_criar(request):
    return redirect('agenda')


def agenda_editar(request, pk):
    return redirect('agenda')


def agenda_deletar(request, pk):
    return redirect('agenda')


def clientes(request):
    """Página de clientes."""
    return render(request, 'clientes.html')


def cliente_criar(request):
    return redirect('clientes')


def cliente_editar(request, pk):
    return redirect('clientes')


def cliente_deletar(request, pk):
    return redirect('clientes')


def veiculos(request):
    """Página de veículos."""
    context = {
        'veiculos': Veiculo.objects.select_related('fabricante', 'tamanho').all(),
        'fabricantes': Fabricante.objects.all(),
        'tamanhos': Tamanho.objects.all(),
    }
    return render(request, 'veiculos.html', context)


def veiculo_criar(request):
    """Cria um novo veículo."""
    if request.method == 'POST':
        Veiculo.objects.create(
            fabricante_id=request.POST['fabricante'],
            modelo=request.POST['modelo'],
            tamanho_id=request.POST['tamanho'],
        )
    return redirect('veiculos')


def veiculo_editar(request, pk):
    """Edita um veículo existente."""
    veiculo = get_object_or_404(Veiculo, pk=pk)
    if request.method == 'POST':
        veiculo.fabricante_id = request.POST['fabricante']
        veiculo.modelo = request.POST['modelo']
        veiculo.tamanho_id = request.POST['tamanho']
        veiculo.save()
    return redirect('veiculos')


def veiculo_deletar(request, pk):
    """Deleta um veículo."""
    veiculo = get_object_or_404(Veiculo, pk=pk)
    if request.method == 'POST':
        veiculo.delete()
    return redirect('veiculos')


def servicos(request):
    """Página de serviços."""
    return render(request, 'servicos.html')


def servico_criar(request):
    return redirect('servicos')


def servico_editar(request, pk):
    return redirect('servicos')


def servico_deletar(request, pk):
    return redirect('servicos')


def usuarios(request):
    """Página de usuários."""
    return render(request, 'usuarios.html')


def usuario_criar(request):
    return redirect('usuarios')


def usuario_editar(request, pk):
    return redirect('usuarios')


def usuario_deletar(request, pk):
    return redirect('usuarios')


def configuracoes(request):
    """Página de configurações."""
    return render(request, 'configuracoes.html')
