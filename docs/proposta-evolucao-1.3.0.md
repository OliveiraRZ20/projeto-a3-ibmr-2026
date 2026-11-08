# Proposta de evolução — Quantium Bank 1.3.0

> Status: implementada.

## Objetivo

Renovar a identidade visual do Quantium Bank para oferecer uma experiência
moderna, consistente e responsiva em todas as telas da aplicação. A versão
1.3.0 terá foco visual e de experiência do usuário, preservando a arquitetura
Flask, Jinja, CSS e JavaScript existente.

A atualização deverá combinar **Glassmorphism moderno** e **Soft UI**, sem
transformar o projeto em uma SPA e sem substituir o backend, as rotas, os
serviços ou o modelo de dados atuais.

## Diretrizes visuais

### Glassmorphism e Soft UI

Os cards, painéis e containers deverão utilizar:

- Fundos translúcidos ou semitransparentes.
- Desfoque de fundo com `backdrop-filter`, quando suportado.
- Bordas arredondadas pronunciadas.
- Bordas sutis e semitransparentes.
- Sombras amplas, suaves e de baixa opacidade.
- Hierarquia visual baseada em camadas e profundidade.
- Fallback visual adequado para navegadores sem suporte a blur.

### Paleta e fundos

A identidade atual dark/high-tech deverá evoluir para uma composição mais
sofisticada, mantendo o contraste e a personalidade do Quantium Bank:

- Fundo escuro neutro como base.
- Mesh gradients suaves e difusos.
- Combinação de verde-azulado, menta, azul-turquesa e lilás.
- Acentos neon usados com moderação.
- Cards em tons escuros translúcidos.
- Cores específicas para sucesso, alerta e erro.

Os gradientes não deverão prejudicar a legibilidade nem o contraste dos textos.

### Tipografia e hierarquia

A interface deverá adotar uma tipografia sans-serif moderna e limpa, utilizando
uma fonte disponível no ambiente ou uma alternativa segura do sistema.

Deverá haver distinção clara entre:

- Títulos de página.
- Títulos de seção.
- Rótulos de métricas.
- Valores principais.
- Dados secundários.
- Mensagens de estado.

Textos secundários poderão utilizar opacidade reduzida, desde que permaneçam
legíveis e acessíveis.

## Componentes a renovar

Criar padrões visuais reutilizáveis para:

- Layout global e navegação.
- Cards de métricas.
- Cards de saldo.
- Containers de conteúdo.
- Botões primários, secundários e de link.
- Campos de formulário.
- Campos de senha e controles de visibilidade.
- Badges e indicadores de status.
- Alertas e mensagens flash.
- Tabelas administrativas.
- Listas de transações.
- Paginação.
- Estados vazios.
- Cabeçalhos de seção.

Os padrões deverão ser implementados no CSS compartilhado, evitando estilos
duplicados entre templates.

## Telas abrangidas

### Layout global

Atualizar `base.html` e o CSS compartilhado para:

- Aplicar a nova identidade visual em toda a aplicação.
- Melhorar a navegação em desktop e telas menores.
- Destacar a página ativa.
- Organizar o menu administrativo sem quebrar a navegação comum.
- Fazer o conteúdo ocupar adequadamente a viewport.
- Manter o logout via `POST` e a proteção CSRF.

### Autenticação

Renovar as telas de login e cadastro com:

- Cards de autenticação glassmorphism.
- Campos e mensagens de validação mais claros.
- Hierarquia visual mais objetiva.
- Estados de foco, erro e sucesso.
- Layout responsivo.

### Área autenticada

Atualizar dashboard, perfil, usuários e transferência com:

- Containers e cards consistentes.
- Melhor destaque para saldo e ações principais.
- Histórico de movimentações mais legível.
- Estados vazios visualmente claros.
- Formulários com melhor agrupamento.
- CPF, valores monetários e datas com apresentação consistente.

### Painel administrativo

Modernizar o painel administrativo com:

- Cards de métricas com hierarquia visual clara.
- Valores monetários sem quebra inadequada.
- Tabela administrativa alinhada por colunas.
- Badges para perfis e estados.
- Filtros organizados.
- Paginação consistente.
- Responsividade para tablets e celulares.

## Microinterações

Adicionar interações sutis usando CSS e JavaScript nativo:

