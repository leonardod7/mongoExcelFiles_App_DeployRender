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




