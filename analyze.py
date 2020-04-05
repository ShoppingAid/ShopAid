import pandas
from datetime import datetime

store=input("Store Name\n")
day=input("Day of visit\n")
now=datetime.today()
time=input("enter planned time of visit, eg:6PM \n")
df=pandas.read_csv('/Users/vikramsingh/Downloads/result_upd.csv')

def get_row(store,day,time):
	subDf=df[(df['name']==store) & (df['time_wait_name']==day) & (df['Store Timing']==time)]
	wait_time=subDf['time_wait_data'].item()
	return wait_time;

wait_time=get_row(store,day,time)
if wait_time <= 5:
	print("Not busy")
elif wait_time < 20:
	print("Slightly busy")
else:	
	print("Extremely busy")

print(wait_time)
