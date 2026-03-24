# LavUP - Documentação RAD do Projeto

**Data de Início:** 22/03/2026
**Última Atualização:** 23/03/2026
**Stack:** Django 4.2 | MySQL 9.6 | Bootstrap 5.3 | Evolution API (WhatsApp)
**Metodologia:** RAD (Rapid Application Development) — Python/Django

---

## Progresso Geral

| Fase RAD | Status | Progresso |
|---|---|---|
| 1. Planejamento de Requisitos | Concluída | 100% |
| 2. Prototipação / Design do Usuário | Em andamento | 40% |
| 3. Construção Rápida | Em andamento | 30% |
| 4. Cutover (Testes e Implantação) | Não iniciada | 0% |

---

## Fase 1 — Planejamento de Requisitos (100%)

> Levantamento do escopo, definição do domínio, modelagem de dados e escolha da stack.

### 1.1 Escopo do Sistema

Sistema de gestão para lava-jato com:
- Cadastro de clientes, veículos e serviços
- Ordens de serviço com múltiplos itens
- Agendamento com controle de tempo e lavador
- Autenticação 2FA via WhatsApp (sem senha)
- Notificações automáticas por WhatsApp

### 1.2 Stack Definida

| Componente | Tecnologia | Versão |
|---|---|---|
| Linguagem | Python | 3.9.6 |
| Framework Web | Django (MVT) | 4.2.29 |
| Banco de Dados | MySQL | 9.6.0 (Homebrew) |
| Frontend | Bootstrap (CDN) | 5.3.3 |
| Ícones | Bootstrap Icons (CDN) | 1.11.3 |
| Mensageria | Evolution API (WhatsApp) | — |
| SO Desenvolvimento | macOS (Apple Silicon) | — |

### 1.3 Modelagem de Dados

```
usuarios ──< codigos_verificacao
    │
    └──< agenda >── ordem_servico >── os_servicos >── servicos
                         │
                    clientes    veiculos >── fabricantes
                                   │
                                tamanhos

bloqueios_login (independente)
```

#### Tabela `usuarios`

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

#### Tabela `clientes`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| nome | CharField(255) | obrigatório |
| whatsapp | CharField(20) | opcional |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

#### Tabela `fabricantes`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| nome | CharField(255) | obrigatório |
| created_at | DateTimeField | auto_now_add |

#### Tabela `tamanhos`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| nome | CharField(100) | obrigatório |
| incremento_valor | DecimalField(10,2) | acréscimo no preço |
| incremento_tempo | IntegerField | acréscimo em minutos |
| created_at | DateTimeField | auto_now_add |

#### Tabela `veiculos`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| fabricante_id | FK → fabricantes | CASCADE |
| tamanho_id | FK → tamanhos | CASCADE |
| modelo | CharField(255) | obrigatório |
| created_at | DateTimeField | auto_now_add |

#### Tabela `servicos`

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

#### Tabela `ordem_servico`

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

#### Tabela `os_servicos`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| ordem_servico_id | FK → ordem_servico | CASCADE |
| servico_id | FK → servicos | CASCADE |
| valor_aplicado | DecimalField(10,2) | valor cobrado |
| tempo_aplicado | IntegerField | tempo em minutos |
| **Constraint** | unique_together | (ordem_servico, servico) |

#### Tabela `agenda`

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

#### Tabela `codigos_verificacao`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| usuario_id | FK → usuarios | CASCADE |
| codigo | CharField(6) | gerado automaticamente |
| tentativas | IntegerField | default 0, max 3 |
| verificado | BooleanField | default False |
| created_at | DateTimeField | auto_now_add |
| expires_at | DateTimeField | auto (created + 5min) |

#### Tabela `bloqueios_login`

| Campo | Tipo | Detalhes |
|---|---|---|
| id | BigAutoField | PK |
| identificador | CharField(255) | único (e-mail ou whatsapp) |
| tentativas_falhas | IntegerField | default 0, max 5 |
| bloqueado_ate | DateTimeField | nullable |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

