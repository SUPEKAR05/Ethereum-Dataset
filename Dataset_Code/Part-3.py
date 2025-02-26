
#Code For Retrieving Ethereum Addresses Data(Illicit & Non-Illicit)
#Part-3 Consist Of Attribute Releated To Gas Releated Attribute

import requests 
import pandas as pd 
import time 
# Your Etherscan API Key 
API_KEY = '7DNR18H7ASKXYSZNATBFRIPT4IZUDCNJ7U' 

# Load non-illicit Ethereum addresses dataset 

file_path = 'normalpart2.csv'  # Update this path if needed 
df = pd.read_csv(file_path) 

# Base Etherscan API URL 
BASE_URL = 'https://api.etherscan.io/api' 

# List to store results 

data_list = [] 

# Function to fetch Ethereum transaction data 

def get_eth_transaction_data(address): 

    try: 

        tx_url = f"{BASE_URL}?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}" 

        response = requests.get(tx_url).json() 

         

        if response.get('status') != '1': 

            return None 

         

        transactions = response.get('result', []) 

        if not transactions: 

            return None 

         

        # Initialize variables 

        gas_prices, gas_limits, gas_used, base_fees, timestamps = [], [], [], [], [] 

        success_count, failure_count = 0, 0 

         

        for tx in transactions: 

            gas_prices.append(int(tx['gasPrice']) / 1e9)  # Convert Wei to Gwei 

            gas_limits.append(int(tx['gas']) / 1e9) 

            gas_used.append(int(tx['gasUsed']) / 1e9) 

            timestamps.append(int(tx['timeStamp'])) 

             

            if 'maxFeePerGas' in tx: 

                base_fees.append(int(tx['maxFeePerGas']) / 1e9) 

             

            if tx['isError'] == '0': 

                success_count += 1 

            else: 

                failure_count += 1 

         

        # Compute statistics 

        transaction_frequency = (max(timestamps) - min(timestamps)) / 60 if len(timestamps) > 1 else None 

        gas_price_volatility = max(gas_prices) - min(gas_prices) if gas_prices else None 

        success_failure_ratio = success_count / failure_count if failure_count > 0 else success_count 

         

        return { 

            'Avg Gas Price (Gwei)': sum(gas_prices) / len(gas_prices) if gas_prices else None, 

            'Avg Gas Limit (Gwei)': sum(gas_limits) / len(gas_limits) if gas_limits else None, 

            'Avg Gas Used (Gwei)': sum(gas_used) / len(gas_used) if gas_used else None, 

            'Avg Base Fee (Gwei)': sum(base_fees) / len(base_fees) if base_fees else None, 

            'Transaction Frequency (min)': transaction_frequency, 

            'Gas Price Volatility (Gwei)': gas_price_volatility, 

            'Transaction Success-Failure Ratio': success_failure_ratio, 

        } 

    except Exception as e: 

        print(f"⚠ Error fetching transaction data for {address}: {e}") 

        return None 

 

# Loop through addresses and retrieve data 

count = 0 

for address in df['Address'].dropna().unique(): 

    if count >= 1633:  # Process up to 1000 addresses 

        break 

     

    try: 

        eth_data = get_eth_transaction_data(address) 

         

        if eth_data:  # Only add to data list if valid data is retrieved 

            data_list.append({'Address': address, **eth_data}) 

             

    except Exception as e: 

        print(f"⚠ Error processing address {address}: {e}") 

     

    count += 1 

    time.sleep(1)  # Avoid API rate limits 

 

# Convert results to DataFrame and save to CSV 

df_results = pd.DataFrame(data_list) 

df_results.to_csv('non_illicit_ethereum_data.csv', index=False) 

 

print("✅ Data retrieval complete. Results saved to 'non_illicit_ethereum_data.csv'") 

print(df_results) 
