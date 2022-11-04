import requests
from requests import Session
import pandas as pd
import re
# we use Session() to allow a snigle HTTP request to persist between API Calls - so we dont have to makea a new connection w/ each call
from pprint import pprint as pp

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
API_KEY = 'ab74ff4f-96b5-40e9-8262-eb29be16a01d'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': API_KEY,
  }

r = requests.get(url, headers = headers)

class CMC:
    def __init__(self,token):
       self.apiurl = 'https://pro-api.coinmarketcap.com'
       self.headers = { 'Accepts': 'application/json','X-CMC_PRO_API_KEY': token, }
       self.session= Session()
       self.session.headers.update(self.headers)
    
    def get_all_coins(self):
        url = self.apiurl + '/v1/cryptocurrency/map'
        r = self.session.get(url)
        data = r.json()['data']
        return data
    
    def get_all_coins_symbol(self):
        url = self.apiurl + '/v1/cryptocurrency/map'
        r = self.session.get(url)
        data = r.json()['data']['symbol']
        return data

    def meta(self,sym):
        url = f'{self.apiurl}/v2/cryptocurrency/info'
        parameters = {'symbol': sym}
        sym = sym.split(',')
        r = self.session.get(url,params = parameters )
        L = []
        for i in sym:
            t = r.json()['data'][i][0]['description']
            tdic = re.search(r'trading on (?P<markets>\d+) active market.*?\$(?P<volume>[\d,\.]+) traded', t)
            
            d = {i: {
                'date_added' : r.json()['data'][i][0]['date_added'],
                'Trading_stats' : tdic.groupdict(),
                }}
            L.append(d)
        return L
    
    def current_price(self, sym):
        url = self.apiurl + '/v2/cryptocurrency/quotes/latest'
        # when usiing requests lib the 'params' parameter is needed to specify paramteres given within the API doc. i.e 'symbol' was given in CMC API doc
        parameters = {'symbol': sym}
        sym = sym.split(',')
        r = self.session.get(url,params = parameters )
        try:   
            pl = [r.json()['data'][item][0]['quote']['USD']['price'] for item in sym ]
        except KeyError:
            print(f'symbol {sym} was not found, please retry')
            
        return pl
    
cmc = CMC(API_KEY)

#pp(cmc.get_all_coins())

pp(cmc.meta('BTC,ETH'))

