# Planejamento: Automacao Sidi NET 4G - Oferta de Chip

**Data:** 24/03/2026
**Objetivo:** Automatizar oferta de chip Sidi NET 4G (1GB) para clientes adimplentes do IXC ERP
**Stack:** Laravel + MySQL + Evolution API (WhatsApp) + Osmocom SMPP (SMS) + Landing Page

---

## 1. Visao Geral

```
IXC ERP (API REST)
    |
    v
Laravel (servidor proprio)
    |
    +-- Scheduler: coleta clientes adimplentes (2 meses)
    +-- Queue/Jobs: envio WhatsApp (primario) + SMS SMPP (fallback)
    +-- Landing Page: /oferta/{token} com aceite
    +-- Banco: controle de ofertas, status, logs
```

---

## 2. Criterio de Adimplencia

- **Regra:** Cliente SEM faturas em atraso nos ultimos 2 meses completos
- **Clientes novos** (< 2 meses de historico): entram em fila separada para analise manual
- **Filtros adicionais:**
  - Cliente ativo no IXC
  - Possui numero de celular valido
  - Nao recebeu oferta anteriormente (deduplicacao)

---

## 3. Arquitetura Laravel

### 3.1 Estrutura de arquivos

```
sidi-oferta/
├── app/
│   ├── Console/Commands/
│   │   └── SincronizarClientesIxc.php      # artisan sidi:sincronizar
│   ├── Jobs/
│   │   ├── EnviarOfertaWhatsApp.php        # Job WhatsApp (primario)
│   │   └── EnviarOfertaSms.php             # Job SMS Osmocom (fallback)
│   ├── Models/
│   │   └── Oferta.php                      # Model principal
│   ├── Services/
│   │   ├── IxcService.php                  # API client IXC ERP
│   │   ├── EvolutionService.php            # API client Evolution (WhatsApp)
│   │   └── OsmocomSmppService.php          # Client SMPP Osmocom
│   └── Http/Controllers/
│       └── OfertaController.php            # Landing page + aceite
├── database/migrations/
│   └── xxxx_create_ofertas_table.php
├── resources/views/oferta/
│   ├── aceite.blade.php                    # Pagina da oferta
│   ├── confirmado.blade.php                # Aceite confirmado
│   └── expirado.blade.php                  # Link expirado
├── routes/web.php
└── config/
    ├── ixc.php                             # IXC_API_URL, IXC_API_TOKEN
    ├── evolution.php                        # EVOLUTION_API_URL, etc
    └── osmocom.php                         # SMPP_HOST, SMPP_PORT, etc
```

### 3.2 Migration: tabela `ofertas`

```php
Schema::create('ofertas', function (Blueprint $table) {
    $table->id();
    $table->integer('cliente_ixc_id')->index();
    $table->string('nome');
    $table->string('celular', 20);
    $table->enum('canal_envio', ['whatsapp', 'sms'])->nullable();
    $table->enum('status', [
        'elegivel',    // filtrado, ainda nao enviado
        'enviado',     // mensagem entregue
        'falha',       // falha no envio (ambos canais)
        'aceito',      // cliente clicou "quero meu chip"
        'expirado',    // token expirou sem aceite
        'cancelado',   // cancelado manualmente
    ])->default('elegivel');
    $table->unsignedTinyInteger('tentativas_envio')->default(0);
    $table->text('motivo_falha')->nullable();
    $table->uuid('token')->unique()->nullable();
    $table->timestamp('token_expira_em')->nullable();
    $table->timestamp('enviado_em')->nullable();
    $table->timestamp('aceito_em')->nullable();
    $table->timestamps();

    $table->unique('cliente_ixc_id'); // deduplicacao
});
```

### 3.3 Rotas

```
GET  /oferta/{token}          → OfertaController@show     (landing page)
POST /oferta/{token}/aceitar  → OfertaController@aceitar  (registra aceite)
```

---

## 4. Fluxo Detalhado

### ETAPA 1: Coleta (Command)

```
artisan sidi:sincronizar
│
├── 1. GET IXC /api/cliente
│      Filtros: ativo=S, possui celular
│
├── 2. Para cada cliente:
│      GET IXC /api/fn_areceber
│      Filtro: ultimos 2 meses, status != 'liquidado'
│      Se tem faturas em aberto → PULA
│
├── 3. Verifica tabela ofertas:
│      Se cliente_ixc_id ja existe → PULA (dedup)
│
├── 4. INSERT na tabela ofertas:
│      status = 'elegivel'
│
└── 5. Para cada elegivel:
       Dispatch EnviarOfertaWhatsApp::class
       (via queue, com rate limiting)
```

### ETAPA 2: Envio (Jobs)

