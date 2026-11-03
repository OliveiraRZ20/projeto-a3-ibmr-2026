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