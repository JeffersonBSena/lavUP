# Planejamento: Sistema de Ciclo de Vida do Chip (SIM Lifecycle)

**Data:** 24/03/2026
**Objetivo:** Gerenciar todo o ciclo de vida dos chips SIM, do perfil eletrico ate a delecao
**Stack:** Laravel + MySQL + API HSS (provisioning proprio) + IXC ERP (billing)
**Projeto:** Separado (nao faz parte do sidi-oferta nem do lavup)

---

## 1. Estados do Chip

```
PERFIL_ELETRICO ──▶ ESTOQUE ──▶ PDV ──▶ ATIVO ──▶ RISCO ──▶ DELETADO
     (1)              (2)       (3)      (4)       (5)        (6)
```

### Detalhamento dos estados

| # | Estado | Descricao | Quem muda | Condicao de entrada |
|---|--------|-----------|-----------|---------------------|
| 1 | `perfil_eletrico` | Perfil criado no HSS, chip ainda nao foi gerado fisicamente | API HSS | Criacao via API da operadora |
| 2 | `estoque` | Chip gerado (SIM fisico ou eSIM), aguardando distribuicao | Operador/sistema | Confirmacao de geracao |
| 3 | `pdv` | Enviado para ponto de venda, na prateleira | Operador | Registro de saida para PDV |
| 4 | `ativo` | Vendido ao cliente final, servico ativo com quota/validade | Sistema/PDV | Ativacao + primeiro uso ou registro de venda |
| 5 | `risco` | Servico expirou (quota zerou ou validade venceu), D+0 em diante | Automatico | Servico/grupo entrou em expired |
| 6 | `deletado` | Perfil removido do HSS, chip inutilizado | Automatico/manual | Fim do periodo de risco (D+60) ou manual |

### Tipos de Ativacao (subcategoria do estado `ativo`)

| Tipo | Descricao | Origem | Regras de risco |
|------|-----------|--------|-----------------|
| `venda` | Chip vendido ao cliente final (PDV ou direto) | PDV ou operador | Risco padrao (D+1 a D+60) |
| `cortesia` | Chip ofertado gratuitamente a clientes FTTH adimplentes (2 meses) via campanha sidi-oferta | Automatico (campanha) | Risco diferenciado (ver abaixo) |

#### Regras especificas para chip cortesia

- **Origem:** Cliente FTTH adimplente no IXC (2 meses sem atraso)
- **Vinculo:** O chip cortesia fica vinculado ao contrato FTTH do cliente no IXC
- **Condicao de manutencao:** Enquanto o cliente FTTH estiver adimplente, o chip cortesia e renovado automaticamente
- **Perda de cortesia:** Se o cliente FTTH ficar inadimplente, o chip cortesia entra em risco com marcos diferenciados:
  - D+0 = cliente FTTH ficou inadimplente (fatura vencida)
  - D+1 a D+30 = mesmos marcos de notificacao, mas mensagem diferente (foca na adimplencia FTTH, nao em recarga)
  - D+30 = suspensao do chip cortesia
  - D+60 = delecao
- **Reativacao:** Se o cliente FTTH quitar o debito, o chip cortesia e reativado automaticamente
- **Sem recarga propria:** O cliente nao paga pelo chip cortesia, entao as notificacoes de risco orientam a regularizar a fatura FTTH, nao a "renovar o plano"

### Sub-estados do Periodo de Risco

O D+0 e o momento em que o servico (ou grupo de servicos) entra em `expired` — seja por falta de quota ou por validade expirada. O cliente fica sem servico.

| Marco | Dias apos D+0 | Acao sugerida |
|-------|---------------|---------------|
| D+1   | 1 dia         | Notificacao: "Seu servico expirou, renove agora" |
| D+3   | 3 dias        | Lembrete: "Faltam X dias para perder seu numero" |
| D+5   | 5 dias        | Alerta: oferta especial de renovacao |
| D+10  | 10 dias       | Alerta critico: "Seu chip sera desativado em breve" |
| D+20  | 20 dias       | Aviso final: "Ultimo aviso antes da desativacao" |
| D+30  | 30 dias       | Pre-delete: suspensao do perfil no HSS |
| D+60  | 60 dias       | Delete: remocao do perfil do HSS, chip inutilizado |

---

## 2. Modelagem do Banco de Dados

### Tabela `chips`

