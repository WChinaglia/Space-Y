# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                               dcc.Dropdown(
                                                id='site-dropdown',
                                                options=[{'label':'All Sites', 'value':'ALL'},
                                                        {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                                        {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                                        {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                                        {'label':'KSC LC-39A', 'value':'KSC LC-39A'}],
                                                value='ALL',
                                                placeholder='Select a SpaceX Launch Site',
                                                searchable=True,
                                                style={'font-size':'20px', 'textAlign':'center'}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                               min=min_payload,
                                               max=max_payload,
                                               step=1000, 
                                               marks={0:'0', 1000:'1000', 2000:'2000', 3000:'3000', 4000:'4000', 5000:'5000',
                                                      6000:'6000', 7000:'7000', 8000:'8000', 9000:'9000', 9600:'9600'},
                                               value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df
        fig = px.pie(data, values='class', names='Launch Site', title='Total Success Launches for All Sites')
        return fig
    else:
        if entered_site == 'CCAFS LC-40':
            data = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
        elif entered_site == 'CCAFS SLC-40':
            data = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        elif entered_site == 'VAFB SLC-4E':
            data = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        elif entered_site == 'KSC LC-39A':
            data = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
        fig = px.pie(data, names='class', title='Success vs Failed Launches for Site ' + entered_site)
        return fig
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(site, payload):
    data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0]) & (spacex_df['Payload Mass (kg)'] <= payload[1])]
    if site == 'ALL':
        fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    else:
        if site == 'CCAFS LC-40':
            data_new = data[data['Launch Site'] == 'CCAFS LC-40']
        elif site == 'CCAFS SLC-40':
            data_new = data[data['Launch Site'] == 'CCAFS SLC-40']
        elif site == 'VAFB SLC-4E':
            data_new = data[data['Launch Site'] == 'VAFB SLC-4E']
        elif site == 'KSC LC-39A':
            data_new = data[data['Launch Site'] == 'KSC LC-39A']        
        
        fig = px.scatter(data_new, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
