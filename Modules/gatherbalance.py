import random
import Settings

def gather(T, BEX, AEX, percentage):
    """
    This was designed to start accumulating coins for arbitrage trading if there wasn't any available. This can be dangerous as it does allow the bot to start accumulate
    any asset on it's own, so you might be surprised to find balance for coins you've never heard of before. This is a very old method as newer methods of technical
    analysis have been created to look for entry points on assets, so it's not buying up while the price is dropping, since the price can drop faster and lose more value
    than this can possibly counter.
    """
    
    if T.AEXOrder == True:
        aao = AEX.active_parse(T.AEXPair)
        if aao is not None:
            if aao == [] and T.AEXBidOrder == False:
                T.AEXBidOrder = False
                T.AEXOrder = False
                T.BEXGatherAmount += T.AEXBidOrder
                T.BEXGatherSize -= T.AEXBidOrder
                calc = float("%.8f" % (T.AEXBidPrice * T.AEXBidAmount))
                fees = float("%.8f" % (calc* 0.002))
                totals = calc - fees
                T.csv(AEX.name, "ACCUMULATE BUY", T.AEXBidAmount, T.AEXBidPrice, T.AEXBidOrderID, totals)
                T.AEXBidPrice = 0
                T.AEXBidAmount = 0
                T.AEXBidOrderID = ""
            if aao != []:
                for x in aao:
                    if str(x['OrderID']) == T.AEXBidOrderID:
                        if T.ABSpread <= percentage:
                            if float(x['Price']) != T.AEXCoin.BestBid:
                                if float(x['Remaining']) != float(x['Amount']):
                                    T.BEXGatherAmount += float(x['Amount']) - float(x['Remaining'])
                                    T.BEXGatherSize -= float(x['Amount']) - float(x['Remaining'])
                                T.AEXCancelOrder(T.AEXBidOrderID, 'buy')
                            if float(x['Price']) > percentage:
                                if float(x['Remaining']) != float(x['Amount']):
                                    T.BEXGatherAmount += float(x['Amount']) - float(x['Remaining'])
                                    T.BEXGatherSize -= float(x['Amount']) - float(x['Remaining'])
                                T.AEXCancelOrder(T.AEXBidOrderID, 'buy')
    
    if T.BEXOrder == True:
        bao = BEX.active_parse(T.BEXPair)
        if bao is not None:
            if bao == [] and T.BEXBidOrder == True:
                T.BEXBidOrder = False
                T.BEXOrder = False
                T.BEXGatherAmount += T.BEXBidAmount
                T.BEXGatherSize -= T.BEXBidAmount
                calc = float("%.8f" % (T.BEXBidPrice * T.BEXBidAmount))
                fees = float("%.8f" % (calc* 0.002))
                totals = calc - fees
                T.csv(BEX.name, "ACCUMULATE BUY", T.BEXBidAmount, T.BEXBidPrice, T.BEXBidOrderID, totals)
                T.BEXBidPrice = 0
                T.BEXBidAmount = 0
                T.BEXBidOrderID = ""
            if bao != []:
                for x in bao:
                    if str(x['OrderID']) == T.BEXBidOrderID:
                        if T.BASpread <= percentage:
                            if float(x['Price']) != T.BEXCoin.BestBid:
                                if float(x['Remaining']) != float(x['Amount']):
                                    T.BEXGatherAmount += float(x['Amount']) - float(x['Remaining'])
                                    T.BEXGatherSize -= float(x['Amount']) - float(x['Remaining'])
                                T.BEXCancelOrder(T.BEXBidOrderID, "buy")
                        elif T.BASpread >= percentage:
                            if float(x['Remaining']) != float(x['Amount']):
                                T.BEXGatherAmount += float(x['Amount']) - float(x['Remaining'])
                                T.BEXGatherSize -= float(x['Amount'])
                            T.BEXCancelOrder(T.BEXBidOrderID, 'buy')
    print("Current gather balance: %f" % T.BEXGatherAmount)
    if T.BEXGatherSize == 0 or T.BEXGatherSize * T.BEXCoin.BestBid < 0.0001:
        T.BEXActiveGather = False
        
    if T.AEXBidOrder == False and T.BEXGatherSize > 0 and T.ABSpread < percentage:
        lot = float("%.6f" % (Settings.liveBitBTCequiv / T.AEXCoin.BestBid))
        lot = float("%.6f" % (random.uniform(lot *0.75, lot*1.25)))
        if T.BEXGatherSize <= lot:
            lot = T.BEXGatherSize
        if round(T.AEXCoin.BestBid+ 0.00000001, 8) > round(T.AEXCoin.BestAsk):
            T.AEXorder(lot, round(T.AEXCoin.BestBid+ 0.00000001, 8), 'buy')
        if round(T.AEXCoin.BestBid, 8) == round(T.AEXCoin.BestAsk, 8):
            T.AEXorder(lot, round(T.AEXCoin.BestBid, 8), 'buy')
        
    if T.BEXBidOrder == False and T.BEXGatherSize > 0 and T.BASpread < percentage:
        lot = float("%.6f" % (Settings.liveBitBTCequiv / T.BEXCoin.BestBid))
        lot = float("%.6f" % (random.uniform(lot *0.75, lot*1.25)))
        if T.BEXGatherSize <= lot:
            lot = T.BEXGatherSize
        if round(T.BEXCoin.BestBid+ 0.00000001, 8) > round(T.BEXCoin.BestAsk):
            T.BEXorder(lot, round(T.BEXCoin.BestBid+ 0.00000001, 8), 'buy')
        if round(T.BEXCoin.BestBid, 8) == round(T.BEXCoin.BestAsk, 8):
            T.BEXorder(lot, round(T.BEXCoin.BestBid, 8), 'buy')
    