| Campo | Tipo | Descricao |
|-------|------|-----------|
| id | BIGINT PK | Auto increment |
| iccid | VARCHAR(20) UNIQUE | Identificador unico do SIM |
| imsi | VARCHAR(15) UNIQUE | IMSI gravado no HSS |
| msisdn | VARCHAR(15) | Numero de telefone (pode ser null ate ativacao) |
| status | ENUM | perfil_eletrico, estoque, pdv, ativo, risco, deletado |
| status_anterior | ENUM | Para auditoria de transicao |
| tipo_ativacao | ENUM nullable | venda, cortesia (preenchido ao ativar) |
| contrato_ftth_ixc_id | INT nullable | ID do contrato FTTH no IXC (apenas cortesia) |
| cortesia_adimplente | BOOLEAN default true | Cliente FTTH em dia? (apenas cortesia) |
| perfil_hss_id | VARCHAR(100) | ID do perfil na API do HSS |
| pdv_id | BIGINT FK nullable | Ponto de venda que recebeu |
| cliente_ixc_id | INT nullable | ID do cliente no IXC (quando ativo) |
| cliente_nome | VARCHAR(255) nullable | Cache do nome |
| cliente_celular | VARCHAR(20) nullable | Numero de contato do cliente |
| servico_expira_em | TIMESTAMP nullable | Data de expiracao do servico atual |
| quota_restante_mb | INT nullable | Quota restante em MB |
| risco_d0 | TIMESTAMP nullable | Data/hora que entrou em D+0 |
| risco_marco_atual | ENUM nullable | d1, d3, d5, d10, d20, d30, d60 |
| ultimo_trafego_em | TIMESTAMP nullable | Ultimo registro de uso |
| ativado_em | TIMESTAMP nullable | Data de ativacao |
| deletado_em | TIMESTAMP nullable | Data de delecao do HSS |
| motivo_delecao | VARCHAR(100) nullable | ex: expirado_d60, manual, fraude |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

### Tabela `chip_historico` (log de transicoes)

| Campo | Tipo | Descricao |
|-------|------|-----------|
| id | BIGINT PK | |
| chip_id | BIGINT FK | |
| status_de | ENUM | Estado anterior |
| status_para | ENUM | Novo estado |
| acao | VARCHAR(100) | O que causou a transicao |
| detalhes | JSON nullable | Dados extras (erro HSS, etc) |
| executado_por | VARCHAR(100) | sistema, operador, api, cron |
| created_at | TIMESTAMP | |

### Tabela `chip_notificacoes` (controle de alertas enviados)

| Campo | Tipo | Descricao |
|-------|------|-----------|
| id | BIGINT PK | |
| chip_id | BIGINT FK | |
| marco | ENUM | d1, d3, d5, d10, d20, d30, d60 |
| canal | ENUM | whatsapp, sms |
| status | ENUM | enviado, falha |
| enviado_em | TIMESTAMP nullable | |
| created_at | TIMESTAMP | |

### Tabela `pdvs` (pontos de venda)

| Campo | Tipo | Descricao |
|-------|------|-----------|
| id | BIGINT PK | |
| nome | VARCHAR(255) | Nome do PDV |
| responsavel | VARCHAR(255) nullable | |
| celular | VARCHAR(20) nullable | |
| endereco | TEXT nullable | |
| ativo | BOOLEAN default true | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

---

## 3. Maquina de Estados (Transicoes Validas)

```
perfil_eletrico ──▶ estoque       (chip gerado)
perfil_eletrico ──▶ deletado      (perfil descartado)

estoque ──▶ pdv                   (enviado para ponto de venda)
estoque ──▶ ativo                 (venda direta sem PDV)
estoque ──▶ deletado              (chip defeituoso/descartado)

pdv ──▶ ativo                     (vendido ao cliente final)
pdv ──▶ estoque                   (devolvido ao estoque)

ativo ──▶ risco                   (servico expirou: quota ou validade)
ativo ──▶ deletado                (cancelamento/fraude)

risco ──▶ ativo                   (cliente renovou/recarregou)
risco ──▶ deletado                (D+60 atingido ou manual)
```

### Transicoes INVALIDAS (bloqueadas)

- deletado → qualquer (estado terminal)
- pdv → risco (nao pode entrar em risco sem ter sido ativo)
- estoque → risco (idem)
- perfil_eletrico → ativo (precisa passar por estoque primeiro)

---

## 4. Arquitetura Laravel

### Estrutura de arquivos

