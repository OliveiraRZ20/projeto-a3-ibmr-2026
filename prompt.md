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
├── cpf.py                    # Validação e representação de CPF
├── templates/
│   ├── login.html            # Tela de login dos usuários
│   ├── register.html         # Tela de cadastro de novos usuários
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
  - `cpf`: String(11), único e obrigatório, armazenado somente com dígitos.
  - `senha`: String(60), obrigatório, armazenando exclusivamente o hash BCrypt da senha.
  - `saldo`: Numeric(12, 2), valor padrão `0.00`, representando o saldo monetário sem utilizar `Float`.
- **Classe `Transacao`**:
  - `id`: Inteiro, chave primária.
  - `conta_origem_id`: Inteiro, chave estrangeira obrigatória apontando para `Usuario.id`.
  - `conta_destino_id`: Inteiro, chave estrangeira obrigatória apontando para `Usuario.id`.
  - `valor`: Numeric(12, 2), valor positivo da transferência.
  - `data_hora`: DateTime com timezone, valor padrão baseado em `datetime.now(timezone.utc)`.
- O modelo deve permanecer simples, usando apenas as tabelas `Usuario`/`Conta` e `Transacao`; não criar uma tabela separada de contas neste escopo.
- Definir relacionamentos ORM entre `Transacao` e `Usuario`, com referências distintas para conta de origem e conta de destino.
- Criar índice único para `Usuario.cpf` e índices nas chaves estrangeiras de `Transacao` para acelerar autenticação e consultas do extrato.
- Declarar restrições de banco para impedir saldo ou valor de transação negativos e autotransferências (`conta_origem_id != conta_destino_id`).
- Configurar as chaves estrangeiras com comportamento `RESTRICT`, impedindo a exclusão de usuários que possuam transações e preservando o histórico financeiro.
- Armazenar datas e horários das transações em UTC, convertendo para o fuso local somente na apresentação.

### 2. `controller.py` (Controller)
- Função `registrar_rotas(app)` que encapsula todos os endpoints da aplicação:
  - `GET /` & `GET /login`: Renderiza a tela de login (`login.html`).
  - `GET /register`: Renderiza a tela de cadastro (`register.html`).
  - `POST /register`: Recebe nome, CPF e senha; normaliza e valida o CPF usando a classe `CPF` de `cpf.py`, verifica se o CPF já existe e cria o novo usuário com saldo inicial. A senha deve ser alfanumérica, seguir o tamanho mínimo definido pela aplicação e ser transformada em hash BCrypt antes de ser persistida.
  - `POST /login`: Aceita exclusivamente CPF e senha. Deve normalizar e validar o CPF, buscar o usuário pelo CPF e verificar a senha usando BCrypt, sem comparar senhas em texto puro e sem aceitar qualquer outro identificador. Em caso de sucesso, regenera ou configura a sessão via `flask.session` sem armazenar a senha.
  - `GET /dashboard`: Exibe saldo atual e lista de transações (enviadas e recebidas) do usuário logado.
  - `POST /transferir`: Executa a lógica de transferência bancária:
    1. Valida se o valor digitado é maior que zero.
    2. Converte o valor recebido para `Decimal`, sem utilizar `float`.
    3. Inicia uma transação única com bloqueio de escrita apropriado para SQLite (como `BEGIN IMMEDIATE`) antes de ler os saldos.
    4. Verifica se a conta de destino existe (por CPF ou ID).
    5. Verifica se a conta de origem possui saldo suficiente (`saldo >= valor`).
    6. Executa o débito na origem (`origem.saldo -= valor`) e o crédito no destino (`destino.saldo += valor`).
    7. Registra o histórico na tabela `Transacao`.
    8. Aplica a alteração com `db.session.commit()`. Em caso de erro, realiza `db.session.rollback()` e informa uma falha sem deixar alterações parciais.
  - `GET /logout`: Encerra a sessão e redireciona para a tela inicial.

