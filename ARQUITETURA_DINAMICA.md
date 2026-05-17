# Dinâmica de Arquitetura LavUP

## 1. O Coração: MVT (Model-View-Template)
O Django separa as responsabilidades em três camadas principais:

*   **📦 Model (Dados)**: 
    *   Representa as tabelas do banco de dados.
    *   Define **o que** os dados são (campos, tipos, validações).
*   **⚙️ View (Lógica)**: 
    *   O "cérebro" da aplicação.
    *   Recebe a requisição, consulta o **Model** e entrega para o **Template**.
*   **🎨 Template (Interface)**: 
    *   O HTML dinâmico que o usuário final enxerga.
    *   Exibe os dados processados pela **View**.

> **Fluxo:** `Usuário` ➔ `URL` ➔ `View` ➔ `Model` ➔ `View` ➔ `Template` ➔ `HTML`

---

## 2. A Fundação: Banco de Dados

### 🏗️ Migrate (Estrutura / "Planta")
Gerencia a **casca** do banco de dados.
1.  `makemigrations`: Registra alterações feitas nos arquivos `models.py`.
2.  `migrate`: Cria ou altera as tabelas reais no MySQL/PostgreSQL.
*   *Foco: Colunas, tipos de dados, chaves estrangeiras.*

### 🌱 Seed (População / "Recheio")
Insere **dados iniciais** para o sistema não nascer vazio.
*   **Exemplos:** Usuário admin inicial, lista de fabricantes, categorias padrão.
*   **Execução:** Comandos como `python manage.py seed_...` ou `loaddata`.
*   *Foco: Conteúdo real para teste e uso imediato.*

---

## 3. Resumo Visual Minimalista
```text
[ ARQUIVOS ]          [ BANCO ]               [ CLIENTE ]
   Models  ────────▶  Migrate (Tabelas)  ──▶  Interface (Browser)
   Seeds   ────────▶  Seed (Registros)   ──▶  Dados (Telas)
```

---

## 4. Exemplo Prático: Módulo de Veículos
Este é o melhor exemplo para ver o ciclo completo, pois inclui o uso de **Seeds** reais.

### A. O Modelo (`lavup/models/veiculo.py`)
Define o veículo e suas relações (Fabricante e Tamanho).
```python
class Veiculo(models.Model):
    fabricante = models.ForeignKey('Fabricante', ...)
    tamanho = models.ForeignKey('Tamanho', ...)
    modelo = models.CharField(max_length=255)
```
*   **Ação (Migrate):** Ao rodar `migrate`, o Django cria a tabela `veiculos` com as chaves estrangeiras para fabricantes e tamanhos.

### B. A View (`lavup/views/crud.py`)
Prepara os dados para a listagem, otimizando a busca.
```python
def veiculos(request):
    # O select_related traz os dados do fabricante e tamanho em uma única consulta
    lista = Veiculo.objects.select_related('fabricante', 'tamanho').all()
    return render(request, 'veiculos.html', {'veiculos': lista})
```

### C. O Template (`lavup/templates/veiculos.html`)
Exibe a tabela dinâmica para o usuário.
```html
{% for veiculo in veiculos %}
  <tr>
    <td>{{ veiculo.fabricante.nome }}</td>
    <td>{{ veiculo.modelo }}</td>
    <td>{{ veiculo.tamanho }}</td>
  </tr>
{% endfor %}
```

### D. O Seed (`lavup/management/commands/seed_veiculos.py`)
**Diferencial:** Este módulo já possui um populador automático!
*   **O que faz:** Lê o arquivo `seeds/veiculos.csv` (com +70 modelos).
*   **Ação:** Insere todos os veículos no banco de uma só vez.
*   **Comando:** `python manage.py seed_veiculos`.

---

## 5. Esquema de Prototipagem (Slides de Interface)
Para o design do usuário (Fase 2 do RAD), seguimos esta sequência visual:

### 🎞️ Slide 1: Identificação (`login_identify`)
*   **Interface:** Tela limpa com logo e campo único (E-mail ou WhatsApp).
*   **Propósito:** Validar a existência do usuário sem pedir senha.
*   **Resultado:** Gatilho para o envio do código via WhatsApp.

### 🎞️ Slide 2: Verificação 2FA (`login_verify`)
*   **Interface:** Campo de 6 dígitos com timer de contagem regressiva.
*   **Propósito:** Segurança máxima. Autenticação por posse do dispositivo.
*   **Resultado:** Login realizado e redirecionamento para o Dashboard.

### 🎞️ Slide 3: Dashboard Principal (`dashboard`)
*   **Interface:** Painel com cards (OS abertas, Agendamentos hoje, Lavadores ativos).
*   **Propósito:** Visão gerencial rápida para tomada de decisão.
*   **Resultado:** Menu lateral liberado para navegação completa.

### 🎞️ Slide 4: Telas de Gestão (`cruds`)
*   **Interface:** Tabela (DataTable) + Botão "Inserir" + Modais de Formulário.
*   **Propósito:** Cadastro de Clientes, Veículos e Serviços.
*   **Padrão:** Todas as telas de gestão seguem o mesmo visual para facilitar o aprendizado.

### 🎞️ Slide 5: Operação de Agenda (`agenda`)
*   **Interface:** Calendário ou Lista de Horários.
*   **Propósito:** Controle de fluxo do lava-jato (quem lava o quê e quando).
*   **Resultado:** Finalização do serviço e notificação automática ao cliente.
