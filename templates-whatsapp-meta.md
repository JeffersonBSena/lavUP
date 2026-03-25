# Templates WhatsApp Business - Meta Approval

**Projeto:** Sidi NET - Chip Lifecycle + Oferta
**Data:** 24/03/2026
**Categoria Meta:** UTILITY (notificacoes de servico) e MARKETING (oferta)

---

## Regras da Meta para Aprovacao

- Sem linguagem ameacadora ou coerciva
- Sem mencao a servicos concorrentes
- Variaveis entre {{1}}, {{2}}, etc
- Maximo 1024 caracteres por template
- Categoria correta (UTILITY para servico, MARKETING para oferta)
- Botoes: maximo 3 (CTA ou quick reply)

---

## LIFECYCLE — Templates de Risco (UTILITY)

### 1. `sidi_risco_d1` — Servico Expirou (D+1)

**Categoria:** UTILITY
**Idioma:** pt_BR

```
Ola {{1}}, aqui e a Sidi NET.

Identificamos que seu plano de dados expirou. Sem ele, voce nao consegue navegar na internet pelo seu chip.

Renove agora e continue conectado!

{{2}}
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = link de renovacao ou instrucao

**Botoes:**
- [Renovar agora] → URL: {{2}}
- [Falar com suporte] → Quick Reply

---

### 2. `sidi_risco_d3` — Lembrete (D+3)

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, seu chip Sidi NET esta sem servico ha 3 dias.

Renove seu plano para voltar a usar a internet no celular. E rapido e facil!

{{2}}
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = link de renovacao

**Botoes:**
- [Renovar agora] → URL: {{2}}

---

### 3. `sidi_risco_d5` — Oferta Especial (D+5)

**Categoria:** MARKETING
**Idioma:** pt_BR

```
{{1}}, sentimos sua falta!

Seu chip Sidi NET esta inativo ha 5 dias. Preparamos uma oferta especial pra voce voltar a navegar:

{{2}}

Aproveite, essa oferta e por tempo limitado.

{{3}}
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = descricao da oferta (ex: "1GB por apenas R$ 9,90")
- {{3}} = link da oferta

**Botoes:**
- [Quero essa oferta] → URL: {{3}}
- [Nao tenho interesse] → Quick Reply

---

### 4. `sidi_risco_d10` — Alerta Critico (D+10)

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, seu chip Sidi NET esta inativo ha 10 dias.

Se o servico nao for renovado, seu numero podera ser desativado.

Renove agora para manter seu numero ativo:

{{2}}
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = link de renovacao

**Botoes:**
- [Renovar agora] → URL: {{2}}
- [Falar com suporte] → Quick Reply

---

### 5. `sidi_risco_d20` — Aviso Final (D+20)

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, este e um aviso importante.

Seu chip Sidi NET esta sem servico ha 20 dias. Em 10 dias seu numero sera suspenso e voce perdera o acesso.

Para evitar a suspensao, renove seu plano:

{{2}}
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = link de renovacao

**Botoes:**
- [Renovar e manter meu numero] → URL: {{2}}

---

### 6. `sidi_risco_d30` — Suspensao (D+30)

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, informamos que seu chip Sidi NET foi suspenso por inatividade de 30 dias.

Voce ainda pode reativar seu numero nos proximos 30 dias entrando em contato com nosso suporte.

Apos esse prazo, o numero sera cancelado definitivamente.
```

**Variaveis:**
- {{1}} = nome do cliente

**Botoes:**
- [Reativar meu chip] → Quick Reply
- [Falar com suporte] → Quick Reply

---

### 7. `sidi_risco_d60` — Cancelamento Definitivo (D+60)

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, informamos que seu chip Sidi NET com o numero {{2}} foi cancelado por inatividade prolongada.

Caso deseje voltar a ser cliente Sidi NET, entre em contato conosco para adquirir um novo chip.

Agradecemos por ter sido nosso cliente.
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = msisdn (numero do chip)

**Botoes:**
- [Quero um novo chip] → Quick Reply

---

## OFERTA — Template de Campanha (MARKETING)

### 8. `sidi_oferta_chip_4g` — Oferta Inicial

**Categoria:** MARKETING
**Idioma:** pt_BR

```
Ola {{1}}!

Voce e cliente especial da Sidi NET e preparamos algo pra voce:

Chip Sidi NET 4G com 1GB de franquia incluso!

Navegue com a mesma qualidade da sua fibra, agora tambem no celular.

Garanta o seu:

{{2}}

Oferta valida por 48 horas.
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = link da landing page com token

**Botoes:**
- [Quero meu chip] → URL: {{2}}
- [Nao tenho interesse] → Quick Reply

---

## CORTESIA — Templates de Risco para Chip Cortesia (UTILITY)

> Chips cortesia sao ofertados gratuitamente a clientes FTTH adimplentes.
> O risco aqui NAO e falta de recarga — e inadimplencia no contrato FTTH.
> As mensagens orientam o cliente a regularizar a fatura da fibra.

