from dash import dcc, html, Input, Output, State, callback, ALL, no_update, callback_context, dash_table
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate

from functions.funcoes import conectar_ao_banco
from functions.funcoes_aux_table import preparar_tabela_graph
from functions.funcao_table import format_data_table

# 1) Dados iniciais das coleções ---------------------------------------------------------------------------------------
# Usamos um nome base para cada coleção para que não tenhamos erro, pois precisamos passar um nome de coleção inicial
collection_biomassa_base_name: str = "Vale do Paraná Albioma"
collection_solar_base_name: str = "Parque Solar 1"
collection_hidro_base_name: str = "UHE 1"


def home_page() -> html.Div:
    page: html.Div = html.Div(
        id="id-home-page",
        className="home-section-page",
        children=[

            html.Div(className="home-section-page-0",
                     children=[

                         # Div - 1 Banco de Dados ----------------------------------------------------------------------
                         html.Div(
                             className="home-section-page-1",
                             children=[
                                 html.H6(children=["Escolha o Banco de Dados no Mongo DB Atlas:"],
                                         style={'fontWeight': 'bold', 'color': 'gray', 'fontFamily': 'Arial Narrow'}),
                                 dcc.RadioItems(
                                     id='id-radio-items-bancos-home-page',
                                     className="custom-radio-items",
                                     options=[
                                         {'label': html.Span(children=[
                                             html.Img(src='/assets/img/db_cinza.png',
                                                      style={'width': '20px', 'height': '20px', 'marginRight': '10px'}),
                                             "Biomassa"
                                         ], style={
                                             'fontWeight': 'bold',
                                             'fontFamily': 'Arial Narrow',
                                             'fontSize': '14px',
                                         }),
                                             'value': 'Biomassa'
                                         },
                                         {'label': html.Span(children=[
                                             html.Img(src='/assets/img/db_cinza.png',
                                                      style={'width': '20px', 'height': '20px', 'marginRight': '10px'}),
                                             "Solar"
                                         ], style={
                                             'fontWeight': 'bold',
                                             'fontFamily': 'Arial Narrow',
                                             'fontSize': '14px',
                                         }),
                                             'value': 'Solar'
                                         },
                                         {'label': html.Span(children=[
                                             html.Img(src='/assets/img/db_cinza.png',
                                                      style={'width': '20px', 'height': '20px', 'marginRight': '10px'}),
                                             "Hidrelétricas"
                                         ], style={
                                             'fontWeight': 'bold',
                                             'fontFamily': 'Arial Narrow',
                                             'fontSize': '14px',
                                         }),
                                             'value': 'Hidrelétricas'
                                         }
                                     ], value='Biomassa'),
                             ]),

                         # Div - 2 SPE Escolha -------------------------------------------------------------------------
                         html.Div(
                             className="home-section-page-2",
                             children=[
                                 html.H6(children=["Escolha a SPE:"],
                                         style={'fontWeight': 'bold', 'color': 'gray', 'fontFamily': 'Arial Narrow'}),
                                 dmc.Select(
                                     # label="With native scroll",
                                     id='id-dropdown-spe-home-page',
                                     # data=[{"label": spe, "value": spe} for spe in spes_names],
                                     # value=spes_names[0],
                                     data=[],
                                     withScrollArea=False,
                                     styles={"dropdown": {"maxHeight": 200, "overflowY": "auto"}},
                                     w=300,
                                     mt="xs",
                                     radius="sm",

                                 )
                             ]),

                         # Div - Cenário Escolha -----------------------------------------------------------------------
                         html.Div(
                             className="home-section-page-3",
                             children=[
                                 html.H6(children=["Escolha o Cenário:"],
                                         style={'fontWeight': 'bold', 'color': 'gray', 'fontFamily': 'Arial Narrow'}),
                                 dmc.Select(
                                     # label="With native scroll",
                                     id='id-dropdown-cenario-spe-home-page',
                                     data=[],
                                     withScrollArea=False,
                                     styles={"dropdown": {"maxHeight": 200, "overflowY": "auto"}},
                                     w=300,
                                     mt="xs",
                                     radius="sm",
                                 )
                             ]),

                     ]),
            html.Div(className="home-section-page-4",
                     children=[
                         html.Button(
                             className='atualizar-btn',
                             id='id-home-btn-processar',
                             children=['Atualizar'],
                             n_clicks=0,
                             # style={'display': 'block', 'marginTop': '20px'}
                         ),
                     ]),


            # # Div para testar se os dados foram armazenados no dcc.Store id-store-banco-spe-selecionado
            # html.Div(id='id-teste-store-banco-spe-selecionado', children=[]),

            dcc.Loading(
                id="loading",
                type="circle",  # Tipos disponíveis: "default", "circle", "dot"
                children=[
                    html.Div(className="home-section-page-dfs-0",
                             id="id-home-section-page-dfs-0",
                             children=[]),
                ],
            ),

        ])

    return page


