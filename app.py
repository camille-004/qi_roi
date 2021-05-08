import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np

data = pd.read_csv('data/data.csv')
data = data.rename(columns={'Unnamed: 0': 'Schools'})
data.set_index('Schools', inplace=True)

str_cols = data.select_dtypes(object).columns
data[str_cols] = data[str_cols].apply(
    lambda x: x.str.replace('$', '').str.replace(',', '')) \
    .astype(float)

data = data.fillna(-1)

# ---- REINDEX CC/FRESHMAN GRAD RATES ---- #
data_grad = data.filter(regex='Schools|CC|Freshman')
idx = data_grad.columns.str.split(' ', 1).str[1].str.split(' ', expand=True)
data_grad.columns = idx
idx = pd.MultiIndex.from_product([idx.levels[0], idx.levels[1]])
data_grad = data_grad.reindex(columns=idx, fill_value=-1)

# ---- CREATE DASH APP ---- #
external_stylesheets = ['css/main.css', 'css/normalize.css',
                        'css/skeleton,css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Label('Choose a UC'),
    dcc.Dropdown(
        id='School',
        options=[
            {'label': i, 'value': i} for i in data.index
        ],
        value='University of California, San Diego'
    ),
    html.H1('Average Number of Years to Graduate'),
    dcc.Graph(id='grad-table'),
    dcc.Graph(id='grad-graph'),
    html.H1('Average Salaries by Engineering Major'),
    dcc.Graph(id='major-graph'),
],
    style={'width': '50%',
           'display': 'inline-block'}
)


# ---- CODE FOR VISUALS ---- #
@app.callback(
    dash.dependencies.Output('grad-table', 'figure'),
    [dash.dependencies.Input('School', 'value')]
)
def update_freshman_grad_table(School):
    df_plot = data_grad.loc[School].to_frame()
    fig = go.Figure(data=[go.Table(header=dict(values=[
        'School Year', 'Freshman', 'Transfer']),
        cells=dict(values=[
            df_plot.loc['Freshman'].index,
            np.round(
                df_plot.loc['Freshman'].values, 2),
            np.round(
                df_plot.loc['Transfer'].values, 2)])
    )])
    return fig


@app.callback(
    dash.dependencies.Output('grad-graph', 'figure'),
    [dash.dependencies.Input('School', 'value')]
)
def update_freshman_grad_graph(School):
    df_plot = data_grad.loc[School].to_frame().T.stack().droplevel(0) \
        .reset_index().rename(
        columns={'index': 'Year'})
    trace1 = px.line(df_plot, x='Year', y=['Freshman', 'Transfer'], labels={
        'index': 'Academic Year',
        'value': 'Avg. Years to Gradudate'
    }, title='Avg. Years to Graduate: First-Time Freshman')
    trace1.update_layout(yaxis_range=[1, 5])
    return trace1


@app.callback(
    dash.dependencies.Output('major-graph', 'figure'),
    [dash.dependencies.Input('School', 'value')]
)
def update_freshman_grad_graph(School):
    df_plot = data.loc[School].filter(like='Engineering')
    df_plot = df_plot[df_plot >= 0]
    trace1 = px.bar(df_plot, labels={'index': 'Major', 'value': 'Salary'},
                    title='Average Salaries by Engineering Major')
    trace1.update_layout(showlegend=False)
    return trace1


# ---- RUN SERVER ---- #
if __name__ == '__main__':
    app.run_server(debug=True)
