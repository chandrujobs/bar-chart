import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the dataset
data = pd.read_excel("C:/Users/Chandru/OneDrive/Desktop/Python Visuals/Sample - Superstore.xls", sheet_name="Orders")
data['Year'] = data['Order Date'].dt.year

# Create a Dash application
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'Sales', 'value': 'Sales'},
            {'label': 'Profit', 'value': 'Profit'}
        ],
        value='Sales',
        multi=False
    ),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in data['Year'].unique()],
        value=data['Year'].unique(),
        multi=True
    ),
    dcc.Graph(id='bar-chart')
])

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('metric-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_graph(selected_metric, selected_years):
    filtered_data = data[data['Year'].isin(selected_years)]
    category_data = filtered_data.groupby(['Category', 'Year'])[selected_metric].sum().reset_index()
    return px.bar(category_data, x='Category', y=selected_metric, color='Year', title=f'{selected_metric} by Product Category Year by Year')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