```
sidi-lifecycle/
├── app/
│   ├── Console/Commands/
│   │   ├── VerificarServicosExpirados.php   # Detecta chips que entraram em D+0
│   │   ├── ProcessarMarcosRisco.php         # Avanca marcos D+1..D+60
│   │   └── DeletarChipsExpirados.php        # Executa delecao no HSS (D+60)
│   │
│   ├── Jobs/
│   │   ├── EnviarNotificacaoRisco.php       # WhatsApp/SMS para cada marco
│   │   └── DeletarPerfilHss.php             # Job de delecao no HSS
│   │
│   ├── Models/
│   │   ├── Chip.php
│   │   ├── ChipHistorico.php
│   │   ├── ChipNotificacao.php
│   │   └── Pdv.php
│   │
│   ├── Services/
│   │   ├── HssService.php                   # API client do HSS
│   │   ├── IxcService.php                   # API client IXC (billing)
│   │   ├── EvolutionService.php             # WhatsApp
│   │   ├── OsmocomSmppService.php           # SMS SMPP
│   │   └── ChipStateMachine.php             # Valida e executa transicoes
│   │
│   ├── Http/Controllers/
│   │   ├── ChipController.php               # CRUD + acoes manuais
│   │   ├── PdvController.php                # CRUD PDVs
│   │   └── DashboardController.php          # Metricas/visao geral
│   │
│   └── Enums/
│       ├── ChipStatus.php                   # Enum dos estados
│       └── RiscoMarco.php                   # Enum dos marcos D+X
│
├── database/migrations/
│   ├── create_pdvs_table.php
│   ├── create_chips_table.php
│   ├── create_chip_historico_table.php
│   └── create_chip_notificacoes_table.php
│
├── resources/views/
│   ├── dashboard/index.blade.php
│   ├── chips/
│   │   ├── index.blade.php                  # Lista com filtros por status
│   │   ├── show.blade.php                   # Detalhe + historico
│   │   └── create.blade.php                 # Criacao manual
│   └── pdvs/
│       ├── index.blade.php
│       └── form.blade.php
│
└── routes/
    ├── web.php                               # Interface web
    └── api.php                               # Endpoints para integracao
```

### Scheduler (Kernel.php)

```php
// Roda a cada 15 minutos — detecta novos D+0
$schedule->command('sidi:verificar-expirados')->everyFifteenMinutes();

// Roda diariamente — avanca marcos e envia notificacoes
$schedule->command('sidi:processar-marcos')->dailyAt('08:00');

// Roda diariamente — deleta chips D+60
$schedule->command('sidi:deletar-expirados')->dailyAt('03:00');
```

---

## 5. Fluxos Detalhados

### 5.1 Criacao de Perfil Eletrico

```
Operador/API → POST /api/chips
│
├── Chama HssService::criarPerfil(imsi, ...)
│   ├── SUCESSO → retorna perfil_hss_id
│   └── FALHA → retorna erro, nao cria registro
│
├── INSERT chip: status='perfil_eletrico'
├── INSERT chip_historico: null → perfil_eletrico
└── Retorna chip criado
```

### 5.2 Deteccao de Risco (Command)

```
sidi:verificar-expirados (a cada 15 min)
│
├── SELECT chips WHERE status='ativo'
│
├── Para cada chip ativo:
│   ├── Consulta servico via HSS ou IXC
│   │   (servico expirou? quota zerou?)
│   │
│   ├── SE expirou:
│   │   ├── UPDATE status='risco', risco_d0=now()
│   │   ├── INSERT chip_historico
│   │   └── Dispatch EnviarNotificacaoRisco (D+1)
│   │
│   └── SE ainda ativo:
│       └── Atualiza quota_restante_mb, servico_expira_em
```

### 5.3 Processamento de Marcos (Command)

```
sidi:processar-marcos (diario 08:00)
│
├── SELECT chips WHERE status='risco'
│
├── Para cada chip em risco:
│   ├── Calcula dias desde risco_d0
│   │
│   ├── Verifica se chip reativou (servico voltou):
│   │   ├── SIM → UPDATE status='ativo', limpa risco_d0
│   │   │         INSERT chip_historico: risco → ativo
│   │   └── NAO → continua
│   │
│   ├── Identifica proximo marco:
│   │   dias=1  → d1
│   │   dias=3  → d3
│   │   dias=5  → d5
│   │   dias=10 → d10
│   │   dias=20 → d20
│   │   dias=30 → d30 (suspende perfil HSS)
│   │   dias=60 → d60 (deleta)
│   │
│   ├── Ja notificou este marco?
│   │   ├── SIM → pula
│   │   └── NAO → Dispatch EnviarNotificacaoRisco
│   │
│   └── Se marco = d30:
│       └── HssService::suspenderPerfil(chip)
```

### 5.4 Delecao D+60

```
sidi:deletar-expirados (diario 03:00)
│
├── SELECT chips WHERE status='risco'
│   AND risco_d0 <= now() - 60 dias
│
├── Para cada chip:
│   ├── Dispatch DeletarPerfilHss
│   │   ├── HssService::deletarPerfil(chip)
│   │   ├── SUCESSO → UPDATE status='deletado'
│   │   │              deletado_em=now()
│   │   │              motivo_delecao='expirado_d60'
│   │   └── FALHA → log erro, retry
│   │
│   └── INSERT chip_historico: risco → deletado
```

