# Proposta de evolução — Quantium Bank 1.2.0

> Status: implementada na versão 1.2.0.

## Objetivo

Evoluir a massa de dados de desenvolvimento do Quantium Bank para que a seed
gere usuários fictícios dinamicamente, sem depender de uma lista fixa de
registros mockados. A versão 1.2.0 manterá a arquitetura atual, o escopo
acadêmico e a execução da seed restrita ao ambiente de desenvolvimento.

A nova abordagem deverá produzir um banco mais variado e próximo de um cenário
real de testes, preservando unicidade, validade dos dados, idempotência e
possibilidade de reprodução controlada.

## Escopo

### Geração dinâmica de usuários

A seed deverá gerar uma quantidade configurável de usuários fictícios,
contendo:

- Nomes completos em português brasileiro.
- CPFs válidos, gerados artificialmente pelos dígitos verificadores.
- E-mails únicos e compatíveis com a validação da aplicação.
- Telefones celulares brasileiros válidos, com DDD permitido e número iniciado
  por `9`.
- Datas de nascimento válidas para usuários maiores de 18 anos.
- Senhas aleatórias compatíveis com a política vigente da aplicação.
- Saldos iniciais variados usando `Decimal`, sem cálculos com `float`.

Os dados não deverão ser baseados em pessoas reais nem utilizar informações
pessoais identificáveis. A geração deverá evitar sequências óbvias, valores
duplicados e combinações incompatíveis com as regras de domínio.

### Quantidade configurável

A quantidade de usuários deverá ser configurável por variável de ambiente:

```env
SEED_USER_COUNT=50
```

Quando a variável não estiver definida, a aplicação deverá usar uma quantidade
 padrão documentado. Valores ausentes, inválidos ou menores que zero deverão
 ser tratados explicitamente, sem criar uma quantidade inesperada de registros.

### Reprodutibilidade opcional

A seed deverá aceitar uma semente aleatória opcional:

```env
SEED_RANDOM_SEED=quantium-dev-2026
```

Quando informada, a mesma semente e a mesma configuração deverão produzir uma
massa equivalente, facilitando a reprodução de bugs, testes e apresentações.
Quando não informada, a geração poderá utilizar aleatoriedade normal para criar
uma massa diferente a cada execução.

A semente não deverá ser tratada como segredo e não deverá ser usada para
gerar credenciais de produção.

### Painel administrativo somente leitura

A versão 1.2.0 deverá adicionar um painel administrativo para consulta
operacional do ambiente de desenvolvimento, sem permitir alterações
financeiras ou cadastrais.

O modelo `Usuario` deverá receber um campo booleano `is_admin`, com valor
padrão `False`. O acesso deverá usar o fluxo normal de autenticação por CPF e
senha, seguido de uma verificação explícita de privilégio administrativo.
Não haverá senha administrativa separada nem rota secreta.

O painel deverá:

- Exigir uma sessão autenticada.
- Permitir acesso somente a usuários com `is_admin=True`.
- Bloquear usuários comuns com mensagem de autorização insuficiente.
- Preservar a proteção CSRF e o logout via `POST`.
- Nunca exibir senhas, hashes ou outros segredos.
- Invalidar sessões que apontem para usuários inexistentes.

#### Indicadores administrativos

O painel deverá apresentar:

- Total de usuários.
- Total de usuários administradores.
- Soma dos saldos.
- Total de transações.
- Volume financeiro transferido.
- Usuários cadastrados recentemente.

#### Consulta de usuários

O administrador poderá consultar uma listagem paginada com:

- Busca por nome, CPF e e-mail.
- Filtros por administrador e período de cadastro.
- Dados cadastrais normalizados.
- Data de cadastro e última atualização.
- Saldo atual.
- Quantidade de transferências enviadas e recebidas.

#### Consulta de transações

O administrador poderá consultar uma listagem paginada com:

- Conta de origem e conta de destino.
- CPF dos envolvidos.
- Valor da transferência.
- Data e hora no timezone configurado.
- Filtros por período, CPF e faixa de valor.
- Quantidade de transações e volume financeiro total.

O painel será inicialmente somente leitura. Não será possível editar usuários,
bloquear contas, alterar saldos, excluir usuários, promover administradores ou
estornar transferências pela interface.

### Idempotência e integração com o banco

- A seed continuará sendo executada automaticamente somente quando
  `SEED_DEMO_DATA=true` estiver configurado.
- A execução automática deverá ocorrer somente quando o banco ainda não tiver
  usuários.
- A execução manual deverá evitar duplicidades de CPF, e-mail e telefone.
- Usuários já existentes não deverão ser alterados nem sobrescritos.
- As inclusões deverão ocorrer dentro de uma transação única.
- Falhas deverão provocar rollback explícito e informar o erro.
- O fluxo existente de `reset_db.py` deverá continuar recriando o banco antes
  de executar a seed.
