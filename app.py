# Importando as bibliotecas --------------------------------------------------------------------------------------------
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
