from datetime import datetime
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
import dash_mantine_components as dmc
from bson import ObjectId
import base64
import io

from dao.MongoCRUD import MongoDBCRUD
from model.MongoConnection import MongoBiomassaConnection, MongoSolarConnection, MongoHidroConnection


# 1) Função para criar as partes do documento --------------------------------------------------------------------------
def criar_partes_documento(file_path: str, setor: str, empresa_nome: str, cenario_nome: str,
                           descricao_cenario: str, sheet_name: str, demonstrativo_name: str,
                           nome_segunda_coluna: str) -> list[dict]:
    """
    O objetivo dessa função é transformar o demonstrativo de cada empresa em partes menores e torná-las documentos que possam ser salvos no MongoDB Atlas
    sem o risco de ultrapassar o tamanho de array recomendado pelo MongoDB.

    :param file_path: Caminho do arquivo Excel
    :param setor: Setor da empresa (eolicas, solar, hidrelétrica, etc)
    :param empresa_nome: Nome da empresa (SPE Moinhos de Vento, SPE Solar Leste, etc)
    :param cenario_nome: Nome do cenário (Cenário 1, Cenário 2, etc)
    :param descricao_cenario: Descrição do cenário (Cenário com investimento em novos parques eólicos)
    :param sheet_name: Nome da aba do arquivo Excel (DRE, FCD, BP)
    :param demonstrativo_name: Nome do demonstrativo (Demonstração de Resultado, Balanço Patrimonial, Fluxo de Caixa Direto)
    :param nome_segunda_coluna: Nome da segunda coluna do demonstrativo (Driver)
    :return: Retorna uma lista com dicionários referentes a cada parte do demonstrativo
    """

    xls = pd.ExcelFile(file_path)
    dre = pd.read_excel(xls, sheet_name=sheet_name)

    # numero_colunas = dre.shape[1]
    # print(numero_colunas)  # Mostra o número de colunas do DataFrame

    # As duas primeiras colunas
    colunas_iniciais = dre.iloc[:, :2]

    # Dividindo o DataFrame em três partes
    df_part_1 = dre.iloc[:, :50]  # As primeiras 70 colunas

    chave_name = 'dre' if sheet_name == 'DRE' else 'bp' if sheet_name == 'BP' else 'fcd'

    # Para as partes 2 e 3, concatenamos as duas primeiras colunas com as colunas específicas
    df_part_2 = pd.concat([colunas_iniciais, dre.iloc[:, 50:100]], axis=1)  # Duas primeiras + colunas 50 a 100
    df_part_3 = pd.concat([colunas_iniciais, dre.iloc[:, 100:150]], axis=1)  # Duas primeiras + colunas 100 a 150
    df_part_4 = pd.concat([colunas_iniciais, dre.iloc[:, 150:]], axis=1)  # Duas primeiras + colunas 152 em diante

    # 1) Criando o primeiro documento --------------------------------------------------------------------------------

    df_long_1 = df_part_1.melt(id_vars=[demonstrativo_name, nome_segunda_coluna], var_name='Data', value_name='Valor')
    df_list_part_1 = df_long_1.to_dict(orient='records')

    documento_spe_dre_part_1 = {
        "nome": cenario_nome,
        "descricao": descricao_cenario,
        "data": datetime.now(),
        "setor": setor,
        "empresa": empresa_nome,
        chave_name: df_list_part_1,
        "tipo": chave_name,
        "parte": 1
    }

    # 2) Criando o segundo documento ---------------------------------------------------------------------------------

    df_long_2 = df_part_2.melt(id_vars=[demonstrativo_name, nome_segunda_coluna], var_name='Data', value_name='Valor')
    df_list_part_2 = df_long_2.to_dict(orient='records')

    documento_spe_dre_part_2 = {
        "nome": cenario_nome,
        "descricao": descricao_cenario,
        "data": datetime.now(),
        "setor": setor,
        "empresa": empresa_nome,
        chave_name: df_list_part_2,
        "tipo": chave_name,
        "parte": 2
    }

    # 3) Criando o terceiro documento --------------------------------------------------------------------------------

    df_long_3 = df_part_3.melt(id_vars=[demonstrativo_name, nome_segunda_coluna], var_name='Data', value_name='Valor')
    df_list_part_3 = df_long_3.to_dict(orient='records')

    documento_spe_dre_part_3 = {
        "nome": cenario_nome,
        "descricao": descricao_cenario,
        "data": datetime.now(),
        "setor": setor,
        "empresa": empresa_nome,
        chave_name: df_list_part_3,
        "tipo": chave_name,
        "parte": 3
    }

    # 4) Criando o quarto documento ---------------------------------------------------------------------------------

    df_long_4 = df_part_4.melt(id_vars=[demonstrativo_name, nome_segunda_coluna], var_name='Data', value_name='Valor')
    df_list_part_4 = df_long_4.to_dict(orient='records')

    documento_spe_dre_part_4 = {
        "nome": cenario_nome,
        "descricao": descricao_cenario,
        "data": datetime.now(),
        "setor": setor,
        "empresa": empresa_nome,
        chave_name: df_list_part_4,
        "tipo": chave_name,
        "parte": 4
    }

    lista: list = [documento_spe_dre_part_1, documento_spe_dre_part_2, documento_spe_dre_part_3,
                   documento_spe_dre_part_4]

    return lista