# 0) Callback para atualizar os dados do dropdown das SPEs  ------------------------------------------------------------
@callback(
    Output(component_id="id-dropdown-spe-home-page", component_property="data"),
    Output(component_id="id-dropdown-spe-home-page", component_property="value"),
    Input(component_id="id-radio-items-bancos-home-page", component_property="value")
)
def update_spe_dropdown(banco: str):
    if banco == 'Biomassa':
        cliente, biomassa_crud = conectar_ao_banco(collection_name=collection_biomassa_base_name,
                                                   database_name=banco)
        try:
            colecoes = biomassa_crud.list_collections()
        finally:
            cliente.close_connection()

        # Temos que verificar se a lista é vazia, pois podemos ter deletado todas as coleções
        if len(colecoes) == 0:
            valor_default = 'Sem coleções.'
            lista_valores = ['Sem coleções.']
        else:
            valor_default = colecoes[0]
            lista_valores = [{"label": spe, "value": spe} for spe in colecoes]

        # print(lista_valores)
        # print(valor_default)
        #
        # # Criar uma lista para armazenar os valores da chave 'value'
        # lista_nome_colecoes = []
        #
        # # Iterar sobre os dados e pegar os valores da chave 'value'
        # for item in lista_valores:
        #     lista_nome_colecoes.append(item['value'])
        #
        # print(lista_nome_colecoes)

        return lista_valores, valor_default

    elif banco == 'Solar':
        cliente, solar_crud = conectar_ao_banco(collection_name=collection_solar_base_name,
                                                database_name=banco)
        try:
            colecoes = solar_crud.list_collections()
        finally:
            cliente.close_connection()

        # Temos que verificar se a lista é vazia, pois podemos ter deletado todas as coleções
        if len(colecoes) == 0:
            valor_default = 'Sem coleções.'
            lista_valores = ['Sem coleções.']
        else:
            valor_default = colecoes[0]
            lista_valores = [{"label": spe, "value": spe} for spe in colecoes]

        # print(lista_valores)
        # print(valor_default)
        #
        # # Criar uma lista para armazenar os nomes das coleções que serão salvas no dcc.Store
        # lista_nome_colecoes = []
        #
        # # Iterar sobre os dados e pegar os valores da chave 'value'
        # for item in lista_valores:
        #     lista_nome_colecoes.append(item['value'])
        #
        # # Lista que será salva com o nome das coleções
        # print(lista_nome_colecoes)

        return lista_valores, valor_default

    elif banco == 'Hidrelétricas':
        cliente, hidro_crud = conectar_ao_banco(collection_name=collection_hidro_base_name,
                                                database_name=banco)
        try:
            colecoes = hidro_crud.list_collections()
        finally:
            cliente.close_connection()

        # Temos que verificar se a lista é vazia, pois podemos ter deletado todas as coleções
        if len(colecoes) == 0:
            valor_default = 'Sem coleções.'
            lista_valores = ['Sem coleções.']
        else:
            valor_default = colecoes[0]
            lista_valores = [{"label": spe, "value": spe} for spe in colecoes]

        # print(lista_valores)
        # print(valor_default)
        #
        # # Criar uma lista para armazenar os valores da chave 'value'
        # lista_nome_colecoes = []
        #
        # # Iterar sobre os dados e pegar os valores da chave 'value'
        # for item in lista_valores:
        #     lista_nome_colecoes.append(item['value'])
        #
        # print(lista_nome_colecoes)

        return lista_valores, valor_default


