# Importando as bibliotecas --------------------------------------------------------------------------------------------
from dash import html, Input, Output, dcc, _dash_renderer
import dash_mantine_components as dmc

from pages.home import home_page
from pages.inserir_documentos import inserir_documentos_page
from pages.listar_documento import consultar_documentos_page

_dash_renderer._set_react_version("18.2.0")

# Importando componentes do app ----------------------------------------------------------------------------------------
from app import *
from components.navbar import navbar

# Criando o app --------------------------------------------------------------------------------------------------------

app.layout = dmc.MantineProvider(
    html.Div(className="index-div-app",
             children=[

                 # Barra de navegação
                 navbar(),

                 # Armazenando os cenários
                 dcc.Store(id="id-cenarios-store"),

                 # Armazenando os cenários com o nome da colecao e do banco
                 dcc.Store(id="id-collection-db_names-store"),

                 # # Adicionando o dcc.Store na estrutura HTML para armazenar os dados
                 dcc.Store(id='id-store-banco-spe-selecionado', storage_type='memory'),

                 # Container de páginas
                 dcc.Location(id='url', refresh=False),

                 # Conteúdo do app
                 html.Div(className="index-div-content", id="page-content", children=[]),

             ])
)


# Atualiza o conteúdo da página com base na URL
@app.callback(
    Output(component_id='page-content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)
def display_page(pathname):
    if pathname is None:
        return html.H3("Erro: Caminho não definido.")
    elif pathname == '/inserir-documento':
        return inserir_documentos_page()
    elif pathname == '/consultar-documentos':
        return consultar_documentos_page()
    elif pathname == '/home':
        return home_page()
    else:
        return home_page()  # Página padrão é a home


# Para rodar localmente com atualização de código
# if __name__ == '__main__':
#     app.run(debug=True, port=8064)

# Para deploy
if __name__ == '__main__':
    app.run(debug=False)


# pip install dash-tools