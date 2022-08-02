import streamlit as st

import requests
import json
import time
from queries import *
import os
import pandas as pd 

#from dotenv import load_dotenv
#load_dotenv()



class Flipsider:
    def __init__(self, API_KEY, TTL_MINUTES=60*24):
        self.API_KEY = API_KEY
        self.TTL_MINUTES = TTL_MINUTES

    def create_query(self, SQL_QUERY):
        r = requests.post(
            'https://node-api.flipsidecrypto.com/queries', 
            data=json.dumps({
                "sql": SQL_QUERY,
                "ttlMinutes": self.TTL_MINUTES
            }),
            headers={"Accept": "application/json", "Content-Type": "application/json", "x-api-key": self.API_KEY},
        )
        if r.status_code != 200:
            raise Exception("Error creating query, got response: " + r.text + "with status code: " + str(r.status_code))

        return json.loads(r.text)    


    def get_query_results(self, token):
        r = requests.get(
            'https://node-api.flipsidecrypto.com/queries/' + token, 
            headers={"Accept": "application/json", "Content-Type": "application/json", "x-api-key": self.API_KEY}
        )
        if r.status_code != 200:
            raise Exception("Error getting query results, got response: " + r.text + "with status code: " + str(r.status_code))
        
        data = json.loads(r.text)
        if data['status'] == 'running':
            time.sleep(10)
            return self.get_query_results(token)

        return data


    def run(self, SQL_QUERY):
        query = self.create_query(SQL_QUERY)
        token = query.get('token')
        data = self.get_query_results(token)
        df = pd.DataFrame(data['results'],columns = data['columnLabels'])
        return df

st.cache()
def load_queries():
    df = pd.read_csv('query1.csv',index_col=0)
    df2 = pd.read_csv('query2.csv',index_col=0)
    df3 = pd.read_csv('query3.csv',index_col=0)
    df4 = pd.read_csv('query4.csv',index_col=0)
    df5 = pd.read_csv('query5.csv',index_col=0)
    df6 = pd.read_csv('query6.csv',index_col=0)
    return df,df2,df3,df4,df5,df6

def save_queries(df,df2,df3,df4,df5,df6):
    df.to_csv('query1.csv')
    df2.to_csv('query2.csv')
    df3.to_csv('query3.csv')
    df4.to_csv('query4.csv')
    df5.to_csv('query5.csv')
    df6.to_csv('query6.csv')
    return 'saved'

def run_queries():
    # so sloooow
    bot = Flipsider(os.getenv('API_KEY'))
    df = bot.run(QUERY)
    print('1 done')
    df2 = bot.run(QUERY2)
    print('2 done')
    df3 = bot.run(QUERY3)
    print('3 done')
    df4 = bot.run(QUERY4)
    print('4 done')
    df5 = bot.run(QUERY5)
    print('5 done')
    df6 = bot.run(QUERY6)
    print('6 done')
    return df,df2,df3,df4,df5,df6

