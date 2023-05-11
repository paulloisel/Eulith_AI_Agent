#1. Import Libraries
import sys
import os

from eulith_web3.erc20 import TokenSymbol
from eulith_web3.eulith_web3 import EulithWeb3
from eulith_web3.requests import EulithShortOnRequest
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
# Why not doing this? In the swap example the wallet is check because the function
#'transfer_float(..) is used when checking the availability of teh founds in the toolkit
# L51 of Swap.py
#But here teh wallet is not checked even though transfer_float(..) L50 of this doc.
#What happen if the wallet doesn't have enough to transfert the collateral to the toolkit?

#4. Define short/collateral token and amount
    usdc = ew3.v0.get_erc_token(TokenSymbol.USDC)
    weth = ew3.v0.get_erc_token(TokenSymbol.WETH)

    collateral_amount = 5

    short_on_params = EulithShortOnRequest(
        collateral_token=usdc,
        short_token=weth,
        collateral_amount=collateral_amount)

#5. Call Eulith's toolkit
    toolkit_address = ew3.v0.ensure_toolkit_contract(wallet.address)

#6. Check toolkit's collateral availability    
    if usdc.balance_of_float(toolkit_address) < collateral_amount * 1.05:
        print('Funding the toolkit contract to prepare for the short...')
        transfer_collateral_to_contract = usdc.transfer_float(toolkit_address, collateral_amount * 1.05,
                                                              {'gas': 100000, 'from': wallet.address})
        ew3.eth.send_transaction(transfer_collateral_to_contract)

#7. Open the atomic bundle
    ew3.v0.start_atomic_transaction(account=wallet.address)

#8. Append to the bundle
    leverage = ew3.v0.short_on(short_on_params)

    print(f'Short leverage: {leverage}')

    # Example tx: https://etherscan.io/tx/0x836cc827e417c066c17bf92032fab0507172a9ac4ca030059bbe9d584804c222

#9. Close bundle and perform short
    tx = ew3.v0.commit_atomic_transaction()
    tx['gas'] = 1000000
    tx_hash = ew3.eth.send_transaction(tx)

    r = ew3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Short tx hash: {r["transactionHash"].hex()}')

#10. Empty remaining balance
    withdraw_weth_from_toolkit_tx = weth.transfer_from_float(
        toolkit_address, wallet.address, collateral_amount, {'from': wallet.address, 'gas': 100000})
    tx_hash = ew3.eth.send_transaction(withdraw_weth_from_toolkit_tx)
    print(f'Withdraw tx: {tx_hash.hex()}')
