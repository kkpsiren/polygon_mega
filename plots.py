import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st

def plot_new_addresses(df,x0='NEW_ADDRESS',x1='CUMULATIVE_ADDRESS'):
    df['MIN_DATE']  =pd.to_datetime(df['MIN_DATE'])
    random_x = df['MIN_DATE'].tolist()
    random_y0 = df[x0].tolist()
    random_y1 = df[x1].tolist()

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=random_x, y=random_y0,
                        #mode='lines',
                        name=x0.capitalize().replace('_', ' ')),secondary_y=True)
    fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                        mode='lines',
                        name=x1.capitalize().replace('_', ' ')),secondary_y=False)

    fig.update_yaxes(title_text="New Addresses", secondary_y=True)
    fig.update_yaxes(title_text="Total Addresses", secondary_y=False)
    fig.update_layout(hovermode="x")
    fig.update_layout(barmode='stack', bargap=0.0,bargroupgap=0.0)
    fig.update_traces(marker_line_width=0)

    return fig

def plot_average_new_addresses_per_day(df2):
    fig =  px.bar(data_frame=df2.sort_values(by='TYPE'),x='TYPE',y='NEW_ADDRESS')
    return fig

def plot_melt(df3):
    df3 = df3.melt()
    fig =  px.bar(data_frame=df3,x='variable',y='value')
    return fig

def plot_active_addresses(df,x0='USERS_DOING_TRANSACTIONS',x1='MATIC_PRICE',x2='USERS_RECEIVING_TOKENS'):
    #st.write(df.columns)
    df['DATE'] = pd.to_datetime(df['DATE'])
    random_x = df['DATE'].tolist()
    random_y0 = df[x0].tolist()
    random_y1 = df[x1].tolist()
    random_y2 = df[x2].tolist()

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=random_x, y=random_y0,
                         offsetgroup=0,
                        #mode='lines',
                        name=x0.capitalize().replace('_', ' ')),secondary_y=False)

    fig.add_trace(go.Bar(x=random_x, y=random_y2,
                         offsetgroup=0,
                         base=random_y0,
                        #mode='lines',
                        name=x2.capitalize().replace('_', ' ')),secondary_y=False)

    fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                        mode='lines',
                        name=x1.capitalize().replace('_', ' ')),secondary_y=True)

    fig.update_yaxes(title_text="MATIC Price", secondary_y=True)
    fig.update_yaxes(title_text="Active Users", secondary_y=False)
    fig.update_layout(hovermode="x")
    fig.update_layout(barmode='stack', bargap=0.0,bargroupgap=0.0)
    fig.update_traces(marker_line_width=0)
    return fig

def plot_marketcap(df,x0='MARKET_CAP',x1='MATIC_AVERAGE_PRICE',x2='CIRCULATING_SUPPLY'):
    df = df.sort_values('DATE')
    df['DATE']  =pd.to_datetime(df['DATE'])
    random_x = df['DATE'].tolist()
    random_y0 = df[x0].tolist()
    random_y1 = df[x1].tolist()
    random_y2 = df[x2].tolist()

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])


    fig.add_trace(go.Bar(x=random_x, y=random_y2,
                         offsetgroup=1,
                         # base=random_y0,
                        #mode='lines',
                        name=x2.capitalize().replace('_', ' ')),secondary_y=False)

    
    fig.add_trace(go.Bar(x=random_x, y=random_y0,
                         offsetgroup=0,
                        #mode='lines',
                        name=x0.capitalize().replace('_', ' ')),secondary_y=False)
    
    fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                        mode='lines',
                        name=x1.capitalize().replace('_', ' ')),secondary_y=True)

    fig.update_yaxes(title_text="MATIC Price", secondary_y=True)
    fig.update_yaxes(title_text="Supply/Cap", secondary_y=False)
    fig.update_layout(hovermode="x")
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig.update_layout(barmode='group', bargap=0.0,bargroupgap=0.0)
    fig.update_traces(marker_line_width=0)
#    fig.update_traces(#marker_color='rgb(158,202,225)', 
#                      marker_line_color='rgb(8,48,107)',
#                  marker_line_width=1.5, opacity=0.6)

    return fig

def plot_fees(df,x0='AVG_TXN',x2='FEES'):
    
    df['DATE']  =pd.to_datetime(df['DATE'])
    df = df.sort_values('DATE')
    random_x = df['DATE'].tolist()
    random_y0 = df[x0].tolist()
    random_y2 = df[x2].tolist()

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=random_x, y=random_y0,
                         offsetgroup=0,
                        #mode='lines',
                        name=x0.capitalize().replace('_', ' ')),secondary_y=False)

    fig.add_trace(go.Bar(x=random_x, y=random_y2,
                         offsetgroup=1,
                         # base=random_y0,
                        #mode='lines',
                        name=x2.capitalize().replace('_', ' ')),secondary_y=True)

    fig.update_yaxes(title_text="Average Fees", secondary_y=True)
    fig.update_yaxes(title_text="Average Transactions", secondary_y=False)
    fig.update_layout(hovermode="x")
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig.update_layout(barmode='stack', bargap=0.0,bargroupgap=0.0)
    fig.update_traces(marker_line_width=0)
#    fig.update_traces(#marker_color='rgb(158,202,225)', 
#                      marker_line_color='rgb(8,48,107)',
#                  marker_line_width=1.5, opacity=0.6)

    return fig