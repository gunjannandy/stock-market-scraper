# ref : https://stackoverflow.com/a/47505102/8141330


import json, time, os
import urllib.request
import json_flatten
import multiprocessing as mp
try:
  import httplib
except:
  import http.client as httplib



def check_internet():
  conn = httplib.HTTPConnection("www.google.com", timeout=5)
  try:
    conn.request("HEAD", "/")
    conn.close()
  except:
    conn.close()
    return False
  return True


def get_data(ticker):

  modules = "%2C".join([
    'assetProfile',
    'summaryProfile',
    'summaryDetail',
    'esgScores',
    'price',
    'incomeStatementHistory',
    'incomeStatementHistoryQuarterly',
    'balanceSheetHistory',
    'balanceSheetHistoryQuarterly',
    'cashflowStatementHistory',
    'cashflowStatementHistoryQuarterly',
    'defaultKeyStatistics',
    'financialData',
    'calendarEvents',
    'secFilings',
    'recommendationTrend',
    'upgradeDowngradeHistory',
    'institutionOwnership',
    'fundOwnership',
    'majorDirectHolders',
    'majorHoldersBreakdown',
    'insiderTransactions',
    'insiderHolders',
    'netSharePurchaseActivity',
    'earnings',
    'earningsHistory',
    'earningsTrend',
    'industryTrend',
    'indexTrend',
    'sectorTrend'])

  query_url = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{}?modules={}".format(ticker, modules)

  while not check_internet():
    print("Could not connect, trying again in 5 seconds...")
    time.sleep(5)

  try:
    with urllib.request.urlopen(query_url) as url:
      parsed = json.loads(url.read().decode())

      downlaod_file_name = os.path.join("stock_fundamental_data", ticker, ticker+".json")
      downlaod_flattened_file_name = os.path.join("stock_fundamental_data", ticker, ticker+"_flattened.json")

      os.makedirs(os.path.dirname(downlaod_file_name), exist_ok=True)

      parsed = json_flatten.flatten(list(parsed["quoteSummary"]["result"])[0])

      for key, value in parsed.copy().items():
        if ".raw" in key or ".longFmt" in key or value == "{}" or value.lower() == "none" or value == "":
          del parsed[key]
        elif ".fmt" in key:
          parsed[key.replace(".fmt","")] = parsed.pop(key)

      with open(downlaod_flattened_file_name, "w") as f:
        json.dump(parsed, f, indent=2, sort_keys=True)

      parsed = json_flatten.unflatten(parsed)

      with open(downlaod_file_name, "w") as f:
        json.dump(parsed, f, indent=2, sort_keys=True)

      print("Downloaded {}".format(ticker))
  except:
    print("Data of {} doesn't exist".format(ticker))

  return


def main():

  ticker_file_path = os.path.join("Assets", "india.csv")
  tickers = []
  with open(ticker_file_path, "r") as f:
    tickers = [line.split(',')[0] for line in f]

  with mp.Pool(processes=mp.cpu_count()*50) as pool:
    pool.map(get_data, tickers)

  return



if __name__ == '__main__':
  main()
