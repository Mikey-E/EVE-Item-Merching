# Author: Michael Elgin

import argparse
import requests
import time

def create_valid_ids(minId, maxId, regionId, systemId, locationId):

    headers = {
        "regionId": str(regionId),
        "systemId" : str(systemId),
        "locationId" : str(locationId),
    }

    validIds = []

    for typeId in range(minId, maxId + 1):
        # URL for the API endpoint
        url = f"https://evetycoon.com/api/v1/market/stats/{regionId}/" + str(typeId)

        headers["typeId"] = str(typeId)

        # Make the GET request
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Process the JSON data
            data = response.json()
            if data["buyVolume"] != 0 or data["sellVolume"] != 0 or data["buyOrders"] != 0 or data["sellOrders"] != 0:
                validIds.append(typeId)
        else:
            print(f"Failed to retrieve data: {response.status_code}")
    return validIds

def make_file_from_ids(idList, regionId, systemId, locationId, minId, maxId):
    with open("valid_ids_region" + str(regionId) + "_system" + str(systemId) + "_location" + str(locationId)
                + "_min" + str(minId) + "_max" + str(maxId) + ".txt", "w") as f:
        f.write("\n".join(str(id) for id in idList))

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Process minimum and maximum integers for item Id.")

    # Add arguments for minimum and maximum integers
    parser.add_argument('--min', type=int, default=0, help='Minimum integer value (default: 0)')
    parser.add_argument('--max', type=int, default=100000, help='Maximum integer value (default: 100000)')
    parser.add_argument('--region', type=int, default=10000002, help='Default region (default: the forge (where Jita is))')
    parser.add_argument('--system', type=int, default=30000142, help='Default system (default: Jita)')
    parser.add_argument('--location', type=int, default=60003760, help='Default location/station (default: Jita trade hub)')

    # Parse the arguments
    args = parser.parse_args()

    # create the file of Ids
    start_time = time.time()
    ids = create_valid_ids(args.min, args.max, args.region, args.system, args.location)
    print(f"Took {time.time() - start_time:.3f} seconds")

    make_file_from_ids(ids, args.region, args.system, args.location, args.min, args.max)

if __name__ == "__main__":
    main()