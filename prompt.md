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
├── app/
│   ├── models.py             # Modelos ORM e instância do SQLAlchemy
│   ├── routes.py             # Rotas HTTP e integração com os serviços
│   ├── services.py           # Regras de negócio testáveis
│   ├── objects/
│   │   └── cpf.py            # Objeto de valor e validação de CPF
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── transferir.html
│   │   └── usuarios.html
│   └── static/
│       ├── css/style.css     # Estilização compartilhada
│       └── js/app.js         # Interações auxiliares do frontend
├── seed.py                   # Criação opcional de dados de demonstração
├── reset_db.py               # Recriação controlada do banco para demonstração
├── .env.example              # Modelo de variáveis de ambiente
├── tests/
│   └── test_business_rules.py # Testes unitários das regras de negócio
├── run.py                    # PONTO DE ENTRADA (Inicialização do servidor Flask)
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
  - `POST /register`: Recebe nome, CPF e senha; normaliza e valida o CPF usando a classe `CPF` de `cpf.py`, verifica se o CPF já existe e cria o novo usuário com saldo inicial. A senha deve ter pelo menos 6 caracteres, não conter espaços e aceitar letras maiúsculas, letras minúsculas, números e caracteres especiais; deve ser transformada em hash BCrypt antes de ser persistida.
  - `POST /login`: Aceita exclusivamente CPF e senha. Deve normalizar e validar o CPF, buscar o usuário pelo CPF e verificar a senha usando BCrypt, sem comparar senhas em texto puro e sem aceitar qualquer outro identificador. Em caso de sucesso, regenera ou configura a sessão via `flask.session` sem armazenar a senha.
  - `GET /dashboard`: Exibe saldo atual e lista de transações (enviadas e recebidas) do usuário logado.
  - `GET /usuarios`: Exige autenticação e lista os usuários cadastrados para facilitar testes e demonstrações, sem expor senhas ou hashes.
  - `POST /transferir`: Executa a lógica de transferência bancária:
    1. Valida se o valor digitado é maior que zero.
    2. Converte o valor recebido para `Decimal`, sem utilizar `float`.
    3. Inicia uma transação única com bloqueio de escrita apropriado para SQLite (como `BEGIN IMMEDIATE`) antes de ler os saldos.
    4. Verifica se a conta de destino existe (por CPF ou ID).
    5. Verifica se a conta de origem possui saldo suficiente (`saldo >= valor`).
    6. Executa o débito na origem (`origem.saldo -= valor`) e o crédito no destino (`destino.saldo += valor`).
    7. Registra o histórico na tabela `Transacao`.
    8. Aplica a alteração com `db.session.commit()`. Em caso de erro, realiza `db.session.rollback()` e informa uma falha sem deixar alterações parciais.
  - `POST /logout`: Encerra a sessão e redireciona para a tela inicial.

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
- Implementar em `seed.py` a criação idempotente de 10 usuários fictícios para demonstração e validação do sistema, executada somente quando `SEED_DEMO_DATA=true` estiver configurado em ambiente de desenvolvimento.
- O seed deve validar os CPFs com a classe `CPF`, gerar hashes BCrypt para as senhas, verificar a existência pelo CPF antes de inserir e confirmar todas as inclusões em uma transação única.
- O seed deve conter 10 registros fictícios versionados, com credenciais de demonstração explícitas e saldos iniciais variados, para facilitar a apresentação acadêmica. Usar estes CPFs válidos e fictícios: `21618722069`, `21718722095`, `21818722011`, `21918722048`, `22018722018`, `22118722044`, `22218722070`, `22318722005`, `22418722023` e `22518722050`.
- Usar os seguintes dados didáticos no seed, todos fictícios e exclusivos da demonstração: `Ana Lima` / `21618722069` / `Quantium@01` / `R$ 100,00`; `Bruno Costa` / `21718722095` / `Quantium@02` / `R$ 250,00`; `Carla Souza` / `21818722011` / `Quantium@03` / `R$ 500,00`; `Diego Alves` / `21918722048` / `Quantium@04` / `R$ 750,00`; `Eva Martins` / `22018722018` / `Quantium@05` / `R$ 1.000,00`; `Felipe Rocha` / `22118722044` / `Quantium@06` / `R$ 1.500,00`; `Gabriela Melo` / `22218722070` / `Quantium@07` / `R$ 2.000,00`; `Henrique Dias` / `22318722005` / `Quantium@08` / `R$ 2.500,00`; `Isabela Reis` / `22418722023` / `Quantium@09` / `R$ 3.000,00`; `Joao Nunes` / `22518722050` / `Quantium@10` / `R$ 5.000,00`.
- Essas senhas de demonstração podem ser explícitas no código versionado, devem respeitar a política da aplicação e nunca podem ser reutilizadas por usuários reais.
- `reset_db.py` deve oferecer uma operação explícita de desenvolvimento que remova e recrie as tabelas e execute o seed completo; nunca executar essa operação automaticamente nem em produção.
- O seed automático na primeira execução deve ocorrer somente quando `SEED_DEMO_DATA=true` estiver configurado e o banco ainda não possuir usuários; execuções posteriores devem ser idempotentes.
- Carregar `SECRET_KEY`, ambiente e demais segredos por `.env` usando `python-dotenv`; versionar somente `.env.example`, nunca o `.env` real.
- Registrar `python-dotenv` e a biblioteca escolhida para CSRF no `requirements.txt`; não implementar proteção criptográfica manualmente.

