import hmac, hashlib
import urllib
import datetime
import time
import requests
import base64
try:
    from Data.Common import *
except ImportError:
    from Common import *


TIMEOUT = 10

class Bittrex:
    
    def __init__(self, apiKey, apiSecret):
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.version = "v1.1"
        self.BASE_URL = "https://bittrex.com/api/" + str(self.version)
        self.fee = 0.0025
        self.mincurrencies = []
        self.name = "Bittrex"

        self.status_code = 0
        self.latency = 0
        self.last_nonce = 0
        self.error_window = 0
        
    def getmarkets(self):
        try:
            req = requests.get("https://bittrex.com/api/v1.1/public/getmarkets", timeout=TIMEOUT)
            self.mincurrencies = req.json()['result']
        except (requests.Timeout, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            pass
        
        
    def gen_sig(self, method, add = None):
        nonce = (int(time.time()))
        if nonce == self.last_nonce:
            nonce = nonce + 1
        nonce = str(nonce)
        request_url = (self.BASE_URL + "/") + method + ""
        request_url += '?apikey=' + self.apiKey + "&nonce=" + nonce + '&'
        if add is not None:
            request_url += str(add)
        headers={"apisign": hmac.new(self.apiSecret.encode(), request_url.encode(), hashlib.sha512).hexdigest()}
        self.last_nonce = nonce
        return headers, nonce, request_url
        
    def request(self, method, add=None):
        h, n, url = self.gen_sig(method, add)
        try:
            req = requests.get(url, headers=h, timeout=TIMEOUT)
            self.status_code = req.status_code
            self.latency = datetime.timedelta.total_seconds(req.elapsed)
            if self.latency > 1:
                print ("High latency on Bittrex. Last request took %f seconds to process" % (float(self.latency)))
            if req is not None:
                try:
                    json_resp = req.json()
                    return json_resp
                except ValueError:
                    pass
        except (requests.Timeout, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            if e == requests.Timeout:
                print("Request has timed out")
                return None
        
    def latest(self, coin, base, i='thirtyMin'):
        symbol = "%s-%s" % (base, coin)
        try:
            req = requests.get("https://bittrex.com/Api/v2.0/pub/market/GetLatestTick?marketName=" + str(symbol) + "&tickInterval="+str(i)+"&_="+str(time.time()))
            self.status_code = req.status_code
            self.latency = datetime.timedelta.total_seconds(req.elapsed)
            if self.latency > 1:
                print ("High latency on Bittrex. Last request took %f seconds to process" % (float(self.latency)))
            if req is not None:
                try:
                    json_resp = req.json()
                    return json_resp
                except ValueError:
                    pass
        except (requests.Timeout, requests.exceptions.SSLError, requests.exceptions.ConnectionError):
            return None
    def historical(self, symbol, i="thirtyMin"):
        try:
            req = requests.get("https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=" + str(symbol) + "&tickInterval="+str(i)+"&_=1499127220008")
            self.status_code = req.status_code
            self.latency = datetime.timedelta.total_seconds(req.elapsed)
            if self.latency > 1:
                print ("High latency on Bittrex. Last request took %f seconds to process" % (float(self.latency)))
            if req is not None:
                try:
                    json_resp = req.json()
                    return json_resp
                except ValueError:
                    pass
        except (requests.Timeout, requests.exceptions.SSLError, requests.exceptions.ConnectionError):
            return None
            
    def coinInfo(self):
        try:
            req = requests.get("https://bittrex.com/api/v1.1/public/getcurrencies", timeout=TIMEOUT)
            self.status_code = req.status_code
            self.latency = datetime.timedelta.total_seconds(req.elapsed)
            if self.latency > 1:
                print ("High latency on Bittrex. Last request took %f seconds to process" % (float(self.latency)))
            if req is not None:
                try:
                    json_resp = req.json()
                    return json_resp
                except ValueError:
                    pass
        except (requests.Timeout, requests.exceptions.SSLError, requests.exceptions.ConnectionError):
            return None
        
    def ticker(self, symbol):
        try:

            req = requests.get(self.BASE_URL+"/public/getticker", params={"market": symbol})
            self.status_code = req.status_code
            self.latency = datetime.timedelta.total_seconds(req.elapsed)
            if self.latency > 1:
                print ("High latency on Bittrex. Last request took %f seconds to process" % (float(self.latency)))
            if req is not None:
                try:
                    json_resp = req.json()
                    return json_resp
                except ValueError:
                    pass
        except (requests.Timeout, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            pass
        
    def orderbook(self, coin, base):
        try:
            req = requests.get(self.BASE_URL+"/public/getorderbook?market=" + str(base)+"-"+str(coin)+"&type=both&depth=50")
            self.status_code = req.status_code
            self.latency = datetime.timedelta.total_seconds(req.elapsed)
            if self.latency > 1:
                print ("High latency on Bittrex. Last request took %f seconds to process" % (float(self.latency)))
            try:
                json_resp = req.json()
                return json_resp
            except ValueError:
                pass

        except (requests.Timeout, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            return None
            
    def tickerParse(self, coin, base, d):
        for x in d:
            if str(x['MarketName']) == "%s-%s" % (base, coin):
                return x
    
    def tickerAll(self):
        try:
            req = requests.get("https://bittrex.com/api/v1.1/public/getmarketsummaries", timeout=TIMEOUT)
            self.status_code = req.status_code
            self.latency = datetime.timedelta.total_seconds(req.elapsed)
            if self.latency > 1:
                print ("High latency on Bittrex. Last request took %f seconds to process" % (float(self.latency)))
            try:
                json_resp = req.json()
                return json_resp
            except ValueError:
                pass

        except (requests.Timeout, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            return None
        
    def get_balance(self, curr):
        req = self.request("account/getbalances")
        if req is not None:
            if str(req['message']) == "":
                return req['result']
        
    def place_order(self, amount, price, side, coin, base):
        market = "%s-%s" % (base, coin)
        if side == "buy":
            url = "market/buylimit"
        if side == "sell":
            url = "market/selllimit"
        req = self.request(url, "&market=" + str(market)+"&quantity=" + str(amount) + "&rate=" + str(price))
        if req is not None:
            return req
        
    def active_orders(self, coin, base):
        market = "%s-%s" % (base, coin)
        req = self.request("market/getopenorders", "market="+ str(market))
        if req is not None:
            if str(req['message']) == "":
                return req['result']
                
    def active_parse(self, coin, base):
        req = self.active_orders(coin, base)
        if req is not None:
            try:
                if req == []:
                    return []
                elif req != []:
                    resp = []
                    for x in req:
                        oside = ""
                        if str(x['OrderType']) == 'LIMIT_SELL':
                            oside = 'Sell'
                        elif str(x['OrderType']) == 'LIMIT_BUY':
                            oside = 'Buy'
                        resp.append({'Amount': float(x['Quantity']),
                        'Remaining': float(x['QuantityRemaining']),
                        'Price': float(x['Price']),
                        'OrderID': str(x['OrderUuid']),
                        'Pair': str(x['Exchange']),
                        'Side': oside
                        })
                    return resp
            except KeyError:
                return None
            
    def cancel_order(self, id):
        req = self.request("market/cancel", "uuid=" + str(id))
        if req is not None:
            if str(req['message']) == "":
                return req['success']
        
    def deposit(self, curr):
        req = self.request("account/getdepositaddress", "currency=" + str(curr))
        if req is not None:
            if str(req['message']) == "":
                return req['result']
            
    def withdraw(self, curr, amount, address):
        req = self.request("account/withdraw", "currency=" + str(curr) +"&quantity=" + str(amount) +"&address=" + str(address))
        if req is not None:
            if str(req['message']) == "":
                return req['result']
    
    def withdrawalhistory(self, curr):
        req = self.request("account/getwithdrawalhistory", "?currency=" + curr)
        if req is not None:
            return req
                
    def order(self, id):
        req = self.request("account/getorder", "&uuid="+str(id))
        if req is not None:
            return req
            
    def markethistory(self, coin, base):
        coin = "%s-%s" % (base, coin)
        try:
            req = requests.get(self.BASE_URL+"/public/getmarkethistory?market=" + str(coin), timeout=TIMEOUT)
            self.status_code = req.status_code
            self.latency = datetime.timedelta.total_seconds(req.elapsed)
            if self.latency > 1:
                print ("High latency on Bittrex. Last request took %f seconds to process" % (float(self.latency)))
            try:
                json_resp = req.json()
                return json_resp
            except ValueError:
                pass

        except (requests.Timeout, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            return None
                
    #def spread(self, Pair):
    
    def info(self):
        req = self.request("public/getcurrencies")
        if req is not None:
            return req
            
    def txfee(self, info, coin):
        for x in info['result']:
            if str(x['Currency']) == coin:
                return float(x['TxFee'])
                
    def walletStatus(self, info, coin):
        for x in info['result']:
            if str(x['Currency']) == coin:
                return str(x['IsActive'])
        
            
    def updateBook(self, coin, base):
        
        OrderBook = self.orderbook(coin, base)
        Pair = getattr(self, coin+base)

        if OrderBook is None:
            self.error_window = self.error_window + 10
            
        if Pair.Book == {}:
            if OrderBook is not None:
                
                if type(OrderBook) is dict:
                    self.error_window = 0
                    Pair.Book = OrderBook
                    try:
                        for x in OrderBook['result']['buy']:
                            a = [x['Rate'], x['Quantity'], float("%.8f" % (x['Rate'] * x['Quantity'])), 0]
                            Pair.Bids.append(a)
                        for x in OrderBook['result']['sell']:
                            a = [float(x['Rate']), float(x['Quantity']), float("%.8f" % (float(x['Rate']) * float(x['Quantity']))), 0]
                            Pair.Asks.append(a)
                        self.error_window = 0
                        Pair.BestBid = Pair.Bids[0][0]
                        Pair.BestAsk = Pair.Asks[0][0]
                        Pair.BestBidFee = Pair.BestBid * (1 + self.fee)
                        Pair.BestAskFee = Pair.BestAsk * (1 - self.fee)
                    except (IndexError, TypeError):
                        self.error_window = self.error_window + 10
        
        else:
            if OrderBook is not None:
                if type(OrderBook) is dict:
                    try:
                        self.error_window = 0
                        Pair.Book = OrderBook
                        Pair.Bids = []
                        Pair.Asks = []
                        
                        for x in OrderBook['result']['buy']:
                            a = [float(x['Rate']), float(x['Quantity']), float("%.8f" % (float(x['Rate']) * float(x['Quantity']))), 0]
                            Pair.Bids.append(a)
                        for x in OrderBook['result']['sell']:
                            a = [float(x['Rate']), float(x['Quantity']), float("%.8f" % (float(x['Rate']) * float(x['Quantity']))), 0]
                            Pair.Asks.append(a)
                        
                        Pair.BestBid = float(Pair.Bids[0][0])
                        Pair.BestAsk = float(Pair.Asks[0][0])
                        Pair.BestBidFee = float("%.8f" % (Pair.BestBid * (1 + self.fee)))
                        Pair.BestAskFee = float("%.8f" % (Pair.BestAsk * (1 - self.fee)))
                    except (IndexError, TypeError):
                        self.error_window = self.error_window + 10
                
    def updateBalance(self):
        
        B = self.get_balance("BTC")
        
        if B is not None:
            for x in B:
                setattr(self, str(x['Currency']), float(x['Available']))
                setattr(self, str(x['Currency'])+"Total", float(x['Balance']))
