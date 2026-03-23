# LavUP - Documentação do Projeto

**Data:** 22/03/2026
**Stack:** Django 4.2 | MySQL 9.6 | Bootstrap 5.3 | Evolution API (WhatsApp)

---

## 1. Estrutura do Projeto

```
lavup/
├── .env                              # Variáveis de ambiente
├── .gitignore                        # Arquivos ignorados pelo Git
├── manage.py                         # CLI do Django
├── requirements.txt                  # Dependências Python
├── seeds/                            # Dados para popular o banco
│   ├── fabricantes.csv               # 20 fabricantes
│   ├── tamanhos.csv                  # 3 tamanhos (Pequeno, Médio, Grande)
│   └── veiculos.csv                  # 73 veículos
├── lavup/                            # App principal Django
│   ├── settings.py                   # Configurações do projeto
│   ├── urls.py                       # Rotas da aplicação
│   ├── context_processors.py         # Variáveis globais nos templates
│   ├── admin.py                      # Registro no Django Admin
│   ├── models/                       # Models do banco de dados
│   │   ├── __init__.py               # Imports centralizados
│   │   ├── usuario.py                # Usuários do sistema
│   │   ├── cliente.py                # Clientes
│   │   ├── fabricante.py             # Fabricantes de veículos
│   │   ├── tamanho.py                # Tamanhos de veículos
│   │   ├── veiculo.py                # Veículos (modelo + fabricante + tamanho)
│   │   ├── servico.py                # Serviços oferecidos
│   │   ├── ordem_servico.py          # OS + itens da OS
│   │   ├── agenda.py                 # Agendamentos
│   │   └── codigo_verificacao.py     # Códigos 2FA + bloqueio de login
│   ├── services/                     # Serviços de integração
│   │   ├── evolution_api.py          # Client da Evolution API (transporte)
│   │   └── mensagens.py              # Templates de mensagens + dispatch
│   ├── views/                        # Views da aplicação
│   │   └── auth.py                   # Login 2FA, logout, dashboard
│   ├── management/commands/          # Comandos de seed
│   │   ├── seed_admin.py             # Cria usuário admin inicial
│   │   ├── seed_fabricantes.py       # Popula fabricantes
│   │   ├── seed_tamanhos.py          # Popula tamanhos
│   │   └── seed_veiculos.py          # Popula veículos
│   ├── templates/                    # Templates HTML
│   │   ├── base.html                 # Layout master (navbar + sidebar)
│   │   ├── dashboard.html            # Página inicial pós-login
│   │   ├── auth/
│   │   │   ├── login_identify.html   # Etapa 1: e-mail ou WhatsApp
│   │   │   └── login_verify.html     # Etapa 2: código de 6 dígitos
│   │   └── partials/
│   │       ├── navbar.html           # Barra de navegação superior
│   │       └── sidebar.html          # Menu lateral esquerdo
│   └── static/
│       ├── css/style.css             # Estilos customizados
│       └── img/                      # Logo + favicons
```

---

## 2. Configuração do Ambiente

### 2.1 Variáveis de ambiente (.env)

| Variável | Descrição |
|---|---|
| `DJANGO_SECRET_KEY` | Chave secreta do Django |
| `DJANGO_DEBUG` | Modo debug (True/False) |
| `DB_NAME` | Nome do banco MySQL |
| `DB_USER` | Usuário MySQL |
| `DB_PASSWORD` | Senha MySQL |
| `DB_HOST` | Host do MySQL |
| `DB_PORT` | Porta do MySQL |
| `EVOLUTION_API_URL` | URL da Evolution API |
| `EVOLUTION_API_TOKEN` | Token de autenticação |
| `EVOLUTION_INSTANCE` | Nome da instância WhatsApp |
| `EVOLUTION_ENABLED` | Habilitar envio WhatsApp |
| `ADMIN_NOME` | Nome do admin inicial |
| `ADMIN_EMAIL` | E-mail do admin inicial |
| `ADMIN_WHATSAPP` | WhatsApp do admin inicial |
| `VERIFICATION_CODE_LENGTH` | Tamanho do código (6) |
| `VERIFICATION_CODE_EXPIRY_MINUTES` | Expiração em minutos (5) |
| `VERIFICATION_CODE_MAX_ATTEMPTS` | Tentativas máximas do código (3) |

### 2.2 Banco de Dados

- **Motor:** MySQL 9.6 (Homebrew)
- **Banco:** `lavup` (charset utf8mb4)
- **Usuário root:** senha configurada
- **Usuário app:** `lavupUser@localhost` com privilégios apenas no DB `lavup`

---

## 3. Models (Banco de Dados)

