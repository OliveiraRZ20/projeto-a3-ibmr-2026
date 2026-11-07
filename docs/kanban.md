PROJETO: Quantium Bank — Sistema Bancário Web

EQUIPE:
- Product Owner (PO): Nathália Granater
- Scrum Master (SM): Lucca Oliveira
- Developer Front-End: Derek Pontes
- Developer Back-End: Vinícius Mousinho

METODOLOGIA:
O projeto será organizado em um quadro Kanban com as colunas:
Backlog → A Fazer → Em Desenvolvimento → Em Revisão → Concluído.

O trabalho será dividido em quatro sprints incrementais. Ao final de cada sprint, deverá existir uma entrega funcional e demonstrável.

==================================================
SPRINT 1 — PLANEJAMENTO E ESTRUTURAÇÃO
Objetivo: definir o produto e preparar a base técnica do projeto.

ATIVIDADES:
S1-01 — Definir a proposta do Quantium Bank
Responsável: PO
Descrição: Documentar o problema, o público-alvo e as principais funcionalidades do sistema bancário.

S1-02 — Levantar e priorizar requisitos
Responsável: PO
Descrição: Definir cadastro, login por CPF, saldo, extrato, transferências e listagem de usuários.

S1-03 — Organizar o backlog do produto
Responsável: PO e SM
Descrição: Criar e priorizar as histórias de usuário e os critérios de aceitação.

S1-04 — Definir o planejamento das quatro sprints
Responsável: SM
Descrição: Distribuir as atividades, estabelecer prazos e organizar o fluxo do Kanban.

S1-05 — Definir arquitetura de arquivos e tecnologias
Responsável: SM e Dev Back-End
Descrição: Confirmar Flask, SQLAlchemy, SQLite, BCrypt, estrutura MVC e organização do projeto.

S1-06 — Configurar o ambiente de desenvolvimento
Responsável: Dev Back-End
Descrição: Configurar Python, ambiente virtual, dependências, Replit e execução inicial do projeto.

S1-07 — Criar o esqueleto inicial da aplicação
Responsável: Dev Back-End
Descrição: Criar os diretórios, módulos, templates, arquivos estáticos e estrutura de testes.

S1-08 — Criar identidade visual inicial
Responsável: Dev Front-End
Descrição: Definir cores, tipografia, componentes e referências visuais do Quantium Bank.

ENTREGA DA SPRINT 1:
- Requisitos priorizados.
- Backlog inicial.
- Arquitetura definida.
- Ambiente configurado.
- Estrutura inicial do projeto.
- Identidade visual estabelecida.

==================================================
SPRINT 2 — BACK-END E AUTENTICAÇÃO
Objetivo: implementar a estrutura de dados, cadastro e autenticação dos usuários.

ATIVIDADES:
S2-01 — Criar os modelos do banco de dados
Responsável: Dev Back-End
Descrição: Implementar as tabelas Usuario e Transacao com relacionamentos e restrições.

S2-02 — Implementar validação de CPF
Responsável: Dev Back-End
Descrição: Integrar a classe CPF, validar dígitos verificadores e garantir unicidade.

S2-03 — Implementar política de senhas
Responsável: Dev Back-End
Descrição: Validar senhas com no mínimo seis caracteres, sem espaços, e gerar hashes BCrypt.

S2-04 — Implementar cadastro de usuários
Responsável: Dev Back-End
Descrição: Criar o fluxo de registro com validações, mensagens de erro e tratamento de CPF duplicado.

S2-05 — Implementar login por CPF
Responsável: Dev Back-End
Descrição: Criar autenticação exclusivamente por CPF e senha, utilizando sessão Flask.

S2-06 — Implementar logout e proteção de sessão
Responsável: Dev Back-End
Descrição: Encerrar sessões, proteger rotas privadas e redirecionar usuários não autenticados.

S2-07 — Criar seed com usuários de demonstração
Responsável: Dev Back-End
Descrição: Criar dez usuários fictícios com CPFs válidos, senhas demonstrativas e saldos variados.

S2-08 — Implementar testes unitários iniciais
Responsável: Dev Back-End
Descrição: Testar CPF, senha, cadastro, autenticação e duplicidade de usuários.

S2-09 — Revisar critérios de aceitação
Responsável: PO e SM
Descrição: Verificar se os fluxos de cadastro e login atendem aos requisitos definidos.

ENTREGA DA SPRINT 2:
- Banco de dados funcional.
- Cadastro de usuários.
- Login e logout por CPF.
- Senhas protegidas com BCrypt.
- Seed de demonstração.
- Testes unitários iniciais.

==================================================
SPRINT 3 — OPERAÇÕES BANCÁRIAS E INTERFACE
Objetivo: implementar saldo, extrato, transferências e as páginas principais.

ATIVIDADES:
S3-01 — Criar página de login
Responsável: Dev Front-End
Descrição: Desenvolver a interface de login por CPF e senha.

S3-02 — Criar página de cadastro
Responsável: Dev Front-End
Descrição: Desenvolver o formulário de registro com validações visuais.

S3-03 — Criar dashboard
Responsável: Dev Front-End
Descrição: Exibir saldo, informações do usuário e histórico de transações.

