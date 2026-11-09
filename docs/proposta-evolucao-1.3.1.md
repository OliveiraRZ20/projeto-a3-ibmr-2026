# Proposta de evolução — Quantium Bank 1.3.1

> Status: implementada.

## Objetivo

Organizar a arquitetura do Quantium Bank como um pacote Python executável,
centralizando os comandos operacionais em uma única interface de linha de
comando. A versão 1.3.1 deverá permitir executar diferentes ações do sistema
por meio de `python -m quantium_bank`, sem misturar a definição dos comandos
com as regras de negócio da aplicação.

A evolução deverá melhorar a organização do código, a reutilização das
operações, a testabilidade e a experiência de desenvolvimento, preservando o
comportamento atual da aplicação web.

## Arquitetura proposta

O diretório `app/` deverá ser renomeado para `quantium_bank/`, transformando-se
no pacote principal da aplicação:

```text
quantium_bank/
├── __init__.py
├── __main__.py
├── cli/
│   ├── __init__.py
│   ├── run.py
│   ├── seed.py
│   ├── reset_db.py
│   └── admin.py
├── server_service.py
├── seed_service.py
├── database_service.py
├── admin_service.py
├── models.py
├── routes.py
├── services.py
├── time.py
├── objects/
├── templates/
└── static/
```

Os scripts atualmente existentes na raiz (`run.py`, `seed.py`, `reset_db.py` e
`admin.py`) deverão ser migrados para módulos equivalentes dentro de
`quantium_bank/cli/` ou para módulos de caso de uso do pacote, conforme sua
responsabilidade. Após a validação da migração, os arquivos da raiz deverão ser
removidos, evitando duas entradas oficiais para a mesma operação.

## Interface de comandos

O pacote deverá aceitar subcomandos:

```powershell
python -m quantium_bank run
python -m quantium_bank seed
python -m quantium_bank reset-db
python -m quantium_bank admin promover --cpf 21618722069
python -m quantium_bank admin criar --nome "Nome do Administrador"
```

Os nomes e opções finais deverão seguir os argumentos já suportados pelos
scripts existentes, evitando mudanças desnecessárias na operação atual.

### Responsabilidades do `__main__.py`

O `__main__.py` deverá:

- ser o ponto de entrada de `python -m quantium_bank`;
- configurar o parser principal e os subcomandos;
- encaminhar cada comando para seu módulo responsável;
- retornar códigos de saída apropriados;
- exibir mensagens claras para comandos inválidos ou falhas operacionais;
- não conter regras financeiras, acesso direto desnecessário ao banco ou
  lógica extensa de seed.

O parser poderá utilizar `argparse`, sem introduzir uma dependência externa
apenas para a CLI.

### Responsabilidades dos módulos de comando

Cada módulo em `quantium_bank/cli/` deverá coordenar uma operação específica:

- `run.py`: criar a aplicação e iniciar o servidor de desenvolvimento;
- `seed.py`: executar a seed utilizando os serviços e configurações existentes;
- `reset_db.py`: recriar o banco no ambiente permitido;
- `admin.py`: criar ou promover administradores usando as validações existentes.

Os módulos de comando deverão ser pequenos e delegar as regras de negócio para
serviços, modelos ou módulos de infraestrutura apropriados.

## Separação entre CLI e regras de negócio

A CLI não deverá duplicar validações nem implementar regras financeiras. As
operações deverão ser expostas por funções reutilizáveis, por exemplo:

```python
def seed_database() -> None:
    ...


def reset_database() -> None:
    ...


def promote_admin(cpf: str) -> None:
    ...
```

Essas funções deverão poder ser chamadas pelos comandos e pelos testes sem
depender da simulação de argumentos de terminal.

Quando necessário, módulos específicos como `database_service.py`,
`seed_service.py` ou `admin_service.py` poderão ser criados dentro do pacote para separar infraestrutura e
casos de uso dos adaptadores da CLI. Os nomes deverão evitar conflito entre o
módulo de negócio e o módulo de comando.

