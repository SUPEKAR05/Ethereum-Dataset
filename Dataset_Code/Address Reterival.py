#Code For Retrieving Addresses For Both Illict And Non Illict

import requests 
import pandas as pd 
import time 

 

# Your Etherscan API Key 

API_KEY = '7DNR18H7ASKXYSZNATBFRIPT4IZUDCNJ7U' 

 

# Base Etherscan API URL 

BASE_URL = "https://api.etherscan.io/api" 

 

# Known illicit Ethereum addresses (source: Ethereum Scam Database) 

ILLICIT_ADDRESSES_URL = "https://raw.githubusercontent.com/MyCryptoHQ/scamdb/master/src/addresses.json" 

 

# Function to fetch Ethereum addresses from recent transactions 

def get_recent_addresses(): 

    url = f"{BASE_URL}?module=proxy&action=eth_blockNumber&apikey={API_KEY}" 

    response = requests.get(url).json() 

     

    if "result" not in response: 

        print("⚠ Error fetching latest block number") 

        return [] 

 

    latest_block = int(response["result"], 16) 

 

    addresses = set() 

     

    for block in range(latest_block, latest_block - 5000, -1):  # Checking last 5000 blocks 

        block_url = f"{BASE_URL}?module=proxy&action=eth_getBlockByNumber&tag={hex(block)}&boolean=true&apikey={API_KEY}" 

        response = requests.get(block_url).json() 

         

        if "result" in response and response["result"] and "transactions" in response["result"]: 

            for tx in response["result"]["transactions"]: 

                if tx["from"]:  # Ensure address is valid 

                    addresses.add(tx["from"].lower()) 

                if tx["to"]: 

                    addresses.add(tx["to"].lower()) 

         

        if len(addresses) >= 2500:  # Collect more than 1000 to filter out illicit ones 

            break 

         

        time.sleep(0.2)  # Avoid rate limits 

     

    return list(addresses) 

 

# Function to get known illicit addresses 

def get_illicit_addresses(): 

    try: 

        response = requests.get(ILLICIT_ADDRESSES_URL) 

        if response.status_code == 200: 

            return set(addr.lower() for addr in response.json() if addr)  # Ensure no None values 

    except Exception as e: 

        print(f"⚠ Error fetching illicit addresses: {e}") 

    return set() 

 

# Retrieve addresses 

print("Fetching recent Ethereum addresses...") 

all_addresses = get_recent_addresses() 

 

# Retrieve illicit addresses 

print("Fetching known illicit addresses...") 

illicit_addresses = get_illicit_addresses() 

 

# Ensure all_addresses is not empty 

if not all_addresses: 

    print("⚠ No addresses fetched. Exiting.") 

    exit() 

 

# Filter out illicit addresses 

non_illicit_addresses = [addr for addr in all_addresses if addr and addr not in illicit_addresses] 

 

# Save 1000 non-illicit addresses 

df = pd.DataFrame(non_illicit_addresses[:2000], columns=["Ethereum Address"]) 

df.to_csv("non_illicit_ethereum_addresses.csv", index=False) 

 

print("✅ 1000 non-illicit Ethereum addresses saved to non_illicit_ethereum_addresses.csv")
