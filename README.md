This project exists to prioritize which items to make market offers for,
given that there are a limited amount of offers that can be made. In essence, this is done by scoring the items in terms of the price differential
between the asks and the bids, times the volume traded per unit of time. This score is effectively the expected profit per unit of time that would be obtained if you were buying near the top bid and selling near the lowest ask.

THIS IS NOT A PERFECT ESTIMATE. Why?
- The market can change at any moment
- You can (and will) get upper/under-cut on your offers

This uses the https://evetycoon.com/api to gather market data for items. Reference: https://evetycoon.com/docs

Note that each file may take > 1 hour to run.

First, there is a file to find valid item ids for the market. It's necessary to run this to
cut down on the amount of API requests that will need to be made. So run it first.
Most likely this will only need to be done once since what's valid in one region *should* be valid in another.

The file can be run as follows. There are optional cmdline arguments. You get their default values if you don't specify them. They are Jita focused.

`python find_valid_ids.py`

It is possible that the system and location parameters to the API don't do anything. This is not something that can be fixed from this side, but it is not a big deal anyway. Taking the overall regional market into account is a fine way to prioritize the items.

Next is the file to score the items in terms of how good they are likely to be for merching/arbitrage.
This requires that the file of valid ids be passed and it will query every one in the file.
There are some other optional cmdline arguments for changing the threshold for filtering out items with too few sells compared to buys,
as well as the broker fee percentage and tax percentage which may change depending on your skill levels or region of operation.
Double check that you are running with the values you expect in game.

`python rank_items.py --fileName <the file produced from find_valid_ids.py>`

The idea behind the volume ratio filter is that you don't want to be buying things you can't easily sell. At 0.1, there are 10 of the items bought in a buy order for every one sold in a sell order. Given not too much time you could sell an excess of inventory purchased.
The actual buy and sell prices are determined by the top 5% most competitive sell orders and top 5% most competitive buy orders. Tax and broker fee shrink this window into the *net* price differential.

Once the file is created, you'll want to open it in excel and sort the items from largest to smallest based on net cashflow. Now you have a prioritization over all items to consider for arbitrage/merching. Enjoy!