# Essa função é a mesma que a de cima, porém, mais otimizada e com menos repetição de código. Além disso, ela parte do
# arquivo no formato DataFrame, ao invés de carregar o arquivo Excel de um caminho.
def criar_partes_documento_from_drag_and_drop(df: pd.DataFrame, setor: str, empresa_nome: str, cenario_nome: str,
                                              descricao_cenario: str, sheet_name: str, demonstrativo_name: str,
                                              nome_segunda_coluna: str) -> list[dict]:
    """
    O objetivo dessa função é transformar o demonstrativo de cada empresa em partes menores e torná-las documentos que possam ser salvos no MongoDB Atlas
    sem o risco de ultrapassar o tamanho de array recomendado pelo MongoDB.

    :param df: DataFrame contendo os dados do arquivo Excel
    :param setor: Setor da empresa (eolicas, solar, hidrelétrica, etc)
    :param empresa_nome: Nome da empresa (SPE Moinhos de Vento, SPE Solar Leste, etc)
    :param cenario_nome: Nome do cenário (Cenário 1, Cenário 2, etc)
    :param descricao_cenario: Descrição do cenário (Cenário com investimento em novos parques eólicos)
    :param sheet_name: Nome da aba do arquivo Excel (DRE, FCD, BP)
    :param demonstrativo_name: Nome do demonstrativo (Demonstração de Resultado, Balanço Patrimonial, Fluxo de Caixa Direto)
    :param nome_segunda_coluna: Nome da segunda coluna do demonstrativo (Driver)
    :return: Retorna uma lista com dicionários referentes a cada parte do demonstrativo
    """

    # Dividindo o DataFrame em três partes
    colunas_iniciais = df.iloc[:, :2]
    df_part_1 = df.iloc[:, :50]  # Primeiras 50 colunas
    df_part_2 = pd.concat([colunas_iniciais, df.iloc[:, 50:100]], axis=1)  # Duas primeiras + colunas 50 a 100
    df_part_3 = pd.concat([colunas_iniciais, df.iloc[:, 100:150]], axis=1)  # Duas primeiras + colunas 100 a 150
    df_part_4 = pd.concat([colunas_iniciais, df.iloc[:, 150:]], axis=1)  # Duas primeiras + colunas 150 em diante

    chave_name = 'dre' if sheet_name == 'DRE' else 'bp' if sheet_name == 'BP' else 'fcd'

    # Criando as partes para salvar no MongoDB
    partes = []
    for i, parte_df in enumerate([df_part_1, df_part_2, df_part_3, df_part_4], start=1):
        df_long = parte_df.melt(id_vars=[demonstrativo_name, nome_segunda_coluna], var_name='Data', value_name='Valor')
        df_list = df_long.to_dict(orient='records')

        documento = {
            "nome": cenario_nome,
            "descricao": descricao_cenario,
            "data": datetime.now(),
            "setor": setor,
            "empresa": empresa_nome,
            chave_name: df_list,
            "tipo": chave_name,
            "parte": i
        }
        partes.append(documento)
    # print(partes)  # debug

    return partes


