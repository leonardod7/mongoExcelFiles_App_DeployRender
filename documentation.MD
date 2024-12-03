<div>
    <img src="assets/img/img.png" width="140" height="100">
</div>

---
Autor: Leonardo dos Santos Costa
<br>
<font color=#ffcc00>MongoDB Atlas - Projeto PUC </font>

Scope: Data Preparation

# <font color=#ffcc00>MongoDB Atlas - Projeto PUC </font>

## <font color=#ffcc00> Considerações do Projeto:</font>

#### <font color=gray>1) Objetivo:</font>

O objetivo do projeto é criar uma aplicação web que receba arquivos em formato Excel do usuário referente aos demonstrativos financeiros: Demonstração de Resultado, Balanço Patrimonial e Fluxo de Caixa.
Os arquivos deverão seguir um padrão de formatação e a aplicação deverá realizar a leitura dos arquivos, armazenar os dados no banco de dados e exibir os dados na tela quando solicitado.

#### <font color=gray>2) Tecnologias Utilizadas:</font>

- Python 3.12
- Flask
- MongoDB Atlas
- HTML
- CSS
- Dash Plotly

#### <font color=gray>3) Requisitos Funcionais:</font>

- O usuário poderá enviar arquivos em formato Excel, através da funcionalidade **Drag and Drop**.
- A aplicação deverá realizar a leitura dos arquivos e armazenar os dados no banco de dados.
- A aplicação deverá exibir os dados na tela quando solicitado.
- A aplicação deverá apresentar opções de consulta e cadastro de arquivos para 3 modalidades de usinas: Biomassa, Solar e Hidrelétricas.
- A aplicação deverá permitir a exclusão de arquivos.

#### <font color=gray>4) Requisitos Não Funcionais:</font>

- A aplicação deverá ser responsiva.
- A aplicação deverá utilizar o banco de dados MongoDB Atlas.
- A aplicação deverá ser hospedada no Heroku.
- O back-end da aplicação deverá ser desenvolvida em Python.
- O front-end da aplicação deverá ser desenvolvida em Dash Plotly.
- A aplicação deverá ser desenvolvida utilizando o framework Flask.
- A aplicação poderá ser desenvolvida utilizando o padrão de arquitetura MVC (Model-View-Controller).

Estamos utilizando esse conceito no projeto, onde o DAO lida com o acesso ao banco de dados, as classes como SPE representam o modelo de negócio e o Dash atua como uma camada de visualização (View)



## <font color=#ffcc00> 1) Conhecendo o Projeto:</font>

### <font color=#ffcc00>1.1) Arquitetura de Pastas do Projeto</font>

O projeto possui a seguinte divisão de pastas:

- > **.venv** - Ambiente virtual do Python.
- > **assets** - Contém os arquivos de imagem e formatação css.
- > **components** - Contém os componentes da aplicação.
- > **dao** - Contém as classes de CRUD da aplicação com o banco de dados.
- > **functions** - Contém as funções auxiliares da aplicação.
- > **model** - Contém as classes de modelo da aplicação.
- > **pages** - Cada arquivo representa uma página da aplicação.
- > **.env** - Contém as variáveis de ambiente para conexão com cada banco de dados.
- > **app** - Arquivo com as configurações do app.
- > **index** - Arquivo principal responsável por iniciar a aplicação.
- > **requirements** - Arquivo com as dependências do projeto.



Este arquivo configura o aplicativo Dash e define as principais configurações, incluindo o cache e os temas para os estilos visuais.
Utilize este arquivo para centralizar as configurações do servidor e iniciar o aplicativo.

Dependências:
-------------
- dash
- dash_bootstrap_components
- flask_caching

Instalação:
-------------
Certifique-se de instalar as dependências necessárias: 
- > pip install dash dash-bootstrap-components Flask-Caching

Descrição das Configurações:
----------------------------
- Tema: SANDSTONE do Dash Bootstrap Components
- Cache: Configurado com 'simple' como cache padrão e um tempo limite de 300 segundos (5 minutos).

Parâmetros do Cache:
--------------------
CACHE_TYPE:
Define o tipo de backend do cache:
- 'simple': Armazena os dados de cache na memória do servidor. É uma opção fácil e rápida para desenvolvimento.
- 'redis': Requer um servidor Redis e é recomendado para ambientes de produção, onde o cache precisa ser compartilhado.
- 'filesystem': Armazena o cache em arquivos locais. Útil para persistir dados temporários.

