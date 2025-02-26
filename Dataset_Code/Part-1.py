#Code For Retrieving Ethereum Addresses Data(Illicit & Non-Illicit)
#Part-1 Consist Of Attribute Releated To Transcation like min,max,avg,difference etc



import requests 
import pandas as pd 
import time 

# Your Etherscan API Key 
API_KEY = '7DNR18H7ASKXYSZNATBFRIPT4IZUDCNJ7U' 

# Load non-illicit Ethereum addresses dataset 

file_path = 'normaladdresss.csv'  # Update this path if needed 
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

        total_transactions = len(transactions) 

        received_values, sent_values = [], [] 

        received_timestamps, sent_timestamps = [], [] 

        received_from_addresses, sent_to_addresses = set(), set() 

         

        # Process transactions 

        for tx in transactions: 

            value = int(tx['value']) / (10**18)  # Convert from Wei to Ether 

            timestamp = int(tx['timeStamp']) 

             

            if tx['from'].lower() == address.lower(): 

                sent_values.append(value) 

                sent_timestamps.append(timestamp) 

                sent_to_addresses.add(tx['to']) 

            elif tx['to'].lower() == address.lower(): 

                received_values.append(value) 

                received_timestamps.append(timestamp) 

                received_from_addresses.add(tx['from']) 

         

        # Calculate time differences 

        time_diff_first_last = (max(received_timestamps + sent_timestamps) - min(received_timestamps + sent_timestamps)) / 60 if received_timestamps or sent_timestamps else None 

        avg_min_between_sent_tnx = (sum(sent_timestamps[i+1] - sent_timestamps[i] for i in range(len(sent_timestamps)-1)) / len(sent_timestamps)-1) / 60 if len(sent_timestamps) > 1 else None 

        avg_min_between_received_tnx = (sum(received_timestamps[i+1] - received_timestamps[i] for i in range(len(received_timestamps)-1)) / len(received_timestamps)-1) / 60 if len(received_timestamps) > 1 else None 

         

        # Calculate min, max, avg values 

        min_val_received = min(received_values) if received_values else None 

        max_val_received = max(received_values) if received_values else None 

        avg_val_received = sum(received_values) / len(received_values) if received_values else None 

        min_val_sent = min(sent_values) if sent_values else None 

        max_val_sent = max(sent_values) if sent_values else None 

        avg_val_sent = sum(sent_values) / len(sent_values) if sent_values else None 

        total_ether_sent = sum(sent_values) 

        total_ether_received = sum(received_values) 

        total_ether_balance = get_eth_balance(address) 

         

        return { 

            'Total Ether Balance': total_ether_balance, 

            'Total Transactions (including contract creation)': total_transactions, 

            'Time Difference First-Last (min)': time_diff_first_last, 

            'Avg Min Between Sent Tnx': avg_min_between_sent_tnx, 

            'Avg Min Between Received Tnx': avg_min_between_received_tnx, 

            'Sent Transactions': len(sent_values), 

            'Received Transactions': len(received_values), 

            'Unique Received From Addresses': len(received_from_addresses), 

            'Unique Sent To Addresses': len(sent_to_addresses), 

            'Min Value Received': min_val_received, 

            'Max Value Received': max_val_received, 

            'Avg Value Received': avg_val_received, 

            'Min Value Sent': min_val_sent, 

            'Max Value Sent': max_val_sent, 

            'Avg Value Sent': avg_val_sent, 

            'Total Ether Sent': total_ether_sent, 

            'Total Ether Received': total_ether_received 

        } 

     

    except Exception as e: 

        print(f"⚠ Error getting ERC20 transactions for {address}: {e}") 

        return None 

 

# Loop through addresses and retrieve data 

count = 0 

for address in df['Ethereum Address'].dropna().unique(): 

    if count >= 2000:  # Process up to 1000 addresses 

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
