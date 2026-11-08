# Proposta de evolução — Quantium Bank 1.1.0

> Status: implementação em andamento, com os itens descritos abaixo já incorporados ao código.

## Objetivo

Evoluir o cadastro do Quantium Bank para coletar informações adicionais do usuário, reforçar as validações de entrada e apresentar uma página **Meu Perfil** com os dados cadastrados. A versão 1.1.0 mantém o escopo acadêmico do projeto e não pretende transformar o sistema em uma instituição financeira real.

Os dados exibidos em **Meu Perfil** serão somente para leitura nesta versão. Não haverá edição de dados pessoais ou alteração de senha pelo perfil.

## Dados adicionais do cadastro

O formulário de cadastro deverá conter os seguintes campos:

- Nome completo.
- CPF.
- E-mail.
- Telefone.
- Data de nascimento.
- Senha.
- Confirmação de senha.

O CPF continuará sendo o identificador de autenticação e deverá preservar o comportamento já existente de normalização, validação e unicidade.

## Regras de validação

### Nome completo

- Remover espaços excedentes no início, no fim e entre as palavras.
- Exigir pelo menos duas partes no nome, representando nome e sobrenome.
- Rejeitar um cadastro composto somente por um nome.
- Aceitar somente letras, incluindo caracteres acentuados, e espaços.
- Normalizar a apresentação para capitalização de nome, evitando CAPS LOCK.
- Aplicar limite de tamanho compatível com o banco e com a interface.
- Preservar a validação no backend mesmo quando houver validação no frontend.

### E-mail

- Validar o formato estrutural de um endereço de e-mail.
- Aceitar somente caracteres usuais na parte local: letras, números, ponto, sublinhado, porcentagem, mais e hífen.
- Rejeitar símbolos incomuns, como `#`.
- Não exigir confirmação de existência ou envio de mensagem.
- Normalizar o valor para minúsculas antes de persistir.
- Impedir e-mails duplicados entre usuários.
- Exibir mensagens claras quando o formato for inválido ou o e-mail já estiver cadastrado.

### Telefone

- Aceitar somente números de celular brasileiros com DDD.
- Validar o DDD conforme a faixa de códigos disponível no Brasil.
- Exigir onze dígitos: DDD mais número de celular iniciado por `9`.
- Permitir entrada com máscara, mas persistir somente os onze dígitos normalizados.
- Rejeitar telefones fixos, números incompletos, com quantidade inválida de dígitos ou estrutura incompatível.

### Data de nascimento

- Aceitar uma data válida no formato apresentado pela interface.
- Persistir o valor como data, sem tratar a data como texto livre.
- Exigir idade mínima de 18 anos na data do cadastro.
- Rejeitar datas futuras.
- Considerar o aniversário do usuário no cálculo da idade, evitando aceitar alguém que ainda não completou 18 anos.

### Senha e confirmação

- Exigir pelo menos seis caracteres, com letras, números e caracteres especiais permitidos.
- Permitir somente letras ASCII, números e os caracteres `! @ # $ % ^ & * ( ) _ + - = [ ] { } ; : , . ?`.
- Rejeitar espaços, caracteres acentuados e símbolos fora da lista.
- Adicionar um campo de confirmação de senha.
- Validar no frontend se os dois valores são iguais para feedback imediato.
- Repetir a comparação no backend antes de criar o usuário.
- Nunca persistir a senha ou a confirmação em texto puro.
- Adicionar controles independentes para mostrar ou ocultar cada campo de senha.

## Página Meu Perfil

Adicionar uma página autenticada acessível pelo usuário após o login, contendo:

- Nome completo.
- CPF.
- E-mail.
- Telefone.
- Data de nascimento.
- Data de cadastro, quando disponível.
- Resumo visual da conta, sem permitir alterações.

### Restrições da primeira versão

- Todos os campos serão somente leitura.
- Não haverá formulário de edição.
- Não haverá alteração de senha nessa página.
- O CPF continuará sendo apenas informativo e não poderá ser alterado.
- O acesso deverá exigir uma sessão autenticada.
- Um usuário não poderá consultar o perfil de outro usuário pela URL.
- Sessões que apontarem para usuários removidos serão invalidadas e redirecionadas ao login.

## Controle de inclusão e alteração

Adicionar timestamps automáticos aos registros de usuário:

- `created_at`: data e hora de criação do registro.
- `updated_at`: data e hora da última atualização do registro.

Os campos são preenchidos e atualizados pelo backend usando UTC. Datas e horários são convertidos para o timezone de apresentação configurado em `DISPLAY_TIMEZONE`, com padrão `America/Sao_Paulo`. A conversão é aplicada ao horário de cadastro do perfil e aos horários exibidos no extrato. Nesta versão, a existência de `updated_at` prepara o modelo para futuras edições, mesmo que o perfil permaneça somente leitura.

## Modelo de dados

O modelo `Usuario` deverá ser ampliado com:

- E-mail.
- Telefone.
- Data de nascimento.
- `created_at`.
- `updated_at`.

As regras de unicidade e os limites de tamanho devem ser refletidos tanto nas validações da aplicação quanto nas restrições apropriadas do banco de dados.

Como o projeto ainda não possui banco de produção, a evolução poderá ser aplicada no ambiente local de desenvolvimento com o fluxo já existente de recriação e seed. Os dados fictícios do seed deverão ser atualizados para preencher os novos campos com valores válidos.

Os campos do modelo possuem comentários descritivos no SQLAlchemy para documentar sua finalidade. O SQLite não persiste comentários de colunas diretamente no arquivo `.db`, mas o metadata do modelo os mantém disponíveis.

## Interface e experiência do usuário

- Atualizar o formulário de cadastro para incluir os novos campos.
- Aplicar máscara progressiva ao CPF no login, cadastro e transferência, aceitando somente dígitos e mantendo um valor oculto normalizado para o envio.
- Permitir somente dígitos no campo de telefone, aplicar automaticamente a máscara `(DD) 9XXXX-XXXX` e remover a máscara antes do envio.
- Abrir o parêntese do telefone desde o primeiro dígito e fechar após o DDD para acompanhar a digitação.
- Filtrar e normalizar nome, e-mail, telefone, CPF e senhas no frontend sem substituir a validação do backend.
- Exibir mensagens de validação próximas aos campos correspondentes.
- Indicar visualmente quando a confirmação de senha não corresponde à senha.
- Adicionar botão de mostrar/ocultar senha para senha e confirmação.
- Adicionar um item de navegação para **Meu Perfil**.
- Manter a identidade visual dark/high-tech do Quantium Bank.
- Garantir que o formulário continue utilizável em telas menores.

## Testes previstos

Criar ou atualizar testes automatizados para cobrir:

- Nome sem sobrenome.
- Nome completo válido.
- Nome com números ou símbolos.
- Normalização de nome em diferentes capitalizações.
- E-mail válido e inválido.
- E-mail com caracteres incomuns.
- E-mail duplicado.
- Telefone brasileiro válido.
- Telefone fixo.
- DDD inválido.
- Telefone incompleto ou com estrutura inválida.
- Data inválida.
- Data futura.
- Usuário com menos de 18 anos.
- Usuário que já completou 18 anos.
- Senhas diferentes.
- Cadastro válido com confirmação correta.
- Persistência dos novos campos.
- Preenchimento de `created_at` e `updated_at`.
- Acesso autenticado à página Meu Perfil.
- Bloqueio de acesso anônimo ao perfil.
- Exibição dos dados sem possibilidade de edição.
- Conversão de UTC para o timezone de apresentação.
- Limpeza de sessão órfã.
- Comentários definidos no metadata das colunas.

## Fora do escopo da 1.1.0

Não fazem parte desta atualização:

- E-mail de confirmação ou recuperação de senha.
- Validação de telefone por SMS ou ligação.
- Alteração de dados pessoais.
- Alteração de senha pelo perfil.
- Upload de foto ou avatar.
- Endereço residencial.
- Integração com serviços externos.
- Migração para PostgreSQL ou outro banco hospedado.
- Múltiplos tipos de conta.
- Funcionalidades financeiras reais.

## Resultado esperado

Ao final da versão 1.1.0, o Quantium Bank deverá oferecer um cadastro mais completo e confiável, com validações adequadas para dados pessoais brasileiros, confirmação de senha, controle básico de auditoria e uma página de perfil informativa. A atualização deverá melhorar a percepção de completude do sistema sem comprometer a simplicidade, a segurança e a coerência do projeto acadêmico.