---

## 6. API Endpoints (para integracao)

| Metodo | Rota | Descricao |
|--------|------|-----------|
| GET    | /api/chips | Lista chips (filtros: status, pdv, cliente) |
| GET    | /api/chips/{iccid} | Detalhe do chip |
| POST   | /api/chips | Criar perfil eletrico (chama HSS) |
| PATCH  | /api/chips/{iccid}/status | Transicao de estado manual |
| POST   | /api/chips/{iccid}/ativar | Ativar para cliente (associa cliente_ixc_id) |
| POST   | /api/chips/lote/estoque | Mover lote para estoque |
| POST   | /api/chips/lote/pdv | Enviar lote para PDV |
| GET    | /api/chips/risco | Lista chips em periodo de risco |
| GET    | /api/dashboard/stats | Contadores por status |
| GET    | /api/pdvs | Lista PDVs |
| POST   | /api/pdvs | Criar PDV |

---

## 7. Dashboard — Metricas

```
┌─────────────────────────────────────────────────────────┐
│                   DASHBOARD LIFECYCLE                     │
│                                                           │
│  Perfil Eletrico: 150    Estoque: 320    PDV: 85         │
│  Ativos: 1.240           Em Risco: 67    Deletados: 430  │
│                                                           │
│  ┌─────────── RISCO DETALHADO ──────────┐               │
│  │  D+1:  12  │  D+10: 8  │  D+30: 5   │               │
│  │  D+3:  10  │  D+20: 6  │  D+60: 3   │               │
│  │  D+5:   9  │           │             │               │
│  └──────────────────────────────────────┘               │
│                                                           │
│  Taxa de reativacao (risco→ativo): 34%                   │
│  Taxa de churn (risco→deletado): 66%                     │
└─────────────────────────────────────────────────────────┘
```

---

## 8. Variaveis de Ambiente

```env
# HSS API (provisioning proprio)
HSS_API_URL=http://hss.interno/api
HSS_API_TOKEN=seu_token
HSS_TIMEOUT_SECONDS=15

# IXC ERP
IXC_API_URL=https://ixc.dominio.com/webservice/v1
IXC_API_TOKEN=token_ixc

# Evolution API (WhatsApp)
EVOLUTION_API_URL=https://evolution.dominio.com
EVOLUTION_API_TOKEN=token_evolution
EVOLUTION_INSTANCE=instancia

# Osmocom SMPP (SMS)
SMPP_HOST=127.0.0.1
SMPP_PORT=2775
SMPP_SYSTEM_ID=sidi
SMPP_PASSWORD=senha
SMPP_SOURCE_ADDR=SidiNET

# Lifecycle
RISCO_MARCOS=1,3,5,10,20,30,60
RISCO_SUSPENDER_DIA=30
RISCO_DELETAR_DIA=60
VERIFICAR_EXPIRADOS_INTERVAL=15
```

---

## 9. Relacao entre os Projetos

```
┌──────────────────┐     ┌──────────────────┐     ┌────────────┐
│ sidi-lifecycle   │     │  sidi-oferta      │     │  IXC ERP   │
│ (ciclo de vida)  │────▶│  (campanhas)      │────▶│  (billing) │
│                  │     │                   │     │            │
│ • Estados chip   │     │ • Filtro clientes │     │ • Clientes │
│ • Marcos risco   │     │ • Envio oferta    │     │ • Faturas  │
│ • HSS API        │     │ • Landing page    │     │ • Servicos │
│ • Notificacoes   │     │ • Aceite          │     │            │
└────────┬─────────┘     └──────────────────┘     └────────────┘
         │
         ▼
┌──────────────────┐
│  HSS (operadora) │
│  Provisioning    │
└──────────────────┘
```

O **sidi-oferta** consulta o **sidi-lifecycle** para saber quais chips estao disponiveis em estoque antes de ofertar. Sao projetos complementares.

---

## 10. Ordem de Desenvolvimento

| Prioridade | Projeto | Motivo |
|------------|---------|--------|
| **1o** | sidi-lifecycle | Base: sem controle de chip, nao ha o que ofertar |
| **2o** | sidi-oferta | Depende do lifecycle para saber estoque e status |

### Sprints do sidi-lifecycle

| Sprint | Escopo |
|--------|--------|
| **1** | Laravel setup + migrations + Enums + ChipStateMachine + HssService |
| **2** | CRUD Chips + PDVs + transicoes manuais (web + API) |
| **3** | Commands automaticos: verificar-expirados + processar-marcos |
| **4** | Notificacoes (WhatsApp/SMS) por marco de risco |
| **5** | Dashboard + metricas + testes + deploy |