## Execução da aplicação

O fluxo principal deverá passar a ser:

```powershell
.\.venv\Scripts\python.exe -m quantium_bank run
```

O comando deverá preservar:

- a criação da aplicação Flask pela factory existente;
- as configurações de desenvolvimento atuais;
- a porta e o modo de execução atuais, salvo quando informados por flags;
- a inicialização correta do banco e da seed automática;
- o comportamento de autenticação, autorização e sessões.

Flags opcionais poderão ser adicionadas de forma compatível, como `--host`,
`--port` e `--debug`, desde que tenham valores padrão equivalentes aos atuais.

## Compatibilidade de migração

Durante a transição:

- imports internos deverão apontar para `quantium_bank`;
- testes deverão utilizar o novo caminho do pacote;
- templates, arquivos estáticos e configuração Flask deverão continuar sendo
  encontrados corretamente;
- o README deverá documentar a nova forma recomendada de execução;
- os comandos documentados deverão ser atualizados para
  `python -m quantium_bank ...`;
- `python -m seed` e a execução direta dos scripts antigos deixarão de ser a
  forma suportada após a migração;
- não deverá haver cópia divergente da lógica entre módulos do pacote.

## Configuração do Pylance

Após a reorganização, a configuração do workspace poderá restringir a análise
ao pacote principal, aos testes e aos pontos de entrada:

```json
"python.analysis.include": [
    "quantium_bank",
    "tests",
    "*.py"
]
```

O `include` deverá ser adotado somente depois da migração dos arquivos, para
evitar que módulos ainda localizados em `app/` ou scripts não migrados deixem
de ser analisados.

## Testes e validação previstos

Criar ou atualizar testes para cobrir:

- execução de `python -m quantium_bank --help`;
- reconhecimento dos subcomandos disponíveis;
- rejeição de comandos e argumentos inválidos;
- execução do comando `run` com os valores padrão;
- encaminhamento de `seed`, `reset-db` e `admin`;
- códigos de saída em sucesso e falha;
- propagação clara de erros operacionais;
- equivalência entre os comandos novos e os scripts atuais durante a migração;
- ausência dos scripts operacionais antigos na raiz após a migração;
- descoberta dos templates e arquivos estáticos após a renomeação do pacote;
- preservação de todos os testes de autenticação, transferências, seed e painel
  administrativo.

A suíte existente deverá continuar passando integralmente:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Também deverá ser validado manualmente:

```powershell
.\.venv\Scripts\python.exe -m quantium_bank --help
.\.venv\Scripts\python.exe -m quantium_bank seed
.\.venv\Scripts\python.exe -m quantium_bank reset-db
```

## Fora do escopo da 1.3.1

Não fazem parte desta atualização:

- alteração das regras de negócio bancárias;
- mudança no modelo de dados ou criação de novas tabelas;
- migração para outro framework web;
- introdução de Click, Typer ou outra dependência de CLI sem necessidade;
- criação de um sistema de plugins;
- empacotamento para publicação no PyPI;
- alteração do comportamento de produção;
- inclusão de novos recursos financeiros;
- reescrita visual da aplicação.

## Critérios de aceite

A evolução será considerada concluída quando:

1. `quantium_bank` for o pacote principal da aplicação.
2. `python -m quantium_bank --help` apresentar a CLI centralizada.
3. Os comandos principais estiverem separados em módulos próprios.
4. O `__main__.py` não concentrar regras de negócio.
5. Seed, reset e administração reutilizarem funções testáveis.
6. `run.py`, `seed.py`, `reset_db.py` e `admin.py` não existirem mais na raiz.
7. Os fluxos existentes continuarem funcionando durante a migração.
8. A suíte automatizada passar sem regressões.
9. O README e a configuração do projeto refletirem a nova arquitetura.
