from django.shortcuts import render, redirect, get_object_or_404

from lavup.models.fabricante import Fabricante
from lavup.models.tamanho import Tamanho
from lavup.models.veiculo import Veiculo


def agenda(request):
    """Página de agendamentos."""
    return render(request, 'agenda.html')


def clientes(request):
    """Página de clientes."""
    return render(request, 'clientes.html')


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


def usuarios(request):
    """Página de usuários."""
    return render(request, 'usuarios.html')


def configuracoes(request):
    """Página de configurações."""
    return render(request, 'configuracoes.html')
