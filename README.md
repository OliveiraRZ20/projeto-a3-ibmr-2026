# Quantium Bank

Sistema bancário web desenvolvido em Flask como projeto acadêmico de Engenharia de Software. O Quantium Bank permite cadastrar usuários, autenticar por CPF, consultar saldo e extrato e realizar transferências entre contas com validações de negócio e consistência transacional.

## Funcionalidades

- Cadastro de usuários com nome completo, CPF, e-mail, telefone e data de nascimento.
- Validação de maioridade, confirmação de senha e dados brasileiros de contato.
- Autenticação exclusivamente por CPF e senha.
- Senhas protegidas com hash BCrypt.
- Sessões Flask protegidas por CSRF.
- Consulta de saldo e histórico de transações.
- Transferências localizadas pelo CPF do destinatário.
- Valor mínimo de transferência de `R$ 0,01`, limitado ao saldo disponível.
- Bloqueio de autotransferências.
- Listagem autenticada de usuários com paginação.
- Página **Meu Perfil** autenticada com dados somente para leitura.
- Timestamps de criação e atualização dos usuários.
- Seed com dez usuários fictícios para demonstração.
- Seed dinâmica configurável para desenvolvimento, com dados reproduzíveis opcionalmente.
- Painel administrativo somente leitura para usuários autorizados.
- Interface em português brasileiro com identidade visual dark/high-tech, Glassmorphism e Soft UI.
- Layout responsivo com cards translúcidos, gradientes difusos, estados de foco e microinterações nativas.

## Tecnologias

- Python 3.13
- Flask
- Flask-SQLAlchemy
- SQLite
- BCrypt
- Flask-WTF
- Faker
- Pytest

## Arquitetura

O projeto utiliza uma organização modular, mantendo modelos, regras de negócio, rotas, objetos de domínio, interface e testes separados:

```text
.
├── quantium_bank/
│   ├── __main__.py           # CLI centralizada do pacote
│   ├── cli/                  # Adaptadores dos subcomandos
│   ├── *_service.py          # Operações reutilizáveis dos comandos
│   ├── models.py             # Modelos Usuario e Transacao
│   ├── routes.py             # Rotas HTTP e controle de acesso
│   ├── services.py           # Regras de negócio testáveis
│   ├── objects/              # Objetos de valor do domínio
│   ├── templates/            # Páginas HTML e layout base
│   └── static/               # CSS e JavaScript compartilhados
├── tests/                    # Testes unitários organizados por domínio
├── instance/                 # Banco SQLite local, não versionado
├── requirements.txt          # Dependências Python
└── README.md
```

## Banco de dados

O sistema utiliza duas tabelas principais:

- `usuario`: dados pessoais, hash da senha, saldo e timestamps de auditoria.
- `transacao`: origem, destino, valor e data/hora da transferência.

Os valores monetários usam `Numeric(12, 2)` no banco e `Decimal` no código. As transferências são confirmadas em uma operação atômica, com rollback em caso de falha. O SQLite mantém as chaves estrangeiras habilitadas e o histórico impede a exclusão de usuários relacionados a transações.

O banco local é criado automaticamente em `instance/banco.db` e não é versionado.

Após atualizar de uma versão anterior do projeto, recrie o banco local para aplicar
as novas colunas do usuário e os dados de demonstração:

```powershell
.\.venv\Scripts\python.exe -m quantium_bank reset-db
```

> O reset remove os dados existentes e deve ser usado apenas no ambiente de desenvolvimento.

## Instalação local

Na raiz do projeto, crie ou reutilize um ambiente virtual Python 3.13:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

No Linux:

```bash
python3.13 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
```

Se o ambiente virtual já estiver configurado, basta atualizar as dependências:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto. Ele não deve ser versionado:

```env
SECRET_KEY=gere-uma-chave-secreta-e-aleatoria
FLASK_ENV=development
SEED_DEMO_DATA=false
SEED_USER_COUNT=10
# Opcional: use uma semente para reproduzir a massa gerada.
SEED_RANDOM_SEED=
```