- A seed deverá continuar utilizando `create_user` para centralizar as regras
  de validação, normalização e hash de senha.

### Credenciais de desenvolvimento

Como as senhas serão geradas dinamicamente:

- A seed deverá disponibilizar as credenciais geradas de forma controlada para
  uso local durante a execução manual.
- Senhas nunca deverão ser persistidas em texto puro no banco.
- As credenciais exibidas deverão ser identificadas como exclusivas para
  desenvolvimento e demonstração.
- A aplicação não deverá exibir senhas em páginas, consultas de usuários,
  logs de requisições ou respostas HTTP.

## Configuração esperada

As variáveis abaixo deverão ser documentadas no `README.md` e no exemplo de
configuração do projeto:

| Variável | Finalidade | Comportamento padrão |
|---|---|---|
| `SEED_DEMO_DATA` | Habilita a seed automática | Desabilitada |
| `SEED_USER_COUNT` | Define a quantidade de usuários | Valor padrão documentado |
| `SEED_RANDOM_SEED` | Permite reproduzir a geração | Aleatória a cada execução |

O nome e o tipo das variáveis deverão seguir o padrão já utilizado pelo
projeto, com conversão e validação realizadas no backend.

## Compatibilidade e arquitetura

A evolução deverá preservar:

- A separação entre modelos, serviços, rotas e objetos de domínio.
- O uso dos objetos `CPF`, `Email`, `Telefone` e `DataNascimento`.
- O armazenamento de CPF, e-mail e telefone em formato normalizado.
- O uso de BCrypt para as senhas.
- O uso de `Decimal` e `Numeric(12, 2)` para valores monetários.
- O comportamento atual de `SEED_DEMO_DATA`.
- O fluxo de reset controlado pelo `reset_db.py`.
- A possibilidade de executar a aplicação sem dados demonstrativos.
- O acesso administrativo pelo fluxo normal de autenticação.
- A criação e promoção administrativa pelo script `admin.py`.
- O uso de um decorator ou serviço próprio para autorização administrativa.

Não deverão ser criadas tabelas adicionais apenas para controlar a seed.

## Testes previstos

Criar ou atualizar testes automatizados para cobrir:

- Geração da quantidade configurada de usuários.
- Valor padrão quando a quantidade não for informada.
- Rejeição de quantidade inválida, negativa ou excessivamente fora do limite
  definido pela aplicação.
- CPFs gerados válidos e únicos.
- E-mails gerados válidos e únicos.
- Telefones gerados válidos e únicos.
- Nomes completos compatíveis com a validação.
- Datas de nascimento de usuários maiores de 18 anos.
- Senhas geradas compatíveis com a política vigente.
- Saldos armazenados com precisão monetária.
- Reprodutibilidade quando `SEED_RANDOM_SEED` for informada.
- Variação entre execuções sem semente fixa.
- Idempotência sem duplicar usuários.
- Preservação de usuários existentes.
- Rollback em caso de falha durante a inclusão.
- Execução automática somente com `SEED_DEMO_DATA=true`.
- Ausência de senhas em texto puro no banco.
- Compatibilidade do fluxo de `reset_db.py`.
- Usuário comum bloqueado no painel administrativo.
- Usuário administrador autorizado no painel.
- Sessão órfã invalidada no acesso administrativo.
- Indicadores administrativos calculados corretamente.
- Paginação e filtros de usuários.
- Paginação e filtros de transações.
- Ausência de controles de alteração no painel.

## Fora do escopo da 1.2.0

Não fazem parte desta atualização:

- Geração de dados reais ou consulta a serviços externos.
- Uso da seed em produção.
- Geração de transações financeiras aleatórias.
- Criação de dados de cartão, contas bancárias reais ou documentos adicionais.
- Alteração da política de autenticação.
- Alteração do modelo de permissões.
- Cadastro em massa pela interface web.
- Armazenamento de senhas em arquivos de saída.
- Migração para outro banco de dados.
- Implementação de uma biblioteca genérica de dados sintéticos para além da seed.
- Edição de dados cadastrais pelo painel.
- Bloqueio ou exclusão de usuários.
- Alteração de saldos ou estorno de transferências.
- Promoção de usuários a administradores pela interface.
- Auditoria administrativa avançada e permissões granulares.

## Resultado esperado

Ao final da versão 1.2.0, o Quantium Bank deverá conseguir criar uma massa de
usuários fictícios variada e configurável para desenvolvimento, sem depender de
registros mockados fixos. A geração deverá permanecer válida para o domínio,
segura para o ambiente acadêmico, idempotente e reproduzível quando necessário,
sem comprometer a arquitetura existente ou os fluxos atuais de autenticação e
transferência. O sistema também deverá oferecer um painel administrativo
somente leitura, protegido por autenticação e autorização, com indicadores e
consultas operacionais da massa de usuários e das transações.
