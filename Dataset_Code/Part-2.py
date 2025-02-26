
#Code For Retrieving Ethereum Addresses Data(Illicit & Non-Illicit)
#Part-2 Consist Of Attribute Releated To ERC20 Tokens

import requests 
import pandas as pd 
import time 

# Your Etherscan API Key 
API_KEY = '7DNR18H7ASKXYSZNATBFRIPT4IZUDCNJ7U' 

# Load non-illicit Ethereum addresses dataset 
file_path = 'non_illicit_ethereum_addresses.csv'  # Update this path if needed 
df = pd.read_csv(file_path) 

# Base Etherscan API URL 
BASE_URL = 'https://api.etherscan.io/api' 

# List to store results 
data_list = [] 

# Function to get Ethereum balance 
def get_eth_balance(address): 
    try:
        balance_url = f"{BASE_URL}?module=account&action=balance&address={address}&tag=latest&apikey={API_KEY}"
        response = requests.get(balance_url).json()
        
        if response.get('status') != '1': 
            return None 
        
        return int(response['result']) / (10**18)  # Convert from Wei to Ether 
    except Exception as e:
        print(f"⚠ Error fetching balance for {address}: {e}") 
        return None 

# Function to get ERC-20 transaction data 
def get_erc20_transaction_data(address): 
    try:
        erc20_url = f"{BASE_URL}?module=account&action=tokentx&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}"
        response = requests.get(erc20_url).json()

        if response.get('status') != '1': 
            return None 

        transactions = response.get('result', [])

        # Initialize variables 
        received_values, sent_values, timestamps_sent, timestamps_received = [], [], [], [] 
        sent_tokens, received_tokens = {}, {} 
        sent_addresses, received_addresses = set(), set() 

        for tx in transactions: 
            value = int(tx['value']) / (10**18)  # Convert from Wei to Ether 
            timestamp = int(tx['timeStamp']) 
            token_name = tx['tokenName'] 

            if tx['from'].lower() == address.lower(): 
                sent_values.append(value) 
                timestamps_sent.append(timestamp) 
                sent_addresses.add(tx['to'].lower()) 
                sent_tokens[token_name] = sent_tokens.get(token_name, 0) + value 
            
            elif tx['to'].lower() == address.lower(): 
                received_values.append(value) 
                timestamps_received.append(timestamp) 
                received_addresses.add(tx['from'].lower()) 
                received_tokens[token_name] = received_tokens.get(token_name, 0) + value 

        # Calculate statistics 
        time_diff = (max(timestamps_sent + timestamps_received) - min(timestamps_sent + timestamps_received)) / 60 if timestamps_sent or timestamps_received else None 
        avg_time_between_sent = sum(timestamps_sent[i] - timestamps_sent[i-1] for i in range(1, len(timestamps_sent))) / len(timestamps_sent) / 60 if len(timestamps_sent) > 1 else None 
        avg_time_between_received = sum(timestamps_received[i] - timestamps_received[i-1] for i in range(1, len(timestamps_received))) / len(timestamps_received) / 60 if len(timestamps_received) > 1 else None 

        most_sent_token = max(sent_tokens, key=sent_tokens.get, default=None) 
        most_received_token = max(received_tokens, key=received_tokens.get, default=None) 

        return { 
            'Total ERC20 Transactions': len(transactions), 
            'ERC20 Total Ether Received': sum(received_values), 
            'ERC20 Total Ether Sent': sum(sent_values), 
            'ERC20 Unique Sent Addresses': len(sent_addresses), 
            'ERC20 Unique Received Addresses': len(received_addresses), 
            'ERC20 Avg Time Between Sent Txn (min)': avg_time_between_sent, 
            'ERC20 Avg Time Between Received Txn (min)': avg_time_between_received, 
            'ERC20 Min Value Received': min(received_values, default=None), 
            'ERC20 Max Value Received': max(received_values, default=None), 
            'ERC20 Avg Value Received': sum(received_values) / len(received_values) if received_values else None, 
            'ERC20 Min Value Sent': min(sent_values, default=None), 
            'ERC20 Max Value Sent': max(sent_values, default=None), 
            'ERC20 Avg Value Sent': sum(sent_values) / len(sent_values) if sent_values else None, 
            'ERC20 Unique Sent Token Names': len(sent_tokens), 
            'ERC20 Unique Received Token Names': len(received_tokens), 
            'ERC20 Most Sent Token Type': most_sent_token, 
            'ERC20 Most Received Token Type': most_received_token, 
            'Total Ether Balance': get_eth_balance(address), 
            'Time Diff Between First and Last Txn (min)': time_diff, 
        } 
    except Exception as e: 
        print(f"⚠ Error getting ERC20 transactions for {address}: {e}") 
        return None 

# Loop through addresses and retrieve data 
count = 0 
for address in df['Ethereum Address'].dropna().unique(): 
    if count >= 1000:  # Process up to 1000 addresses 
        break 
    try: 
        eth_data = get_erc20_transaction_data(address) 
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
