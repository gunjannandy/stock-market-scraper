import urllib.request, json , time, os, difflib, itertools
import pandas as pd
from multiprocessing.dummy import Pool
from datetime import datetime

try:
    import httplib
except:
    import http.client as httplib

def check_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        # print("True")
        return True
    except:
        conn.close()
        # print("False")
        return False

def get_historic_price(query_url,json_path,csv_path):
    
    stock_id=query_url.split("&period")[0].split("symbol=")[1]

    if os.path.exists(csv_path+stock_id+'.csv') and os.stat(csv_path+stock_id+'.csv').st_size != 0:
        print("<<<  Historical data of "+stock_id+" already exists")
        return
    
    while not check_internet():
        print("Could not connect, trying again in 5 seconds...")
        time.sleep(5)

    try:
        with urllib.request.urlopen(query_url) as url:
            parsed = json.loads(url.read().decode())
    
    except:
        print("|||  Historical data of "+stock_id+" doesn't exist")
        return
    
    else:
        if os.path.exists(json_path+stock_id+'.json') and os.stat(json_path+stock_id+'.json').st_size != 0:
            os.remove(json_path+stock_id+'.json')
        with open(json_path+stock_id+'.json', 'w') as outfile:
            json.dump(parsed, outfile, indent=4)
        try:
            Date=[]
            for i in parsed['chart']['result'][0]['timestamp']:
                Date.append(datetime.utcfromtimestamp(int(i)).strftime('%d-%m-%Y'))

            Low=parsed['chart']['result'][0]['indicators']['quote'][0]['low']
            Open=parsed['chart']['result'][0]['indicators']['quote'][0]['open']
            Volume=parsed['chart']['result'][0]['indicators']['quote'][0]['volume']
            High=parsed['chart']['result'][0]['indicators']['quote'][0]['high']
            Close=parsed['chart']['result'][0]['indicators']['quote'][0]['close']
            Adjusted_Close=parsed['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']

            df=pd.DataFrame(list(zip(Date,Low,Open,Volume,High,Close,Adjusted_Close)),columns =['Date','Low','Open','Volume','High','Close','Adjusted Close'])

            if os.path.exists(csv_path+stock_id+'.csv'):
                os.remove(csv_path+stock_id+'.csv')
            df.to_csv(csv_path+stock_id+'.csv', sep=',', index=None)
            print(">>>  Historical data of "+stock_id+" saved")
        except:
            print(">>>  Historical data of "+stock_id+" could not be saved")
        return


json_path = os.getcwd()+os.sep+".."+os.sep+"historic_data"+os.sep+"json"+os.sep
csv_path = os.getcwd()+os.sep+".."+os.sep+"historic_data"+os.sep+"csv"+os.sep

if not os.path.isdir(json_path):
    os.makedirs(json_path)
if not os.path.isdir(csv_path):
    os.makedirs(csv_path)


# country_name = "india"



ticker_file_path = "Assets"+os.sep+"Yahoo Ticker Symbols - September 2017.xlsx"
temp_df = pd.read_excel(ticker_file_path)
# print("Total stocks:",len(temp_df))


temp_df = temp_df.drop(temp_df.columns[[5, 6, 7]], axis=1)
headers = temp_df.iloc[2]
df  = pd.DataFrame(temp_df.values[3:], columns=headers)
print("Total stocks:",len(df))



# new_df = df[df["Country"].str.lower().str.contains(country_name.lower()) == True]
# print("Total stocks:",len(new_df))
# new_df.head(10)

# new_df.to_csv('Assets'+os.sep+country_name+'.csv', sep=',', index=None)


# print(difflib.get_close_matches('igarashi motors india', new_df['Name'])[0])
# print ('State Bank of India' in new_df['Name'])
# my_str = 'apple'
# str_list = ['ape' , 'fjsdf', 'aerewtg', 'dgyow', 'paepd']
# print(difflib.get_close_matches(my_str,str_list,1)[0])


query_urls=[]

# The below list is for stocks belonging to only one country

# for ticker in new_df['Ticker']:
#     query_urls.append("https://query1.finance.yahoo.com/v8/finance/chart/"+ticker+"?symbol="+ticker+"&period1=0&period2=9999999999&interval=1d&includePrePost=true&events=div%2Csplit")

# The below list is for stocks belonging to all countries

for ticker in df['Ticker']:
    query_urls.append("https://query1.finance.yahoo.com/v8/finance/chart/"+ticker+"?symbol="+ticker+"&period1=0&period2=9999999999&interval=1d&includePrePost=true&events=div%2Csplit")
with Pool(processes=1000) as pool:
    pool.starmap(get_historic_price, zip(query_urls, itertools.repeat(json_path), itertools.repeat(csv_path)))
print("<|>  Historical data of all stocks saved")