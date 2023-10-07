"""
Primary logic handling for arbitrage orders. All code used to be in multiple locations so there may be some redundency. Still plenty ugly.


"""

def trade(T, AEX, BEX, percentage, takepercentage, autowithdraw):
    #Buys on AExchange
    if T.basecoin == "BTC":
        AEXbase = AEX.BTC
        BEXbase = BEX.BTC
        minbase = 0.01
    if T.basecoin == "USD":
        AEXbase = AEX.USD
        BEXbase = BEX.USD
        minbase = 40

    #Market take order system.
    #Market take from A to B Exchange
    if T.BATake < takepercentage and T.AEXWallet and T.BEXWallet:
        T.updateBalance()
        if T.AEXCoin.Bids[0][1] > T.BEXCoin.Asks[0][1]:
            if BEXbase > T.BEXCoin.Asks[0][2]:
                if T.AEXBal > T.BEXCoin.Asks[0][1] and T.BEXCoin.Asks[0][1] * T.BEXCoin.Asks[0][0] > 0.0005:
                    T.BEXTake(T.BEXCoin.Asks[0][1], T.BEXCoin.Asks[0][0], T.AEXCoin.Bids[0][0], "buy", "sell")
                elif T.AEXBal < T.BEXCoin.Asks[0][1] and T.AEXBal * T.BEXCoin.Asks[0][0] > 0.0005:
                    T.BEXTake(T.AEXBal, T.BEXCoin.Asks[0][0], T.AEXCoin.Bids[0][0], "buy", "sell")
            elif BEXbase < T.BEXCoin.Asks[0][2]:
                amount = float("%.6f" % (T.BEXCoin.Asks[0][0] * (BEXbase - minbase)))
                if T.AEXBal > amount and amount * T.BEXCoin.Asks[0][0] > 0.0005:
                    T.BEXTake(amount, T.BEXCoin.Asks[0][0], T.AEXCoin.Bids[0][0], "buy", "sell")
                elif T.AEXBal < amount and T.AEXBal * T.BEXCoin.Asks[0][0] > 0.0005:
                    T.BEXTake(T.AEXBal, T.BEXCoin.Asks[0][0], T.AEXCoin.Bids[0][0], "buy", "sell")
        elif T.AEXCoin.Bids[0][1] < T.BEXCoin.Asks[0][1]:
            if BEXbase > T.AEXCoin.Bids[0][2]:
                if T.AEXBal > T.AEXCoin.Bids[0][1] and T.AEXCoin.Bids[0][1] * T.AEXCoin.Bids[0][0] > 0.0005:
                    T.BEXTake(T.AEXCoin.Bids[0][1], T.BEXCoin.Asks[0][0], T.AEXCoin.Bids[0][0], "buy", "sell")
                elif T.AEXBal < T.AEXCoin.Bids[0][1] and T.AEXBal * T.AEXCoin.Bids[0][0] > 0.0005:
                    T.BEXTake(T.AEXBal, T.BEXCoin.Asks[0][0], T.AEXCoin.Bids[0][0], "buy", "sell")
            elif BEXbase < T.AEXCoin.Bids[0][2]:
                amount = float("%.6f" % (T.AEXCoin.Bids[0][0] * (BEXbase - minbase)))
                if T.AEXBal > amount and amount * T.AEXCoin.Bids[0][0] > 0.0005:
                    T.BEXTake(amount, T.BEXCoin.Asks[0][0], T.AEXCoin.Bids[0][0], "buy", "sell")
                elif T.AEXBal < amount and T.AEXBal * T.AEXCoin.Bids[0][0] > 0.0005:
                    T.BEXTake(T.AEXBal, T.BEXCoin.Asks[0][0], T.AEXCoin.Bids[0][0], "buy", "sell")
                        
        #Market take from B to A Exchange
    if T.ABTake < takepercentage and T.AEXWallet and T.BEXWallet:
        T.updateBalance()
        if T.BEXCoin.Bids[0][1] > T.AEXCoin.Asks[0][1]:
            if AEXbase > T.AEXCoin.Asks[0][2]:
                if T.BEXBal > T.AEXCoin.Asks[0][1] and T.AEXCoin.Asks[0][1] * T.AEXCoin.Bids[0][0] > 0.0005:
                    T.BEXTake(T.AEXCoin.Asks[0][1], T.BEXCoin.Asks[0][0], T.AEXCoin.Bids[0][0], "sell", "buy")
                elif T.BEXBal < T.AEXCoin.Asks[0][1] and T.BEXBal * T.AEXCoin.Bids[0][0] > 0.0005:
                    T.BEXTake(T.BEXBal, T.BEXCoin.Asks[0][0], T.AEXCoin.Bids[0][0], "sell", "buy")
            elif AEXbase < T.AEXCoin.Asks[0][2]:
                amount = float("%.6f" % (T.AEXCoin.Asks[0][0] * (AEXbase - minbase)))
                if T.BEXBal > amount and amount * T.AEXCoin.Bids[0][0] > 0.0005:
                    T.BEXTake(amount, T.BEXCoin.Asks[0][0], T.AEXCoin.Bids[0][0], "sell", "buy")
                elif T.BEXBal < amount and T.BEXBal * T.AEXCoin.Bids[0][0] > 0.0005:
                    T.BEXTake(T.BEXBal, T.BEXCoin.Asks[0][0], T.AEXCoin.Bids[0][0], "sell", "buy")
        elif T.BEXCoin.Bids[0][1] < T.AEXCoin.Asks[0][1]:
            if AEXbase > T.BEXCoin.Bids[0][2]:
                if T.BEXBal > T.BEXCoin.Bids[0][1] and T.BEXCoin.Bids[0][1] * T.BEXCoin.Bids[0][0] > 0.0005:
                    T.BEXTake(T.BEXCoin.Bids[0][1], T.BEXCoin.Bids[0][0], T.AEXCoin.Asks[0][0], "sell", "buy")
                elif T.BEXBal < T.BEXCoin.Bids[0][1] and T.BEXBal * T.BEXCoin.Bids[0][0] > 0.0005:
                    T.BEXTake(T.BEXBal, T.BEXCoin.Bids[0][0], T.AEXCoin.Asks[0][0], "sell", "buy")
            elif AEXbase < T.BEXCoin.Bids[0][2]:
                amount = float("%.6f" % (T.BEXCoin.Bids[0][0] * (AEXbase - minbase)))
                if T.BEXBal > amount and amount * T.BEXCoin.Bids[0][0] > 0.0005:
                    T.BEXTake(amount, T.BEXCoin.Bids[0][0], T.AEXCoin.Asks[0][0], "sell", "buy")
                elif T.BEXBal < amount and T.BEXBal * T.BEXCoin.Bids[0][0] > 0.0005:
                    T.BEXTake(T.BEXBal, T.BEXCoin.Bids[0][0], T.AEXCoin.Asks[0][0], "sell", "buy")

    #Regular order posting system
    if T.BEXOrder == True:
        cao = BEX.active_parse(T.BEXPair)
        if T.debugwrite == True:
            T.aog(cao)
        if cao is not None:

            if cao == []: #Order is no longer listed, meaning it has been filled
                if T.BEXBidOrderID == '' and T.BEXBidOrder == True:
                    T.BEXBidOrder = False
                if T.BEXAskOrderID == '' and T.BEXAskOrder == True:
                    T.BEXAskOrder = False
                T.BEXOrder = False
                if T.BEXAskOrder and T.BEXBidOrder == True and T.BEXAskOpen == False and T.BEXBidOpen == False:
                    bidchk = T.BEXHistory(T.BEXBidAmount, T.BEXBidPrice) #Fix
                    if bidchk:
                        T.trend += T.BEXAEXAmount
                        T.BEXBidOpen = True
                        T.BEXBidMin = 0
                        T.BEXBidCalc = 0
                        T.BEXBidRemaining = 0
                        calc = float("%.8f" % (T.BEXBidAmount * T.BEXBidPrice))
                        fees = float("%.8f" % (calc*0.002))
                        totals = calc-fees
                        totals = -totals
                        T.csv(BEX.name, "LIMIT BUY", T.BEXBidAmount, float("%.8f" % T.BEXBidPrice), T.BEXBidOrderID, totals)
                        if T.BidWallet == False:
                            T.BEXBidMod += 0.3
                    askchk = T.BEXHistory(T.BEXAskOrderID)
                    if askchk:
                        T.trend -= T.BEXAskAmount
                        T.BEXAskOpen = True
                        T.BEXAskCalc = 0
                        T.BEXAskMin = 0
                        T.BEXAskRemaining = 0
                        calc = float("%.8f" % (T.BEXAskAmount * T.BEXAskPrice))
                        fees = float("%.8f" % (calc * 0.002))
                        totals = calc-fees
                        T.csv(BEX.name, "LIMIT SELL", T.BEXAskAmount, float("%.8f" % T.BEXAskPrice), T.BEXAskOrderID, totals)
                        if T.BEXWallet == False:
                            T.BEXAskMod += 0.3
                if T.BEXAskOrder == True and T.BEXAskOpen == False and T.BEXAskOpen == False:
                    askchk = T.BEXHistory(T.BEXAskAmount, T.BEXAskPrice)
                    if askchk:
                        T.trend -= T.BEXAskAmount
                        T.BEXAskOpen = True
                        T.BEXAskCalc = 0
                        T.BEXAskMin = 0
                        T.BEXAskRemaining = 0
                        calc = float("%.8f" % (T.BEXAskAmount * T.BEXAskPrice))
                        fees = float("%.8f" % (calc * 0.002))
                        totals = calc-fees
                        T.csv(BEX.name, "LIMIT SELL", T.BEXAskAmount, float("%.8f" % T.BEXAskPrice), T.BEXAskOrderID, totals)
                        if T.BEXWallet == False:
                            T.BEXAskMod += 0.3
                    
                if T.BEXBidOrder == True and T.BEXBidOpen == False and T.BEXBidOpen == False:
                    bidchk = T.BEXHistory(T.BEXBidAmount, T.BEXBidPrice)
                    if bidchk:
                        T.trend += T.BEXAEXAmount
                        T.BEXBidOpen = True
                        T.BEXBidMin = 0
                        T.BEXBidCalc = 0
                        T.BEXBidRemaining = 0
                        calc = float("%.8f" % (T.BEXBidAmount * T.BEXBidPrice))
                        fees = float("%.8f" % (calc*0.002))
                        totals = calc-fees
                        totals = -totals
                        T.csv(BEX.name, "LIMIT BUY", T.BEXBidAmount, float("%.8f" % T.BEXBidPrice), T.BEXBidOrderID, totals)
                        if T.BidWallet == False:
                            T.BEXBidMod += 0.3
            elif cao != []: #Active order still listed on exchange
                marketbids = []
                marketasks = []
                for x in cao:
                    if x['Side'] == "Sell":
                        marketasks.append(x)
                    if x['Side'] == "Buy":
                        marketbids.append(x)
                if T.BEXBidOrder == True and T.BEXBidOrderID ==  '':
                    T.BEXBidOrderID = int(marketbids[0]['OrderId'])
                    T.BEXBidPrice = float(marketbids[0]['Rate'])
                    T.BEXBidAmount = float(marketbids[0]['Amount'])
                if T.BEXAskOrder == True and T.BEXAskOrderID == '':
                    T.BEXAskOrderID = int(marketasks[0]['OrderId'])
                    T.BEXAskPrice = float(marketasks[0]['Rate'])
                    T.BEXAskAmount = float(marketasks[0]['Amount'])
                if T.BEXBidOrder == True and T.BEXAskOrder == True:
                    if marketbids == [] and T.BEXBidOpen == False:
                        T.BEXBidOpen = True
                        T.BEXBidCalc = 0
                        T.BEXBidMin = 0
                        calc = float("%.8f" % (T.BEXBidAmount * T.BEXBidPrice))
                        fees = float("%.8f" % (calc*0.002))
                        totals = calc-fees
                        totals = -totals
                        T.csv(BEX.name, "LIMIT BUY", T.BEXBidAmount, float("%.8f" % T.BEXBidPrice), T.BEXBidOrderID, totals)
                        if T.BidWallet == False:
                            T.BEXBidMod += 0.3
                    if marketbids != []:
                        verify = 0
                        for x in marketbids:
                            if int(x['OrderId']) != T.BEXBidOrderID:
                                BEX.cancel_order(int(x['OrderId']))
                            if int(x['OrderId']) == T.BEXBidOrderID:
                                verify = 1
                                if T.BASpread > percentage:
                                    if float(x['Remaining']) != float(x['Amount']):
                                        T.trend += (float(x['Amount']) - float(x['Remaining']))
                                        T.BEXBidRemaining = T.BEXBidMin + (float(x['Amount'])-float(x['Remaining']))
                                        T.BEXBidMin = float(x['Remaining'])
                                        calc = float("%.8f" % (T.BEXBidPrice * (float(x['Amount'])-float(x['Remaining']))))
                                        fees = float("%.8f" %  (calc*0.002))
                                        totals = calc-fees
                                        totals = -totals
                                        T.csv(BEX.name, "LIMIT BUY", float(x['Amount'])-float(x['Remaining']), T.BEXBidPrice, T.BEXBidOrderID, totals)
                                        T.BEXBidCalc = T.BEXBidCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXBidPrice)
                                        if T.debugwrite == True:
                                            T.debug("%f %f %f" % (T.BEXBidRemaining, T.BEXBidMin, T.BEXBidCalc))
                                        if T.BEXBidCalc > 0.0005:
                                            T.BEXBidCalc = 0
                                            T.BEXBidMin = 0
                                            T.BEXBidOpen = True
                                    T.BEXCancelOrder(T.BEXBidOrderID, "buy")
                                elif T.BASpread < percentage:
                                    if float(x['Rate']) != T.BEXCoin.Bids[0][0]:
                                        buycheck = T.bidcheck(T.BEXBidPrice, T.BEXBidAmount)
                                        if buycheck == False:
                                            if float(x['Remaining']) != float(x['Amount']):
                                                T.trend += (float(x['Amount']) - float(x['Remaining']))
                                                T.BEXBidRemaining = T.BEXBidMin + (float(x['Amount'])-float(x['Remaining']))
                                                T.BEXBidMin = float(x['Remaining'])
                                                calc = float("%.8f" % (T.BEXBidPrice * (float(x['Amount'])-float(x['Remaining']))))
                                                fees = float("%.8f" %  (calc*0.002))
                                                totals = calc-fees
                                                totals = -totals
                                                T.csv(BEX.name, "LIMIT BUY", float(x['Amount'])-float(x['Remaining']), T.BEXBidPrice, T.BEXBidOrderID, totals)
                                                T.BEXBidCalc = T.BEXBidCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXBidPrice)
                                                if T.debugwrite == True:
                                                    T.debug("%f %f %f" % (T.BEXBidRemaining, T.BEXBidMin, T.BEXBidCalc))
                                                if T.BEXBidCalc > 0.0005:
                                                    T.BEXBidCalc = 0
                                                    T.BEXBidMin = 0
                                                    T.BEXBidOpen = True
                                                T.BEXCancelOrder(T.BEXBidOrderID, "buy")
                                        if buycheck is True:
                                            if float(x['Remaining']) != float(x['Amount']):
                                                T.trend += (float(x['Amount']) - float(x['Remaining']))
                                                T.BEXBidRemaining = T.BEXBidMin + (float(x['Amount'])-float(x['Remaining']))
                                                T.BEXBidMin = float(x['Remaining'])
                                                calc = float("%.8f" % (T.BEXBidPrice * (float(x['Amount'])-float(x['Remaining']))))
                                                fees = float("%.8f" %  (calc*0.002))
                                                totals = calc-fees
                                                totals = -totals
                                                T.csv(BEX.name, "LIMIT BUY", float(x['Amount'])-float(x['Remaining']), T.BEXBidPrice, T.BEXBidOrderID, totals)
                                                T.BEXBidCalc = T.BEXBidCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXBidPrice)
                                                if T.debugwrite == True:
                                                    T.debug("%f %f %f" % (T.BEXBidRemaining, T.BEXBidMin, T.BEXBidCalc))
                                                if T.BEXBidCalc > 0.0005:
                                                    T.BEXBidCalc = 0
                                                    T.BEXBidMin = 0
                                                    T.BEXBidOpen = True
                                            T.BEXCancelOrder(T.BEXBidOrderID, "buy")
                                    elif float(x['Rate']) == T.BEXCoin.Bids[0][0]:
                                        if T.BEXCoin.Bids[0][0] - T.BEXCoin.Bids[1][0] > 0.00000005:
                                            if float(x['Remaining']) != float(x['Amount']):
                                                T.trend += (float(x['Amount']) - float(x['Remaining']))
                                                T.BEXBidRemaining = T.BEXBidMin + (float(x['Amount'])-float(x['Remaining']))
                                                T.BEXBidMin = float(x['Remaining'])
                                                calc = float("%.8f" % (T.BEXBidPrice * (float(x['Amount'])-float(x['Remaining']))))
                                                fees = float("%.8f" %  (calc*0.002))
                                                totals = calc-fees
                                                totals = -totals
                                                T.csv(BEX.name, "LIMIT BUY", float(x['Amount'])-float(x['Remaining']), T.BEXBidPrice, T.BEXBidOrderID, totals)
                                                T.BEXBidCalc = T.BEXBidCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXBidPrice)
                                                if T.debugwrite == True:
                                                    T.debug("%f %f %f" % (T.BEXBidRemaining, T.BEXBidMin, T.BEXBidCalc))
                                                if T.BEXBidCalc > 0.0005:
                                                    T.BEXBidCalc = 0
                                                    T.BEXBidMin = 0
                                                    T.BEXBidOpen = True
                                            T.BEXCancelOrder(T.BEXBidOrderID, "buy")
                        if verify == 0 and T.BEXBidOpen == False:
                            T.trend += T.BEXBidAmount
                            T.BEXBidOpen = True
                            T.BEXBidCalc = 0
                            T.BEXBidMin = 0
                            calc = float("%.8f" % (T.BEXBidAmount * T.BEXBidPrice))
                            fees = float("%.8f" % (calc*0.002))
                            totals = calc-fees
                            totals = -totals
                            T.csv(BEX.name, "LIMIT BUY", T.BEXBidAmount, float("%.8f" % T.BEXBidPrice), T.BEXBidOrderID, totals)
                            if T.BidWallet == False:
                                T.BEXBidMod += 0.3
                    if marketasks == [] and T.BEXAskOpen == False:
                        T.trend -= T.BEXAskAmount
                        T.BEXAskOpen = True
                        T.BEXAskCalc = 0
                        T.BEXAskMin = 0
                        calc = float("%.8f" % (T.BEXAskAmount * T.BEXAskPrice))
                        fees = float("%.8f" % (calc*0.002))
                        totals = calc-fees
                        T.csv(BEX.name, "LIMIT SELL", T.BEXAskAmount, float("%.8f" % T.BEXAskPrice), T.BEXAskOrderID, totals)
                        if T.BEXWallet == False:
                            T.BEXAskMod += 0.3
                    if marketasks != []:
                        verify = 0
                        for x in marketasks:
                            if int(x['OrderId']) != T.BEXAskOrderID:
                                BEX.cancel_order(int(x['OrderId']))
                            if int(x['OrderId']) == T.BEXAskOrderID:
                                verify = 1
                                if T.ABSpread > percentage:
                                    if float(x['Remaining']) != float(x['Amount']):
                                        T.trend -= (float(x['Amount']) - float(x['Remaining']))
                                        T.BEXAskRemaining = T.BEXAskMin + (float(x['Amount'])-float(x['Remaining']))
                                        T.BEXAskMin = float(x['Remaining'])
                                        calc = float("%.8f" % (T.BEXAskPrice * (float(x['Amount'])-float(x['Remaining']))))
                                        fees = float("%.8f" %  (calc*0.002))
                                        totals = calc-fees
                                        T.csv(BEX.name, "LIMIT SELL", float(x['Amount'])-float(x['Remaining']), T.BEXAskPrice, T.BEXAskOrderID, totals)
                                        T.BEXAskCalc = T.BEXAskCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXAskPrice)
                                        if T.debugwrite == True:
                                            T.debug("%f %f %f" % (T.BEXAskRemaining, T.BEXAskMin, T.BEXAskCalc))
                                        if T.BEXAskCalc > 0.0005:
                                            T.BEXAskMin = 0
                                            T.BEXAskCalc = 0
                                            T.BEXAskOpen = True
                                    T.BEXCancelOrder(T.BEXAskOrderID, "sell")
                                elif T.ABSpread < percentage:
                                    if float(x['Rate']) != T.BEXCoin.Asks[0][0]:
                                        askcheck = T.askcheck(T.BEXAskPrice, T.BEXAskAmount)
                                        if askcheck == False:
                                            if float(x['Remaining']) != float(x['Amount']):
                                                T.trend -= (float(x['Amount']) - float(x['Remaining']))
                                                T.BEXAskRemaining = T.BEXAskMin + (float(x['Amount'])-float(x['Remaining']))
                                                T.BEXAskMin = float(x['Remaining'])
                                                calc = float("%.8f" % (T.BEXAskPrice * (float(x['Amount'])-float(x['Remaining']))))
                                                fees = float("%.8f" %  (calc*0.002))
                                                totals = calc-fees
                                                T.csv(BEX.name, "LIMIT SELL", float(x['Amount'])-float(x['Remaining']), T.BEXAskPrice, T.BEXAskOrderID, totals)
                                                T.BEXAskCalc = T.BEXAskCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXAskPrice)
                                                if T.debugwrite == True:
                                                    T.debug("%f %f %f" % (T.BEXAskRemaining, T.BEXAskMin, T.BEXAskCalc))
                                                if T.BEXAskCalc > 0.0005:
                                                    T.CrypAskOpen = True
                                                    T.BEXAskMin = 0
                                                    T.BEXAskCalc = 0
                                                T.BEXCancelOrder(T.BEXAskOrderID, "sell")
                                        if askcheck is True:
                                            if float(x['Remaining']) != float(x['Amount']):
                                                T.trend -= (float(x['Amount']) - float(x['Remaining']))
                                                T.BEXAskRemaining = T.BEXAskMin + (float(x['Amount'])-float(x['Remaining']))
                                                T.BEXAskMin = float(x['Remaining'])
                                                calc = float("%.8f" % (T.BEXAskPrice * (float(x['Amount'])-float(x['Remaining']))))
                                                fees = float("%.8f" %  (calc*0.002))
                                                totals = calc-fees
                                                T.csv(BEX.name, "LIMIT SELL", float(x['Amount'])-float(x['Remaining']), T.BEXAskPrice, T.BEXAskOrderID, totals)
                                                T.BEXAskCalc = T.BEXAskCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXAskPrice)
                                                if T.debugwrite == True:
                                                    T.debug("%f %f %f" % (T.BEXAskRemaining, T.BEXAskMin, T.BEXAskCalc))
                                                if T.BEXAskCalc > 0.0005:
                                                    T.CrypAskOpen = True
                                                    T.BEXAskMin = 0
                                                    T.BEXAskCalc = 0
                                            T.BEXCancelOrder(T.BEXAskOrderID, "sell")
                                    elif float(x['Rate']) == T.BEXCoin.Asks[0][0]:
                                        if T.BEXCoin.Asks[1][0] - T.BEXCoin.Asks[0][0] > 0.00000005:
                                            if float(x['Remaining']) != float(x['Amount']):
                                                T.trend -= (float(x['Amount']) - float(x['Remaining']))
                                                T.BEXAskRemaining = T.BEXAskMin + (float(x['Amount'])-float(x['Remaining']))
                                                T.BEXAskMin = float(x['Remaining'])
                                                calc = float("%.8f" % (T.BEXAskPrice * (float(x['Amount'])-float(x['Remaining']))))
                                                fees = float("%.8f" %  (calc*0.002))
                                                totals = calc-fees
                                                T.csv(BEX.name, "LIMIT SELL", float(x['Amount'])-float(x['Remaining']), T.BEXAskPrice, T.BEXAskOrderID, totals)
                                                T.BEXAskCalc = T.BEXAskCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXAskPrice)
                                                if T.debugwrite == True:
                                                    T.debug("%f %f %f" % (T.BEXAskRemaining, T.BEXAskMin, T.BEXAskCalc))
                                                if T.BEXAskCalc > 0.0005:
                                                    T.CrypAskOpen = True
                                                    T.BEXAskMin = 0
                                                    T.BEXAskCalc = 0
                                            T.BEXCancelOrder(T.BEXAskOrderID, "sell")
                        if verify == 0 and T.BEXAskOpen == False:
                            T.trend -= T.BEXAskAmount
                            T.BEXAskOpen = True
                            T.BEXAskCalc = 0
                            T.BEXAskMin = 0
                            calc = float("%.8f" % (T.BEXAskAmount * T.BEXAskPrice))
                            fees = float("%.8f" % (calc*0.002))
                            totals = calc-fees
                            T.csv(BEX.name, "LIMIT SELL", T.BEXAskAmount, float("%.8f" % T.BEXAskPrice), T.BEXAskOrderID, totals)
                            if T.BEXWallet == False:
                                T.BEXAskMod += 0.3
                elif T.BEXBidOrder == True and T.BEXAskOrder == False:
                    if marketbids == [] and T.BEXBidOpen == False:
                        T.trend += T.BEXBidAmount
                        T.BEXBidOpen = True
                        T.BEXBidCalc = 0
                        T.BEXBidMin = 0
                        calc = float("%.8f" % (T.BEXBidAmount * T.BEXBidPrice))
                        fee = float("%.8f" % (calc*0.002))
                        totals = calc-fee
                        totals = -totals
                        T.csv(BEX.name, "LIMIT BUY", T.BEXBidAmount, T.BEXBidPrice,T.BEXBidOrderID, totals)
                        if T.BidWallet == False:
                            T.BEXBidMod += 0.3
                    if marketbids != []:
                        verify = 0
                        for x in marketbids:
                            if int(x['OrderId']) != T.BEXBidOrderID:
                                BEX.cancel_order(int(x['OrderId']))
                            if int(x['OrderId']) == T.BEXBidOrderID:
                                verify = 1
                                if T.BASpread > percentage:
                                    if float(x['Remaining']) != float(x['Amount']):
                                        T.trend += (float(x['Amount']) - float(x['Remaining']))
                                        T.BEXBidRemaining = T.BEXBidMin + (float(x['Amount'])-float(x['Remaining']))
                                        T.BEXBidMin = float(x['Remaining'])
                                        calc = float("%.8f" % (T.BEXBidPrice * (float(x['Amount'])-float(x['Remaining']))))
                                        fees = float("%.8f" %  (calc*0.002))
                                        totals = calc-fees
                                        totals = -totals
                                        T.csv(BEX.name, "LIMIT BUY", float(x['Amount'])-float(x['Remaining']), T.BEXBidPrice, T.BEXBidOrderID, totals)
                                        T.BEXBidCalc = T.BEXBidCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXBidPrice)
                                        if T.debugwrite == True:
                                            T.debug("%f %f %f" % (T.BEXAskRemaining, T.BEXAskMin, T.BEXAskCalc))
                                        if T.BEXBidCalc > 0.0005:
                                            T.BEXBidCalc = 0
                                            T.BEXBidMin = 0
                                            T.BEXBidOpen = True
                                    T.BEXCancelOrder(T.BEXBidOrderID, "buy")
                                elif T.BASpread < percentage:
                                    if float(x['Rate']) != T.BEXCoin.Bids[0][0]:
                                        buycheck = T.bidcheck(T.BEXBidPrice, T.BEXBidAmount)
                                        if buycheck == False:
                                            if float(x['Remaining']) != float(x['Amount']):
                                                T.trend += (float(x['Amount']) - float(x['Remaining']))
                                                T.BEXBidRemaining = T.BEXBidMin + (float(x['Amount'])-float(x['Remaining']))
                                                T.BEXBidMin = float(x['Remaining'])
                                                calc = float("%.8f" % (T.BEXBidPrice * (float(x['Amount'])-float(x['Remaining']))))
                                                fees = float("%.8f" %  (calc*0.002))
                                                totals = calc-fees
                                                totals = -totals
                                                T.csv(BEX.name, "LIMIT BUY", float(x['Amount'])-float(x['Remaining']), T.BEXBidPrice, T.BEXBidOrderID, totals)
                                                T.BEXBidCalc = T.BEXBidCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXBidPrice)
                                                if T.debugwrite == True:
                                                    T.debug("%f %f %f" % (T.BEXAskRemaining, T.BEXAskMin, T.BEXAskCalc))
                                                if T.BEXBidCalc > 0.0005:
                                                    T.BEXBidCalc = 0
                                                    T.BEXBidMin = 0
                                                    T.BEXBidOpen = True
                                                T.BEXCancelOrder(T.BEXBidOrderID, "buy")
                                        if buycheck is True:
                                            if float(x['Remaining']) != float(x['Amount']):
                                                T.trend += (float(x['Amount']) - float(x['Remaining']))
                                                T.BEXBidRemaining = T.BEXBidMin + (float(x['Amount'])-float(x['Remaining']))
                                                T.BEXBidMin = float(x['Remaining'])
                                                calc = float("%.8f" % (T.BEXBidPrice * (float(x['Amount'])-float(x['Remaining']))))
                                                fees = float("%.8f" %  (calc*0.002))
                                                totals = calc-fees
                                                totals = -totals
                                                T.csv(BEX.name, "LIMIT BUY", float(x['Amount'])-float(x['Remaining']), T.BEXBidPrice, T.BEXBidOrderID, totals)
                                                T.BEXBidCalc = T.BEXBidCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXBidPrice)
                                                if T.debugwrite == True:
                                                    T.debug("%f %f %f" % (T.BEXAskRemaining, T.BEXAskMin, T.BEXAskCalc))
                                                if T.BEXBidCalc > 0.0005:
                                                    T.BEXBidCalc = 0
                                                    T.BEXBidMin = 0
                                                    T.BEXBidOpen = True
                                            T.BEXCancelOrder(T.BEXBidOrderID, "buy")
                                    elif float(x['Rate']) == T.BEXCoin.Bids[0][0]:
                                        if T.BEXCoin.Bids[0][0] - T.BEXCoin.Bids[1][0] > 0.00000005:
                                            if float(x['Remaining']) != float(x['Amount']):
                                                T.trend += (float(x['Amount']) - float(x['Remaining']))
                                                T.BEXBidRemaining = T.BEXBidMin + (float(x['Amount'])-float(x['Remaining']))
                                                T.BEXBidMin = float(x['Remaining'])
                                                calc = float("%.8f" % (T.BEXBidPrice * (float(x['Amount'])-float(x['Remaining']))))
                                                fees = float("%.8f" %  (calc*0.002))
                                                totals = calc-fees
                                                totals = -totals
                                                T.csv(BEX.name, "LIMIT BUY", float(x['Amount'])-float(x['Remaining']), T.BEXBidPrice, T.BEXBidOrderID, totals)
                                                T.BEXBidCalc = T.BEXBidCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXBidPrice)
                                                if T.debugwrite == True:
                                                    T.debug("%f %f %f" % (T.BEXAskRemaining, T.BEXAskMin, T.BEXAskCalc))
                                                if T.BEXBidCalc > 0.0005:
                                                    T.BEXBidCalc = 0
                                                    T.BEXBidMin = 0
                                                    T.BEXBidOpen = True

                                            T.BEXCancelOrder(T.BEXBidOrderID, "buy")
                        if verify == 0 and T.BEXBidOpen == False:
                            T.trend += T.BEXBidAmount
                            T.BEXBidOpen = True
                            T.BEXBidCalc = 0
                            T.BEXBidMin = 0
                            calc = float("%.8f" % (T.BEXBidAmount * T.BEXBidPrice))
                            fee = float("%.8f" % (calc*0.002))
                            totals = calc-fee
                            totals = -totals
                            T.csv(BEX.name, "LIMIT BUY", T.BEXBidAmount, T.BEXBidPrice,T.BEXBidOrderID, totals)
                            if T.BidWallet == False:
                                T.BEXBidMod += 0.3
                elif T.BEXBidOrder == False and T.BEXAskOrder == True:
                    if marketasks == [] and T.BEXAskOpen == False:
                        T.trend -= T.BEXAskAmount
                        T.BEXAskOpen = True
                        T.BEXAskCalc = 0
                        T.BEXAskMin = 0
                        calc = float("%.8f" % (T.BEXAskAmount * T.BEXAskPrice))
                        fees = float("%.8f" % (calc*0.002))
                        totals = calc-fees
                        T.csv(BEX.name, "LIMIT SELL", T.BEXAskAmount, float("%.8f" % T.BEXAskPrice), T.BEXAskOrderID, totals)
                        if T.BEXWallet == False:
                            T.BEXAskMod += 0.3
                    if marketasks != []:
                        verify = 0
                        for x in marketasks:
                            if int(x['OrderId']) != T.BEXAskOrderID:
                                BEX.cancel_order(int(x['OrderId']))
                            if int(x['OrderId']) == T.BEXAskOrderID:
                                verify = 1
                                if T.ABSpread > percentage:
                                    if float(x['Remaining']) != float(x['Amount']):
                                        T.trend -= (float(x['Amount']) - float(x['Remaining']))
                                        T.BEXAskRemaining = T.BEXAskMin + (float(x['Amount'])-float(x['Remaining']))
                                        T.BEXAskMin = float(x['Remaining'])
                                        calc = float("%.8f" % (T.BEXAskPrice * (float(x['Amount'])-float(x['Remaining']))))
                                        fees = float("%.8f" %  (calc*0.002))
                                        totals = calc-fees
                                        T.csv(BEX.name, "LIMIT SELL", float(x['Amount'])-float(x['Remaining']), T.BEXAskPrice, T.BEXAskOrderID, totals)
                                        T.BEXAskCalc = T.BEXAskCalc +  ((float(x['Amount']) - float(x['Remaining'])) * T.BEXAskPrice)
                                        if T.debugwrite == True:
                                            T.debug("%f %f %f" % (T.BEXAskRemaining, T.BEXAskMin, T.BEXAskCalc))
                                        if T.BEXAskCalc > 0.0005:
                                            T.CrypAskOpen = True
                                            T.BEXAskMin = 0
                                            T.BEXAskCalc = 0
                                    T.BEXCancelOrder(T.BEXAskOrderID, "sell")
                                if T.ABSpread < percentage:
                                    if float(x['Rate']) != T.BEXCoin.Asks[0][0]:
                                        askcheck = T.askcheck(T.BEXAskPrice, T.BEXAskAmount)
                                        if askcheck == False:
                                            if float(x['Remaining']) != float(x['Amount']):
                                                T.trend -= (float(x['Amount']) - float(x['Remaining']))
                                                T.BEXAskRemaining = T.BEXAskMin + (float(x['Amount'])-float(x['Remaining']))
                                                T.BEXAskMin = float(x['Remaining'])
                                                calc = float("%.8f" % (T.BEXAskPrice * (float(x['Amount'])-float(x['Remaining']))))
                                                fees = float("%.8f" %  (calc*0.002))
                                                totals = calc-fees
                                                T.csv(BEX.name, "LIMIT SELL", float(x['Amount'])-float(x['Remaining']), T.BEXAskPrice, T.BEXAskOrderID, totals)
                                                T.BEXAskCalc = T.BEXAskCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXAskPrice)
                                                if T.debugwrite == True:
                                                    T.debug("%f %f %f" % (T.BEXAskRemaining, T.BEXAskMin, T.BEXAskCalc))
                                                if T.BEXAskCalc > 0.0005:
                                                    T.CrypAskOpen = True
                                                    T.BEXAskMin = 0
                                                    T.BEXAskCalc = 0
                                                T.BEXCancelOrder(T.BEXAskOrderID, "sell")
                                        if askcheck is True:
                                            if float(x['Remaining']) != float(x['Amount']):
                                                T.trend -= (float(x['Amount']) - float(x['Remaining']))
                                                T.BEXAskRemaining = T.BEXAskMin + (float(x['Amount'])-float(x['Remaining']))
                                                T.BEXAskMin = float(x['Remaining'])
                                                calc = float("%.8f" % (T.BEXAskPrice * (float(x['Amount'])-float(x['Remaining']))))
                                                fees = float("%.8f" %  (calc*0.002))
                                                totals = calc-fees
                                                T.csv(BEX.name, "LIMIT SELL", float(x['Amount'])-float(x['Remaining']), T.BEXAskPrice, T.BEXAskOrderID, totals)
                                                T.BEXAskCalc = T.BEXAskCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXAskPrice)
                                                if T.debugwrite == True:
                                                    T.debug("%f %f %f" % (T.BEXAskRemaining, T.BEXAskMin, T.BEXAskCalc))
                                                if T.BEXAskCalc > 0.0005:
                                                    T.CrypAskOpen = True
                                                    T.BEXAskMin = 0
                                                    T.BEXAskCalc = 0
                                            T.BEXCancelOrder(T.BEXAskOrderID, "sell")
                                    elif float(x['Rate']) == T.BEXCoin.Asks[0][0]:
                                        if T.BEXCoin.Asks[1][0] - T.BEXCoin.Asks[0][0] > 0.00000005:
                                            if float(x['Remaining']) != float(x['Amount']):
                                                T.trend -= (float(x['Amount']) - float(x['Remaining']))
                                                T.BEXAskRemaining = T.BEXAskMin + (float(x['Amount'])-float(x['Remaining']))
                                                T.BEXAskMin = float(x['Remaining'])
                                                calc = float("%.8f" % (T.BEXAskPrice * (float(x['Amount'])-float(x['Remaining']))))
                                                fees = float("%.8f" %  (calc*0.002))
                                                totals = calc-fees
                                                T.csv(BEX.name, "LIMIT SELL", float(x['Amount'])-float(x['Remaining']), T.BEXAskPrice, T.BEXAskOrderID, totals)
                                                T.BEXAskCalc = T.BEXAskCalc + ((float(x['Amount']) - float(x['Remaining'])) * T.BEXAskPrice)
                                                if T.debugwrite == True:
                                                    T.debug("%f %f %f" % (T.BEXAskRemaining, T.BEXAskMin, T.BEXAskCalc))
                                                if T.BEXAskCalc > 0.0005:
                                                    T.CrypAskOpen = True
                                                    T.BEXAskMin = 0
                                                    T.BEXAskCalc = 0
                                            T.BEXCancelOrder(T.BEXAskOrderID, "sell")
                        if verify == 0 and T.BEXAskOpen == False:
                            T.trend -= T.BEXAskAmount
                            T.BEXAskOpen = True
                            T.BEXAskCalc = 0
                            T.BEXAskMin = 0
                            T.BEXAskCalc = 0
                            calc = float("%.8f" % (T.BEXAskAmount * T.BEXAskPrice))
                            fees = float("%.8f" % (calc*0.002))
                            totals = calc-fees
                            T.csv(BEX.name, "LIMIT SELL", T.BEXAskAmount, float("%.8f" % T.BEXAskPrice), T.BEXAskOrderID, totals)
                            if T.BEXWallet == False:
                                T.BEXAskMod += 0.3
    #If there's an active order on AExchange
    if T.AEXOrder == True:
        bao = AEX.active_parse(T.AEXPair)
        if T.debugwrite == True:
            T.aog(bao)
        if T.AEXBidOrderID == "" and T.AEXBidPrice == 0:
            T.AEXBidOrder = False
            if T.AEXAskOrder == False:
                T.AEXOrder = False
        if T.AEXAskOrderID == "" and T.AEXAskPrice == 0:
            T.AEXAskOrder = False
            if T.AEXBidOrder == False:
                T.AEXOrder = False
        if bao is not None:
            if bao == []:
                #This means that the order has filled on AExchange
                if T.AEXBidOrder == False and T.AEXAskOrder == True:
                    calc = float("%.8f" % (T.AEXAskAmount * T.AEXAskPrice))
                    fees = float("%.8f" % (calc*AEX.fee))
                    totals = calc-fees
                    T.csv(AEX.name, "LIMIT SELL", T.AEXAskAmount, float("%.8f" % T.AEXAskPrice), T.AEXAskOrderID, totals)
                    T.AEXOrderType = ""
                    T.AEXAskPrice = 0
                    T.AEXAskAmount = 0
                    T.BEXBidOrder = False
                    T.BEXBidOpen = False
                    T.AEXAskOrder = False
                    T.BEXBidPrice = 0
                    T.BEXBidAmount = 0
                    T.BEXBidRemaining = 0
                    T.AEXOrder = False
                elif T.AEXBidOrder == True and T.AEXAskOrder == False:
                    calc = float("%.8f" % (T.AEXBidAmount * T.AEXBidPrice))
                    fees = float("%.8f" % (calc*AEX.fee))
                    totals = calc-fees
                    totals = -totals
                    T.csv(AEX.name, "LIMIT BUY", T.AEXBidAmount, float("%.8f" % T.AEXBidPrice), T.AEXBidOrderID, totals)
                    T.AEXOrderType = ""
                    T.AEXBidPrice = 0
                    T.AEXBidAmount = 0
                    T.BEXAskOrder = False
                    T.BEXAskOpen = False
                    T.AEXBidOrder = False
                    T.BEXAskPrice = 0
                    T.BEXAskAmount = 0
                    T.BEXAskRemaining = 0
                    T.AEXOrder = False
                elif T.AEXBidOrder == True and T.AEXAskOrder == True:
                    T.AEXOrderType = ""
                    calc = float("%.8f" % (T.AEXAskAmount*T.AEXAskPrice))
                    fees = float("%.8f" %(calc*AEX.fee))
                    totals = calc-fees
                    T.csv(AEX.name, "LIMIT SELL", T.AEXAskAmount, float("%.8f" % T.AEXAskPrice), T.AEXAskOrderID, totals)
                    calc = float("%.8f" % (T.AEXBidAmount * T.AEXBidPrice))
                    fees = float("%.8f" % (calc*AEX.fee))
                    totals = calc-fees
                    totals = -totals
                    T.csv(AEX.name, "LIMIT BUY", T.AEXBidAmount, float("%.8f" % T.AEXBidPrice), T.AEXBidOrderID, totals)
                    T.AEXAskPrice = 0
                    T.AEXAskAmount = 0
                    T.BEXBidOrder = False
                    T.BEXBidOpen = False
                    T.AEXAskOrder = False
                    T.BEXBidPrice = 0
                    T.BEXBidAmount = 0
                    T.AEXOrderType = ""
                    T.AEXBidPrice = 0
                    T.AEXBidAmount = 0
                    T.BEXAskOrder = False
                    T.BEXAskOpen = False
                    T.AEXAskOrder = False
                    T.BEXAskPrice = 0
                    T.BEXAskAmount = 0
                    T.AEXOrder = False
                    T.BEXAskRemaining = 0
                    T.BEXBidRemaining = 0
            elif bao != []:
                #This means there's still an active order on AExchange
                updated = False
                bbids = []
                basks = []
                for x in bao:
                    if str(x['OrderType']) == "Sell":
                        basks.append(x)
                        updated = True
                    if str(x['OrderType']) == "Buy":
                        bbids.append(x)
                        updated = True
                if updated == True:
                    if T.AEXBidOrder == True and T.AEXBidOrderID == '' and bbids != []:
                        T.AEXBidOrderID = bbids[0]['OrderID']
                        T.AEXBidPrice = bbids[0]['Price']
                        T.AEXBidAmount = bbids[0]['Remaining']
                    if T.AEXAskOrder == True and T.AEXAskOrderID == '' and basks != []:
                        T.AEXAskOrderID == basks[0]['OrderID']
                        T.AEXAskPrice = basks[0]['Price']
                        T.AEXAskAmount = basks[0]['Remaining']
                    if T.AEXBidOrder == True and T.AEXBidOrderID == '' and bbids == []:
                        T.AEXBidOrder = False
                    if T.AEXAskOrder == True and T.AEXAskOrderID == '' and basks == []:
                        T.AEXAskOrder = False
                    if T.AEXBidOrder and T.AEXAskOrder == True:
                        if basks == []:
                            T.AEXOrderType = ""
                            calc = float("%.8f" % (T.AEXAskAmount * T.AEXAskPrice))
                            fees = float("%.8f" % (calc*AEX.fee))
                            totals = calc-fees
                            T.csv(AEX.name, "LIMIT SELL", T.AEXAskAmount, float("%.8f" % T.AEXAskPrice), T.AEXAskOrderID, totals)
                            T.AEXAskPrice = 0
                            T.AEXAskAmount = 0
                            T.AEXAskRemaining = 0
                            T.BEXBidOrder = False
                            T.BEXBidOpen = False
                            T.AEXAskOrder = False
                            T.BEXBidPrice = 0
                            T.BEXBidAmount = 0
                            T.BEXBidRemaining = 0
                            if T.AEXBidOrder == False:
                                T.AEXOrder = False
                        if bbids == []:
                            T.AEXOrderType = ""
                            calc = float("%.8f" % (T.AEXBidAmount * T.AEXBidPrice))
                            fees = float("%.8f" % (calc*AEX.fee))
                            totals = calc-fees
                            totals = -totals
                            T.csv(AEX.name, "LIMIT BUY", T.AEXBidAmount, float("%.8f" % T.AEXBidPrice), T.AEXBidOrderID, totals)
                            T.AEXBidPrice = 0
                            T.AEXBidAmount = 0
                            T.AEXBidRemaining = 0
                            T.BEXAskOrder = False
                            T.BEXAskOpen = False
                            T.AEXBidOrder = False
                            T.BEXAskPrice = 0
                            T.BEXAskAmount = 0
                            T.BEXAskRemaining = 0
                            if T.AEXAskOrder == False:
                                T.AEXOrder = False
                        if basks != []:
                            #Verifying how much may have been filled in a sell order and adjusting any new orders to reflect a partial fill
                            verify = 0
                            for x in basks:
                                if str(x['OrderID']) == T.AEXAskOrderID:
                                    verify = 1
                                    if float(x['Price']) != T.AEXCoin.Asks[0][0]:
                                        if float(x['Remaining']) != float(x['Quantity']):
                                            T.AEXAskRemaining = float(x['Remaining'])
                                            calc = float("%.8f" % (((float(x['Quantity']) - float(x['Remaining'])) * T.AEXAskPrice)))
                                            fees = float("%.8f" % (calc*AEX.fee))
                                            totals = calc-fees
                                            T.csv(AEX.name, "LIMIT SELL", -(float(x['Quantity']) - float(x['Remaining'])), float("%.8f" % T.AEXAskPrice), T.AEXAskOrderID, totals)
                                        T.AEXCancelOrder(T.AEXAskOrderID, T.AEXAskAmount, T.AEXAskPrice, "sell")
                                    elif float(x['Price']) == T.AEXCoin.Asks[0][0]:
                                        if T.AEXCoin.Asks[1][0] - T.AEXCoin.Asks[0][0] > 0.00000005:
                                            if float(x['Remaining']) != float(x['Quantity']):
                                                T.AEXAskRemaining = float(x['Remaining'])
                                                calc = float("%.8f" % (((float(x['Quantity']) - float(x['Remaining'])) * T.AEXAskPrice)))
                                                fees = float("%.8f" % (calc*AEX.fee))
                                                totals = calc-fees
                                                T.csv(AEX.name, "LIMIT SELL", -(float(x['Quantity']) - float(x['Remaining'])), float("%.8f" % T.AEXAskPrice), T.AEXAskOrderID, totals)
                                            T.AEXCancelOrder(T.AEXAskOrderID, T.AEXAskAmount, T.AEXAskPrice, "sell")
                            if verify == 0:
                                calc = float("%.8f" % (T.AEXAskAmount * T.AEXAskPrice))
                                fees = float("%.8f" % (calc*AEX.fee))
                                totals = calc-fees
                                T.csv(AEX.name, "LIMIT SELL", T.AEXAskAmount, float("%.8f" % T.AEXAskPrice), T.AEXAskOrderID, totals)
                                T.AEXOrderType = ""
                                T.AEXAskPrice = 0
                                T.AEXAskAmount = 0
                                T.BEXBidOrder = False
                                T.BEXBidOpen = False
                                T.AEXAskOrder = False
                                T.BEXBidPrice = 0
                                T.BEXBidAmount = 0
                                T.BEXBidRemaining = 0
                                T.AEXOrder = False
                        if bbids != []:
                            #Verifying how much may have been filled in a buy order and adjusting any new orders to reflect a partial fill
                            verify = 0
                            for x in bbids:
                                if str(x['OrderID']) == T.AEXBidOrderID:
                                    verify = 1
                                    if float(x['Price']) != T.AEXCoin.Bids[0][0]:
                                        if float(x['Remaining']) != float(x['Quantity']):
                                            T.AEXBidRemaining = float(x['Remaining'])
                                            calc = float("%.8f" % (((float(x['Quantity']) - float(x['Remaining']))*T.AEXBidPrice)))
                                            fees = float("%.8f" % (calc*AEX.fee))
                                            totals = calc-fees
                                            totals = -totals
                                            T.csv(AEX.name, "LIMIT BUY", float(x['Quantity'])-float(x['Remaining']),float("%.8f" % T.AEXBidPrice), T.AEXBidOrderID, totals)
                                        T.AEXCancelOrder(T.AEXBidOrderID, T.AEXBidAmount, T.AEXBidPrice, "buy")
                                    elif float(x['Limit']) == T.AEXCoin.Bids[0][0]:
                                        if T.AEXCoin.Bids[0][0] - T.AEXCoin.Bids[1][0] > 0.00000005:
                                            if float(x['Remaining']) != float(x['Quantity']):
                                                T.AEXBidRemaining = float(x['Remaining'])
                                                calc = float("%.8f" % (((float(x['Quantity']) - float(x['Remaining']))*T.AEXBidPrice)))
                                                fees = float("%.8f" % (calc*AEX.fee))
                                                totals = calc-fees
                                                totals = -totals
                                                T.csv(AEX.name, "LIMIT BUY", float(x['Quantity'])-float(x['Remaining']),float("%.8f" % T.AEXBidPrice), T.AEXBidOrderID, totals)
                                                T.AEXCancelOrder(T.AEXBidOrderID, T.AEXBidAmount, T.AEXBidPrice, "buy")
                            if verify == 0:
                                T.AEXOrderType = ""
                                calc = float("%.8f" % (T.AEXBidAmount * T.AEXBidPrice))
                                fees = float("%.8f" % (calc*AEX.fee))
                                totals = calc-fees
                                totals = -totals
                                T.csv(AEX.name, "LIMIT BUY", T.AEXBidAmount, float("%.8f" % T.AEXBidPrice), T.AEXBidOrderID, totals)
                                T.AEXBidPrice = 0
                                T.AEXBidAmount = 0
                                T.AEXBidRemaining = 0
                                T.BEXAskOrder = False
                                T.BEXAskOpen = False
                                T.AEXBidOrder = False
                                T.BEXAskPrice = 0
                                T.BEXAskAmount = 0
                                T.BEXAskRemaining = 0
                                if T.AEXAskOrder == False:
                                    T.AEXOrder = False
                    elif T.AEXBidOrder == True and T.AEXAskOrder == False:
                        if bbids == []:
                            T.AEXOrderType = ""
                            calc = float("%.8f" % (T.AEXBidAmount * T.AEXBidPrice))
                            fees = float("%.8f" % (calc*AEX.fee))
                            totals = calc-fees
                            totals = -totals
                            T.csv(AEX.name, "LIMIT BUY", T.AEXBidAmount, float("%.8f" % T.AEXBidPrice), T.AEXBidOrderID, totals)
                            T.AEXBidPrice = 0
                            T.AEXBidAmount = 0
                            T.AEXBidRemaining = 0
                            T.BEXAskOrder = False
                            T.BEXAskOpen = False
                            T.AEXBidOrder = False
                            T.BEXAskPrice = 0
                            T.BEXAskAmount = 0
                            T.BEXAskRemaining = 0
                            if T.AEXAskOrder == False:
                                T.AEXOrder = False
                        elif bbids != []:
                            verify = 0
                            for x in bbids:
                                if str(x['OrderID']) == T.AEXBidOrderID:
                                    verify = 1
                                    if float(bbids[0]['Price']) != T.AEXCoin.Bids[0][0]:
                                        if float(x['Remaining']) != float(x['Quantity']):
                                            T.AEXBidRemaining = float(x['Remaining'])
                                            calc = float("%.8f" % (((float(x['Quantity']) - float(x['Remaining']))*T.AEXBidPrice)))
                                            fees = float("%.8f" %(calc*AEX.fee))
                                            totals = calc-fees
                                            totals = -totals
                                            T.csv(AEX.name, "LIMIT BUY", float(x['Quantity'])-float(x['Remaining']),float("%.8f" % T.AEXBidPrice), T.AEXBidOrderID, totals)
                                        T.AEXCancelOrder(T.AEXBidOrderID, T.AEXBidAmount, T.AEXBidPrice, "buy")
                                    elif float(x['Price']) == T.AEXCoin.Bids[0][0]:
                                        if T.AEXCoin.Bids[0][0] - T.AEXCoin.Bids[1][0] > 0.00000005:
                                            if float(x['Remaining']) != float(x['Quantity']):
                                                T.AEXBidRemaining = float(x['Remaining'])
                                                totals = float("%.8f"% ((float(x['Quantity'])-float(x['Remaining']))*T.AEXBidPrice)) - float("%.8f"% (((float(bbids[0]['Quantity'])-float(bbids[0]['QuantityRemaining']))*T.AEXBidPrice)*0.002))
                                                calc = float("%.8f" % (((float(x['Quantity']) - float(x['Remaining']))*T.AEXBidPrice)))
                                                fees = float("%.8f" % (calc*AEX.fee))
                                                totals = calc-fees
                                                totals = -totals
                                                T.csv(AEX.name, "LIMIT BUY", float(x['Quantity'])-float(x['Remaining']),float("%.8f" % T.AEXBidPrice), T.AEXBidOrderID, totals)
                                            T.AEXCancelOrder(T.AEXBidOrderID, T.AEXBidAmount, T.AEXBidPrice, "buy")
                            if verify == 0:
                                T.AEXOrderType = ""
                                calc = float("%.8f" % (T.AEXBidAmount * T.AEXBidPrice))
                                fees = float("%.8f" % (calc*AEX.fee))
                                totals = calc-fees
                                totals = -totals
                                T.csv(AEX.name, "LIMIT BUY", T.AEXBidAmount, float("%.8f" % T.AEXBidPrice), T.AEXBidOrderID, totals)
                                T.AEXBidPrice = 0
                                T.AEXBidAmount = 0
                                T.AEXBidRemaining = 0
                                T.BEXAskOrder = False
                                T.BEXAskOpen = False
                                T.AEXBidOrder = False
                                T.BEXAskPrice = 0
                                T.BEXAskAmount = 0
                                T.BEXAskRemaining = 0
                                if T.AEXAskOrder == False:
                                    T.AEXOrder = False
                    elif T.AEXBidOrder == False and T.AEXAskOrder == True:
                        if basks == []:
                            T.AEXOrderType = ""
                            calc = float("%.8f" % (T.AEXAskAmount * T.AEXAskPrice))
                            fees = float("%.8f" % (calc*AEX.fee))
                            totals = calc-fees
                            T.csv(AEX.name, "LIMIT SELL", T.AEXAskAmount, float("%.8f" % T.AEXAskPrice), T.AEXAskOrderID, totals)
                            T.AEXAskPrice = 0
                            T.AEXAskAmount = 0
                            T.AEXAskRemaining = 0
                            T.BEXBidOrder = False
                            T.BEXBidOpen = False
                            T.AEXAskOrder = False
                            T.BEXBidPrice = 0
                            T.BEXBidAmount = 0
                            T.BEXAskRemaining = 0
                            if T.AEXBidOrder == False:
                                T.AEXOrder = False
                        elif basks != []:
                            verify = 0
                            for x in basks:
                                if str(x['OrderID']) == T.AEXAskOrderID:
                                    verify = 1
                                    if float(x['Price']) != T.AEXCoin.Asks[0][0]:
                                        if float(x['Remaining']) != float(x['Quantity']):
                                            T.AEXAskRemaining = float(x['Remaining'])
                                            calc = float("%.8f" % (((float(x['Quantity']) - float(x['Remaining'])) * T.AEXAskPrice)))
                                            fees = float("%.8f" % (calc*AEX.fee))
                                            totals = calc-fees
                                            T.csv(AEX.name, "LIMIT SELL", float(x['Quantity']) - float(x['Remaining']), float("%.8f" % T.AEXAskPrice), T.AEXAskOrderID, totals)
                                        T.AEXCancelOrder(T.AEXAskOrderID, T.AEXAskAmount, T.AEXAskPrice, "sell")
                                    elif float(x['Price']) == T.AEXCoin.Asks[0][0]:
                                        if T.AEXCoin.Asks[1][0] - T.AEXCoin.Asks[0][0] > 0.00000005:
                                            if float(x['Remaining']) != float(x['Quantity']):
                                                T.AEXAskRemaining = float(x['Remaining'])
                                                calc = float("%.8f" % (((float(x['Quantity']) - float(x['Remaining'])) * T.AEXAskPrice)))
                                                fees = float("%.8f" % (calc*AEX.fee))
                                                totals = calc-fees
                                                T.csv(AEX.name, "LIMIT SELL", float(x['Quantity']) - float(x['Remaining']), float("%.8f" % T.AEXAskPrice), T.AEXAskOrderID, totals)
                                            T.AEXCancelOrder(T.AEXAskOrderID, T.AEXAskAmount, T.AEXAskPrice, "sell")
                            if verify == 0:
                                calc = float("%.8f" % (T.AEXAskAmount * T.AEXAskPrice))
                                fees = float("%.8f" % (calc*AEX.fee))
                                totals = calc-fees
                                T.csv(AEX.name, "LIMIT SELL", T.AEXAskAmount, float("%.8f" % T.AEXAskPrice), T.AEXAskOrderID, totals)
                                T.AEXOrderType = ""
                                T.AEXAskPrice = 0
                                T.AEXAskAmount = 0
                                T.BEXBidOrder = False
                                T.BEXBidOpen = False
                                T.AEXAskOrder = False
                                T.BEXBidPrice = 0
                                T.BEXBidAmount = 0
                                T.BEXBidRemaining = 0
                                T.AEXOrder = False
    
    #Verbose order status                                   
    if T.BEXAskOrder == True and T.BEXAskOpen == False:
        print ("Sell order active at %f for %f on %s" % (T.BEXAskPrice, T.BEXAskAmount, BEX.name))
            
    if T.BEXBidOrder == True and T.BEXBidOpen == False:
        print ("Buy order active at %f for %f on %s" % (T.BEXBidPrice, T.BEXBidAmount, BEX.name))
        
    if T.AEXBidOrder == True:
        print ("Buy order active at %f for %f on %s" % (T.AEXBidPrice, T.AEXBidAmount, AEX.name))
    if T.AEXAskOrder == True:
        print ("Sell order active at %f for %f on %s" % (T.AEXAskPrice, T.AEXAskAmount, AEX.name))
        
    #Randomizes the amount of coins being used per trades to hide the bot
    if T.AEXBidOrder and T.AEXAskOrder and T.BEXBidOrder and T.BEXAskOrder == False:
        if counter > 40:
            T.randAmount()
            
    #Warning in case orderbooks haven't been updated
    if AEX.error_window > 0:
        print ("Warning: %s order book has not been updated for %f seconds. NO new orders will be processed until new data has been received" % (AEX.name, AEX.error_window))
    if BEX.error_window > 0:
        print ("Warning: %s orderbook has not been updated for %f seconds. No new orders will be processed until new data has been received" % (BEX.name, BEX.error_window))
    if AEX.error_window > 30:
        print ("Warning: %s orderbook has not been updated in %f seconds. Any active orders on %s will be cancelled" % (AEX.name, AEX.error_window, BEX.name))
        if T.BEXBidOrder == True:
            T.BEXCancelOrder(T.BEXBidOrderID, "buy")
        if T.BEXAskOrder == True:
            T.BEXCancelOrder(T.BEXAskOrderID, "sell")
            
    if AEX.error_window == 0 and BEX.error_window == 0:
        
        if T.AEXBidOrder == False and T.BEXAskOpen == True and AEXbase >= minbase:
                if T.AEXBidRemaining != 0:
                        if T.AEXBidRemaining * T.AEXCoin.Bids[0][0] < 0.0006:
                            T.AEXBidRemaining = 0
                            T.AEXBidAmount = 0
                            T.AEXBidPrice = 0
                            T.BEXAskRemaining = 0
                            T.BEXAskPrice = 0
                            T.BEXAskAmount = 0
                            T.BEXAskOpen = False
                            T.BEXAskOrder = False
                        if T.AEXBidRemaining * T.AEXCoin.Bids[0][0] >= 0.0006:
                            T.AEXorder(T.AEXBidRemaining, T.AEXCoin.Bids[0][0] + 0.00000001, "buy")
                elif T.AEXBidRemaining == 0:
                    if T.BEXAskRemaining == 0:
                        if T.AEXCoin.Asks[0][0] - 0.00000001 > T.AEXCoin.Bids[0][0]:
                            T.AEXorder(T.askBlock, T.AEXCoin.Bids[0][0] + 0.00000001, "buy")
                        else:
                            T.AEXorder(T.askBlock, T.AEXCoin.Bids[0][0], "buy")
                    elif T.BEXAskRemaining != 0:
                        if T.AEXCoin.Asks[0][0] - 0.00000001 > T.AEXCoin.Bids[0][0]:
                            T.AEXorder(T.BEXAskRemaining, T.AEXCoin.Bids[0][0] + 0.00000001, "buy")
                        else:
                            T.AEXorder(T.BEXAskRemaining, T.AEXCoin.Bids[0][0], "buy")
        
        buymod = 0
        if T.AEXWallet == False:
            buymod = (2 + T.BEXBidMod)
            print ("Warning: %s wallet is down" % AEX.name)
        if T.BASpread < (percentage * buymod) and T.BEXBidOrder == False and T.AEXBal >= T.bidBlock and BEXbase >= minbase and T.BEXBidOpen == False and T.AEXBalTotal >= T.bidBlock:
            if T.BEXBidMin == 0:
                T.BEXorder(T.bidBlock, T.BEXCoin.Bids[0][0] + 0.00000001, "buy")
            elif T.BEXBidMin > 0:
                T.BEXorder(T.BEXBidMin, T.BEXCoin.Bids[0][0] + 0.00000001, "buy")
            
        #Sells on AExchange
        if T.AEXAskOrder == False and T.BEXBidOpen == True and T.AEXBal > T.base*1.25:
            if T.AEXAskRemaining != 0:
                if T.AEXAskRemaining * T.AEXCoin.Asks[0][0] < 0.0006:
                    T.AEXAskRemaining = 0
                    T.AEXAskAmount = 0
                    T.AEXAskPrice = 0
                    T.BEXBidRemaining = 0
                    T.BEXBidAmount = 0
                    T.BEXBidPrice = 0
                    T.BEXBidOpen = False
                    T.BEXBidOrder = False
                if T.AEXAskRemaining * T.AEXCoin.Asks[0][0] >= 0.0006:
                    T.AEXorder(T.AEXAskRemaining, T.AEXCoin.Asks[0][0] - 0.00000001, "sell")
            elif T.AEXAskRemaining == 0:
                                
                if T.BEXBidRemaining == 0:
                    if T.AEXCoin.Asks[0][0] - 0.00000001 > T.AEXCoin.Bids[0][0]:
                        T.AEXorder(T.bidBlock, T.AEXCoin.Asks[0][0] - 0.00000001, "sell")
                    else:
                        T.AEXorder(T.bidBlock, T.AEXCoin.Asks[0][0], "sell")
                elif T.BEXBidRemaining != 0:
                    if T.AEXCoin.Asks[0][0] - 0.00000001 > T.AEXCoin.Bids[0][0]:
                        T.AEXorder(T.BEXBidRemaining, T.AEXCoin.Asks[0][0] - 0.00000001, "sell")
                    else:
                        T.AEXorder(T.BEXBidRemaining, T.AEXCoin.Asks[0][0], "sell")
                        
        #Sells on BExchange
        sellmod = 0
        if T.BEXWallet == False:
            sellmod = (2 + T.BEXAskMod)
            print ("Warning: Wallet is currently down on %s. Sell threshold is now %f" % (BEX.name, percentage * sellmod))
        if T.ABSpread < (percentage * sellmod) and T.BEXAskOrder == False and T.BEXBal >= T.base * 1.25 and T.BEXAskOpen == False:
            if T.BEXAskMin == 0:
                T.BEXorder(T.askBlock, T.BEXCoin.Asks[0][0] - 0.00000001, "sell")
            elif T.BEXAskMin > 0:
                T.BEXorder(T.BEXAskMin, T.BEXCoin.Asks[0][0] - 0.00000001, "sell")
                
    if autowithdraw == True:
        T.autowithdrawal()
