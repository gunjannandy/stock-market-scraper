#!/usr/bin/env python
# coding: utf-8

# ![](https://lh3.googleusercontent.com/qbqjDFiK6wInTH4KrDaNIxbvng1XMs2F7Cv_DbzZcm-ljDA0Ikyp9y4HxOLIhp2r_ks=s180-rw?v=0.1?raw=true)
# ![](https://img-d02.moneycontrol.co.in/images/common/header/logo.png?v=0.1?raw=true)

# # Moneycontrol scraping
# ### First we need to scrape all the companies under Indian Market

# In[1]:


from IPython.display import display, HTML
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
import pandas as pd
import requests,json,itertools


# #### The function which scraps links like:
# 
# https://www.moneycontrol.com/india/stockpricequote/A  
# https://www.moneycontrol.com/india/stockpricequote/B  
# .
# .
# .  
# https://www.moneycontrol.com/india/stockpricequote/Z  
# https://www.moneycontrol.com/india/stockpricequote/others

# #### You can refer to this [Stack Overflow answer](https://stackoverflow.com/a/55046746/8141330) to get an idea how to get sc_id from any stock, which we will require to get historical prices later
# 

# In[90]:


company_list=[]

# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# def get_sc(company_name):
#     from selenium import webdriver

#     driver = webdriver.Chrome(ChromeDriverManager().install())
#     driver.get("https://www.moneycontrol.com/stocks/histstock.php?")

#     search_input_box = driver.find_element_by_id("mycomp")
#     search_input_box.send_keys(company_name)
#     print(driver.find_element_by_text(search_input_box))

'''
def get_sc_id(company_name):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
    # Enter search text
    query_input = company_name
    #Get suggested sc_id
    suggest_query_url = 'https://www.moneycontrol.com/mccode/common/autosuggestion_solr.php'
    query = {
    'classic': 'true',
    'query': query_input,
    'type': '1',
    'format': 'json',
    'callback': 'suggest1'}
    # Pull out the sc_id
    suggested_response = requests.get(suggest_query_url , headers=headers, params=query).text
    print("\n\n\n\n",company_name,suggested_response.split('\"sc_id\":\"')[1],"\n\n\n\n")
#     suggested_response = suggested_response.split('(',1)[1]
#     suggested_response = suggested_response.rsplit(')',1)[0]
#     sc_id = json.loads(suggested_response)[0]['sc_id']
#     return(sc_id)
'''

def get_company_list(url,example_list):
    per_row=[]
    while(1):
        try:
            page_response = requests.get(url, timeout=5)
            soup = BeautifulSoup(page_response.content,"lxml")
        except:
            raise
            continue
        else:
            companies = soup.findAll("a", attrs={"class":"bl_12"})
            for company in companies:
                if "moneycontrol" in company["href"]:
        #             sc_id = get_sc_id(company.text)
        #             print([company.text,company["href"],sc_id])
                    print(company.text)
                    per_row.append(company.text)
                    per_row.append(company['href'])
        #             company_list.append([company.text,company["href"]])
                    for i in example_list:
                        # print("https://www.moneycontrol.com"+i.replace("igarashimotors",company['href'].split("/")[6]).replace("IM01",company['href'].split("/")[7]).replace("electric-equipment",company['href'].split("/")[5]))
                        per_row.append("https://www.moneycontrol.com"+i.replace("igarashimotors",company['href'].split("/")[6]).replace("IM01",company['href'].split("/")[7]).replace("electric-equipment",company['href'].split("/")[5]))
                        # print(company['href'].split("/")[6])
                        # print(company['href'].split("/")[7])
                company_list.append(per_row)
                # print(len(company_list))
                # print(per_row)
            break
# example_list=[]
# any_page=requests.get("https://www.moneycontrol.com/india/stockpricequote/electric-equipment/igarashimotors/IM01", timeout=5)
# soup=BeautifulSoup(any_page.content,"lxml")
# for li in soup.findAll("table",attrs={"class":"comInfo"}):
#     for a in (li.findAll("a")):
#         # column_list.append(a.text)
#         example_list.append(a["href"])
# get_company_list("https://www.moneycontrol.com/india/stockpricequote/A",example_list)


# #### This generates all links and sends to the function through multithreading

# In[ ]:


urls=[]
incomplete_url="https://www.moneycontrol.com/india/stockpricequote/"
column_list=['Company Names', 'Company Links']
example_list=[]
any_page=requests.get("https://www.moneycontrol.com/india/stockpricequote/electric-equipment/igarashimotors/IM01", timeout=5)
soup=BeautifulSoup(any_page.content,"lxml")
for li in soup.findAll("table",attrs={"class":"comInfo"}):
    for a in (li.findAll("a")):
        column_list.append(a.text)
        example_list.append(a["href"])
for i in range (ord("A"),ord("Z")+1):
    urls.append(incomplete_url+chr(i))
urls.append((incomplete_url+"others"))
with Pool(processes=27) as pool:
    (pool.starmap(get_company_list, zip(urls,itertools.repeat(example_list))))
# for url in urls:
#     get_company_list(url,example_list)
print(company_list)
# df =  pd.DataFrame(company_list)

# df.columns = ['Company Names', 'Company Links']
# df.columns = column_list
# df.to_csv('company_list.csv', sep=',', header=None, index=None)


# #### This is the table (only part of it)

# In[8]:

'''
print ("Dataframe 1:")
df[:10]


# #### Now get a perticular company and get the link to that Stock Website

# In[10]:


company_name_given_by_user = "igarashi motors"
company_link=df[df["Company Names"].str.contains(company_name_given_by_user, case=False)]["Company Links"].iloc[0]
# sc_id=df[df["Company Names"].str.contains(company_name_given_by_user, case=False)]["sc_id"].iloc[0]
print("The link: "+company_link)
# print("sc_id: "+sc_id)


# ### Now get live BSE, NSE data from the user given website

# In[11]:


page_response = requests.get(company_link, timeout=5)
soup = BeautifulSoup(page_response.content,"lxml")


# #### Get BSE data

# In[12]:


bse_live = soup.findAll("span", attrs={"id":"Bse_Prc_tick"})[0].text
bse_change = soup.findAll("div", attrs={"id":"b_changetext"})[0].text
bse_change_volume = bse_change.split("(")[0]
bse_change_percentage = bse_change.split("(")[1].split(")")[0]
print("Live BSE: "+bse_live+" | BSE change: "+bse_change_volume+" | BSE change percentage: "+bse_change_percentage)


# #### Get NSE data

# nse_live = soup.findAll("span", attrs={"id":"Nse_Prc_tick"})[0].text
# nse_change = soup.findAll("div", attrs={"id":"n_changetext"})[0].text
# nse_change_volume = nse_change.split("(")[0]
# nse_change_percentage = nse_change.split("(")[1].split(")")[0]
# print("Live NSE: "+nse_live+" | NSE change: "+nse_change_volume+" | NSE change percentage: "+nse_change_percentage)

# In[87]:


lista=[]
for li in soup.findAll("table",attrs={"class":"comInfo"}):
    for a in (li.findAll("a")):
        lista.append([a.text,"https://www.moneycontrol.com"+a["href"]])
print(len(lista))

'''