# Guia de Construção de Templates e CRUD — LavUP

Este guia orienta o desenvolvedor na criação de novas páginas e na implementação das ações de botões CRUD (Create, Read, Update, Delete) seguindo o padrão estabelecido no projeto.

---

## 1. Estrutura Base do Template

Todas as novas páginas devem herdar de `base.html` para manter a consistência visual (Navbar, Sidebar e CSS).

### Exemplo de início de arquivo:
```html
{% extends 'base.html' %}

{% block title %}Nome do Módulo - {{ APP_NAME }}{% endblock %}

{% block extra_css %}
<!-- DataTables CSS se houver listagem -->
<link rel="stylesheet" href="https://cdn.datatables.net/1.13.8/css/dataTables.bootstrap5.min.css">
{% endblock %}

{% block content %}
<div class="mb-5">
    <h2 class="mb-4"><i class="bi bi-tag me-2"></i>Título do Módulo</h2>
    
    <!-- Botão de Inserir -->
    <div class="mb-3">
        <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#modalEntidade">Inserir</button>
    </div>

    <!-- Includes de Modais (Formulário e Deleção) -->
    {% include 'partials/form_entidade.html' %}
    {% include 'partials/modal_deletar.html' %}

    <!-- Tabela de Listagem -->
    <div class="table-responsive">
        <table id="tabela-entidade" class="table table-striped">
            <thead>
                <tr>
                    <th>Campo 1</th>
                    <th>Campo 2</th>
                    <th class="text-end">Ações</th>
                </tr>
            </thead>
            <tbody>
                {% for item in itens %}
                <tr>
                    <td>{{ item.campo1 }}</td>
                    <td>{{ item.campo2 }}</td>
                    <td class="text-end">
                        <!-- Botões de Ação -->
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
```

---

## 2. Implementando as Ações CRUD nos Botões

O projeto utiliza um padrão onde um único modal é reutilizado para **Inserir** e **Editar**, e um modal genérico para **Deletar**. A lógica é controlada por atributos `data-*` e JavaScript.

### A) Botão Inserir (Novo)
O botão de inserir apenas abre o modal. O JavaScript deve garantir que o formulário esteja limpo e com a URL de criação correta.
```html
<button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#modalEntidade">
    Inserir
</button>
```

### B) Botão Editar
O botão deve carregar todos os dados do objeto em atributos `data-`. O JavaScript usará esses valores para preencher o modal.
```html
<button class="btn btn-warning btn-sm btn-editar"
    data-id="{{ item.id }}"
    data-campo1="{{ item.campo1 }}"
    data-campo2="{{ item.campo2 }}"
    data-bs-toggle="modal"
    data-bs-target="#modalEntidade">
    Editar
</button>
```

### C) Botão Deletar
Utiliza o modal genérico `partials/modal_deletar.html`. Você só precisa passar a URL de exclusão e as informações de exibição.
```html
<button class="btn btn-danger btn-sm btn-deletar"
    data-url="/rota-para-deletar/{{ item.id }}/"
    data-entidade="o registro"
    data-nome="{{ item.campo1 }}"
    data-bs-toggle="modal"
    data-bs-target="#modalDeletar">
    Deletar
</button>
```

---

## 3. O JavaScript de Orquestração

No bloco `extra_js`, adicione o script que manipula as trocas de URLs e preenchimento de campos.

```javascript
{% block extra_js %}
<script src="https://code.jquery.com/jquery-3.7.1.slim.min.js"></script>
<!-- Scripts do DataTable se necessário -->

<script>
  $(document).ready(function () {
    var urlCriar = '{% url "nome_da_rota_criar" %}';

    // 1. Ação de INSERIR (Limpa formulário e define URL de Criar)
    $('[data-bs-target="#modalEntidade"]').not('.btn-editar').on('click', function () {
      $('#modalEntidadeLabel').text('Nova Entidade');
      $('#formEntidade').attr('action', urlCriar);
      $('#formEntidade')[0].reset();
    });

    // 2. Ação de EDITAR (Preenche campos e define URL de Editar)
    $(document).on('click', '.btn-editar', function () {
      var id = $(this).data('id');
      $('#modalEntidadeLabel').text('Editar Entidade');
      
      // Define a URL de destino do form (ex: /entidade/5/editar/)
      $('#formEntidade').attr('action', '/entidade/' + id + '/editar/');
      
      // Preenche os inputs do modal
      $('#id_campo1').val($(this).data('campo1'));
      $('#id_campo2').val($(this).data('campo2'));
    });

    // 3. Ação de DELETAR (Preenche o modal genérico de confirmação)
    $(document).on('click', '.btn-deletar', function () {
      $('#deletarEntidade').text($(this).data('entidade'));
      $('#deletarNome').text($(this).data('nome'));
      $('#formDeletar').attr('action', $(this).data('url'));
    });
  });
</script>
{% endblock %}
```

---

## 4. Checklist para o Desenvolvedor

1.  **Identificadores Únicos**: Certifique-se de que o formulário no partial tenha um `id` claro (ex: `id="formEntidade"`) e os inputs também (ex: `id="id_campo1"`).
2.  **CSRF Token**: Verifique se o formulário dentro do modal inclui `{% csrf_token %}`.
3.  **URLs no Django**: As rotas no `urls.py` devem coincidir com o que o JavaScript está montando ou chamando.
4.  **Método POST**: Para Editar e Deletar, o formulário deve obrigatoriamente usar `method="post"`.
