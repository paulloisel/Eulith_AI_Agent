#1. Import Libraries
import os
import sys

from eulith_web3.eulith_web3 import *
from eulith_web3.signing import construct_signing_middleware, LocalSigner

sys.path.insert(0, os.getcwd())
from utils.settings import PRIVATE_KEY, EULITH_REFRESH_TOKEN
from utils.banner import print_banner

#2. Fill constructor
if __name__ == '__main__':
    print_banner()

    wallet = LocalSigner("<PRIVATE_KEY>")
    ew3 = EulithWeb3("https://eth-main.eulithrpc.com/v0", "<EULITH_REFRESH_TOKEN>", construct_signing_middleware(wallet))

#3. Define transaction's tokens and amount

    weth = ew3.eulith_get_erc_token(TokenSymbol.WETH)
    t1_send_amount = 0.0001
    t2_send_amount = 0.0001
    amount = t1_send_amount + t2_send_amount
    t1_wallet_address = '0xFc11E697f23E5CbBeD3c59aC249955da57e57672'
    t2_wallet_address = '0x47256A41027e94d1141Dd06f05DcB3ddE0421551'

#4. Check wallet's funds' availability

    if ew3.eth.get_balance(wallet.address) / 1e18 < amount + 0.003:
        print(f'insufficient balance, deposit at least {amount + 0.002} ETH to perform operation')
        exit(1)

#5. Call and check funds availability in Eulith toolkit
    toolkit_address = ew3.v0.ensure_toolkit_contract(wallet.address)

    if weth.balance_of_float(toolkit_address) < amount:
        deposit_tx = weth.deposit_eth(amount, {'from': wallet.address, 'gas': 100000})
        deposit_hash = ew3.eth.send_transaction(deposit_tx)
        print(f'Converting ETH to WETH: {deposit_hash.hex()}')
        ew3.eth.wait_for_transaction_receipt(deposit_hash)

        transfer_to_toolkit_contract = weth.transfer_float(
            toolkit_address, amount, {'from': wallet.address, 'gas': 100000})
        transfer_hash = ew3.eth.send_transaction(transfer_to_toolkit_contract)
        print(f'Sending enough WETH to the toolkit contract to cover the swap: {transfer_hash.hex()}')
        ew3.eth.wait_for_transaction_receipt(transfer_hash)
    
#6. Open the atomic bundle
    ew3.v0.start_atomic_transaction(wallet.address)

    try:
        ew3.eth.send_transaction({'from': wallet.address,
                                  'to': t1_wallet_address,
                                  'value': hex(int(t1_send_amount * 1e18))})
        ew3.eth.send_transaction({'from': wallet.address,
                                  'to': t2_wallet_address,
                                  'value': hex(int(t2_send_amount * 1e18))})
    except Exception as e:
        print("Error: Failed to execute transactions:", str(e))
        exit(1)
#7. Close bundle
    try:
        atomic_tx = ew3.v0.commit_atomic_transaction()
    except Exception as e:
        print("Error: Failed to commit atomic transaction:", str(e))
        exit(1)


#8. Perform transaction
    try:
        tx_hash = ew3.eth.send_transaction(atomic_tx)
        receipt = ew3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"\nTransaction hash: {receipt['transactionHash'].hex()}")
    except web3.exceptions.TimeExhausted:
        print("Error: Transaction not found in the chain after 120 seconds. Try the atomic transaction again.")
        exit(1)

#9. Empty remaining balance
    withdraw_weth_from_toolkit_tx = weth.transfer_from_float(
        toolkit_address, wallet.address, amount, {'from': wallet.address, 'gas': 100000})
    tx_hash = ew3.eth.send_transaction(withdraw_weth_from_toolkit_tx)
    print(f'Withdraw tx: {tx_hash.hex()}')