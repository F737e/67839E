import random
import itertools
from web3 import Web3
from eth_account import Account
from eth_utils.exceptions import ValidationError
import requests

# Enable Mnemonic features
Account.enable_unaudited_hdwallet_features()

def generate_mnemonic():
    wordlist_file = "wordlist.txt" 
    with open(wordlist_file, "r") as f:
        wordlist = f.read().splitlines()
    return " ".join(random.sample(wordlist, 12))

def check_account_validation(mnemonic, api_keys):
    try:
        private_key = Account.from_mnemonic(mnemonic)._private_key
        account = Account.from_key(private_key)
        address = account.address

        random.shuffle(api_keys)
        selected_keys = api_keys[:3]  # Select a random subset of 3 API keys

        for api_key in selected_keys:
            etherscan_url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&apikey={api_key}"
            response = requests.get(etherscan_url)
            result = response.json()

            if result["status"] == "1":
                return True  # Account exists, return True

        return False  # Account does not exist for any of the selected API keys
    except ValidationError:
        return False  # Return False if mnemonic is not valid

def check_account_balance(address, api_key):
    etherscan_url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&apikey={api_key}"
    response = requests.get(etherscan_url)
    result = response.json()
    balance = result["result"]
    return balance

def save_mnemonic(mnemonic, file_name):
    with open(file_name, "a") as f:
        f.write(mnemonic + "\n")

def main():
    api_keys = ["9GZY45Y32BDG7C4ECUBD5RYQ1Y42IM2GYM", "ZF2IAUQBXG4Q2E86BT59U8GBHBQNTBEMRF", "G5W25HC7AB9KMC96FVM5QDGYRZ4IHMVKNS"]  # Insert your Ethereum Scan API keys here
    non_zero_count = 0

    while True:
        # Generate a random mnemonic phrase
        mnemonic = generate_mnemonic()
        print("Generated Mnemonic:", mnemonic)

        # Check if the account associated with the mnemonic exists
        if check_account_validation(mnemonic, api_keys):
            # Save the mnemonic to a file for further processing
            save_mnemonic(mnemonic, "valid_mnemonics.txt")
            print("Mnemonic saved at valid_mnemonics.txt")

            # Retrieve the account address from the mnemonic
            private_key = Account.from_mnemonic(mnemonic)._private_key
            account = Account.from_key(private_key)
            address = account.address

            # Check the account balance for each API key
            random.shuffle(api_keys)
            selected_keys = api_keys[:3]  # Select a random subset of 3 API keys

            for api_key in selected_keys:
                balance = check_account_balance(address, api_key)
                print(f"Account Balance with API Key {api_key}: {balance}")

                # Save mnemonic to the recovery file if balance is non-zero
                if int(balance) > 0:
                    save_mnemonic(mnemonic, "recovery_phase.txt")
                    print("Mnemonic saved at recovery_phase.txt")
                    non_zero_count += 1
                    break

        print(f"Non-zero Count: {non_zero_count}")

if __name__ == "__main__":
    main()