**Regra:** Após 5 tentativas falhas → bloqueio de 30 minutos.

### 1.4 Enums do Domínio

| Model | Campo | Valores |
|---|---|---|
| Usuario | tipo | `admin`, `lavador` |
| OrdemServico | status | `aberta`, `iniciada`, `agendada`, `concluida`, `cancelada` |
| Agenda | status | `agendado`, `iniciado`, `concluido`, `cancelado` |

### 1.5 Variáveis de Ambiente (.env)

| Variável | Descrição |
|---|---|
| `DJANGO_SECRET_KEY` | Chave secreta do Django |
| `DJANGO_DEBUG` | Modo debug (True/False) |
| `DB_NAME` / `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT` | Conexão MySQL |
| `EVOLUTION_API_URL` / `EVOLUTION_API_TOKEN` / `EVOLUTION_INSTANCE` / `EVOLUTION_ENABLED` | Evolution API |
| `ADMIN_NOME` / `ADMIN_EMAIL` / `ADMIN_WHATSAPP` | Admin inicial |
| `VERIFICATION_CODE_LENGTH` / `VERIFICATION_CODE_EXPIRY_MINUTES` / `VERIFICATION_CODE_MAX_ATTEMPTS` | Configurações 2FA |

---

## Fase 2 — Prototipação / Design do Usuário (40%)

> Prototipação iterativa das interfaces e fluxos com feedback rápido.

### 2.1 Layout Base — Concluído

- **Estrutura:** Navbar fixa + Sidebar lateral + Conteúdo principal
- **Template master:** `base.html` com blocos extensíveis
- **Logo:** SVG em `static/img/logo.svg`
- **Favicons:** Completo (ico, png 16/32, apple-touch, android-chrome, webmanifest)

### 2.2 Telas Implementadas

| Tela | Template | Status |
|---|---|---|
| Login — Identificação | `auth/login_identify.html` | Concluído |
| Login — Verificação 2FA | `auth/login_verify.html` | Concluído |
| Dashboard | `dashboard.html` | Concluído |

### 2.3 Telas Pendentes

| Tela | Prioridade | Status |
|---|---|---|
| CRUD Clientes | Alta | Pendente |
| CRUD Serviços | Alta | Pendente |
| CRUD Ordens de Serviço | Alta | Pendente |
| Agenda / Calendário | Alta | Pendente |
| CRUD Usuários (admin) | Média | Pendente |
| Relatórios | Baixa | Pendente |

### 2.4 Fluxo de Autenticação 2FA — Concluído

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

## Fase 3 — Construção Rápida (30%)

> Desenvolvimento iterativo dos módulos com integração contínua.

