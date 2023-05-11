#1. Import Libraries
import os
import sys

from eulith_web3.erc20 import TokenSymbol
from eulith_web3.eulith_web3 import EulithWeb3
from eulith_web3.signing import LocalSigner, construct_signing_middleware

sys.path.insert(0, os.getcwd())
from utils.banner import print_banner
from utils.settings import *

#2. Fill the constructor
if __name__ == '__main__':
    print_banner()

    wallet = LocalSigner("<PRIVATE_KEY>")
    ew3 = EulithWeb3("https://eth-main.eulithrpc.com/v0", "<EULITH_REFRESH_TOKEN>", construct_signing_middleware(wallet))

#3. Check wallet's founds availability 
    if ew3.eth.get_balance(wallet.address) / 10 ** 18 < 0.008:
        print(f'Insufficient wallet balance to run the example. '
              f'Please send at least 0.01 ETH to {wallet.address} to continue')
        exit(1)

#4. Define transaction's token and amount
    weth = ew3.v0.get_erc_token(TokenSymbol.WETH)
    amount = 0.001

#5. Call Eulith's toolkit
    toolkit_address = ew3.v0.ensure_toolkit_contract(wallet.address)
    weth_toolkit_balance = weth.balance_of_float(toolkit_address)

#6. Check toolkit's founds availability, if True, transfert founds to the toolkit
    if weth_toolkit_balance < amount:
        print('The toolkit contract doesnt have sufficient WETH to demonstrate the withdraw. '
              f'Please send 0.001 WETH to {toolkit_address} to continue')
        exit(1)

#7. Open the atomic bundle    
    ew3.v0.start_atomic_transaction(wallet.address)
    approval_tx = weth.approve_float(wallet.address, amount)

#8. Append to the bundle
    ew3.eth.send_transaction(approval_tx)

#9. Close bundle and perform transaction
    atomic_tx = ew3.v0.commit_atomic_transaction()
    tx_hash = ew3.eth.send_transaction(atomic_tx)
    print(f'Approve wallet from the toolkit contract tx: {tx_hash.hex()}')
    ew3.eth.wait_for_transaction_receipt(tx_hash)

#10. Empty remaining balance
    withdraw_weth_from_toolkit_tx = weth.transfer_from_float(
        toolkit_address, wallet.address, amount, {'from': wallet.address, 'gas': 100000})
    tx_hash = ew3.eth.send_transaction(withdraw_weth_from_toolkit_tx)
    print(f'Withdraw tx: {tx_hash.hex()}')
