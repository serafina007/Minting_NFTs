from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

# Avalanche Fuji Testnet RPC
RPC_URL = "https://api.avax-test.network/ext/bc/C/rpc"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Add middleware for Proof of Authority
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Your wallet private key and address
PRIVATE_KEY = "0xf1ff44546f17e475e08a84b47a88332975f7b179cf9b1f6871800113d078d610"  # <- your private key
ADDRESS = w3.eth.account.from_key(PRIVATE_KEY).address

# Contract info
CONTRACT_ADDRESS = "0x85ac2e065d4526FBeE6a2253389669a12318A412"

# Load ABI (paste the full ABI JSON as a string)
with open("nft_abi.json", "r") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# Create claim transaction
nonce = w3.eth.get_transaction_count(ADDRESS)
tx = contract.functions.claim(1234).build_transaction({
    'from': ADDRESS,
    'nonce': nonce,
    'gas': 300000,
    'gasPrice': w3.to_wei('25', 'gwei')
})

# Sign and send
signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

print("Transaction sent:", tx_hash.hex())
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Minted NFT successfully!", receipt)
