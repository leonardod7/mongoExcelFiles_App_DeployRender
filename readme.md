<!-- antes de enviar a versão final, solicitamos que todos os comentários, colocados para orientação ao aluno, sejam removidos do arquivo -->
# Sistema Inteligente para Gestão de Arquivos Excel no Mongo DB Atlas

#### Aluno: [Leonardo dos Santos Costa](https://github.com/link_do_github)
#### Orientadora: [Nome Sobrenome](https://github.com/link_do_github).
#### Co-orientador(/a/es/as): [Nome Sobrenome](https://github.com/link_do_github). <!-- caso não aplicável, remover esta linha -->

---

Trabalho apresentado ao curso [BI MASTER](https://ica.puc-rio.ai/bi-master) como pré-requisito para conclusão de curso e obtenção de crédito na disciplina "Projetos de Sistemas Inteligentes de Apoio à Decisão".

<!-- para os links a seguir, caso os arquivos estejam no mesmo repositório que este README, não há necessidade de incluir o link completo: basta incluir o nome do arquivo, com extensão, que o GitHub completa o link corretamente -->
- [Link para o código](https://github.com/link_do_repositorio). <!-- caso não aplicável, remover esta linha -->

- [Link para a monografia](https://link_da_monografia.com). <!-- caso não aplicável, remover esta linha -->

- Fontes de Consulta: <!-- caso não aplicável, remover estas linhas -->
    - [Fonte 1](https://dash.plotly.com/dash-core-components/loading).
    - [Fonte 2](https://www.dash-mantine-components.com).
    - [Fonte 3](https://cloud.mongodb.com/).

---

### Resumo

<!-- trocar o texto abaixo pelo resumo do trabalho, em português -->

Este projeto tem como objetivo o desenvolvimento de um sistema web interativo utilizando Dash e Plotly, que permite ao usuário gerenciar e visualizar cenários financeiros gerados a partir de uma modelagem econômica-financeira em Excel. A principal funcionalidade do sistema é fornecer uma plataforma acessível e eficiente para que o usuário tenha governança e segurança sobre os dados financeiros, transformando informações extraídas de planilhas em relatórios estruturados e dinâmicos

### Abstract <!-- Opcional! Caso não aplicável, remover esta seção -->

<!-- trocar o texto abaixo pelo resumo do trabalho, em inglês -->

This project develops a web-based system using Dash and Plotly to provide users with governance and management of financial scenarios generated from an economic-financial model created in Excel. The system allows users to upload financial reports, such as income statements, cash flows, and balance sheets, through a drag-and-drop functionality. The data is processed, stored in a MongoDB database, and presented in a structured format for easy visualization. This system aims to replace the need for direct database interaction, allowing users to access and interact with their financial data in a secure and user-friendly manner. The implementation leverages MongoDB's flexible data storage capabilities, although challenges such as limitations in the free-tier plan, latency, and performance issues were encountered. Despite these challenges, the system provides a robust solution for financial data management and governance, empowering users to make informed decisions based on their financial models.

### 1. Introdução

O sistema desenvolvido visa testar a hipótese de criarmos uma maneira mais eficiente e segura para gerenciar e visualizar cenários financeiros complexos de diferentes ativos de uma holding. Utilizando Dash e Plotly, a plataforma permite ao usuário importar dados financeiros, que são processados e organizados automaticamente a partir de uma máscara padronizada em modelos financeiros Excel. Essas máscarás de dados são salvos em um banco de dados MongoDB, tornando o processo de gestão e governaça das informações mais seguro.

### 2. Modelagem

A importação dos dados é realizada por meio de uma funcionalidade de *drag and drop*, o que torna o processo de integração de novos cenários econômicos muito mais simples e rápido. Após a importação, o algoritmo organiza os dados e os salva em um banco de dados MongoDB, facilitando posteriormente a consulta e a visualização. Devido ao acesso gratuito ao MongoDB Atlas, o algoritmo foi construído para respeitar indicadores de performance do Mongo DB Atlas, como por exemplo o Schema Anti-Patterns. Além disso, cabe ressaltar que devido ao tamanho dos arquivos em formato Excel, eles foram segregados em documentos menores para respeitar as regras de performance. 

#### <font color=gray>2.1) Tecnologias Utilizadas:</font>

- Python 3.12
- Flask
- MongoDB Atlas
- HTML
- CSS
- Dash Plotly

#### <font color=gray>2.2) Requisitos Funcionais:</font>

- O usuário poderá enviar arquivos em formato Excel, através da funcionalidade **Drag and Drop**.
- A aplicação deverá realizar a leitura dos arquivos e armazenar os dados no banco de dados.
- A aplicação deverá exibir os dados na tela quando solicitado.
- A aplicação deverá possuir um banco de dados para cada segmento de usina.
- A aplicação deverá apresentar opções de consulta e cadastro de arquivos para 3 modalidades de usinas: Eólicas, Solar e Hidrelétricas.
- A aplicação deverá permitir a exclusão de arquivos.

#### <font color=gray>2.3) Requisitos Não Funcionais:</font>

- A aplicação deverá ser responsiva.
- A aplicação deverá utilizar o banco de dados MongoDB Atlas.
- A aplicação deverá ser hospedada no Heroku.
- O back-end da aplicação deverá ser desenvolvida em Python.
- O front-end da aplicação deverá ser desenvolvida em Dash Plotly.
- A aplicação deverá ser desenvolvida utilizando o framework Flask.
- A aplicação poderá ser desenvolvida utilizando o padrão de arquitetura MVC (Model-View-Controller).

Estamos utilizando parte do conceito de MVC para refletir a estrutura de DAO que lida com todo o processo de CRUD, MODEL que será responsável por estruturar as classes de acesso ao banco de dados e o Dash atuando como uma camada de visualização (View)

### 3. Resultados

A inserção de documentos Excel via funcionalidades drag and drop apresentou uma boa experiência para o usuário final, possibilitando a importação de arquivos de forma rápida e intuitiva. A visualização dos dados financeiros usando bibliotecas de visualização do Dash também apresentou uma experiência positiva, principalmente na visualização de tabelas com importação de dados diretamente do MongoDB, sem a necessidade de algum tipo de armazenagem intermediária para que fosse otimizado o tempo de resposta de cada request. A funcionalidade de exclusão de arquivos também foi implementada com sucesso, garantindo a integridade dos dados e a segurança do sistema. 
Porém, é importante destacar que durante o processo o desenvolvimento do sistema, um dos principais desafios foi o uso do MongoDB no plano gratuito, que impôs algumas limitações em termos de armazenamento e desempenho. A versão gratuita do MongoDB oferece uma quantidade limitada de armazenamento (até 512 MB), o que pode ser um fator limitante à medida que o volume de dados cresce. Além disso, a funcionalidade de backups automáticos e recursos avançados de segurança são restritos na versão gratuita, o que exige maior controle por parte da equipe de desenvolvimento.

Outro desafio importante foi a latência nas operações de leitura no banco de dados. Como o MongoDB gratuito não oferece garantias de desempenho de alta disponibilidade, a latência pode aumentar significativamente em momentos de pico de acesso ao banco de dados, prejudicando a experiência do usuário. Isso impacta principalmente nas visualizações em tempo real dos relatórios financeiros, onde a velocidade de resposta é crítica.

Em relação à performance, o sistema enfrentou limitações na velocidade de processamento de grandes volumes de dados. Embora o MongoDB seja eficiente para armazenar e consultar grandes quantidades de dados, a versão gratuita não conta com as otimizações avançadas disponíveis em planos pagos, como o particionamento de dados ou o uso de índices específicos para acelerar consultas complexas. Essas limitações exigiram ajustes e otimizações no design do banco de dados e na forma como os dados eram processados antes de serem exibidos ao usuário.

Esses desafios de latência, performance e limitações de armazenamento demandaram a construção de algoritmo totalmente customizado para lidar com essas especificidades do MongoDB gratuito, garantindo que o sistema fosse capaz de lidar com grandes volumes de dados e manter a integridade e segurança dos dados financeiros.


### 4. Conclusões

Este projeto apresenta uma solução funcional, porém com uma janela enorme de melhorias no processo de performance no consumo de informações diretamente do Mongo DB. O uso do Dash e Plotly para criar gráficos e tabelas interativas, juntamente com o armazenamento e organização no MongoDB, resulta em uma plataforma de fácil uso.

---

Matrícula: 221.100.157

Pontifícia Universidade Católica do Rio de Janeiro

Curso de Pós Graduação *Business Intelligence Master*
