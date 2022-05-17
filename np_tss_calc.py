# import libraries
import pandas as pd
import numpy as np
import psycopg2

# normalized power function
# source article: https://jaylocycling.com/easily-understand-cycling-normalized-power/
def normalized_power(activity_id):
    df = pd.read_sql_query("""select power, rank () over (order by timestamp asc) as rank_no from record 
                            where activity_id = {}""".format(activity_id), conn)  
    WindowSize = 30; # second rolling average
    NumberSeries = pd.Series(df.power)
    NumberSeries = NumberSeries.dropna()
    Windows      = NumberSeries.rolling(WindowSize)
    Power_30s    = Windows.mean().dropna()
    PowerAvg     = round(Power_30s.mean(),0)
    NP = round((((Power_30s**4).mean())**0.25),0)
    return(NP)

# TSS function
# source article: https://www.trainingpeaks.com/learn/articles/estimating-training-stress-score-tss/
def tss(activity_id, ftp, NP):
    sec = pd.read_sql_query("""select count(*) from record 
                            where activity_id = {}""".format(activity_id), conn).iloc[0][0]
    TSS = (sec*NP*NP/ftp)/(ftp*3600) *100
    return(TSS)

conn = psycopg2.connect(host="localhost", database="garmin_data", user="postgres", password="*****")
tss_df = pd.read_csv('power_zones_data_rf_comparison.csv', index_col=0)
tss_df['NP'] = tss_df.apply(lambda row: normalized_power(row['activity_id']), axis=1)
tss_df['TSS'] = tss_df.apply(lambda row: tss(row['activity_id'], row['power_threshold'], row['NP']), axis=1)