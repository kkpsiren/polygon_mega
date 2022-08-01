import streamlit as st
import pandas as pd
from scripts import run_queries
from plots import * 
#cm = sns.light_palette("green", as_cmap=True)
#   with st.expander('show list'):
#        st.dataframe(data.sort_values(by='USD',ascending=False).style.background_gradient(cmap=cm))
        

def landing_page():
    #st.image('https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/pstweatifgo8tmub5atc')
    st.markdown("""## Polygon Mega 
Powered by GodMode by FlipsideCrypto and ShroomDK""")
    
    with st.spinner(text="Fetching Data..."):
        df,df2,df3,df4,df5,df6 = run_queries()
    
    
    l,r = st.columns(2)
    with l:
        st.plotly_chart(plot_new_addresses(df,x0='NEW_ADDRESS',x1='CUMULATIVE_ADDRESS'),use_container_width=True)
    with r:
        st.plotly_chart(plot_active_addresses(df4,x0='USERS_DOING_TRANSACTIONS',x1='MATIC_PRICE',x2='USERS_RECEIVING_TOKENS'),use_container_width=True)

    l,r = st.columns(2)
    with l:
        st.plotly_chart(plot_average_new_addresses_per_day(df2),use_container_width=True)
    with r:
        st.plotly_chart(plot_melt(df3),use_container_width=True)
    
    l,r = st.columns(2)
    with l:
        st.plotly_chart(plot_marketcap(df5,x0='MARKET_CAP',x1='MATIC_AVERAGE_PRICE',x2='CIRCULATING_SUPPLY'),use_container_width=True)
    with r:
        st.plotly_chart(plot_fees(df6,x0='AVG_TXN',x2='FEES'),use_container_width=True)

    
    st.markdown(
        """
The total number of new addresses is growing faster 2022 than ever before. It has now reaches over 15M. 
Recently on June 27th, there was an all time high for the new daily addresses of almost 180k.  
The user activity seems to follow the Matic price. The highs followed by decrease will create many active users.  
Most of the active users are active as they sending transcations and only every sixth user is active because of receiving tokens.  
Although there are more than 15M wallets, only 300k users are active. The activity of the userbase has dropped as the marketcap and MATIC price have fallen since the bearmarket.  
Interestingly the recent positive upturn has not increased any activeuser base currently.  While the active userbase has peaked, the transaction fees when measured with MATIC stay constant.  
This is with the exception of few days. Interestingly the fees have stayed similar while the Average transaction count has dropped. 
    """)

    
    st.markdown(f""" ## Conclusion
                

### Queries reproduced here originated from the following Grand Prize winning Dashboards:  
https://app.flipsidecrypto.com/dashboard/active-addresses-AL7ktc  

https://app.flipsidecrypto.com/dashboard/new-addresses-4z1-_c  

https://app.flipsidecrypto.com/dashboard/price-circulating-supply-YBc5sp  

https://app.flipsidecrypto.com/dashboard/polygon-vs-harmony-l13ITg  

### Github
[kkpsiren/polygon_mega](https://github.com/kkpsiren/polygon_mega)  
    """)