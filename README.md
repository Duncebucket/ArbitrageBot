# ArbitrageBot
Crypto Arbitrage Bot

This was the final version of a crypto centralized exchange arbitrage trading bot I wrote several years ago. It has been stripped down to two random exchange pairings I had running many
years ago (at least one of which no longer operates) which means this will not run out of the box. This was developed during the 2016-2017 price run and has fell out of use since far more bots
have been introduced which really dropped how many inefficiencies there have been to tap.

Arbitrage trading is not a particularly advanced trading model. It takes advantage of market inefficencies between the same asset on two seperate exchanges by placing either a buy 
or sell order on a lower volume exchange and, once that order is filled, a closing order is placed on the higher volume exchange (which should be filled much faster) for the same 
volume as the initial order was filled. A second order type is a market order which looks for orders that can be filled immediately (ex: a sell order on exchange A is at $1 and a buy
order exists on exchange B for $1.10, meaning the bot can immediately buy at $1 and sell at $1.10 and will continue to do so until the orders are filled, or the bot runs out of assets).

The bot does have the ability to automatically withdraw funds from one exchange to another so there isn't a build up of assets causing the bot to run out of funds. It also randomized
lot sizes so it appears more like a natural order so other bots won't try to counter trades. When placing an order it will attempt to be the best buy/sell order listed if there's
a big enough spread to profit (including fees), but won't step in front of smaller orders so it's not going to be easily beat by other bots trying to close the spread. It generally
doesn't place large orders to smother out any other orders being placed on the exchange, so it likely wouldn't make substantial money on every trade, but, like a drips into a
bathtub, it will grow over time. It also confirms orders made so all loops should close for the exact amount of the initial order loop size (assuming it is within the minimum order size).

It also checks to see if an asset has active wallets, meaning if a wallet is down on either exchange it raises the minimum spread to prevent assets from piling up in a pair which
may cause liquidity issues if there's a trading pair with active wallets. It also checks to ensure both exchanges are sending data and will stop orders if one exchange is down
for regular or unscheduled maintanence, in the event there's major price momentum during that time which may cause losses if the closing order is well outside the calculated
price. 

This is not a market neutral strategy. It worked best while markets are trending higher which reduced capital losses from holding assets which may be losing value faster than the 
bot can make profits. Since a few of these exchanges no longer exists also shows that this strategy also subject to counter-party risk, meaning if a smaller exchange went down,
it may take your assets with it. Or if a wallet goes down there's no guarantee it will go back up again, meaning there's not guarantee that assets being traded on a centralized
exchange are backed by anything. Smaller, less known exchanges may have more opportunities, but also comes with risk.

Some of the code is painful to look at since this was developed from a proof-of-concept script I wrote that kept getting expanded with scope creep. There are many aspects I could
have written better, but this was capable to running for months on end and many thousands of successful trades so it was never a big priority. Much of the low hanging fruit from this strategy
has already been picked so it's not likely to be very successful anymore. I'm asked about this frequently enough as well as noticing so many exchanges this used to work on no 
longer exist that it seems fairly safe to post this, particularly since it's not capable of running as is.

Again, this is a very stripped down version of an old branch of this project. It may have some hardcoded values which don't make sense, but the last updates to the code were in 2019. I've moved on
to other strategies and keep this in the toolbox. Maybe others might get use from the ungodly number of hours I've put into writing, testing and improving this. 
