import hmac, hashlib
import urllib
try:
    import urllib.parse
except ImportError:
    pass
import datetime
import time
import requests
import base64
import json
from collections import OrderedDict
try:
    from Common import *
except ImportError:
    from Data.Common import *
#from urllib3.exceptions import InsecureRequestWarning

PUBLIC_SET = [
    'ticker', 'last_trades', 'order_book', 'all/order_book',
    'maxbid_minask', 'restrictions'
]

GET_SET = ['trades', 'client_orders', 'order', 'balances', 'balance', 'ticker', 'order_book', 'get/address', 'history/transactions', 'commissionCommonInfo']
POST_SET = ['cancellimit', 'sellmarket', 'selllimit', 'buymarket', 'buylimit', 'out/coin']
MARKET_SET = ['getopenorders', 'cancellimit', 'sellmarket', 'selllimit', 'buymarket', 'buylimit', 'order', 'client_orders', 'commissionCommonInfo', 'trades']

ACCOUNT_SET = ['getdepositaddress', 'withdraw', 'getorder', 'getorderhistory', 'getwithdrawalhistory', 'getdeposithistory']

PAYMENT_SET = ['balances', 'getbalances', 'balance', 'get/address', 'history/transactions', 'out/coin']

TIMEOUT = 10

class Livecoin:
    
    def __init__(self, apiKey, apiSecret):
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.BASE_URL = "https://api.livecoin.net/"
        self.fee = 0.002
        self.name = 'Livecoin'
        
        self.latency = 0
        self.status_code = 0
        self.error_window = 0
        self.last_nonce = 0
        self.bookupdated = 0
        
        self.public_set = set(PUBLIC_SET)
        self.market_set = set(MARKET_SET)
        self.account_set = set(ACCOUNT_SET)
        self.payment_set = set(PAYMENT_SET)
        self.get_set = set(GET_SET)
        self.post_set = set(POST_SET)
        
    def gen_sig(self, method, options=None):
        if not options:
            options = {}
            
        nonce = int(time.time() * 1000)
        if nonce == self.last_nonce:
            nonce = nonce + 1
        nonce = str(nonce)
        request_url = ''
        self.last_nonce = nonce

        if method in self.public_set:
            request_url = self.BASE_URL + 'exchange/' + method
            if options:
                try:
                    request_url += '?' + urllib.urlencode(options)
                except AttributeError:
                    request_url += '?' + urllib.parse.urlencode(options)
                
        #msg = urllib.urlencode(options)
        elif method in self.market_set:
            if method in self.get_set:
                try:
                    msg = urllib.urlencode(options)
                except AttributeError:
                    msg = urllib.parse.urlencode(options)
                request_url = self.BASE_URL + 'exchange/' + method + '?apikey=' + self.apiKey + "&nonce=" + nonce + '&' + msg
            else:
                request_url = self.BASE_URL + 'exchange/' + method + '?apikey=' + self.apiKey + "&nonce=" + nonce + '&'
        elif method in self.account_set:
            request_url = self.BASE_URL + 'account/' + method + '?apikey=' + self.apiKey + "&nonce=" + nonce + '&'
        elif method in self.payment_set:
            if method in self.post_set:
                request_url = self.BASE_URL + 'payment/' + method + '?apikey=' + self.apiKey + "&nonce=" + nonce + '&'
            else:
                try:
                    msg = urllib.urlencode(options)
                except AttributeError:
                    msg = urllib.parse.urlencode(options)
                request_url = self.BASE_URL + 'payment/' + method + '?apikey=' + self.apiKey + "&nonce=" + nonce + '&' + msg
        try:
            msg = urllib.urlencode(options)
        except AttributeError:
            msg = urllib.parse.urlencode(options)
        signature = hmac.new(self.apiSecret.encode(), msg.encode(), hashlib.sha256).hexdigest().upper()
        headers = {"Api-key": self.apiKey, "Sign": signature, "Content-type": "application/x-www-form-urlencoded"}
        return request_url, msg, headers
        
    def request(self, method, options=None):
        request_url, msg, headers = self.gen_sig(method, options)
        req = None
        if method in self.payment_set:
            if method in self.post_set:
                try:
                    req = requests.post(request_url, data=msg, headers=headers, timeout=TIMEOUT, verify=False)
                    self.status_code = req.status_code
                    self.latency = datetime.timedelta.total_seconds(req.elapsed)
                except (requests.Timeout, requests.exceptions.SSLError, requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
                    print (e)
            else:
                try:
                    req = requests.get(request_url, headers=headers, timeout=TIMEOUT, verify=False)
                    self.status_code = req.status_code
                    self.latency = datetime.timedelta.total_seconds(req.elapsed)
                except (requests.Timeout, requests.exceptions.SSLError, requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
                    print (e)
        else:
            if method in self.get_set:
                try:
                    req = requests.get(request_url, headers=headers, timeout=TIMEOUT, verify=False)
                    self.status_code = req.status_code
                    self.latency = datetime.timedelta.total_seconds(req.elapsed)
                except (requests.Timeout, requests.exceptions.SSLError, requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
                    print (e)
            else:
                try:
                    req = requests.post(request_url, data=msg, headers=headers, timeout=TIMEOUT, verify=False)
                    self.status_code = req.status_code
                    self.latency = datetime.timedelta.total_seconds(req.elapsed)
                except (requests.Timeout, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
                    print (e)

            #self.status_code = req.status_code
            #self.latency = datetime.timedelta.total_seconds(req.elapsed)
        if self.latency > 1:
            print ("High latency on Livecoin. Last request took %f seconds to process" % (float(self.latency)))
        if req is not None:
            try:
                json_resp = req.json()
                return json_resp
            except ValueError as err:
                print (err)
                return None
        #except requests.Timeout:
        #    pass
        
    def orderbook(self, coin, base):
        data = OrderedDict(sorted([('currencyPair', coin+"/"+base)]))
        return self.request('order_book', data)
    
    def orderbookAll(self):
        try:
            req = requests.get("https://api.livecoin.net/exchange/all/order_book", timeout=TIMEOUT)
            try:
                resp = req.json()
                return resp
            except ValueError:
                pass
        except req.Timeout as err:
            print (err)
    def tickerParse(self, coin, base, d):
        for x in d:
            if str(x['symbol']) == '%s/%s'%(coin, base):
                return x
                
    def active_parse(self, coin, base):
        req = self.active_orders(coin, base)
        if req is not None:
            try:
                req = req['data']
                pao = []
                for x in req:
                    side = ''
                    if str(x['type']) == 'LIMIT_BUY':
                        side = 'Buy'
                    if str(x['type']) == 'LIMIT_SELL':
                        side = 'Sell'
                    pao.append({'Amount': float(x['quantity']),
                        'Remaining': float(x['remainingQuantity']),
                        'Price': float(x['price']),
                        'OrderID': str(x['id']),
                        'Pair': str(x['currencyPair']),
                        'Side': side
                        })
                return pao
            except KeyError:
                return []
                
    def tickerAll(self):
            try:
                req = requests.get("https://api.livecoin.net/exchange/ticker", timeout=TIMEOUT)
                try:
                    resp = req.json()
                    return resp
                except ValueError:
                    pass
            except (requests.Timeout, requests.exceptions.ConnectionError) as err:
                print (err)
                
    def txfee(self, info, coin):
        for x in info['info']:
            if str(x['symbol']) == coin:
                return float(x['withdrawFee'])
                
    def info(self):
        try:
            req = requests.get("https://api.livecoin.net/info/coinInfo", timeout=TIMEOUT)
            try:
                resp = req.json()
                return resp
            except ValueError:
                pass
        except (requests.Timeout, requests.exceptions.ConnectionError) as err:
            print (err)
            
    def walletStatus(self, info, coin):
        for x in info['info']:
            if str(x['symbol']) == coin:
                return str(x['walletStatus'])
                
    def balance(self, coin):
        data = OrderedDict(sorted([('currency', coin)]))
        return self.request('balance', data)
        
    def balances(self):
        return self.request('balances')
        
    def userfees(self):
        return self.request('commissionCommonInfo')
        
    def order(self, id):
        data = OrderedDict(sorted([('orderId', id)]))
        return self.request("order", data)
        
    def place_order(self, amount, price, side, coin, base):
        market = '%s/%s' % (coin, base)
        data = OrderedDict(sorted([('currencyPair', market),('price', price),('quantity', amount)]))
        if side == "buy":
            return self.request('buylimit', data)
        if side == "sell":
            return self.request('selllimit', data)
            
    def active_orders(self, coin, base):
        pair = '%s/%s' % (coin, base)
        data = OrderedDict(sorted([("currencyPair", pair), ("openClosed", "OPEN")]))
        return self.request('client_orders', data)
        
    def cancel_order(self, coin, base, id):
        pair = '%s/%s' % (coin, base)
        data = OrderedDict(sorted([('currencyPair', pair),('orderId', id)]))
        #data = OrderDict(sorted({'currencyPair': pair ,'orderId': int(id))})
        return self.request('cancellimit', data)
        
    def deposit(self, curr):
        data = OrderedDict(sorted([('currency', curr)]))
        return self.request('get/address', data)
        
    def withdraw(self, curr, amount, address):
        data = OrderedDict(sorted([('amount', amount), ('currency', curr),('wallet', address)]))
        #data = OrderedDict(sorted([('currency', curr,'amount', amount, 'address': address)]))
        return self.request('out/coin', data)
    def transactions(self, start, end, types):
        data = OrderedDict(sorted([('start', start), ('end',end), ('types', types)]))
        return self.request('history/transactions', data)
        
    def trades(self, pair):
        data = OrderedDict(sorted([(('currencyPair'), pair)]))
        return self.request('trades', data)
        

    def updateBook(self, coin, base):
        
        OrderBook = self.orderbook(coin, base)
        self.bookupdated = 0

        Pair = getattr(self, coin+base)
            
        if OrderBook is None:
            self.error_window = self.error_window + 8
            
        Pair.BestBid = 0
        Pair.BestAsk = 0
        Pair.BestBidFee = 0
        Pair.BestAskFee = 0
            
        if Pair.Book == {}:
            if OrderBook is not None:
                if type(OrderBook) is not dict:
                    self.error_window = self.error_window + 8
                if type(OrderBook) is dict:
                    Pair.Book = OrderBook
                    self.error_window = 0
                    for x in OrderBook['bids']:
                        a = [float(x[0]), float(x[1]), float(x[0]) * float(x[1]), 0]
                        Pair.Bids.append(a)
                    for x in OrderBook['asks']:
                        a = [float(x[0]), float(x[1]), float(x[0]) * float(x[0]), 0]
                        Pair.Asks.append(a)
                    
                    Pair.BestBid = float(Pair.Bids[0][0])
                    Pair.BestAsk = float(Pair.Asks[0][0])
                    Pair.BestBidFee = Pair.BestBid * (1 + self.fee)
                    Pair.BestAskFee = Pair.BestAsk * (1 - self.fee)
                    self.bookupdated = 1
        else:
            if OrderBook is not None:
                if type(OrderBook) is not dict:
                    self.error_window = self.error_window + 8
                if type(OrderBook) is dict:
                    
                    Pair.Book = OrderBook
                    Pair.Bids = []
                    Pair.Asks = []
                    try:
                        self.error_window = 0
                        for x in OrderBook['bids']:
                            a = [float(x[0]), float(x[1]), float(x[0]) * float(x[1]), 0]
                            Pair.Bids.append(a)
                        for x in OrderBook['asks']:
                            a = [float(x[0]), float(x[1]), float(x[0]) * float(x[1]), 0]
                            Pair.Asks.append(a)
                        Pair.BestBid = float(Pair.Bids[0][0])
                        Pair.BestAsk = float(Pair.Asks[0][0])
                        Pair.BestBidFee = Pair.BestBid * (1 + self.fee)
                        Pair.BestAskFee = Pair.BestAsk * (1 - self.fee)
                        self.bookupdated = 1
                    except (KeyError, IndexError):
                        self.error_window = self.error_window + 10
                    
                    
    def updateBalance(self):
        
        B = self.balances()
        
        if B is not None:
            if type(B) is list:
                for x in B:
                    if str(x['type']) == 'available':
                        setattr(self, str(x['currency']), float(x['value']))
                            
	
                    if str(x['type']) == "total":
                        setattr(self, str(x['currency'])+"Total", float(x['value']))