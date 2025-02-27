#1️⃣ Code for Both Incoming & Outgoing Transactions
import requests
import pandas as pd
import time

API_KEY = '7DNR18H7ASKXYSZNATBFRIPT4IZUDCNJ7U'
file_path = 'normalpart2.csv'  # Update if needed
df = pd.read_csv(file_path)

BASE_URL = 'https://api.etherscan.io/api'
data_list = []

def get_eth_transaction_data(address):
    """Fetch Ethereum transaction data (both incoming & outgoing)."""
    try:
        tx_url = f"{BASE_URL}?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}"
        response = requests.get(tx_url).json()

        if response.get('status') != '1':
            return None

        transactions = response.get('result', [])
        if not transactions:
            return None

        # Initialize total gas price
        total_gas_price = sum(int(tx['gasPrice']) / 1e9 for tx in transactions)  # Convert Wei to Gwei

        return {'Total Gas Price (Gwei)': total_gas_price}

    except Exception as e:
        print(f"⚠ Error fetching data for {address}: {e}")
        return None

# Process addresses
for count, address in enumerate(df['Address'].dropna().unique(), start=1):
    if count > 1633:  # Limit to 1633 addresses
        break

    try:
        eth_data = get_eth_transaction_data(address)
        if eth_data:
            data_list.append({'Address': address, **eth_data})

        if count % 10 == 0:
            print(f"Processed {count} addresses...")

    except Exception as e:
        print(f"⚠ Error processing address {address}: {e}")

    time.sleep(1)  # Avoid API rate limits

# Save results
df_results = pd.DataFrame(data_list)
df_results.to_csv('gas_price_total_incoming_outgoing.csv', index=False)

print("✅ Data retrieval complete. Results saved to 'gas_price_total_incoming_outgoing.csv'")



#2️⃣ Code for Only Outgoing Transactions

import requests
import pandas as pd
import time

API_KEY = '7DNR18H7ASKXYSZNATBFRIPT4IZUDCNJ7U'
file_path = 'normalpart2.csv'  # Update if needed
df = pd.read_csv(file_path)

BASE_URL = 'https://api.etherscan.io/api'
data_list = []

def get_eth_transaction_data(address):
    """Fetch Ethereum transaction data (only outgoing)."""
    try:
        tx_url = f"{BASE_URL}?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}"
        response = requests.get(tx_url).json()

        if response.get('status') != '1':
            return None

        transactions = response.get('result', [])
        if not transactions:
            return None

        # Initialize total gas price (only for outgoing transactions)
        total_gas_price = sum(int(tx['gasPrice']) / 1e9 for tx in transactions if tx['from'].lower() == address.lower())

        return {'Total Gas Price (Gwei)': total_gas_price}

    except Exception as e:
        print(f"⚠ Error fetching data for {address}: {e}")
        return None

# Process addresses
for count, address in enumerate(df['Address'].dropna().unique(), start=1):
    if count > 1633:  # Limit to 1633 addresses
        break

    try:
        eth_data = get_eth_transaction_data(address)
        if eth_data:
            data_list.append({'Address': address, **eth_data})

        if count % 10 == 0:
            print(f"Processed {count} addresses...")

    except Exception as e:
        print(f"⚠ Error processing address {address}: {e}")

    time.sleep(1)  # Avoid API rate limits

# Save results
df_results = pd.DataFrame(data_list)
df_results.to_csv('gas_price_total_outgoing.csv', index=False)

print("✅ Data retrieval complete. Results saved to 'gas_price_total_outgoing.csv'")