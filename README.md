# Quantium Bank

Sistema bancário web desenvolvido em Flask como projeto acadêmico de Engenharia de Software. O Quantium Bank permite cadastrar usuários, autenticar por CPF, consultar saldo e extrato e realizar transferências entre contas com validações de negócio e consistência transacional.

## Funcionalidades

- Cadastro de usuários com CPF válido e único.
- Autenticação exclusivamente por CPF e senha.
- Senhas protegidas com hash BCrypt.
- Sessões Flask protegidas por CSRF.
- Consulta de saldo e histórico de transações.
- Transferências localizadas pelo CPF do destinatário.
- Valor mínimo de transferência de `R$ 0,01`, limitado ao saldo disponível.
- Bloqueio de autotransferências.
- Listagem autenticada de usuários com paginação.
- Seed com dez usuários fictícios para demonstração.
- Interface em português brasileiro com identidade visual escura, high-tech e neon.

## Tecnologias

- Python 3.13
- Flask
- Flask-SQLAlchemy
- SQLite
- BCrypt
- Flask-WTF
- Pytest

## Arquitetura

O projeto utiliza uma organização modular, mantendo modelos, regras de negócio, rotas, objetos de domínio, interface e testes separados:

```text
.
├── app/
│   ├── models.py             # Modelos Usuario e Transacao
│   ├── routes.py             # Rotas HTTP e controle de acesso
│   ├── services.py           # Regras de negócio testáveis
│   ├── objects/
│   │   └── cpf.py            # Objeto de valor CPF
│   ├── templates/            # Páginas HTML e layout base
│   └── static/
│       ├── css/style.css     # Estilos da aplicação
│       └── js/app.js         # Interações auxiliares
├── tests/                    # Testes unitários organizados por domínio
├── instance/                 # Banco SQLite local, não versionado
├── run.py                    # Ponto de entrada da aplicação
├── seed.py                   # Usuários fictícios de demonstração
├── reset_db.py               # Recriação controlada do banco
├── requirements.txt          # Dependências Python
└── README.md
```

## Banco de dados

O sistema utiliza duas tabelas principais:

- `usuario`: nome, CPF, hash da senha e saldo.
- `transacao`: origem, destino, valor e data/hora da transferência.

Os valores monetários usam `Numeric(12, 2)` no banco e `Decimal` no código. As transferências são confirmadas em uma operação atômica, com rollback em caso de falha. O SQLite mantém as chaves estrangeiras habilitadas e o histórico impede a exclusão de usuários relacionados a transações.

O banco local é criado automaticamente em `instance/banco.db` e não é versionado.

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
```

Uma chave pode ser gerada com:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

`SEED_DEMO_DATA=true` cria os usuários de demonstração automaticamente quando o banco ainda não possui usuários. Para um cadastro manual, mantenha o valor como `false`.

## Executando a aplicação

```powershell
.\.venv\Scripts\python.exe run.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

## Usuários de demonstração

Para criar os dez usuários fictícios manualmente:

```powershell
.\.venv\Scripts\python.exe -m seed
```

As senhas demonstrativas seguem o padrão `Quantium@01` até `Quantium@10`. Os CPFs e saldos estão definidos em `seed.py` exclusivamente para testes e apresentação acadêmica.

Para apagar e recriar o banco com os dados demonstrativos:

```powershell
.\.venv\Scripts\python.exe reset_db.py
```

> O reset remove os dados existentes. Use apenas em desenvolvimento.

## Testes

Os testes são unitários e estão separados por responsabilidade:

- `test_cpf.py`: normalização e validação de CPF.
- `test_authentication.py`: política de senha, hash e cadastro.
- `test_transfers.py`: transferências, saldos e regras de negócio.

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
- Auditoria, migrações e múltiplos tipos de conta não fazem parte da versão 1.0.

## Equipe

Projeto desenvolvido para a disciplina de Engenharia de Software:

- **Product Owner:** Nathália Granater
- **Scrum Master:** Lucca Oliveira
- **Developer Front-End:** Derek Pontes
- **Developer Back-End:** Vinícius Mousinho