# 1) Callback para atualizar o dcc.Store com o banco e a SPE escolhida
@callback(
    Output(component_id='id-store-banco-spe-selecionado', component_property='data'),
    Input(component_id='id-radio-items-bancos-home-page', component_property='value'),
    Input(component_id='id-dropdown-spe-home-page', component_property='value')
)
def update_store_with_banco_and_spe(banco, spe):
    if banco and spe:
        # Retorna uma lista com o banco e a SPE
        return [banco, spe]
    raise PreventUpdate


# 2) Callback para atualizar o dropdown de cenários conforme a SPE escolhida ------------------------------------------
# Agora, criamos o callback para atualizar o dropdown de Cenário com base nos dados armazenados no dcc.Store.
# Esse callback vai ser disparado sempre que os valores do dcc.Store forem alterados:
# 2) Callback para atualizar os cenários com base no banco e na SPE armazenados
@callback(
    Output(component_id='id-dropdown-cenario-spe-home-page', component_property='data'),
    Output(component_id='id-dropdown-cenario-spe-home-page', component_property='value'),
    Input(component_id='id-store-banco-spe-selecionado', component_property='data')
)
def update_cenario_dropdown(store_data):
    if store_data:
        banco = store_data[0]
        spe = store_data[1]
        # print(store_data)  # debug
        cliente, crud = conectar_ao_banco(collection_name=spe, database_name=banco)
        # print(cliente)  # debug
        try:
            documentos = crud.list_documents()
            # print(documentos)  # debug
            # Vamos listar todos os nomes dos cenários. Ele retorna uma lista com nomes de todos os documentos
            cenarios = [doc['nome'] for doc in documentos]
            # Precisamos pegar os nomes únicos, pois podemos ter cenários repetidos
            cenarios = list(set(cenarios))
            # print(cenarios)  # debug
            default_value = cenarios[0]
        except Exception as e:
            # print(e)  # debug
            cenarios = ['Sem cenários.']
            default_value = 'Sem cenários.'
        finally:
            cliente.close_connection()

        return cenarios, default_value