- Elevação leve dos cards no hover.
- Brilho discreto nas bordas.
- Transições suaves em botões e links.
- Animação de entrada dos principais componentes.
- Feedback visual ao focar ou enviar formulários.
- Estados de carregamento quando aplicável.
- Respeito à preferência `prefers-reduced-motion`.

As animações deverão ser rápidas, discretas e não poderão dificultar o uso da
interface ou causar distração excessiva.

Não será adotado React ou Framer Motion nesta versão. Os efeitos deverão ser
implementados com CSS moderno e JavaScript nativo para preservar a arquitetura,
o fluxo de renderização Jinja e a simplicidade operacional do projeto.

## Ícones e elementos visuais

Os ícones deverão ser minimalistas e consistentes. Poderá ser adotada uma
biblioteca leve de ícones ou SVGs locais, desde que:

- Não sejam introduzidas dependências desnecessárias.
- Os ícones tenham significado complementar ao texto.
- Haja texto alternativo ou acessibilidade apropriada.
- O uso de ícones não substitua informações essenciais.

## Responsividade

A interface deverá ser validada em:

- Monitores e notebooks.
- Telas ultrawide.
- Tablets.
- Celulares.

O layout deverá:

- Usar a largura disponível sem esticar excessivamente o conteúdo.
- Reorganizar grids e tabelas em telas menores.
- Evitar overflow horizontal não intencional.
- Preservar a leitura de valores monetários longos.
- Manter controles de formulário utilizáveis por toque.
- Ajustar a navegação para larguras reduzidas.

## Acessibilidade

A renovação visual deverá preservar e melhorar:

- Contraste entre texto e fundo.
- Foco visível via teclado.
- Ordem lógica de navegação.
- Labels associados aos campos.
- Mensagens compreensíveis para erros e estados.
- Uso sem depender exclusivamente de cor.
- Respeito a `prefers-reduced-motion`.
- Legibilidade em diferentes tamanhos de tela.

O efeito de transparência não deverá comprometer a leitura do conteúdo.

## Compatibilidade e arquitetura

A evolução deverá preservar:

- Flask e Jinja como tecnologias de apresentação.
- Um CSS compartilhado em `app/static/css/style.css`.
- Um JavaScript compartilhado em `app/static/js/app.js`.
- A separação entre templates, rotas, serviços e modelos.
- O comportamento atual de autenticação e autorização.
- A proteção CSRF.
- A formatação de CPF, moeda e datas.
- O painel administrativo somente leitura.
- A funcionalidade da seed dinâmica.
- O suporte aos mesmos fluxos de desenvolvimento.

Não fazem parte desta evolução:

- Migração do frontend para React.
- Introdução de uma SPA.
- Alteração do banco de dados.
- Alteração das regras de negócio.
- Mudança no fluxo de autenticação.
- Criação de um design system externo obrigatório.

## Testes e validação previstos

Validar a evolução por meio de:

- Execução da suíte automatizada existente.
- Verificação de que nenhuma rota ou formulário perdeu funcionalidade.
- Validação visual das telas principais em diferentes larguras.
- Testes de navegação por teclado.
- Verificação de foco visível.
- Verificação de contraste e legibilidade.
- Verificação de `prefers-reduced-motion`.
- Verificação de overflow em valores monetários e textos longos.
- Verificação da responsividade das tabelas administrativas.
- Verificação de que mensagens flash continuam visíveis e compreensíveis.

Quando possível, a validação visual deverá ser feita com capturas das telas
principais em desktop, tablet e celular.

## Fora do escopo da 1.3.0

Não fazem parte desta atualização:

- Migração para React, Vue ou outro framework de frontend.
- Uso de Framer Motion.
- Reescrita do backend.
- Alteração das regras financeiras.
- Alteração do modelo de permissões.
- Novos recursos administrativos mutáveis.
- Dashboard com dados em tempo real.
- Integração com serviços externos de analytics.
- Personalização individual de temas por usuário.
- Tema claro completo, caso não seja necessário para a identidade definida.

## Resultado esperado

Ao final da versão 1.3.0, o Quantium Bank deverá apresentar uma identidade
visual moderna, consistente e responsiva, combinando Glassmorphism e Soft UI
com a estética dark/high-tech existente. Todas as telas deverão compartilhar
os mesmos padrões de componentes, hierarquia, espaçamento, estados e
microinterações, sem comprometer acessibilidade, desempenho ou a arquitetura
Flask/Jinja atual.
