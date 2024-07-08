This project exists to prioritize which items to make market offers for,
given that there are a limited amount of offers that can be made. In essence, this is done by scoring the items in terms of the price differential
(between the highest bid and lowest ask) times the volume traded per unit of time. This score is effectively the expected profit per unit of time that would be obtained if you were buying at the top bid and selling at the lowest ask.

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

It is possible that the system and location parameters to the API don't do anything. This is not something that can be fixed from this side, but it is not a big deal anyway. Taking the overall regional market into account is a fine way to order the items.

Next is the file to score the items in terms of how good they are likely to be for merching/arbitrage.

`python rank_items.py`

#@@@ note that tax/fees/etc is not yet taken into account!!!

#@@@ note to open in excel and sort by the score?