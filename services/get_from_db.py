import pandas as pd 

data = pd.read_csv('database/data_clened.csv', index_col='station')
def get_loaded(station, date):
    return data.at[station, date]