---

## Arquitetura Web
- Utilizar cinco templates HTML: `login.html`, `register.html`, `dashboard.html`, `transferir.html` e `usuarios.html`, com `base.html` para o layout compartilhado.
- Adicionar uma área autenticada para listar todos os usuários cadastrados, com busca por CPF/nome e paginação quando a quantidade ultrapassar o limite definido pela aplicação. Nesta demonstração, os CPFs podem ser exibidos integralmente.
- Utilizar um único arquivo CSS compartilhado em `static/css/style.css`, concentrando layout, cores, formulários, mensagens, componentes e responsividade.
- Utilizar um único arquivo JavaScript compartilhado em `static/js/app.js` para máscara e normalização visual do CPF, validações auxiliares dos formulários, confirmação de transferências e interações comuns.
- O JavaScript deve remover pontuação do CPF antes do envio quando necessário, mas não substitui a validação definitiva da classe `CPF` no backend.
- A validação de segurança e das regras de negócio deve ocorrer no backend mesmo que o JavaScript esteja desabilitado ou seja manipulado.
- Cada template deve carregar os arquivos compartilhados por `url_for('static', filename=...)`, evitando duplicação de CSS e JavaScript por página.

---

## Regras de Negócio e Segurança de Transação
1. **Validação de Saldo**: O remetente nunca pode transferir um valor superior ao seu saldo disponível.
2. **Atomicidade (ACID)**: A operação de transferência (débito + crédito + histórico) deve ocorrer dentro de um mesmo bloco de transação do banco.
3. **Prevenção de Autotransferência**: Um usuário não pode realizar transferências para a própria conta.
4. **Mensagens de Feedback**: A View deve exibir mensagens amigáveis em caso de erro (ex: "Saldo insuficiente", "Conta de destino não encontrada") ou sucesso.
5. **Autenticação por CPF**: O CPF é o único identificador permitido no formulário e no endpoint de login. Deve ser normalizado para 11 dígitos, validado pelos dígitos verificadores com `CPF` e protegido por restrição de unicidade no banco.
6. **Proteção de Senhas**: A senha nunca pode ser armazenada ou registrada em texto puro. O cadastro deve gerar um hash BCrypt com fator de custo adequado, e o login deve verificar o hash com uma função segura de comparação.
7. **Política de Senha**: A senha deve ter no mínimo 6 caracteres, não conter espaços e aceitar letras maiúsculas, letras minúsculas, números e caracteres especiais.
8. **Sessão e Segredos**: Usar uma `SECRET_KEY` forte fora do código-fonte em ambientes reais, definir atributos seguros dos cookies de sessão e invalidar a sessão no logout.
9. **Integridade Monetária**: Usar `Numeric(12, 2)` para saldo e transferências, validar valores positivos na aplicação e manter as mesmas restrições no banco.
10. **Integridade Referencial**: Toda transação deve apontar para usuários existentes, e consultas do extrato devem usar os relacionamentos de origem e destino.
11. **Concorrência**: A transferência deve bloquear a operação de escrita durante a leitura e atualização dos saldos, evitando condições de corrida e saldo utilizado por operações simultâneas.
12. **Precisão Numérica**: Usar `Decimal` no código Python e `Numeric(12, 2)` no banco; valores monetários não podem ser calculados com `float`.
13. **Exclusão de Dados**: Não excluir fisicamente usuários que possuam transações; o comportamento padrão deve preservar o histórico por meio de `RESTRICT`.
14. **SQLite**: A conexão deve habilitar `PRAGMA foreign_keys = ON` para que as restrições referenciais sejam efetivas.
15. **Data e Hora**: Persistir `data_hora` em UTC e realizar a conversão de fuso horário somente na interface.
16. **Dados de Demonstração**: Os 10 usuários iniciais devem ser fictícios, idempotentes e limitados ao ambiente de desenvolvimento, sem alterar usuários já existentes nem criar duplicidades.
17. **Senha**: Exigir no mínimo 6 caracteres, sem espaços, permitindo maiúsculas, minúsculas, números e caracteres especiais.
18. **Transferência**: Localizar o destinatário exclusivamente pelo CPF, aceitar valor mínimo de `0.01`, não impor limite máximo além do saldo disponível e rejeitar saldo insuficiente.
19. **Feedback Demonstrativo**: Para fins acadêmicos, informar separadamente quando o CPF não existe e quando a senha está incorreta, apesar de essa distinção reduzir a proteção contra enumeração.
20. **Usuários Cadastrados**: Permitir a usuários autenticados consultar a lista de usuários, exibindo CPF integralmente nesta versão demonstrativa; nunca exibir senhas, hashes ou dados secretos.
21. **Proteção Web**: Implementar CSRF nos formulários, cookies `HttpOnly` e `SameSite`, `Secure` quando executado sob HTTPS, redirecionamento de não autenticados, bloqueio de páginas de autenticação para usuários logados, logout via `POST` e limitação básica de tentativas de login.
22. **Banco de Dados**: Manter SQLite e o bloqueio de escrita durante transferências; essa escolha é aceitável para a demonstração, mas deve ser reavaliada se a concorrência real superar poucos usuários e poucas solicitações por minuto.
23. **Apresentação**: Usar português brasileiro, valores monetários no formato `R$ 1.234,56`, identidade visual “Quantium Bank”, tema escuro high-tech e cores neon/LED. Priorizar desktop nesta versão, sem exigir otimização específica para celulares.
24. **Testes**: Criar somente testes unitários, sem testes de rotas, cobrindo validação de CPF, política de senha, cadastro, autenticação, CPF duplicado, transferências válidas e inválidas, saldo insuficiente, autotransferência, precisão monetária, rollback e erros de banco.

