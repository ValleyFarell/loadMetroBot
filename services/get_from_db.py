import pandas as pd 

def get_loaded(station, date) -> int:
    data = pd.read_csv('database/data_clened.csv')
    data = data.set_index('station')
    