Uma chave pode ser gerada com:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

`SEED_DEMO_DATA=true` cria usuários fictícios automaticamente quando o banco
ainda não possui usuários. Para um cadastro manual, mantenha o valor como
`false`.
`SEED_USER_COUNT` define a quantidade de usuários gerados pela seed dinâmica,
com padrão `10`. `SEED_RANDOM_SEED` permite reproduzir a mesma massa de dados
quando informado. A seed não cria administradores automaticamente; use o
comando `admin` para promover ou criar um administrador.

O painel administrativo fica disponível em `/admin` apenas para usuários com
permissão administrativa. Ele é somente leitura e apresenta indicadores,
usuários e transações, sem permitir alteração de saldo, exclusão ou promoção
de usuários.

Para promover um usuário existente a administrador:

```powershell
.\.venv\Scripts\python.exe -m quantium_bank admin promover --cpf 21618722069
```

Para criar um novo administrador, informe os dados cadastrais. A senha será
solicitada de forma oculta no terminal:

```powershell
.\.venv\Scripts\python.exe -m quantium_bank admin criar `
  --nome "Nome do Administrador" `
  --cpf 21618722069 `
  --email admin@quantium.test `
  --telefone "(21) 99876-5401" `
  --data-nascimento 1990-04-12
```

O script reutiliza as validações do cadastro, cria o hash BCrypt da senha e
não salva a senha em texto puro.

## Executando a aplicação

```powershell
.\.venv\Scripts\python.exe -m quantium_bank run
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

## Usuários de demonstração

Para criar os usuários fictícios manualmente:

```powershell
.\.venv\Scripts\python.exe -m quantium_bank seed
```

Os dados são gerados dinamicamente, com CPFs válidos, nomes, e-mails,
telefones, datas de nascimento, senhas e saldos fictícios. As credenciais
geradas são exibidas somente no terminal durante a execução manual da seed e
não são armazenadas em texto puro.

A seed é idempotente: quando o banco já possui usuários, nenhuma nova inclusão
é realizada. Para gerar uma massa nova, use o reset do banco, exclusivamente
em desenvolvimento.

Para apagar e recriar o banco com os dados demonstrativos:

```powershell
.\.venv\Scripts\python.exe -m quantium_bank reset-db
```

> O reset remove os dados existentes. Use apenas em desenvolvimento.

## Testes

Os testes são unitários e estão separados por responsabilidade:

- `test_cpf.py`: normalização e validação de CPF.
- `test_authentication.py`: política de senha, hash, cadastro e perfil.
- `test_objects.py`: validação de e-mail, telefone e data de nascimento.
- `test_transfers.py`: transferências, saldos e regras de negócio.
- `test_seed.py`: geração dinâmica, unicidade e idempotência da seed.
- `test_admin.py`: autorização e consultas do painel administrativo.
- `test_admin_script.py`: criação e promoção de administradores.
- `test_cli.py`: registro e validação dos subcomandos do pacote.
- `test_formatting.py`: formatação de CPF e valores monetários.

Execute todos com:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Segurança e decisões de escopo

- O CPF é normalizado antes de ser persistido.
- Senhas nunca são armazenadas em texto puro.
- O backend repete todas as validações importantes feitas no frontend.
- Formulários utilizam proteção CSRF.
- O banco SQLite atende ao escopo acadêmico e de demonstração.
- Não há exclusão física de usuários que possuam histórico financeiro.
- O painel administrativo é somente leitura; alterações administrativas não
  são realizadas pela interface.
- Auditoria avançada, migrações e múltiplos tipos de conta permanecem fora do
  escopo da versão 1.2.0.

## Equipe

Projeto desenvolvido para a disciplina de Engenharia de Software:

- **Product Owner:** Nathália Granater
- **Scrum Master:** Lucca Oliveira
- **Developer Front-End:** Derek Pontes
- **Developer Back-End:** Vinícius Mousinho
