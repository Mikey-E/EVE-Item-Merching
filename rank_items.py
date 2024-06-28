# Author: Michael Elgin

import argparse
import requests
import pandas as pd
import time

#@@@ is possible that the system and location don't do anything

def rank_items(regionId, systemId, locationId, fileName, volumeRatioFilter=0.1):

    headers = {
        "regionId": str(regionId),
        "systemId" : str(systemId),
        "locationId" : str(locationId),
    }

    items = {
        'item': [],
        'net_cashflow': []
    }
    ids = []

    with open(fileName, "r") as f:
        for line in f:
            ids.append(int(line))

    for typeId in ids:
        # URL for the API endpoint
        stats_url = f"https://evetycoon.com/api/v1/market/stats/{regionId}/{typeId}"
        name_url = f"https://evetycoon.com/api/v1/market/orders/{typeId}"

        headers["typeId"] = str(typeId)

        # Make the GET request
        stats_response = requests.get(stats_url, headers=headers)
        name_response = requests.get(name_url, headers=headers)

        # Check if the request was successful
        if name_response.status_code == 200:
            # Process the JSON data
            data = name_response.json()
            name = data["itemType"]["typeName"]
        else:
            print(f"Failed to retrieve data: {name_response.status_code}")

        # Check if the request was successful
        if stats_response.status_code == 200:
            # Process the JSON data
            data = stats_response.json()
            buyVolume = data["buyVolume"]
            sellVolume = data["sellVolume"]
            buyAvgFivePercent = data["buyAvgFivePercent"]
            sellAvgFivePercent = data["sellAvgFivePercent"]
        else:
            print(f"Failed to retrieve data: {stats_response.status_code}")
        
        try:
            if sellVolume/buyVolume < volumeRatioFilter: #don't want to be buying stuff I can't sell
                continue
        except ZeroDivisionError:
            continue
        
        differential = sellAvgFivePercent - buyAvgFivePercent #@@@ might want to take into account tax/fees right here by modifying sellavg5
        netCashflow = differential * buyVolume # is diff * quantity, where buyVolume is the quantity here as long as it isn't too much under the sellVolume, as protected above by the set ratio.

        items['item'].append(name)
        items['net_cashflow'].append(netCashflow)

    return pd.DataFrame(items)

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Process minimum and maximum integers for item Id.")

    # Add arguments for minimum and maximum integers
    parser.add_argument('--region', type=int, default=10000002, help='Default region (default: the forge (where Jita is))')
    parser.add_argument('--system', type=int, default=30000142, help='Default system (default: Jita)')
    parser.add_argument('--location', type=int, default=60003760, help='Default location/station (default: Jita trade hub)')
    parser.add_argument('-f', '--fileName', type=str, required=True, help='file name for valid ids')

    # Parse the arguments
    args = parser.parse_args()

    # create the file of Ids
    start_time = time.time()
    ranked_items = rank_items(args.region, args.system, args.location, args.fileName)
    print(f"Took {time.time() - start_time:.3f} seconds")

    ranked_items.to_csv("ranked_items_region" + str(args.region) + "_system" + str(args.system) + "_location" + str(args.location)
                      + "_count" + str(ranked_items.shape[0]) + ".csv")

if __name__ == "__main__":
    main()