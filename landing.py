import streamlit as st
import pandas as pd
from scripts import load_queries
from plots import * 
import datetime
#cm = sns.light_palette("green", as_cmap=True)
#   with st.expander('show list'):
#        st.dataframe(data.sort_values(by='USD',ascending=False).style.background_gradient(cmap=cm))
        

def get_change(ser,previous,what='NEW_ADDRESS'):
    if what =='USER':
        a = ser['USERS_DOING_TRANSACTIONS']+ser['USERS_RECEIVING_TOKENS']
        b = previous['USERS_DOING_TRANSACTIONS']+previous['USERS_RECEIVING_TOKENS']
        change = f"{((a.values[0] / b.values[0])-1)*100:.2f} %"
        
    else:
        change = f"{((ser[what].values[0] / previous[what].values[0])-1)*100:.2f} %"
    return change

def merge_data(df,df4,df5,df6):
    df5['DATE'] = pd.to_datetime(df5['DATE'])
    df4['DATE'] = pd.to_datetime(df4['DATE'])
    df6['DATE'] = pd.to_datetime(df6['DATE'])
    df['MIN_DATE'] = pd.to_datetime(df['MIN_DATE'])
    df_combined = df.merge(df4,left_on='MIN_DATE',right_on='DATE').merge(df5,on='DATE').merge(df6,on='DATE')
    df_combined = df_combined.drop(['MIN_DATE','MATIC_AVERAGE_PRICE'],axis=1)
    return df_combined.drop_duplicates()

def landing_page():
    #st.image('https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/pstweatifgo8tmub5atc')

    st.sidebar.image("https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/pstweatifgo8tmub5atc",width=40)
    st.sidebar.title("Polygon Megaboard")
    st.sidebar.write("""Let's combine the dashboards from the Polygon Grand Prize Winners. 🏆 """)
                     
    
    with st.spinner(text="Fetching Data..."):
        df,df2,df3,df4,df5,df6 = load_queries()
    

    st.sidebar.markdown(
        """
## 👤 New Users 

The total number of new addresses is growing faster in 2022 than ever before. It has now reaches over 15M. Recently on June 27th, there was an all time high for the new daily addresses of almost 180k. 

### 🏃‍♀️ Active Users 

The user activity seems to follow the Matic price. The highs followed by decrease will create many active users.
Most of the active users are active as they sending transcations and only every sixth user is active because of receiving tokens. Although there are more than 15M wallets, only 300k users are active. 

### Activity is linked with MATIC 🏃 🟰 🤑

The overall activity of the userbase has dropped as the market cap and MATIC price have fallen since the bear market.
Interestingly the recent positive upturn has not increased the active user base so far.  While the active userbase has peaked, the transaction fees when measured with MATIC stay constant. This is with the exception of few days. Interestingly the fees have stayed similar while the Average transaction count has dropped. 
    """)
    st.sidebar.write("""#### Powered by GodMode by FlipsideCrypto and ShroomDK 🫡""")


#l,r = st.columns(2)
#with l:
    st.subheader('Overall status of the Polygon')
    st.write('Matic Price, Circulating Supply and Market cap')
    
    st.plotly_chart(plot_marketcap(df5,x0='MARKET_CAP',x1='MATIC_AVERAGE_PRICE',x2='CIRCULATING_SUPPLY'),use_container_width=True)
#with r:
    st.write('Average Number of Transactions and Fees generated')
    
    st.plotly_chart(plot_fees(df6,x0='AVG_TXN',x2='FEES'),use_container_width=True)

    l,r = st.columns(2)
    with l:
        st.subheader('User Growth')
        st.write('Yearly Comparison')
        st.plotly_chart(plot_average_new_addresses_per_day(df2),use_container_width=True)
    with r:
        st.subheader('Activity Breakdown')
        st.write('Does the activity come from receiving tokens or from executing transactions?')
        st.plotly_chart(plot_melt(df3),use_container_width=True)
    


#l,r = st.columns(2)
#with l:
    st.subheader('Users')
    st.write('Daily new addresses and the cumulative total')
    st.plotly_chart(plot_new_addresses(df,x0='NEW_ADDRESS',x1='CUMULATIVE_ADDRESS'),use_container_width=True)
