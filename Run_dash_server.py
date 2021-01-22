# Back-end libs
import sqlite3
import pandas as pd
import numpy
from pathlib import Path

# -----------------------------------------------------

# Fornt-end libs
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# -----------------------------------------------------
def rename(dataframe):
#     col=['Date','Ref','Ab_change','Rel_change','Close','Vol','Open','High','Low','Agreement','For_sell','For_buy','For_net']
    
#     col=['Date','Ref','Ab_change','Rel_change','Close','Vol','Open','High','Low','Agreement','For_sell','For_buy']
    dataframe.columns = dataframe.iloc[0,:]
    dataframe.drop(index=0,inplace=True)
#     dataframe.drop(columns=['STT'],inplace=True)
    dataframe.reset_index(inplace=True,drop=True)
    
#     dataframe.columns = col

def all_files():
    return [path for path in list(Path(r'./All_prices').glob('**/*')) if '.xlsx' in str(path)]


def thousand_handle(ar):
    if type(ar) == str:
        if '%' in ar:
            ar = ar.replace('%','')
            ar= ar.replace(',','')
            ar = ar.replace('.','')
            ar = int(ar)/10000
        else:
            ar= ar.replace(',','')
#             ar = ar.replace('.','')
            ar = float(ar)
    return ar

def all_handle(dataframe):
    rename(dataframe)
    dataframe.drop(columns=[0,'STT'],inplace=True)
    dataframe.dropna(how='all',axis=0,inplace=True)

    dataframe['Ngày'] = pd.to_datetime(dataframe['Ngày'],format='%d-%m-%Y') 

    dataframe.sort_values(by=['Ngày'], inplace=True, ascending=True)

#     for col in dataframe.columns:
#         dataframe[col] = dataframe[col].map(thousand_handle)
    return dataframe


def sql_conn(ind):
    conn =  sqlite3.connect('D:/Simulation/Data/%s.db'%ind , check_same_thread=False)
    return conn


def to_sql(dataframe,stk,conn,if_existed):
    dataframe.to_sql('%s'%stk,con=conn,if_exists = if_existed)


def get_stk(stk):
    return pd.read_sql('select * from %s' %(stk),con=conn)
# It's better if we could add cols argurment for choosing  columns.
#     if not cols:
#         return pd.read_sql('select * from %s' %(stock),con=conn)
#     else:
#         cols.append(stk)
#         return pd.read_sql('select %s from %s' %(cols),con=conn)


def get_stk_excel(stk):
    return pd.read_excel('D:/Simulation/All_prices/%s.xlsx'%stk, engine='openpyxl',converters= {'Ngày': pd.to_datetime},thousands=',')


def get_stk_name():
    f= open("D:/Simulation/All_prices/sorted_all_prices.txt","r")
    String_stk= f.read()
    stk_lis = String_stk.split(",")
    f.close()
    stk_dict = [{'value':stk_lis[i],'label':stk_lis[i]} for i in range(len(stk_lis))]
    return stk_dict


opt_lis = get_stk_name()


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div([
            html.Div(
                [
                    html.H6("""Select stock ID""",
                            style={'margin-right': '2em'})
                ],
            ),

            dcc.Dropdown(
                id='my-input',
                options=opt_lis,
                placeholder="Select stock ID",
                style=dict(
                    width='40%',
                    verticalAlign="middle"
                )
            )
        ],
        style=dict(display='flex')
    ),
    html.Br(),
    # html.Div(id='my-output'),
    dcc.Graph(id='my-output',figure={})

])


@app.callback(
    Output(component_id='my-output', component_property='figure'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    # print(type(input_value))
#     conn = sql_conn("All_stock")
#     df = get_stk(input_value)
    if input_value is not None:
        df = all_handle(get_stk_excel(input_value))

        df.sort_values(by=['Ngày'], inplace=True, ascending=True)
        # print(df['Ngày'][0],type(df['Ngày'][0]))

        fig = go.Figure(data=[go.Candlestick(x=df['Ngày'],
                    open=df['Mở Cửa (*)'],
                    high=df['Cao Nhất(*)'],
                    low=df['Thấp Nhất(*)'],
                    close=df['Đóng Cửa (*)'])])
        fig.update_layout(
	    yaxis = dict(
     fixedrange = False),autosize=False,
    width=1300,
    height=700)

    fig.update_xaxes(
        rangeslider_visible=True,
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "sun"]),  # hide weekends, eg. hide sat to before mon
            # dict(bounds=[16, 9.5], pattern="hour"),  # hide hours outside of 9.30am-4pm
            # dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
        ]
    )
    
    return fig


if __name__ == '__main__':
    app.run_server(debug= True,host= '0.0.0.0',port = 80)