def criar_partes_documento2(df: pd.DataFrame, setor: str, empresa_nome: str, cenario_nome: str,
                            descricao_cenario: str, sheet_name: str, demonstrativo_name: str,
                            nome_segunda_coluna: str) -> list[dict]:
    """
    O objetivo dessa função é transformar o demonstrativo de cada empresa em partes menores e torná-las documentos que possam ser salvos no MongoDB Atlas
    sem o risco de ultrapassar o tamanho de array recomendado pelo MongoDB.

    :param df: Caminho do arquivo Excel
    :param setor: Setor da empresa (eolicas, solar, hidrelétrica, etc)
    :param empresa_nome: Nome da empresa (SPE Moinhos de Vento, SPE Solar Leste, etc)
    :param cenario_nome: Nome do cenário (Cenário 1, Cenário 2, etc)
    :param descricao_cenario: Descrição do cenário (Cenário com investimento em novos parques eólicos)
    :param sheet_name: Nome da aba do arquivo Excel (DRE, FCD, BP)
    :param demonstrativo_name: Nome do demonstrativo (Demonstração de Resultado, Balanço Patrimonial, Fluxo de Caixa Direto)
    :param nome_segunda_coluna: Nome da segunda coluna do demonstrativo (Driver)
    :return: Retorna uma lista com dicionários referentes a cada parte do demonstrativo
    """

    # numero_colunas = dre.shape[1]
    # print(numero_colunas)  # Mostra o número de colunas do DataFrame

    # As duas primeiras colunas
    colunas_iniciais = df.iloc[:, :2]

    # Dividindo o DataFrame em três partes
    df_part_1 = df.iloc[:, :50]  # As primeiras 70 colunas

    chave_name = 'dre' if sheet_name == 'DRE' else 'bp' if sheet_name == 'BP' else 'fcd'

    # Para as partes 2 e 3, concatenamos as duas primeiras colunas com as colunas específicas
    df_part_2 = pd.concat([colunas_iniciais, df.iloc[:, 50:100]], axis=1)  # Duas primeiras + colunas 50 a 100
    df_part_3 = pd.concat([colunas_iniciais, df.iloc[:, 100:150]], axis=1)  # Duas primeiras + colunas 100 a 150
    df_part_4 = pd.concat([colunas_iniciais, df.iloc[:, 150:]], axis=1)  # Duas primeiras + colunas 152 em diante

    # 1) Criando o primeiro documento --------------------------------------------------------------------------------

    df_long_1 = df_part_1.melt(id_vars=[demonstrativo_name, nome_segunda_coluna], var_name='Data', value_name='Valor')
    df_list_part_1 = df_long_1.to_dict(orient='records')

    documento_spe_dre_part_1 = {
        "nome": cenario_nome,
        "descricao": descricao_cenario,
        "data": datetime.now(),
        "setor": setor,
        "empresa": empresa_nome,
        chave_name: df_list_part_1,
        "tipo": chave_name,
        "parte": 1
    }

    # 2) Criando o segundo documento ---------------------------------------------------------------------------------

    df_long_2 = df_part_2.melt(id_vars=[demonstrativo_name, nome_segunda_coluna], var_name='Data', value_name='Valor')
    df_list_part_2 = df_long_2.to_dict(orient='records')

    documento_spe_dre_part_2 = {
        "nome": cenario_nome,
        "descricao": descricao_cenario,
        "data": datetime.now(),
        "setor": setor,
        "empresa": empresa_nome,
        chave_name: df_list_part_2,
        "tipo": chave_name,
        "parte": 2
    }

    # 3) Criando o terceiro documento --------------------------------------------------------------------------------

    df_long_3 = df_part_3.melt(id_vars=[demonstrativo_name, nome_segunda_coluna], var_name='Data', value_name='Valor')
    df_list_part_3 = df_long_3.to_dict(orient='records')

    documento_spe_dre_part_3 = {
        "nome": cenario_nome,
        "descricao": descricao_cenario,
        "data": datetime.now(),
        "setor": setor,
        "empresa": empresa_nome,
        chave_name: df_list_part_3,
        "tipo": chave_name,
        "parte": 3
    }

    # 4) Criando o quarto documento ---------------------------------------------------------------------------------

    df_long_4 = df_part_4.melt(id_vars=[demonstrativo_name, nome_segunda_coluna], var_name='Data', value_name='Valor')
    df_list_part_4 = df_long_4.to_dict(orient='records')

    documento_spe_dre_part_4 = {
        "nome": cenario_nome,
        "descricao": descricao_cenario,
        "data": datetime.now(),
        "setor": setor,
        "empresa": empresa_nome,
        chave_name: df_list_part_4,
        "tipo": chave_name,
        "parte": 4
    }

    lista: list = [documento_spe_dre_part_1, documento_spe_dre_part_2, documento_spe_dre_part_3,
                   documento_spe_dre_part_4]

    return lista


def parse_contents(contents: str, sheetname: str | None = None) -> pd.DataFrame:
    """
    Função para ler o arquivo Excel e gerar um DataFrame de uma aba específica.
    :param contents: contents é uma string codificada em Base64, que contém o arquivo Excel.
    :param sheetname: Nome da aba do Excel que deseja carregar. Se None, carrega a primeira aba.
    :return: Retorna um DataFrame ou uma mensagem de erro.
    """

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        df = pd.read_excel(io.BytesIO(decoded), sheet_name=sheetname)
        print("DataFrame carregado:")
    except Exception as e:
        print(e)
        return html.Div([
            'Erro ao processar o arquivo: {}'.format(e)
        ])

    # Converte as colunas de data para strings, caso existam
    df.columns = [str(col) for col in df.columns]

    return df