### 3.1 Tabela `usuarios`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| nome | CharField(255) | obrigatório |
| email | CharField(255) | único |
| whatsapp | CharField(20) | opcional |
| tipo | CharField(20) | enum: `admin`, `lavador` |
| ativo | BooleanField | default True |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |
| deleted_at | DateTimeField | nullable (soft delete) |

### 3.2 Tabela `clientes`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| nome | CharField(255) | obrigatório |
| whatsapp | CharField(20) | opcional |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

### 3.3 Tabela `fabricantes`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| nome | CharField(255) | obrigatório |
| created_at | DateTimeField | auto_now_add |

### 3.4 Tabela `tamanhos`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| nome | CharField(100) | obrigatório |
| incremento_valor | DecimalField(10,2) | acréscimo no preço |
| incremento_tempo | IntegerField | acréscimo em minutos |
| created_at | DateTimeField | auto_now_add |

### 3.5 Tabela `veiculos`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| fabricante_id | FK → fabricantes | CASCADE |
| tamanho_id | FK → tamanhos | CASCADE |
| modelo | CharField(255) | obrigatório |
| created_at | DateTimeField | auto_now_add |

### 3.6 Tabela `servicos`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| nome | CharField(255) | obrigatório |
| ativo | BooleanField | default True |
| descricao | TextField | opcional |
| valor_base | DecimalField(10,2) | preço base |
| incremento_tempo | IntegerField | tempo em minutos |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

### 3.7 Tabela `ordem_servico`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| cliente_id | FK → clientes | CASCADE |
| veiculo_id | FK → veiculos | CASCADE |
| status | CharField(20) | enum: `aberta`, `iniciada`, `agendada`, `concluida`, `cancelada` |
| observacoes | TextField | opcional |
| placa_veiculo | CharField(10) | obrigatório |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

### 3.8 Tabela `os_servicos`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| ordem_servico_id | FK → ordem_servico | CASCADE |
| servico_id | FK → servicos | CASCADE |
| valor_aplicado | DecimalField(10,2) | valor cobrado |
| tempo_aplicado | IntegerField | tempo em minutos |
| **Constraint** | unique_together | (ordem_servico, servico) |

### 3.9 Tabela `agenda`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| os_id | FK → ordem_servico | CASCADE |
| lavador_id | FK → usuarios | CASCADE |
| inicio_previsto | DateTimeField | obrigatório |
| fim_previsto | DateTimeField | obrigatório |
| inicio_real | DateTimeField | opcional |
| fim_real | DateTimeField | opcional |
| status | CharField(20) | enum: `agendado`, `iniciado`, `concluido`, `cancelado` |
| motivo_cancelamento | TextField | opcional |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

### 3.10 Tabela `codigos_verificacao`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| usuario_id | FK → usuarios | CASCADE |
| codigo | CharField(6) | gerado automaticamente |
| tentativas | IntegerField | default 0, max 3 |
| verificado | BooleanField | default False |
| created_at | DateTimeField | auto_now_add |
| expires_at | DateTimeField | auto (created + 5min) |

### 3.11 Tabela `bloqueios_login`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| identificador | CharField(255) | único (e-mail ou whatsapp) |
| tentativas_falhas | IntegerField | default 0, max 5 |
| bloqueado_ate | DateTimeField | nullable |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

**Regra:** Após 5 tentativas falhas → bloqueio de 30 minutos.

---

## 4. Enums

### 4.1 Usuario.tipo
| Valor | Descrição |
|---|---|
| `admin` | Administrador |
| `lavador` | Lavador |

### 4.2 OrdemServico.status
| Valor | Descrição |
|---|---|
| `aberta` | OS criada |
| `iniciada` | Lavagem em andamento |
| `agendada` | Agendamento futuro |
| `concluida` | Finalizada |
| `cancelada` | Cancelada |

### 4.3 Agenda.status
| Valor | Descrição |
|---|---|
| `agendado` | Agendamento confirmado |
| `iniciado` | Em execução |
| `concluido` | Finalizado |
| `cancelado` | Cancelado |

---

