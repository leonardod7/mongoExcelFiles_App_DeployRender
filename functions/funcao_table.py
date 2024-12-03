from dash import dash_table


def format_data_table(dataframe):
    # Converte os valores numéricos para o formato brasileiro (R$ ou números formatados)
    for col in dataframe.select_dtypes(include=['float', 'int']).columns:
        dataframe[col] = dataframe[col].apply(lambda x: f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

    # Configurações de estilo para o DataTable
    tabela: dash_table.DataTable = dash_table.DataTable(
        data=dataframe.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in dataframe.columns],
        page_size=5,
        style_cell={
            'textAlign': 'center',  # Alinhamento centralizado
            'padding': '10px',  # Espaçamento interno
            'fontFamily': 'Arial, sans-serif',  # Fonte
            'fontSize': '14px'  # Tamanho da fonte
        },
        style_header={
            'backgroundColor': '#f4f4f4',  # Cor de fundo do cabeçalho
            'fontWeight': 'bold',  # Negrito no cabeçalho
            'border': '1px solid #ddd',  # Borda ao redor do cabeçalho
            'textAlign': 'left',  # Alinhamento centralizado
        },
        style_data={
            'backgroundColor': '#ffffff',  # Cor de fundo das células
            'border': '1px solid #ddd'  # Borda ao redor das células
        },
        style_data_conditional=[
            # Alinhamento à esquerda da primeira coluna
            {
                'if': {'column_id': dataframe.columns[0]},
                'textAlign': 'left'
            },

            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f9f9f9',  # Cor alternada para linhas ímpares
            },
            {
                'if': {'filter_query': '{Valor} < 0', 'column_id': 'Valor'},
                'color': 'red',  # Formata valores negativos em vermelho
                'fontWeight': 'bold'  # Valores negativos em negrito
            }
        ],
        style_as_list_view=True,  # Estilo de tabela mais compacto
        page_action='none',  # Desativa a paginação
        fixed_rows={'headers': True},  # Cabeçalho fixo
    )

    return tabela
