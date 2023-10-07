import time
import decimal
import os
import shutil
import random
import operator

import Settings
import Keys
import Modules.arbitrage
import Modules.gatherbalance
from Data.Common import Coin

from Data.Bittrex import Bittrex
from Data.Livecoin import Livecoin

counter = 0
withdrw = 0

def main(coins, Bittrex, Live):
    global counter
    global withdrw
    
    Bittrex.updateBalance()
    Live.updateBalance()
    bitAll = Bittrex.tickerAll()
    liveAll = Live.tickerAll()
    bitTr = Bittrex.info()
    liveTr = Live.info()

    if bitAll is not None and liveAll is not None:
        bitAll = bitAll['result']
        for x in coins:
            try:
                #test
                x[1] = False
                btick = Bittrex.tickerParse(x[0].coin, x[0].basecoin, bitAll)
                ltick = Live.tickerParse(x[0].coin, x[0].basecoin, liveAll)
                x[0].askBlock = random.uniform(x[0].base*0.75, x[0].base*1.25)
                x[0].AEXCoin.BestBid = float(btick['Bid'])
                x[0].AEXCoin.BestBidFee = x[0].AEXCoin.BestBid * (1 + Bittrex.fee)
                x[0].AEXCoin.BestAsk = float(btick['Ask'])
                x[0].AEXCoin.BestAskFee = x[0].AEXCoin.BestAsk * (1 + Bittrex.fee)
                x[0].BEXCoin.BestBid = float(ltick['best_bid'])
                x[0].BEXCoin.BestBidFee = x[0].BEXCoin.BestBid * (1 + Live.fee)
                x[0].BEXCoin.BestAsk = float(ltick['best_ask'])
                x[0].BEXCoin.BestAskFee = x[0].BEXCoin.BestAsk* (1 + Live.fee)
                x[0].updateSpreads(False)
                x[0].balanceCheck()
                bv = float("%.8f" % (Live.tickerParse(x[0].coin, x[0].basecoin, liveAll)['volume']*x[0].BEXCoin.BestAsk))
                if x[0].ABSpread < Settings.liveBitpercent or x[0].BASpread < Settings.liveBitpercent or x[0].AEXBidOrder == True or x[0].AEXAskOrder == True or x[0].BEXBidOrder == True or x[0].BEXAskOrder == True:
                    x[1] = True
                if bv <= 0.25:
                    x[1] = False
                if bitTr is not None and liveTr is not None and x[0].init == False:
                	livestat = Live.walletStatus(liveTr, x[0].coin)
                	if livestat == 'normal':
                		x[0].BEXWallet = True
                		x[0].BEXAskMod = 0
                	if livestat != 'normal':
                		x[0].BEXWallet = False
                	bitstat = Bittrex.walletStatus(bitTr, x[0].coin)
                	if bitstat == 'True':
                		x[0].AEXWallet = True
                		x[0].BEXBidMod = 0
                	if bitstat != 'True':
                		x[0].AEXWallet = False
                
                if x[0].init == True:
                    lstatus = Live.walletStatus(liveTr, x[0].coin)
                    bstatus = Bittrex.walletStatus(bitTr, x[0].coin)
                    if lstatus == 'normal':
                        x[0].BEXWallet = True
                    if bstatus == 'True':
                        x[0].AEXWallet = True
                    x[0].AEXTX = Bittrex.txfee(bitTr, x[0].coin)
                    x[0].BEXTX = Live.txfee(liveTr, x[0].coin)
                    x[0].AEXTXBTC = float("%.8f" % (x[0].AEXTX * x[0].AEXCoin.BestBid))
                    x[0].BEXTXBTC = float("%.8f" % (x[0].BEXTX * x[0].AEXCoin.BestBid))
                    x[0].coinfloat = x[0].AEXBalTotal + x[0].BEXBalTotal
                    if (x[0].coinfloat == 0 or x[0].coinfloat * x[0].BEXCoin.BestBid < 0.008) and bv > 0.25 and (x[0].BEXTXBTC and x[0].AEXTXBTC < 0.00015) and Settings.autogather == True:
                        x[0].BEXActiveGather = True
                        x[0].BEXGatherSize = float("%.6f" %((x[0].AEXTX + x[0].BEXTX) * 35))
                        if x[0].BEXGatherSize * x[0].BEXCoin.BestBid < (x[0].AEXTX + x[0].BEXTX) * 300:
                            x[0].BEXGatherSize = round((x[0].AEXTX + x[0].BEXTX) * 100, 6)
                    if x[0].basecoin == 'BTC':
                        if float(btick['Bid']) != 0:
                            x[0].base = Settings.liveBitBTCequiv / float(btick['Bid'])
                            x[0].bidBlock = float("%.8f" %(random.uniform(x[0].base*0.75, x[0].base*1.25)))
                            x[0].askBlock = float("%.8f" %(random.uniform(x[0].base*0.75, x[0].base*1.25)))
                    elif x[0].basecoin == 'ETH':
                        ethver = Bittrex.tickerParse("BTC-ETH")
                        if float(ethver['Bid']) != 0:
                            etheq = float('%.4f' % (Settings.liveBitBTCequiv / float(ethver['Bid'])))
                            x[0].base = etheq / float(btick['Bid'])
                            x[0].bidBlock = float("%.8f" %(random.uniform(x[0].base*0.75, x[0].base*1.25)))
                            x[0].askBlock = float("%.8f" %(random.uniform(x[0].base*0.75, x[0].base*1.25)))
                    x[0].init = False
            except (KeyError, TypeError):
                pass

    for x in coins:
        if x[1] == True:
            percentage = Settings.liveBitpercent
            takepercentage = Settings.liveBittake
            print(x[0].coin)
            x[0].updateBalance()
            x[0].updateBook()
            spreads = x[0].updateSpreads(False)

            print(time.ctime())
            print("")
            print("%s/BTC Rates:" % (x[0].coin))
            print("")
            x[0].AVerbose()
            x[0].BVerbose()
            print("")
            x[0].updateSpreads(True)
            print("")
            print("")
            if liveAll is not None:
                print ("Livecoin market volume: %s" % (Live.tickerParse(x[0].coin, x[0].basecoin, liveAll)['volume']*x[0].BEXCoin.BestAsk))
                print ("Min coin balance for Bittrex is %f. For Livecoin %f" % (x[0].AEXTX*33.33 + x[0].AEXTX, x[0].BEXTX*33.33+ x[0].BEXTX))
            print ("Bittrex TX fee: %s. Live TX fee: %s" % ('{0:.8f}'.format(x[0].AEXTXBTC), '{0:.8f}'.format(x[0].BEXTXBTC)))
            print("Gather mode:")
            print(x[0].BEXActiveGather)
            if x[0].AEXWallet == False:
                print("%s wallet down" % x[0].AEX.name)
            if x[0].BEXWallet == False:
                print("%s wallet down" % x[0].BEX.name)
            if x[0].BEXActiveGather == True:
                Modules.gatherbalance.gather(x[0], Live, Bittrex, percentage)
            if x[0].BEXActiveGather == False:
                Modules.arbitrage.trade(x[0], Bittrex, Live, percentage, takepercentage, Settings.livecoinbittrex_withdrawals, counter)
                    
            print("")
                
            counter = counter + 4
            if counter >= 30:
                counter = 0
            time.sleep(8)
    Bittrex.updateBalance()
    Live.updateBalance()
    
    if Live.BTC < 0.15 and withdrw == 0:
        unc = unconfirmed()
        if unc is None:
            pass
        if unc is not None:
            if unc > 500000:
                pass
            elif unc < 50000:
                print "Withdrawing 0.35 BTC from Bittrex to Livecoin"
                addr = Live.deposit("BTC")
                if addr is not None:
                    try:
                        address = str(addr['wallet'])
                        withdrawl = Bittrex.withdraw("BTC", 0.35, address)
                        if withdrawl is not None:
                            try:
                                wid = str(withdrawl['uuid'])
                                print "Withdrawal from Bittrex to Livecoin successful"
                                withdrw = time.time()
                            except KeyError:
                                print "Cannot get deposit address from Livecoin."
                    except KeyError:
                        print "Cannot get deposit address from Livecoin."
    if Bittrex.BTC < 0.15 and withdrw == 0:
        unc = unconfirmed()
        if unc is None:
            pass
        if unc is not None:
            if unc > 200000:
                pass
            elif unc < 200000:
                print "Withdrawing 0.35 BTC from Livecoin to Bittrex"
                addr = Bittrex.deposit("BTC")
                if addr is not None:
                    try:
                        address = str(addr['Address'])
                        withdrawl = Live.withdraw("BTC", 0.35, address)
                        if withdrawl is None:
                            print "Withdrawal request was sent to Livecoin but doesn't appear to be accepted. Will attempt on next cycle."
                            withdrw = time.time()
                        if withdrawl is not None:
                            try:
                                if str(withdrawl['state']) == 'APPROVED':
                                    print "Withdrawal approved from Livecoin to Bittrex."
                                    withdrw = time.time()
                            except KeyError:
                                print "Withdrawal request was sent to Livecoin but doesn't appear to be approved. Will attempt on next cycle."
                                withdrw = time.time()
                    except KeyError:
                        print "Cannot get deposit address for BTC on Bittrex. Will attempt on next cycle. Reason:"
                        print addr
                        
    
Bittrex = Bittrex(Keys.bittrexKey, Keys.bittrexSecret)
Live = Livecoin(Keys.liveKey, Keys.liveSecret)
csort = sorted(Settings.livebitBTC)
coins = []
for x in csort:
    if Settings.livebitBTC[x]['isActive'] == True:
        setattr(Bittrex, Settings.livebitBTC[x]['coin']+Settings.livebitBTC[x]['base'], Coin(Bittrex.fee))
        setattr(Live, Settings.livebitBTC[x]['coin']+Settings.livebitBTC[x]['base'], Coin(Live.fee))
        x = [Exchanges.livebit.T(Settings.livebitBTC[x]['coin'], 'BTC', Bittrex, Live), Settings.livebitBTC[x]['isActive']]
        coins.append(x)

if __name__ == '__main__':
    while True:
        main(coins, Bittrex, Live)
        
