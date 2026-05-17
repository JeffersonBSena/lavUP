# Guia de Construção de Templates e CRUD — LavUP

Este guia define o padrão técnico para construção de interfaces e operações CRUD no projeto LavUP, baseado na estrutura consolidada do módulo de **Veículos**.

---

## 1. Organização de Arquivos
Cada módulo deve seguir esta estrutura de arquivos:
- `lavup/templates/[modulo].html` (Página principal)
- `lavup/templates/partials/form_[modulo].html` (Modal de criação/edição)
- `lavup/templates/partials/modal_deletar.html` (Modal global de exclusão - **não recriar**)

---

## 2. Padrão de Nomenclatura (ID e Classes)
Para que o JavaScript funcione corretamente sem conflitos, use o prefixo do módulo:
- **Modal**: `id="modalModulo"`
- **Formulário**: `id="formModulo"`
- **Título do Modal**: `id="modalModuloLabel"`
- **Botão Editar**: `class="btn-editar-modulo"`
- **Tabela**: `id="tabela-modulo"`

---

## 3. Estrutura do Template Principal (`modulo.html`)

A página principal deve gerenciar a listagem e os gatilhos dos modais.

```html
{% extends 'base.html' %}

{% block content %}
<div id="modulo-container" class="mb-5">
  <h2 class="mb-4"><i class="bi bi-box me-2"></i>Módulo</h2>
  
  <div class="mb-3">
    <!-- Gatilho para NOVO: não usa classe btn-editar -->
    <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#modalModulo">Inserir</button>
  </div>

  <!-- Inclui os componentes -->
  {% include 'partials/form_modulo.html' %}
  {% include 'partials/modal_deletar.html' %}

  <div class="table-responsive">
    <table id="tabela-modulo" class="table table-striped">
      <thead>
        <tr>
          <th>Nome</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        {% for item in itens %}
        <tr>
          <td>{{ item.nome }}</td>
          <td>
            <!-- Botão EDITAR: Carrega dados nos atributos data-* -->
            <button class="btn btn-warning btn-sm btn-editar-modulo"
              data-id="{{ item.id }}"
              data-nome="{{ item.nome }}"
              data-bs-toggle="modal"
              data-bs-target="#modalModulo">Editar</button>

            <!-- Botão DELETAR: Usa o modal genérico -->
            <button class="btn btn-danger btn-sm btn-deletar"
              data-url="/modulo/{{ item.id }}/deletar/"
              data-entidade="o registro"
              data-nome="{{ item.nome }}"
              data-bs-toggle="modal"
              data-bs-target="#modalDeletar">Deletar</button>
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

## 4. Como Chamar as Actions (JavaScript)

O segredo do CRUD LavUP está no bloco `extra_js`. Ele orquestra o comportamento do modal único para Inserir/Editar.

### Script Padrão:
```javascript
{% block extra_js %}
<script>
  $(document).ready(function () {
    // 1. URL base para criação (definida pelo Django)
    var urlCriar = '{% url "modulo_criar" %}';

    // 2. Ação de EDITAR
    // Captura o clique, muda o action do form e preenche os campos
    $(document).on('click', '.btn-editar-modulo', function () {
      var id = $(this).data('id');
      $('#modalModuloLabel').text('Editar Registro');
      $('#formModulo').attr('action', '/modulo/' + id + '/editar/');
      
      // Preenchimento manual dos campos do formulário
      $('#nome').val($(this).data('nome'));
    });

    // 3. Ação de DELETAR (Global)
    // Preenche o modal de confirmação com os dados do botão
    $(document).on('click', '.btn-deletar', function () {
      $('#deletarEntidade').text($(this).data('entidade'));
      $('#deletarNome').text($(this).data('nome'));
      $('#formDeletar').attr('action', $(this).data('url'));
    });

    // 4. Ação de INSERIR (Reset)
    // Quando o modal abre via botão "Inserir", limpa o form e volta para a URL de criar
    $('[data-bs-target="#modalModulo"]').not('.btn-editar-modulo').on('click', function () {
      $('#modalModuloLabel').text('Novo Registro');
      $('#formModulo').attr('action', urlCriar);
      $('#formModulo')[0].reset();
    });

    // 5. Inicialização do DataTable (Opcional)
    $('#tabela-modulo').DataTable({
      language: { url: 'https://cdn.datatables.net/plug-ins/1.13.8/i18n/pt-BR.json' }
    });
  });
</script>
{% endblock %}
```

---

## 5. Regras de Ouro (Checklist)
1.  **CSRF**: Todo `form` dentro de partial deve ter `{% csrf_token %}`.
2.  **IDs nos Inputs**: Os inputs no `form_modulo.html` devem ter `id` idêntico ao que o JavaScript tenta preencher (ex: `id="nome"`).
3.  **Delegated Events**: Use `$(document).on('click', '.classe', ...)` para que os botões funcionem mesmo após a paginação do DataTable.
4.  **Generic Delete**: Nunca recrie o modal de deletar. Use o `partials/modal_deletar.html` e apenas alimente-o via `data-url`.