### 3.1 Estrutura do Projeto

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
│   ├── services/                     # Serviços de integração
│   ├── views/                        # Views da aplicação
│   ├── management/commands/          # Comandos de seed
│   ├── templates/                    # Templates HTML
│   └── static/                       # CSS + imagens
```

### 3.2 Módulos — Status de Construção

| Módulo | Camadas | Status |
|---|---|---|
| **Autenticação 2FA** | Model + View + Template + Service | Concluído |
| **Dashboard** | View + Template | Concluído |
| **Mensageria WhatsApp** | Service (transport + templates) | Concluído |
| **Seeds / Data Migrations** | Migrations + Commands + CSVs | Concluído |
| **Clientes** | Model pronto, CRUD pendente | Em andamento |
| **Serviços** | Model pronto, CRUD pendente | Em andamento |
| **Veículos** | Model pronto, CRUD pendente | Em andamento |
| **Ordens de Serviço** | Model pronto, CRUD pendente | Em andamento |
| **Agenda** | Model pronto, CRUD pendente | Em andamento |
| **Usuários (admin)** | Model pronto, CRUD pendente | Em andamento |

### 3.3 Rotas Implementadas

| URL | View | Módulo |
|---|---|---|
| `/` | `login_identify` | Autenticação |
| `/login/` | `login_identify` | Autenticação |
| `/login/verificar/` | `login_verify` | Autenticação |
| `/logout/` | `logout_view` | Autenticação |
| `/dashboard/` | `dashboard` | Dashboard |
| `/admin/` | Django Admin | Administração |

### 3.4 Serviços de Mensageria — Concluído

| Camada | Arquivo | Responsabilidade |
|---|---|---|
| **Transporte** | `services/evolution_api.py` | Enviar mensagem via Evolution API |
| **Conteúdo** | `services/mensagens.py` | Templates + despacho |

**Templates disponíveis:**

| Método | Uso |
|---|---|
| `codigo_verificacao(codigo)` | Código 2FA |
| `boas_vindas(nome)` | Boas-vindas ao novo usuário |
| `os_criada(numero_os, servicos)` | OS aberta |
| `os_concluida(numero_os)` | OS finalizada |
| `agendamento_confirmado(data, horario, servicos)` | Agendamento criado |
| `agendamento_cancelado(data, horario)` | Agendamento cancelado |
| `lembrete_agendamento(data, horario)` | Lembrete de agendamento |

### 3.5 Migrations

```
0001_initial
  └── 0002_bloqueiologin_codigoverificacao
        └── 0003_seed_fabricantes_tamanhos_veiculos
              └── 0004_seed_admin
                    └── 0005_seed_admins_extras
```

| Migration | Tipo | Descrição |
|---|---|---|
| `0001_initial` | Schema | 9 tabelas principais com FKs e constraints |
| `0002_bloqueiologin_codigoverificacao` | Schema | Tabelas de autenticação 2FA |
| `0003_seed_fabricantes_tamanhos_veiculos` | Data | 20 fabricantes + 3 tamanhos + 73 veículos (via CSV) |
| `0004_seed_admin` | Data | Admin inicial (do `.env`) |
| `0005_seed_admins_extras` | Data | 3 admins adicionais da equipe |

### 3.6 Dados Pré-populados (Seeds)

| Tamanho | Valor Extra | Tempo Extra |
|---|---|---|
| Pequeno | R$ 0,00 | 0 min |
| Médio | R$ 15,00 | 15 min |
| Grande | R$ 30,00 | 30 min |

**Fabricantes:** Fiat, Volkswagen, Chevrolet, Hyundai, Toyota, Renault, Honda, Jeep, Nissan, Ford, Peugeot, Citroën, Mitsubishi, Kia, BMW, Mercedes-Benz, Audi, Volvo, Caoa Chery, BYD

**Veículos:** 73 registros distribuídos entre Pequeno, Médio e Grande. Relação por nome (não por ID), resolvida via `get_or_create`.

### 3.7 Dependências (requirements.txt)

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

## Fase 4 — Cutover: Testes e Implantação (0%)

> Testes finais, migração de dados e deploy em produção.

### 4.1 Pendências para Cutover

- [ ] Testes unitários dos models
- [ ] Testes de integração das views
- [ ] Testes do fluxo 2FA completo
- [ ] Testes de carga / stress
- [ ] Configuração de servidor de produção
- [ ] Variáveis de ambiente de produção
- [ ] HTTPS / Certificado SSL
- [ ] Backup automatizado do MySQL
- [ ] Monitoramento e logs
- [ ] Deploy final

---

## Referência Rápida — Comandos

```bash
# Ambiente
source venv/bin/activate
python manage.py runserver

# Banco de Dados
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations

# Seeds (via management commands)
python manage.py seed_admin
python manage.py seed_fabricantes
python manage.py seed_tamanhos
python manage.py seed_veiculos

# MySQL
brew services start mysql
brew services stop mysql
mysql -u lavupUser -p lavup

# Verificação
python manage.py check
```
