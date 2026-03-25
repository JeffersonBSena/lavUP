# RAD Python Create Approach — LavUP

Este documento descreve a abordagem de **Rapid Application Development (RAD)** aplicada ao projeto LavUP, utilizando o ecossistema Python/Django para acelerar o ciclo de vida do desenvolvimento.

---

## 🚀 Princípios RAD no Ecossistema Python

A escolha do Python e do framework Django foi estratégica para permitir:
1.  **Modelagem Rápida**: Utilização do ORM para definir o banco de dados via classes Python.
2.  **Prototipagem de Interface**: Uso do sistema de templates e Bootstrap para UI funcional imediata.
3.  **Desenvolvimento Iterativo**: Ciclos curtos de entrega (Sprints de 1-2 dias) para módulos específicos.
4.  **Automação de Dados**: Seeds automatizados para testar fluxos reais desde o dia 1.

---

## 🛠️ Passo a Passo da Criação RAD

### Passo 1: Modelagem de Domínio Agnóstica
Em vez de focar no SQL, focamos nas entidades de negócio.
- **Ferramenta**: `models.Model` do Django.
- **Ação**: Definição de relacionamentos (`ForeignKey`, `OneToOne`) e enums diretamente no código.
- **Velocidade**: `python manage.py makemigrations` gera o esquema SQL automaticamente para MySQL.

### Passo 2: Construção de "Vias Rápidas" (Fast-Tracks)
Para cada novo módulo, seguimos o padrão:
1.  **Model**: Criação da tabela.
2.  **Seed**: População via CSV (`management commands`).
3.  **Admin**: Registro no `admin.py` para gestão imediata dos dados antes mesmo da UI final.
4.  **View/Template**: Implementação da interface do usuário com herança de `base.html`.

### Passo 3: Integração de Serviços (Service Layer)
Para serviços externos (como Evolution API), desacoplamos a lógica da View:
- **Local**: `lavup/services/`
- **Vantagem**: Facilita a troca de provedores ou a manutenção sem afetar a interface.

---

## 📋 Checklist de Criação de Novo Módulo (Checklist RAD)

Sempre que um novo recurso for necessário (ex: Relatórios), siga este checklist:

- [ ] **Data Model**: Definir os campos e constraints no `models/`.
- [ ] **Migration Check**: Validar se a migration não gera conflitos no MySQL.
- [ ] **Seed Data**: Criar um CSV em `seeds/` e um comando em `management/commands/`.
- [ ] **Business Logic**: Isolar regras de negócio em `services/` ou no `model`.
- [ ] **UI Prototype**: Criar o template usando blocos do `base.html`.
- [ ] **WhatsApp Sync**: Se necessário, registrar os templates de mensagem em `services/mensagens.py`.

---

## ⚡ Comandos para Aceleração

| Ação | Comando |
|---|---|
| Resetar e Popular | `python manage.py migrate` + `python manage.py seed_all` |
| Ver Rotas | `python manage.py show_urls` |
| Testar Envio Whats | `python manage.py test_whatsapp_connection` |

---

## 🎯 Próximos Passos (Iteração Atual)
Conforme a `documentacao.md`, o foco RAD agora é:
- Implementar os CRUDs de **Clientes**, **Serviços** e **Ordens de Serviço** usando o padrão de "Vias Rápidas" descrito acima.
- Finalizar o **Cutover** com testes integrados de 2FA.

---
> **Nota:** Este documento é vivo e deve ser atualizado a cada nova ferramenta ou padrão de automação adotado pela equipe.