CACHE_DEFAULT_TIMEOUT:
Tempo, em segundos, para o cache expirar automaticamente. Neste caso, está definido para 300 segundos (5 minutos).
Esse valor pode ser ajustado conforme a necessidade do projeto.

Uso do Cache:
-------------
- O cache pode ser aplicado em callbacks do Dash para otimizar o desempenho, evitando processamento repetitivo para dados que
  não mudam com frequência.
- Para utilizar o cache em um callback, basta aplicar o decorador `@cache.memoize(timeout=N)`, onde `N` é o tempo de cache em segundos.

#### Nota: Importante ressaltar que inicialmente no desenvolvimento do app, o Cache estava sendo utilizado para armazenar o nome dos bancos. Porém, optamos por não utilizar no app final.

### <font color=#ffcc00>1.2) Pasta assets</font>

A pasta assets contém os arquivos de imagem e formatação css utilizados na aplicação. Temos os seguintes arquivos:

- > **consult_page** - arquivo de formatação css da página listar_documentos.py.
- > **insert_page** - arquivo de formatação css da página inserir_documentos.py.
- > **cores** - arquivo de formatação css padrão para todo o projeto. Ele trás as paletas de cores utilizadas no projeto.
- > **home** - arquivo de formatação css da página home.py.
- > **img** - pasta com as imagens utilizadas no projeto.


### <font color=#ffcc00>1.3) Pasta components</font>

A pasta components contém os arquivos de componentes utilizados na aplicação. Temos os seguintes arquivos:

- > **navbar.py** - componente de barra de navegação.

Esse é o único componente utilizado no projeto, ele é responsável por criar a barra de navegação que é utilizada em todas as páginas do projeto.

```python
import dash_bootstrap_components as dbc
from dash import html

def navbar() -> dbc.NavbarSimple:
    # Definir o caminho da imagem
    image_path = "assets/img/database.png"  # Substitua pelo caminho da sua imagem

    navbar: dbc.NavbarSimple = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(children="Home", href="/home")),
            dbc.NavItem(dbc.NavLink(children="Consultar Documentos", href="/consultar-documentos")),
            dbc.NavItem(dbc.NavLink(children="Inserir Documento", href="/inserir-documento")),
        ],
        # Usar dbc.Row para organizar a imagem e o nome da marca lado a lado
        brand=dbc.Row(
            children=[
                dbc.Col(html.Img(src=image_path, height="40px")),  # Defina a altura da imagem
                dbc.Col(dbc.NavbarBrand(children="Mongo DB DataBase Management", className="ms-2",
                                        style={"fontSize": "16px", "fontWeight": "bold", "color": "white"})),
            ],
            align="center",  # Centraliza verticalmente
            className="g-0",  # Remove o espaçamento entre as colunas
        ),
        brand_href="#",
        color="dark",
        dark=True,
        className="mb-4",
        id="id-navbar",
        style={"marginTop": "20px"}  # Adiciona margens
    )

    return navbar

```

Veja que o app possui um componente de barra de navegação que é utilizado em todas as páginas do projeto. O componente é responsável por criar a barra de navegação que contém os links para as páginas Home, Consultar Documentos e Inserir Documento.





---

### <font color=#ffcc00>1.2) Configuração Mongo DB </font>



## <font color=#ffcc00> 2) Arquivos.py:</font>

### <font color=#ffcc00>2.1) app.py </font>


```python
# Importando as bibliotecas 
import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache  # pip install Flask-Caching

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server
app.config.suppress_callback_exceptions = True


# Configuração do cache
cache = Cache(app.server, config={
    'CACHE_TYPE': 'simple',  # Pode mudar para 'redis', 'filesystem', etc. conforme necessidade
    'CACHE_DEFAULT_TIMEOUT': 300  # Cache expira em 5 minutos (300 segundos)
})
```






Precisamos em Network Access, adicionar o IP 0.0.0.0/0, para que qualquer máquina possa acessar o banco de dados.


[//]: # (![Docker]&#40;img/img_1.png&#41;)