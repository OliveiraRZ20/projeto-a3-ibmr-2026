# Prompt de Inicialização - Sistema Bancário MVC (Flask + SQLAlchemy)

## Contexto do Projeto
Este projeto é um sistema bancário desenvolvido para fins acadêmicos (matéria de Engenharia de Software), projetado para rodar no ambiente Replit utilizando **Python 3**, **Flask**, **Flask-SQLAlchemy** e banco de dados **SQLite**.

O objetivo principal é permitir o cadastro de usuários, autenticação/login, consulta de saldo/extrato e a realização de transferências financeiras entre contas com validação de saldo e atomicidade.

---

## Arquitetura do Sistema (Pattern MVC)

O repositório deve seguir rigorosamente a seguinte estrutura de arquivos e separação de responsabilidades:

```text
.
├── instance/
│   └── banco.db              # Banco de dados SQLite (gerado automaticamente)
├── static/
│   └── style.css             # Estilização CSS da aplicação
├── templates/
│   ├── login.html            # Tela de login e cadastro de novos usuários
│   ├── dashboard.html        # Painel principal (saldo atual e histórico de extrato)
│   └── transferir.html       # Formulário para realizar transferências
├── model.py                  # CAMADA MODEL (Mapeamento ORM com SQLAlchemy)
├── controller.py             # CAMADA CONTROLLER (Regras de negócio e Rotas HTTP)
├── server.py                 # PONTO DE ENTRADA (Inicialização do servidor Flask)
└── README.md
```

---

## Especificações dos Módulos

### 1. `model.py` (Model)
- Configurar a instância do `SQLAlchemy` (`db = SQLAlchemy()`).
- **Classe `Usuario` / `Conta`**:
  - `id`: Inteiro, chave primária (`primary_key=True`).
  - `nome`: String(100), obrigatório.
  - `email`: String(100), único e obrigatório.
  - `senha`: String(200), armazenamento da senha (ou hash).
  - `saldo`: Float/Numeric, valor padrão `0.0`.
- **Classe `Transacao`**:
  - `id`: Inteiro, chave primária.
  - `conta_origem_id`: Inteiro, Chave Estrangeira apontando para `Usuario.id`.
  - `conta_destino_id`: Inteiro, Chave Estrangeira apontando para `Usuario.id`.
  - `valor`: Float/Numeric, valor positivo da transferência.
  - `data_hora`: DateTime, valor padrão `datetime.utcnow`.

### 2. `controller.py` (Controller)
- Função `registrar_rotas(app)` que encapsula todos os endpoints da aplicação:
  - `GET /` & `GET /login`: Renderiza a tela de login (`login.html`).
  - `POST /cadastrar`: Recebe dados do formulário, valida se o e-mail já existe e cria o novo usuário com saldo inicial.
  - `POST /login`: Valida as credenciais do usuário e gerencia a sessão via `flask.session`.
  - `GET /dashboard`: Exibe saldo atual e lista de transações (enviadas e recebidas) do usuário logado.
  - `POST /transferir`: Executa a lógica de transferência bancária:
    1. Valida se o valor digitado é maior que zero.
    2. Verifica se a conta de destino existe (por e-mail ou ID).
    3. Verifica se a conta de origem possui saldo suficiente (`saldo >= valor`).
    4. Executa o débito na origem (`origem.saldo -= valor`) e o crédito no destino (`destino.saldo += valor`).
    5. Registra o histórico na tabela `Transacao`.
    6. Aplica a alteração com `db.session.commit()`. Em caso de erro, realiza `db.session.rollback()`.
  - `GET /logout`: Encerra a sessão e redireciona para a tela inicial.

### 3. `server.py` (Main / Server)
- Instanciar a aplicação Flask (`app = Flask(__name__)`).
- Configurar a URI do banco de dados: `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'`.
- Configurar `app.config['SECRET_KEY']` para suporte a sessões HTTP.
- Inicializar a extensão SQLAlchemy: `db.init_app(app)`.
- No bloco `with app.app_context():`, invocar `db.create_all()` para gerar as tabelas no SQLite caso não existam.
- Registrar as rotas do controller.
- Executar a aplicação em `0.0.0.0:5000` (compatível com o preview do Replit).

---

## Regras de Negócio e Segurança de Transação
1. **Validação de Saldo**: O remetente nunca pode transferir um valor superior ao seu saldo disponível.
2. **Atomicidade (ACID)**: A operação de transferência (débito + crédito + histórico) deve ocorrer dentro de um mesmo bloco de transação do banco.
3. **Prevenção de Autotransferência**: Um usuário não pode realizar transferências para a própria conta.
4. **Mensagens de Feedback**: A View deve exibir mensagens amigáveis em caso de erro (ex: "Saldo insuficiente", "Conta de destino não encontrada") ou sucesso.

---

## Diretrizes para o Copilot / Assistente de Código
- Escreva o código utilizando práticas limpas, legíveis e alinhadas ao **PEP 8**.
- Garanta a separação estrita de responsabilidades entre `model.py`, `controller.py`, `server.py` e os templates `.html`.
- Adicione comentários curtos explicando a lógica de transação atômica e as validações de regra de negócio no `controller.py`.
```