#1. Import Libraries
import argparse
import os
import sys

from eulith_web3.eulith_web3 import EulithWeb3
from eulith_web3.exceptions import EulithRpcException
from eulith_web3.signing import LocalSigner, construct_signing_middleware

sys.path.insert(0, os.getcwd())
from utils.banner import print_banner
from utils.settings import *

#1.1 Set up the argparser
parser = argparse.ArgumentParser(
    prog='Test Send ETH to Wallet',
    description='Send ETH to a test wallet of your choosing.')

parser.add_argument('destination_wallet')

#2. Fill the constructor
if __name__ == '__main__':
    print_banner()

    wallet = LocalSigner("<PRIVATE_KEY>")
    ew3 = EulithWeb3("https://eth-main.eulithrpc.com/v0", "<EULITH_REFRESH_TOKEN>", construct_signing_middleware(wallet))

#4. Define destination wallet and amount
    args = parser.parse_args()
    destination = ''

    try:
        destination = ew3.toChecksumAddress(args.destination_wallet)
    except ValueError:
        print(f'Failed to parse {args.destination_wallet} as a valid Ethereum address')
        exit(1)

    amount_in_eth = 0.001

#3. Check wallet's founds availability
    if ew3.eth.get_balance(wallet.address) / 10 ** 18 < amount_in_eth + 0.002:  # we don't have enough ETH to complete the tx
        print(f'You have insufficient balance to run this example. Please fund the test wallet with '
              f'at least {amount_in_eth + 0.002} ETH')
        exit(1)

    print(f'Sending {amount_in_eth} ETH to: {destination}')

#9. Perform transaction
    try:
        tx_hash = ew3.eth.send_transaction({
            'from': wallet.address,
            'to': destination,
            'value': hex(int(amount_in_eth * 1e18))
        })

        print(f'Tx hash: {tx_hash.hex()}')
    except EulithRpcException:
        print('Looks like you dont have enough gas to complete this tx. Please fund the wallet a bit more.')