S3-04 — Criar página de transferências
Responsável: Dev Front-End
Descrição: Criar formulário para transferência utilizando exclusivamente o CPF do destinatário.

S3-05 — Criar estilo visual Quantium Bank
Responsável: Dev Front-End
Descrição: Implementar tema escuro, estética high-tech, cores neon/LED, mensagens e componentes visuais.

S3-06 — Implementar saldo e extrato
Responsável: Dev Back-End
Descrição: Exibir saldo atual e listar transações enviadas e recebidas.

S3-07 — Implementar transferência bancária
Responsável: Dev Back-End
Descrição: Validar destinatário, valor mínimo de R$ 0,01, saldo disponível e autotransferência.

S3-08 — Garantir atomicidade da transferência
Responsável: Dev Back-End
Descrição: Executar débito, crédito e registro da transação em uma única operação de banco.

S3-09 — Implementar listagem de usuários
Responsável: Dev Back-End
Descrição: Criar área autenticada para visualizar usuários cadastrados, com busca e paginação.

S3-10 — Implementar JavaScript compartilhado
Responsável: Dev Front-End
Descrição: Criar máscara de CPF, validações auxiliares, confirmação de transferência e interações da interface.

S3-11 — Integrar front-end e back-end
Responsável: Dev Front-End e Dev Back-End
Descrição: Conectar formulários, rotas, mensagens e dados reais do banco.

ENTREGA DA SPRINT 3:
- Sistema visual navegável.
- Dashboard funcional.
- Extrato bancário.
- Transferências entre usuários.
- Listagem de usuários.
- Integração entre frontend, backend e banco.

==================================================
SPRINT 4 — TESTES, REVISÃO E ENTREGA
Objetivo: validar o funcionamento completo e preparar a apresentação.

ATIVIDADES:
S4-01 — Testar transferências válidas
Responsável: Dev Back-End
Descrição: Verificar débito, crédito e registro correto no extrato.

S4-02 — Testar regras de erro
Responsável: Dev Back-End
Descrição: Testar saldo insuficiente, CPF inexistente, valor inválido e autotransferência.

S4-03 — Testar atomicidade e rollback
Responsável: Dev Back-End
Descrição: Garantir que falhas não deixem alterações parciais no banco.

S4-04 — Completar testes unitários de negócio
Responsável: Dev Back-End
Descrição: Cobrir as principais regras que podem causar falhas no sistema.

S4-05 — Revisar interface e experiência do usuário
Responsável: Dev Front-End
Descrição: Ajustar layout, mensagens, contraste, navegação e consistência visual.

S4-06 — Validar responsividade básica e acessibilidade
Responsável: Dev Front-End
Descrição: Garantir legibilidade, navegação clara e uso adequado dos componentes.

S4-07 — Realizar revisão geral do sistema
Responsável: SM
Descrição: Conferir o Kanban, critérios de aceitação, pendências e integração das entregas.

S4-08 — Realizar validação final do produto
Responsável: PO
Descrição: Verificar se o sistema atende aos requisitos e objetivos definidos.

S4-09 — Preparar demonstração
Responsável: Toda a equipe
Descrição: Organizar o roteiro de apresentação, usuários demonstrativos e principais funcionalidades.

S4-10 — Preparar explicação da dinâmica do projeto
Responsável: SM
Descrição: Explicar a proposta, organização da equipe, funcionamento do Kanban e evolução das sprints.

S4-11 — Criar versão final para entrega
Responsável: SM e toda a equipe
Descrição: Conferir arquivos, testes, configuração, execução e materiais da apresentação.

ENTREGA DA SPRINT 4:
- Sistema validado.
- Testes unitários concluídos.
- Interface revisada.
- Fluxos principais funcionando.
- Demonstração preparada.
- Apresentação final organizada.

==================================================
RESPONSABILIDADES GERAIS

PRODUCT OWNER — Nathália Granater:
- Definir e priorizar requisitos.
- Representar os objetivos do produto.
- Validar as entregas.
- Confirmar se as funcionalidades atendem ao escopo.

SCRUM MASTER — Lucca Oliveira:
- Organizar o Kanban e as sprints.
- Acompanhar o andamento das atividades.
- Facilitar a comunicação da equipe.
- Remover impedimentos.
- Explicar a dinâmica do projeto na apresentação.

DEVELOPER FRONT-END — Derek Pontes:
- Desenvolver templates HTML.
- Criar estilos CSS e identidade visual.
- Implementar JavaScript e interações.
- Integrar a interface com as rotas do sistema.

DEVELOPER BACK-END — Vinícius Mousinho:
- Implementar modelos e banco de dados.
- Criar regras de negócio e rotas.
- Implementar autenticação e transferências.
- Criar seeds e testes unitários.

FLUXO DE TRABALHO:
1. A atividade é retirada do Backlog.
2. O responsável move a atividade para A Fazer.
3. Durante a execução, a atividade vai para Em Desenvolvimento.
4. Após concluída, passa para Em Revisão.
5. Depois da validação, é movida para Concluído.
6. O SM acompanha o fluxo e evita acúmulo de tarefas.
7. O PO valida se a entrega atende aos critérios de aceitação.