---

## Diretrizes para o Copilot / Assistente de Código
- Escreva o código utilizando práticas limpas, legíveis e alinhadas ao **PEP 8**.
- Garanta a separação estrita de responsabilidades entre `model.py`, `controller.py`, `server.py` e os templates `.html`.
- Adicione comentários curtos explicando a lógica de transação atômica e as validações de regra de negócio no `controller.py`.
- Utilize `bcrypt` ou `Flask-Bcrypt` e registre a dependência no `requirements.txt`; não implemente o algoritmo de hash manualmente.
- Reutilize a classe `CPF` de `app/objects/cpf.py` como objeto de valor, mantendo o valor persistido sem pontuação e evitando duplicidade.
- Trate erros de CPF duplicado e falhas de banco explicitamente, com mensagens apropriadas e rollback quando necessário.
- Mantenha `README.md` fora do escopo inicial; documentá-lo após a implementação e a primeira fase de testes.

## Diretrizes de Complexidade e Estilo
- Priorizar o funcionamento correto, a segurança, a organização e a legibilidade do backend, pois a lógica de negócio é o foco principal do projeto acadêmico.
- Utilizar recursos idiomáticos do Python e funcionalidades da linguagem quando tornarem o código mais claro, seguro ou fácil de manter.
- Manter a complexidade proporcional ao escopo: evitar abstrações, otimizações, padrões e fluxos excessivamente sofisticados quando não forem necessários.
- Preferir código explícito e didático, com responsabilidades bem separadas, nomes claros e comentários somente quando ajudarem a explicar decisões não óbvias.
- No frontend, investir em uma experiência visual mais elaborada e fluida, sem comprometer acessibilidade, responsividade, desempenho ou clareza de uso.
- Adotar uma identidade visual em modo escuro, com estética high-tech e cores vibrantes inspiradas em LEDs/neon, mantendo contraste suficiente para leitura.
- Usar animações e interações moderadas para melhorar a experiência, evitando efeitos que prejudiquem usabilidade, acessibilidade ou compreensão das mensagens do sistema.
```