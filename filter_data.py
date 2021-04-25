#%%
import pandas as pd
import plotly.graph_objects as go
pd.options.plotting.backend = "plotly"

data = pd.read_csv('data/data.csv')
data = data.rename(columns={'Unnamed: 0': 'Schools'})

str_cols = data.select_dtypes(object).columns[1:]
data[str_cols] = data[str_cols].apply(
    lambda x: x.str.replace('$', '').str.replace(',', ''))\
    .astype(float)

data = data.fillna(-1)

fig = go.Figure()
data.set_index('Schools').T.plot()
fig.show()