# # 3) Callback para apresentar os dados de cada SPE conforme escolha do banco de dados.
@callback(
    Output(component_id="id-home-section-page-dfs-0", component_property="children"),
    Input(component_id="id-home-btn-processar", component_property="n_clicks"),
    [State(component_id="id-radio-items-bancos-home-page", component_property="value"),
     State(component_id="id-dropdown-spe-home-page", component_property="value"),
     State(component_id="id-dropdown-cenario-spe-home-page", component_property="value")],
)
def update_spe_dfs(n_clicks: int, banco: str, spe: str, nome_cenario: str):
    if n_clicks == 0:
        return no_update

    if n_clicks > 0:

        if banco == 'Biomassa':
            tipo: str = 'dre'
            chave: str = 'dre'
            conta_index: str = "Demonstração de Resultado"
            cenario_nome: str = nome_cenario
            tabela_dre = preparar_tabela_graph(collection_name=spe, banco=banco, tipo=tipo, chave=chave,
                                               conta_index=conta_index, cenario_nome=cenario_nome)

            tipo: str = 'bp'
            chave: str = 'bp'
            conta_index: str = "Balanço Patrimonial"
            cenario_nome: str = nome_cenario
            tabela_bp = preparar_tabela_graph(collection_name=spe, banco=banco, tipo=tipo, chave=chave,
                                              conta_index=conta_index, cenario_nome=cenario_nome)

            tipo: str = 'fcd'
            chave: str = 'fcd'
            conta_index: str = "Fluxo de Caixa Direto"
            cenario_nome: str = nome_cenario
            tabela_fcd = preparar_tabela_graph(collection_name=spe, banco=banco, tipo=tipo, chave=chave,
                                               conta_index=conta_index, cenario_nome=cenario_nome)

            dash_dre_format = format_data_table(tabela_dre)
            dash_bp_format = format_data_table(tabela_bp)
            dash_fcd_format = format_data_table(tabela_fcd)

            div_retorno = html.Div(
                children=[
                    html.H6(f"DRE Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                    html.Hr(),
                    dash_dre_format,
                    html.Hr(),
                    html.H6(f"BP Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                    html.Hr(),
                    dash_bp_format,
                    html.Hr(),
                    html.H6(f"FCD Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                    html.Hr(),
                    dash_fcd_format
                ]
            )

            return div_retorno

        elif banco == 'Solar':
            tipo: str = 'dre'
            chave: str = 'dre'
            conta_index: str = "Demonstração de Resultado"
            cenario_nome: str = nome_cenario
            tabela_dre = preparar_tabela_graph(collection_name=spe, banco=banco, tipo=tipo, chave=chave,
                                               conta_index=conta_index, cenario_nome=cenario_nome)

            tipo: str = 'bp'
            chave: str = 'bp'
            conta_index: str = "Balanço Patrimonial"
            cenario_nome: str = nome_cenario
            tabela_bp = preparar_tabela_graph(collection_name=spe, banco=banco, tipo=tipo, chave=chave,
                                              conta_index=conta_index, cenario_nome=cenario_nome)

            tipo: str = 'fcd'
            chave: str = 'fcd'
            conta_index: str = "Fluxo de Caixa Direto"
            cenario_nome: str = nome_cenario
            tabela_fcd = preparar_tabela_graph(collection_name=spe, banco=banco, tipo=tipo, chave=chave,
                                               conta_index=conta_index, cenario_nome=cenario_nome)

            dash_dre_format = format_data_table(tabela_dre)
            dash_bp_format = format_data_table(tabela_bp)
            dash_fcd_format = format_data_table(tabela_fcd)

            div_retorno = html.Div(
                children=[
                    html.H6(f"DRE Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                    html.Hr(),
                    dash_dre_format,
                    html.Hr(),
                    html.H6(f"BP Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                    html.Hr(),
                    dash_bp_format,
                    html.Hr(),
                    html.H6(f"FCD Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                    html.Hr(),
                    dash_fcd_format
                ]
            )

            return div_retorno

        elif banco == 'Hidrelétricas':
            tipo: str = 'dre'
            chave: str = 'dre'
            conta_index: str = "Demonstração de Resultado"
            cenario_nome: str = nome_cenario
            tabela_dre = preparar_tabela_graph(collection_name=spe, banco=banco, tipo=tipo, chave=chave,
                                               conta_index=conta_index, cenario_nome=cenario_nome)

            tipo: str = 'bp'
            chave: str = 'bp'
            conta_index: str = "Balanço Patrimonial"
            cenario_nome: str = nome_cenario
            tabela_bp = preparar_tabela_graph(collection_name=spe, banco=banco, tipo=tipo, chave=chave,
                                              conta_index=conta_index, cenario_nome=cenario_nome)

            tipo: str = 'fcd'
            chave: str = 'fcd'
            conta_index: str = "Fluxo de Caixa Direto"
            cenario_nome: str = nome_cenario
            tabela_fcd = preparar_tabela_graph(collection_name=spe, banco=banco, tipo=tipo, chave=chave,
                                               conta_index=conta_index, cenario_nome=cenario_nome)

            dash_dre_format = format_data_table(tabela_dre)
            dash_bp_format = format_data_table(tabela_bp)
            dash_fcd_format = format_data_table(tabela_fcd)

            div_retorno = html.Div(
                children=[
                    html.H6(f"DRE Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                    html.Hr(),
                    dash_dre_format,
                    html.Hr(),
                    html.H6(f"BP Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                    html.Hr(),
                    dash_bp_format,
                    html.Hr(),
                    html.H6(f"FCD Gerencial da SPE {spe} referente ao banco de dados {banco}."),
                    html.Hr(),
                    dash_fcd_format
                ]
            )

            return div_retorno


# Callback de teste para check dos dados armazenados ------------------------------------------------------------------
# @callback(
#     Output(component_id="id-teste-store-banco-spe-selecionado", component_property="children"),
#     Input(component_id="id-store-banco-spe-selecionado", component_property="data"),
# )
# def verificar_dados_store(store_data):
#     return f"Dados no Store: {store_data}"


# TODO: Fazer callback para manter o estado das informações selecionadas pelo usuário na sua sessão.
# TODO: Temos que pensar em como otimizar o consumo de dados no mongo db.
# TODO: Temos que atualizar o estado quando inserimos uma informação e ela retorna "Arquivo Inserido com Sucesso",
#  na página inserir documento.