#with r:
    st.write('Daily active addresses and the cumulative total with $MATIC Price')
    st.plotly_chart(plot_active_addresses(df4,x0='USERS_DOING_TRANSACTIONS',x1='MATIC_PRICE',x2='USERS_RECEIVING_TOKENS'),use_container_width=True)

    st.write('MATIC holders vs circulating supply')
    st.plotly_chart(plot_holder(df5,x0='HOLDERS',x2='CIRCULATING_SUPPLY'),use_container_width=True)

    st.write('MATIC holders vs market cap')
    st.plotly_chart(plot_holder(df5,x0='HOLDERS',x2='MARKET_CAP'),use_container_width=True)


    st.subheader('Investigate Specific Dates')
    df_combined = merge_data(df,df4,df5,df6)
    
    d = st.date_input(
     "Select Date",value=datetime.datetime.today()-datetime.timedelta(days=1),min_value=df_combined['DATE'].min(),
     max_value=datetime.datetime.today()-datetime.timedelta(days=1))
    
    ser = df_combined[df_combined['DATE']==pd.to_datetime(d)]
    if ser.shape[0] == 0:
        ser = df_combined[df_combined['DATE']==pd.to_datetime('2022-08-03')]
    previous = df_combined[df_combined['DATE']==(pd.to_datetime(d) - datetime.timedelta(days=1))]
    r = st.columns(3)
    
    
    with r[0]:
        st.write(ser)
        label = 'New Users'
        value = ser['NEW_ADDRESS'].values[0]
        delta = get_change(ser,previous,what='NEW_ADDRESS')
        st.metric(label, value, delta=delta, delta_color="normal", help=None)
    with r[1]:
        label = 'Active Users'
        value = (ser['USERS_DOING_TRANSACTIONS']+ser['USERS_RECEIVING_TOKENS']).values[0]
        delta = get_change(ser,previous,what='USER')
        st.metric(label, value, delta=delta, delta_color="normal", help=None)
    with r[2]:
        label = 'Matic Holders'
        value = ser['HOLDERS'].values[0]
        delta = get_change(ser,previous,what='HOLDERS')
        st.metric(label, value, delta=delta, delta_color="normal", help=None)
    
    r = st.columns(3)
    with r[0]:
        label = 'MarketCap'
        value = int(f"{ser['MARKET_CAP'].values[0]:.0f}")
        delta = get_change(ser,previous,what='MARKET_CAP')
        st.metric(label, value, delta=delta, delta_color="normal", help=None)
    with r[1]:
        label = 'Circulating Supply'
        value = int(f"{ser['CIRCULATING_SUPPLY'].values[0]:.0f}")
        delta = get_change(ser,previous,what='CIRCULATING_SUPPLY')
        st.metric(label, value, delta=delta, delta_color="normal", help=None)
    with r[2]:
       label = 'MATIC avg Price'
       value = float(f"{ser['MATIC_PRICE'].values[0]:.2f}")
       delta = get_change(ser,previous,what='MATIC_PRICE')
       st.metric(label, value, delta=delta, delta_color="normal", help=None)
    r = st.columns(3)
    with r[0]:
       label = 'Avg Hourly TX-rate'
       value = ser['AVG_TXN'].values[0]
       delta = get_change(ser,previous,what='AVG_TXN')
       st.metric(label, value, delta=delta, delta_color="normal", help=None)
    with r[1]:
       label = 'AVG Fees'
       value = int(f"{ser['FEES'].values[0]:.0f}")
       delta = get_change(ser,previous,what='FEES')
       st.metric(label, value, delta=delta, delta_color="normal", help=None)
       
       

    
    st.markdown(f""" 
### Credit
Queries reproduced here originated from the following Grand Prize winning Dashboards:  
🏆 https://app.flipsidecrypto.com/dashboard/active-addresses-AL7ktc  
🏆 https://app.flipsidecrypto.com/dashboard/new-addresses-4z1-_c  
🏆 https://app.flipsidecrypto.com/dashboard/price-circulating-supply-YBc5sp  
🏆 https://app.flipsidecrypto.com/dashboard/polygon-vs-harmony-l13ITg  

### 💻 Github
[kkpsiren/polygon_mega](https://github.com/kkpsiren/polygon_mega)  
    """)