```
EnviarOfertaWhatsApp
│
├── Gera UUID token + link
├── Monta mensagem com oferta
├── POST Evolution API /message/sendText
│
├── SUCESSO:
│   └── UPDATE status='enviado', canal='whatsapp', enviado_em=now()
│
└── FALHA:
    └── Dispatch EnviarOfertaSms (fallback)
        │
        ├── Conecta SMPP Osmocom
        ├── Envia SMS com link curto
        │
        ├── SUCESSO:
        │   └── UPDATE status='enviado', canal='sms', enviado_em=now()
        │
        └── FALHA:
            ├── tentativas_envio++
            ├── motivo_falha = erro
            ├── Se tentativas < 3:
            │   └── release(delay: 1h) → volta pra fila
            └── Se tentativas >= 3:
                └── UPDATE status='falha'
```

### ETAPA 3: Landing Page + Aceite

```
GET /oferta/{token}
│
├── Busca oferta pelo token
├── Valida:
│   ├── Token existe?          NÃO → 404
│   ├── Ja foi aceito?         SIM → exibe "ja aceito"
│   ├── Token expirou?         SIM → exibe "expirado" + contato
│   └── VALIDO → exibe pagina de aceite
│
POST /oferta/{token}/aceitar
│
├── Mesmas validacoes
├── UPDATE status='aceito', aceito_em=now()
└── Exibe pagina de confirmacao
```

---

## 5. Protecoes (A Prova de Falhas)

| Protecao | Como |
|----------|------|
| **Deduplicacao** | UNIQUE em `cliente_ixc_id` — mesmo cliente nao recebe 2x |
| **Idempotencia** | Reexecutar `sidi:sincronizar` nao duplica registros |
| **Fallback WhatsApp→SMS** | Job de SMS dispatchado automaticamente na falha |
| **Retry com backoff** | Ate 3 tentativas, com delay de 1h entre cada |
| **Token unico** | UUID v4, expira em 48h, uso unico |
| **Rate limiting** | Queue com rate limit (ex: 30 msgs/min) |
| **Validacao celular** | Regex + DDD valido antes de enviar |
| **Log completo** | Cada passo registrado com timestamp e resultado |
| **Transacao atomica** | Aceite em transaction para evitar race condition |
| **Timeout de API** | Timeout de 10s nas chamadas IXC/Evolution/SMPP |

---

## 6. Variaveis de Ambiente (.env)

```env
# IXC ERP
IXC_API_URL=https://ixc.seudominio.com/webservice/v1
IXC_API_TOKEN=seu_token_aqui

# Evolution API (WhatsApp)
EVOLUTION_API_URL=https://evolution.seudominio.com
EVOLUTION_API_TOKEN=seu_token
EVOLUTION_INSTANCE=instancia

# Osmocom SMPP
SMPP_HOST=127.0.0.1
SMPP_PORT=2775
SMPP_SYSTEM_ID=sidi
SMPP_PASSWORD=senha
SMPP_SOURCE_ADDR=SidiNET

# Oferta
OFERTA_TOKEN_EXPIRY_HOURS=48
OFERTA_MAX_TENTATIVAS=3
OFERTA_RATE_LIMIT_PER_MINUTE=30
OFERTA_BASE_URL=https://seudominio.com/oferta
```

---

## 7. Mensagem da Oferta

### WhatsApp (via Evolution API)
```
Ola {nome}! 👋

Voce e cliente especial da Sidi NET e queremos te oferecer um presente:

📱 *Chip Sidi NET 4G* com *1GB de franquia* GRATIS!

Navegue com a mesma qualidade da sua internet fibra, agora tambem no celular.

👉 Clique aqui para garantir o seu:
{link}

⏰ Oferta valida por 48 horas.

Duvidas? Responda esta mensagem.
```

### SMS (via Osmocom SMPP)
```
SidiNET: {nome}, ganhe um Chip 4G com 1GB gratis! Garanta: {link_curto} Valido 48h
```

---

## 8. Dependencias PHP/Composer

| Pacote | Uso |
|--------|-----|
| `laravel/framework` | Framework |
| `guzzlehttp/guzzle` | HTTP client (IXC + Evolution) |
| `php-smpp/php-smpp` ou `glushko/smpp` | Client SMPP para Osmocom |
| `ramsey/uuid` | Geracao de tokens (ja incluso no Laravel) |

---

## 9. Proximos Passos (pos-aceite)

> A planejar depois que o fluxo de oferta estiver validado:

- [ ] Logistica de entrega/ativacao do chip
- [ ] Integracao com sistema de provisioning LTE
- [ ] Acompanhamento de uso (consumo do 1GB)
- [ ] Dashboard de metricas (taxa de aceite, canal mais efetivo)
- [ ] Campanhas recorrentes (novas ofertas, upgrades)

---

## 10. Cronograma Sugerido

| Fase | Escopo |
|------|--------|
| **Sprint 1** | Estrutura Laravel + IxcService + Migration + Command de coleta |
| **Sprint 2** | Jobs de envio (WhatsApp + SMS SMPP) + testes |
| **Sprint 3** | Landing page + aceite + validacoes |
| **Sprint 4** | Testes end-to-end + deploy + monitoramento |