### 12. `sidi_cortesia_risco_d1` — Fatura FTTH Vencida (D+1)

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, identificamos que sua fatura da internet fibra esta em atraso.

Seu chip Sidi NET 4G cortesia esta vinculado ao seu plano de fibra. Regularize sua fatura para manter o chip ativo.

{{2}}
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = link de segunda via / pagamento

**Botoes:**
- [Pagar fatura] → URL: {{2}}
- [Falar com suporte] → Quick Reply

---

### 13. `sidi_cortesia_risco_d3` — Lembrete (D+3)

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, sua fatura da fibra esta com 3 dias de atraso.

Seu chip 4G cortesia pode ser suspenso caso a fatura nao seja regularizada.

Acesse a segunda via:

{{2}}
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = link de pagamento

**Botoes:**
- [Pagar agora] → URL: {{2}}

---

### 14. `sidi_cortesia_risco_d5` — Alerta (D+5)

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, sua fatura da fibra continua pendente (5 dias).

Para manter seu chip Sidi NET 4G cortesia ativo, regularize o pagamento:

{{2}}
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = link de pagamento

**Botoes:**
- [Regularizar] → URL: {{2}}

---

### 15. `sidi_cortesia_risco_d10` — Alerta Critico (D+10)

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, sua fatura da fibra esta com 10 dias de atraso.

Seu chip 4G cortesia sera suspenso em breve. Regularize agora para evitar a interrupcao:

{{2}}
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = link de pagamento

**Botoes:**
- [Pagar fatura] → URL: {{2}}
- [Ja paguei] → Quick Reply

---

### 16. `sidi_cortesia_risco_d20` — Aviso Final (D+20)

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, este e um aviso importante.

Sua fatura da fibra esta com 20 dias de atraso. Em 10 dias seu chip Sidi NET 4G cortesia sera suspenso.

Regularize para manter seu beneficio:

{{2}}
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = link de pagamento

**Botoes:**
- [Regularizar agora] → URL: {{2}}

---

### 17. `sidi_cortesia_risco_d30` — Suspensao (D+30)

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, seu chip Sidi NET 4G cortesia foi suspenso devido ao atraso na fatura da fibra.

Regularize sua situacao financeira nos proximos 30 dias para reativar seu chip automaticamente.
```

**Variaveis:**
- {{1}} = nome do cliente

**Botoes:**
- [Falar com suporte] → Quick Reply

---

### 18. `sidi_cortesia_risco_d60` — Cancelamento (D+60)

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, seu chip Sidi NET 4G cortesia (numero {{2}}) foi cancelado devido a inadimplencia prolongada no contrato de fibra.

Caso regularize sua situacao, voce podera solicitar um novo chip cortesia.
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = msisdn

**Botoes:**
- [Falar com suporte] → Quick Reply

---

### 19. `sidi_cortesia_reativado` — Chip Cortesia Reativado

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, boa noticia!

Sua fatura foi regularizada e seu chip Sidi NET 4G cortesia foi reativado automaticamente.

Numero: {{2}}

Obrigado por manter sua fibra em dia!
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = msisdn

---

## LIFECYCLE — Templates Positivos (UTILITY)

### 9. `sidi_chip_ativado` — Chip Ativado com Sucesso

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, seu chip Sidi NET foi ativado com sucesso!

Numero: {{2}}
Plano: {{3}}

Insira o chip no seu celular e comece a navegar. Se precisar de ajuda, estamos aqui.
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = msisdn
- {{3}} = nome do plano (ex: "1GB - 30 dias")

**Botoes:**
- [Preciso de ajuda] → Quick Reply

---

### 10. `sidi_chip_renovado` — Servico Renovado

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, seu plano Sidi NET foi renovado!

Plano: {{2}}
Valido ate: {{3}}

Aproveite sua internet!
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = nome do plano
- {{3}} = data de validade (ex: "25/04/2026")

---

### 11. `sidi_quota_baixa` — Quota Quase Esgotada

**Categoria:** UTILITY
**Idioma:** pt_BR

```
{{1}}, sua franquia Sidi NET esta quase no fim.

Restam apenas {{2}} do seu plano.

Renove antes que acabe para continuar navegando sem interrupcao:

{{3}}
```

**Variaveis:**
- {{1}} = nome do cliente
- {{2}} = quota restante (ex: "50MB")
- {{3}} = link de renovacao

**Botoes:**
- [Renovar agora] → URL: {{3}}

---

## SMS (Osmocom SMPP) — Versoes Curtas (Fallback)

Limite: 160 caracteres por SMS.

| Template | Mensagem |
|----------|----------|
| `sms_risco_d1` | `SidiNET: {{nome}}, seu plano expirou. Renove em {{link}} e continue conectado.` |
| `sms_risco_d3` | `SidiNET: {{nome}}, 3 dias sem servico. Renove agora: {{link}}` |
| `sms_risco_d5` | `SidiNET: {{nome}}, oferta especial pra voce voltar! {{link}}` |
| `sms_risco_d10` | `SidiNET: {{nome}}, seu numero pode ser desativado. Renove: {{link}}` |
| `sms_risco_d20` | `SidiNET: AVISO {{nome}}, 10 dias para suspensao. Renove: {{link}}` |
| `sms_risco_d30` | `SidiNET: {{nome}}, seu chip foi suspenso. Reative em ate 30 dias. Ligue: {{tel}}` |
| `sms_risco_d60` | `SidiNET: {{nome}}, seu chip {{msisdn}} foi cancelado. Obrigado por ser cliente.` |
| `sms_oferta` | `SidiNET: {{nome}}, ganhe Chip 4G com 1GB gratis! {{link}} Valido 48h` |
| `sms_cortesia_d1` | `SidiNET: {{nome}}, fatura fibra em atraso. Regularize para manter seu chip cortesia: {{link}}` |
| `sms_cortesia_d3` | `SidiNET: {{nome}}, 3 dias de atraso na fibra. Chip cortesia pode ser suspenso: {{link}}` |
| `sms_cortesia_d5` | `SidiNET: {{nome}}, fatura pendente 5 dias. Regularize: {{link}}` |
| `sms_cortesia_d10` | `SidiNET: {{nome}}, chip cortesia sera suspenso. Pague a fatura: {{link}}` |
| `sms_cortesia_d20` | `SidiNET: AVISO {{nome}}, 10 dias p/ suspensao do chip cortesia. Regularize: {{link}}` |
| `sms_cortesia_d30` | `SidiNET: {{nome}}, chip cortesia suspenso. Regularize em 30 dias. Contato: {{tel}}` |
| `sms_cortesia_d60` | `SidiNET: {{nome}}, chip cortesia {{msisdn}} cancelado por inadimplencia.` |
| `sms_cortesia_reativado` | `SidiNET: {{nome}}, fatura regularizada! Chip cortesia reativado. Boa navegacao!` |
| `sms_ativado` | `SidiNET: Chip ativado! Numero: {{msisdn}}. Insira no celular e navegue.` |
| `sms_renovado` | `SidiNET: Plano renovado! {{plano}} ate {{data}}. Boa navegacao!` |
| `sms_quota_baixa` | `SidiNET: Sua franquia esta acabando ({{resto}}). Renove: {{link}}` |

---

## Resumo para Submissao na Meta

| # | Nome do Template | Categoria | Botoes | Tipo Chip |
|---|-----------------|-----------|--------|-----------|
| 1 | sidi_risco_d1 | UTILITY | 2 (URL + QR) | Venda |
| 2 | sidi_risco_d3 | UTILITY | 1 (URL) | Venda |
| 3 | sidi_risco_d5 | MARKETING | 2 (URL + QR) | Venda |
| 4 | sidi_risco_d10 | UTILITY | 2 (URL + QR) | Venda |
| 5 | sidi_risco_d20 | UTILITY | 1 (URL) | Venda |
| 6 | sidi_risco_d30 | UTILITY | 2 (QR + QR) | Venda |
| 7 | sidi_risco_d60 | UTILITY | 1 (QR) | Venda |
| 8 | sidi_oferta_chip_4g | MARKETING | 2 (URL + QR) | Campanha |
| 9 | sidi_chip_ativado | UTILITY | 1 (QR) | Ambos |
| 10 | sidi_chip_renovado | UTILITY | 0 | Venda |
| 11 | sidi_quota_baixa | UTILITY | 1 (URL) | Venda |
| 12 | sidi_cortesia_risco_d1 | UTILITY | 2 (URL + QR) | Cortesia |
| 13 | sidi_cortesia_risco_d3 | UTILITY | 1 (URL) | Cortesia |
| 14 | sidi_cortesia_risco_d5 | UTILITY | 1 (URL) | Cortesia |
| 15 | sidi_cortesia_risco_d10 | UTILITY | 2 (URL + QR) | Cortesia |
| 16 | sidi_cortesia_risco_d20 | UTILITY | 1 (URL) | Cortesia |
| 17 | sidi_cortesia_risco_d30 | UTILITY | 1 (QR) | Cortesia |
| 18 | sidi_cortesia_risco_d60 | UTILITY | 1 (QR) | Cortesia |
| 19 | sidi_cortesia_reativado | UTILITY | 0 | Cortesia |

**QR** = Quick Reply | **URL** = Call to Action com link

---

## Notas de Implementacao

1. **Templates MARKETING** precisam de opt-in do cliente (LGPD)
2. **Templates UTILITY** nao precisam de opt-in (sao transacionais)
3. A Meta demora 24-48h para aprovar templates
4. Templates rejeitados afetam o quality rating do numero
5. Manter taxa de leitura acima de 80% para evitar restricoes
6. O D+5 e MARKETING porque inclui oferta promocional
7. Links devem usar dominio proprio (nao encurtadores genericos)
8. Incluir opcao de opt-out nos templates MARKETING
