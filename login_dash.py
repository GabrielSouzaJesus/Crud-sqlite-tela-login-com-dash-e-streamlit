import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from Crud import ler_usuarios

app = dash.Dash(__name__)

usuarios = ler_usuarios()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app.layout = html.Div([
    html.Div([
        html.H2('Bem-vindo a tela de login', style={'textAlign': 'center', 'color': 'white'}),  

        dcc.Dropdown(id='user-dropdown', options=[{'label': user.nome, 'value': user.nome} for user in usuarios],
                     style={'width': '100%', 'margin-bottom': '10px', 'border-radius': '5px'}),  

        dcc.Input(id="password", type="password", placeholder="Senha", style={'width': '100%', 'margin-bottom': '10px', 'border-radius': '5px'}),

        html.Button('Entrar', id='login-button', style={'width': '100%', 'border-radius': '5px', 'transition': 'background-color 0.3s'}),
        

        html.Div(id='login-output', style={'marginTop': '10px'})  

    ], className='login-form', style={'width': '300px', 'margin': 'auto', 'marginTop': '50px', 'padding': '20px',
                                      'border': '2px solid white', 'border-radius': '10px', 'background': 'rgba(0, 0, 0, 0.3)'}),
    

], id='login-page', style={'background': 'url("https://e1.pxfuel.com/desktop-wallpaper/646/773/desktop-wallpaper-login-page-login.jpg")',
                            'background-size': 'cover', 'height': '100vh', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})


app.css.append_css({'external_url': external_stylesheets})

@app.callback(
    [Output('login-page', 'children'),
     Output('login-output', 'children')],
    [Input('login-button', 'n_clicks')],
    [State('user-dropdown', 'value'),
     State('password', 'value')]
)
def update_output(n_clicks, selected_user, password):
    if n_clicks is None:
        return dash.no_update

    usuarios_dict = {usuario.nome: usuario for usuario in usuarios}
    if selected_user in usuarios_dict:
        usuario = usuarios_dict[selected_user]
        if usuario.verifica_senha(password):
            return html.H2(f'Bem-vindo ao WebApp, {selected_user}', style={'textAlign': 'center', 'color': 'white'}), ''
        else:
            return dash.no_update, 'Senha Incorreta'

    return html.H2(f'Bem-vindo ao WebApp, {selected_user}', style={'textAlign': 'center', 'color': 'white'}), ''

if __name__ == '__main__':
    app.run_server(debug=True)