### 3. `server.py` (Main / Server)
- Instanciar a aplicação Flask (`app = Flask(__name__)`).
- Configurar a URI do banco de dados: `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'`.
- Configurar `app.config['SECRET_KEY']` para suporte a sessões HTTP.
- Inicializar a extensão SQLAlchemy: `db.init_app(app)`.
- Ativar explicitamente `PRAGMA foreign_keys = ON` em toda conexão SQLite para garantir a integridade das chaves estrangeiras.
- No bloco `with app.app_context():`, invocar `db.create_all()` para gerar as tabelas no SQLite caso não existam.
- Registrar as rotas do controller.
- Executar a aplicação em `0.0.0.0:5000` (compatível com o preview do Replit).
- Para este escopo simples, usar `db.create_all()` apenas para criar o banco inicial; não adicionar tabela de auditoria nem mecanismo de migrações neste projeto.

---

## Regras de Negócio e Segurança de Transação
1. **Validação de Saldo**: O remetente nunca pode transferir um valor superior ao seu saldo disponível.
2. **Atomicidade (ACID)**: A operação de transferência (débito + crédito + histórico) deve ocorrer dentro de um mesmo bloco de transação do banco.
3. **Prevenção de Autotransferência**: Um usuário não pode realizar transferências para a própria conta.
4. **Mensagens de Feedback**: A View deve exibir mensagens amigáveis em caso de erro (ex: "Saldo insuficiente", "Conta de destino não encontrada") ou sucesso.
5. **Autenticação por CPF**: O CPF é o único identificador permitido no formulário e no endpoint de login. Deve ser normalizado para 11 dígitos, validado pelos dígitos verificadores com `CPF` e protegido por restrição de unicidade no banco.
6. **Proteção de Senhas**: A senha nunca pode ser armazenada ou registrada em texto puro. O cadastro deve gerar um hash BCrypt com fator de custo adequado, e o login deve verificar o hash com uma função segura de comparação.
7. **Política de Senha**: A senha deve ser alfanumérica e atender ao tamanho mínimo definido pela aplicação; mensagens de erro não podem revelar se o CPF existe.
8. **Sessão e Segredos**: Usar uma `SECRET_KEY` forte fora do código-fonte em ambientes reais, definir atributos seguros dos cookies de sessão e invalidar a sessão no logout.
9. **Integridade Monetária**: Usar `Numeric(12, 2)` para saldo e transferências, validar valores positivos na aplicação e manter as mesmas restrições no banco.
10. **Integridade Referencial**: Toda transação deve apontar para usuários existentes, e consultas do extrato devem usar os relacionamentos de origem e destino.
11. **Concorrência**: A transferência deve bloquear a operação de escrita durante a leitura e atualização dos saldos, evitando condições de corrida e saldo utilizado por operações simultâneas.
12. **Precisão Numérica**: Usar `Decimal` no código Python e `Numeric(12, 2)` no banco; valores monetários não podem ser calculados com `float`.
13. **Exclusão de Dados**: Não excluir fisicamente usuários que possuam transações; o comportamento padrão deve preservar o histórico por meio de `RESTRICT`.
14. **SQLite**: A conexão deve habilitar `PRAGMA foreign_keys = ON` para que as restrições referenciais sejam efetivas.
15. **Data e Hora**: Persistir `data_hora` em UTC e realizar a conversão de fuso horário somente na interface.

---

## Diretrizes para o Copilot / Assistente de Código
- Escreva o código utilizando práticas limpas, legíveis e alinhadas ao **PEP 8**.
- Garanta a separação estrita de responsabilidades entre `model.py`, `controller.py`, `server.py` e os templates `.html`.
- Adicione comentários curtos explicando a lógica de transação atômica e as validações de regra de negócio no `controller.py`.
- Utilize `bcrypt` ou `Flask-Bcrypt` e registre a dependência no `requirements.txt`; não implemente o algoritmo de hash manualmente.
- Reutilize a classe `CPF` de `cpf.py` para validar CPFs, mantendo o valor persistido sem pontuação e evitando duplicidade.
```