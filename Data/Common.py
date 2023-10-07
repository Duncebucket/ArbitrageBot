

class Coin:
    
    def __init__(self, fee):
        self.fee = fee
        self.Book = {}
        self.Bids = []
        self.Asks = []
        self.BestBid = 0
        self.BestAsk = 0
        self.BestBidFee = 0
        self.BestAskFee = 0