def conectar_ao_banco(collection_name: str, database_name: str):
    if database_name == 'Biomassa':
        cliente = MongoBiomassaConnection()
        cliente.connect_to_db()
        biomassa_crud = MongoDBCRUD(db_connection=cliente, collection_name=collection_name)
        return cliente, biomassa_crud
    elif database_name == 'Solar':
        cliente = MongoSolarConnection()
        cliente.connect_to_db()
        solar_crud = MongoDBCRUD(db_connection=cliente, collection_name=collection_name)
        return cliente, solar_crud
    else:
        cliente = MongoHidroConnection()
        cliente.connect_to_db()
        hidro_crud = MongoDBCRUD(db_connection=cliente, collection_name=collection_name)
        return cliente, hidro_crud


# 3) Função de agrupamento por chave -----------------------------------------------------------------------------------
def agrupar_por_chave(lista: list[dict], chave: str):
    grupos = {}
    for item in lista:
        key = item[chave]
        if key not in grupos:
            grupos[key] = []
        grupos[key].append(item)
    return grupos


# 4) Função para renderizar cards --------------------------------------------------------------------------------------
def render_card(cenario) -> dbc.Card:
    card: dbc.Card = dbc.Card(
        dbc.CardBody([
            html.H4(
                children=[html.Span(children=[f"{cenario['nome']}"], style={'fontWeight': 'bold', 'color': 'gray'})],
                className="card-title", style={'fontFamily': 'Arial Narrow',
                                               'fontSize': '14px',
                                               'borderBottom': '0.5px solid gray',
                                               # 'paddingBottom': '5px',
                                               'marginTop': '1px', }),

            # Div com o título, parte, empresa, data e tipo
            html.Div(children=[

                html.P(children=[
                    html.Span(children=["Parte: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                    f"{cenario['parte']}",
                    html.Span(children=[" |"], style={'fontStyle': 'italic', 'color': 'black'})
                    # Estilizando o separador
                ], className="card-text",
                    style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                html.P(children=[
                    html.Span(children=["Empresa: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                    f"{cenario['empresa']}",
                    html.Span(children=[" |"], style={'fontStyle': 'italic', 'color': 'black'})
                    # Estilizando o separador
                ], className="card-text",
                    style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                html.P(children=[
                    html.Span(children=["Data: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                    f"{cenario['data']}",
                    html.Span(children=[" |"], style={'fontStyle': 'italic', 'color': 'black'})
                    # Estilizando o separador
                ], className="card-text",
                    style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),

                html.P(children=[
                    html.Span(children=["Tipo: "], style={'fontWeight': 'bold', 'color': 'gray'}),
                    f"{cenario['tipo']}",
                    html.Span(children=[" |"], style={'fontStyle': 'italic', 'color': 'black'})
                    # Estilizando o separador
                ], className="card-text",
                    style={'fontFamily': 'Arial Narrow', 'fontSize': '12px'}),
            ],
                style={'display': 'flex', 'flexDirection': 'row', 'gap': '35px'}
            ),

            # Div com a descrição
            html.Div(children=[
                # Texto da descrição
                html.Span(children=["Descrição: "],
                          style={
                              'fontWeight': 'bold',
                              'color': 'gray',
                              'fontSize': '12px',
                              'fontFamily': 'Arial Narrow',
                              'lineHeight': '20px'  # Ajuste para alinhar com a altura da imagem
                          }),

                # Descrição em si
                html.P(children=[f"{cenario['descricao']}"],
                       style={
                           'fontFamily': 'Arial Narrow',
                           'fontSize': '12px',
                           'margin': '0',  # Remover margens para alinhamento exato
                           'lineHeight': '20px'  # Mesma altura de linha que o span e a imagem
                       }),

                # Imagem ao lado do texto
                html.Img(src='/assets/img/excel_icon.png',
                         style={
                             'height': '20px',
                             'width': '20px',
                             'marginLeft': '260px',
                             'verticalAlign': 'middle'  # Garantir que a imagem alinhe ao centro
                         })
            ],
                style={
                    'display': 'flex',
                    'flexDirection': 'row',
                    'gap': '10px',  # Ajuste de espaço entre os elementos
                    # 'border': '1px solid #ccc',
                    'alignItems': 'center',  # Centralizar verticalmente
                    'padding': '5px'  # Um pouco mais de padding para garantir espaço interno
                }
            ),

            # Botão de exclusão
            # dbc.Button(children=["🗑️"], id={"type": "delete-button", "index": cenario["id"]}, n_clicks=0, color="danger")
        ]),
        style={'border': '1px solid #ccc',
               'margin': '10px',
               'marginBottom': '20px',
               'padding': '3px',
               'width': '600px',  # Largura fixa
               'height': '130px',  # Altura fixa
               'background': "linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), "
                             "url('/assets/img/eolicas.jpg')",
               'backgroundSize': 'cover',
               'backgroundPosition': 'center',
               'border-radius': '10px'
               }
    )
    return card


# 5) Função para formatar a data brasileira ----------------------------------------------------------------------------
def formatar_data_brasileira(data):
    """Formata uma data do Python para o formato DD/MM/AAAA HH:MM:SS."""
    if isinstance(data, datetime):
        return data.strftime('%d/%m/%Y %H:%M:%S')
    return data


# 6) Função para aplicar formatação de datas ---------------------------------------------------------------------------
def aplicar_formato_data(documento):
    """Percorre o documento e formata as datas encontradas no formato brasileiro."""
    for chave_cenario, entradas in documento.items():
        for entrada in entradas:
            # Formata a data de cada entrada se for uma instância de datetime
            if 'data' in entrada and isinstance(entrada['data'], datetime):
                entrada['data'] = formatar_data_brasileira(entrada['data'])
    return documento


# 7) Função para gerar a lista de cards -------------------------------------------------------------------------------
def gerar_lista_cards(agrupado_formatado: dict[list[dict]],
                      agrupado_formatado_cenarios: dict[list[dict]]) -> list[html.Div]:
    cards = []

    for grupo, itens in agrupado_formatado.items():
        # print(grupo)  # debug Cenário 1, Cenário 2, etc

        div: html.Div = html.Div(children=[
            # Div com o título do grupo
            dmc.Stack([
                dmc.Divider(label=grupo,
                            color="lightgray",
                            labelPosition="left",
                            size="md",
                            style={
                                'fontWeight': 'bold',
                                'fontFamily': 'Arial Narrow',
                                'fontSize': '16px',
                                'marginTop': '10px',
                                'marginBottom': '10px',
                                'color': 'gray',
                            })]),

            # Div com o botão de exclusão
            html.Div([
                dbc.Button(children=["🗑️"], n_clicks=0,
                           className="delete-button-cenarios",
                           id={"type": "delete-btn", "index": grupo}
                           ),
            ]),

            # Div com os cards
            html.Div([render_card(cenario=item) for item in itens], style={'display': 'flex',
                                                                           'flexDirection': 'column',
                                                                           # 'border': '1px solid gold',
                                                                           'padding': '10px',
                                                                           'marginBottom': '10px', })
        ], style={
            # 'border': '1px solid red',
            'marginBottom': '10px',
        })
        # print(grupo)  # debug Cenário 1, Cenário 2, etc
        # print(itens)  # debug Lista com os dicionários dos cenários parte 1, 2, 3, 4.
        cards.append(div)  # Título do grupo

    return cards


# 8) Função para criar os cenários -------------------------------------------------------------------------------------
def criar_cenarios(dicionario: dict[list[dict]]) -> dict[dict:list[dict]]:
    # Criar um novo dicionário com a chave "Cenários"
    cenarios = {"Cenários": dicionario}
    return cenarios


# 9) Função para deserializar JSON -------------------------------------------------------------------------------------
def json_deserial(data):
    # Verifica se 'data' é um dicionário que contém cenários
    if isinstance(data, dict) and 'Cenários' in data:
        for cenario, documentos in data['Cenários'].items():
            # Verifica se 'documentos' é uma lista
            if isinstance(documentos, list):
                for doc in documentos:
                    for key, value in doc.items():
                        # Converte strings que representam ObjectId de volta ao formato ObjectId
                        if key == '_id' and isinstance(value, str):
                            doc[key] = ObjectId(value)
                        # Converte strings ISO de volta para datetime
                        elif isinstance(value, str) and 'T' in value and ':' in value:
                            try:
                                doc[key] = datetime.fromisoformat(value)
                            except ValueError:
                                pass  # Ignora erros de conversão
    return data


# 10) Função para serializar JSON --------------------------------------------------------------------------------------
def stringify_object_ids(data):
    for cenario, docs in data.items():
        for doc in docs:
            if '_id' in doc and isinstance(doc['_id'], ObjectId):
                doc['_id'] = str(doc['_id'])
    return data