## 5. Fluxo de Autenticação (2FA via WhatsApp)

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│  login_identify  │────▶│  Evolution API    │────▶│  WhatsApp   │
│  (email/whats)   │     │  (envio código)   │     │  do usuário │
└────────┬────────┘     └──────────────────┘     └─────────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│  login_verify    │────▶│  Dashboard       │
│  (código 6 dig)  │     │  (autenticado)   │
└─────────────────┘     └──────────────────┘
```

**Regras de segurança:**
- Código de 6 dígitos com expiração de 5 minutos
- Máximo 3 tentativas por código
- Bloqueio de 30 minutos após 5 tentativas de login falhas
- Timer visual de contagem regressiva na tela
- Auto-submit ao digitar 6 dígitos

---

## 6. Serviços de Mensageria

### 6.1 Arquitetura (desmembrada)

| Camada | Arquivo | Responsabilidade |
|---|---|---|
| **Transporte** | `evolution_api.py` | Enviar mensagem via API |
| **Conteúdo** | `mensagens.py` | Templates + despacho |

### 6.2 Templates de Mensagens Disponíveis

| Método | Uso |
|---|---|
| `codigo_verificacao(codigo)` | Código 2FA |
| `boas_vindas(nome)` | Boas-vindas ao novo usuário |
| `os_criada(numero_os, servicos)` | OS aberta |
| `os_concluida(numero_os)` | OS finalizada |
| `agendamento_confirmado(data, horario, servicos)` | Agendamento criado |
| `agendamento_cancelado(data, horario)` | Agendamento cancelado |
| `lembrete_agendamento(data, horario)` | Lembrete de agendamento |

---

## 7. Dados Pré-populados (Seeds)

### Execução

```bash
python manage.py seed_admin         # Admin inicial (do .env)
python manage.py seed_fabricantes   # 20 fabricantes
python manage.py seed_tamanhos      # 3 tamanhos
python manage.py seed_veiculos      # 73 veículos
```

### Tamanhos e Incrementos

| Tamanho | Valor Extra | Tempo Extra |
|---|---|---|
| Pequeno | R$ 0,00 | 0 min |
| Médio | R$ 15,00 | 15 min |
| Grande | R$ 30,00 | 30 min |

### Fabricantes
Fiat, Volkswagen, Chevrolet, Hyundai, Toyota, Renault, Honda, Jeep, Nissan, Ford, Peugeot, Citroën, Mitsubishi, Kia, BMW, Mercedes-Benz, Audi, Volvo, Caoa Chery, BYD

### Veículos (73 registros)
Distribuídos entre Pequeno, Médio e Grande com fabricantes variados. Relação por nome (não por ID), resolvida no seed via `get_or_create`.

---

## 8. Rotas da Aplicação

| URL | View | Descrição |
|---|---|---|
| `/` | `login_identify` | Página de login (etapa 1) |
| `/login/` | `login_identify` | Página de login (etapa 1) |
| `/login/verificar/` | `login_verify` | Verificação do código (etapa 2) |
| `/logout/` | `logout_view` | Encerrar sessão |
| `/dashboard/` | `dashboard` | Painel principal (requer login) |
| `/admin/` | Django Admin | Administração do Django |

---

## 9. Frontend

- **Framework CSS:** Bootstrap 5.3.3 (CDN)
- **Ícones:** Bootstrap Icons 1.11.3 (CDN)
- **Layout:** Navbar fixa + Sidebar lateral + Conteúdo principal
- **Logo:** SVG em `static/img/logo.svg`
- **Favicons:** Completo (ico, png 16/32, apple-touch, android-chrome, webmanifest)

---

## 10. Dependências (requirements.txt)

| Pacote | Versão | Uso |
|---|---|---|
| Django | 4.2.29 | Framework web |
| mysqlclient | 2.2.7 | Driver MySQL |
| python-dotenv | 1.2.1 | Variáveis de ambiente |
| requests | 2.32.5 | HTTP client (Evolution API) |
| sqlparse | 0.5.5 | Parser SQL (Django) |
| asgiref | 3.11.1 | ASGI (Django) |
| typing_extensions | 4.15.0 | Tipagem (Django) |
| certifi | 2026.2.25 | Certificados SSL |
| urllib3 | 2.6.3 | HTTP (dependência requests) |

---

## 11. Comandos Úteis

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Rodar servidor de desenvolvimento
python manage.py runserver

# Criar/aplicar migrações
python manage.py makemigrations
python manage.py migrate

# Popular banco de dados
python manage.py seed_admin
python manage.py seed_fabricantes
python manage.py seed_tamanhos
python manage.py seed_veiculos

# Verificar integridade do projeto
python manage.py check

# MySQL
brew services start mysql
brew services stop mysql
mysql -u lavupUser -p lavup
```

---

## 12. Infraestrutura

| Componente | Detalhes |
|---|---|
| **Python** | 3.9.6 |
| **Django** | 4.2.29 |
| **MySQL** | 9.6.0 (Homebrew) |
| **SO** | macOS (Apple Silicon) |
| **IDE** | VS Code (venv configurado) |
| **WhatsApp** | Evolution API (zapi.devnativo.com.br) |
