import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State

### Load Data
df1 = pd.read_csv('data/index.csv')
df2 = pd.read_csv('data/details.csv')

### General Functions to render data
def getTabs(idx):
    tabs = []
    i=-1
    for num in idx:
        i +=1
        tabs.append(
            dbc.Tab(
                    label=f"Context: {df2.iloc[num]['context']}",
                    tab_id=f"tab{i}",
                    children=[
                        html.Div([
                            dbc.Card(
                                dbc.CardBody([
                                        html.P(f"Data: {df2.iloc[num]['data']}", className="card-text"),
                                    ]),className="mt-3",
                                )
                        ])
                    ])
        )
    return dbc.Tabs(
        id="tab",
        children=tabs,
        active_tab="tab0"
    )

def getmodal(country):
    idx = df2[df2['country'] == country]['context'].index.to_list()
    return dbc.Modal(
            [
                dbc.ModalHeader(f"Country Details: {df2.iloc[idx[0]]['country']}"),
                dbc.ModalBody([
                        getTabs(idx)
                ],className="m-2 p-2"),
                dbc.ModalFooter(
                    dbc.Button("CLOSE BUTTON", id="close", className="ml-auto")
                ),
            ],
            id="modal",is_open=True,style={"height":"100rem"},size="xl"
        )

def getCard(index):
    return dbc.Card([
                    html.H6(f"{df1.iloc[index]['country']}", className="card-header"),
                    html.P(f"Number of Contexts: {df1.iloc[index]['NumContext']}",className="card-text"),
                    html.P(f"Total Cases: {df1.iloc[index]['totalCases']}",className="card-text"),
                    dbc.Button("Open", id="open" + str(index), n_clicks_timestamp=0, className="m-2 button-info align-self-center rounded-3",style={"width":"5rem"})
        ],style={"width":"20rem","text-align":"center"},className="m-2")

#### Dash App Starts
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO],suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

app.layout = dbc.Container([
    dbc.Col([
            dbc.Row(
                        children=[getCard(i) for i in range(len(df1['country']))],className="m-2 py-5",justify="center"
            )
        ],width=12),
    html.Div(id="modal-div",style={"height":"100rem"})
],fluid=True)

@app.callback(
    Output("modal-div", "children"),
    [Input(f'open{i}', 'n_clicks_timestamp') for i in range(len(df1['country']))]
)
def update(*button_clicks):
    if(dash.callback_context.triggered[0].get('prop_id')!='.'):
        #print(f'************** {dash.callback_context.triggered[0]}')
        #print(f"************** {int(dash.callback_context.triggered[0].get('prop_id').split('.')[0][-1])}")
        id = int(dash.callback_context.triggered[0].get('prop_id').split('.')[0][-1])
        print(f"id = {id} country selected: {df1.iloc[id]['country']}")
        return getmodal(df1.iloc[id]['country'])
    else:
        return ''

@app.callback(
    Output("modal", "is_open"),
    Input("close", "n_clicks")
)
def toggle_modal1(c1):
    if c1:
        return False
    else:
        return True


if __name__=='__main__':
    app.run_server(host="0.0.0.0",debug=True, port = 8080)
