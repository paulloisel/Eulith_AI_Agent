const PORT = 8000
const express = require('express')
const cors = require('cors')
require('dotenv').config()
const app = express()
app.use(express.json())
app.use(cors())

const API_KEY = process.env.API_KEY

app.post('/completions', async (req, res) => {
    const options = {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${API_KEY}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            model: "gpt-3.5-turbo",
            messages: [
                {role: "user", content: "Learn the following.\nThe protocols powered by Eulith share common general steps. \nThose steps come in a standard format and should be adapted to each specific protocol.\nHere is a list of the diffreent steps. They must follow each other in the right order so that protocols are executed correctly.\n\nStep 1: Import Libraries consist in importing:\n- the os module to provide functions for interacting with the operating system\n- the sys module to access variables used or maintained by the interpreter\n- the Eulith packages (depending on the protocole you want to use and the operation you want to perform, different packages are necessary to access the required modules).\n\nStep 1 example START\nimport os\nimport sys\n\nfrom eulith_web3.eulith_web3 import *\nfrom eulith_web3.signing import construct_signing_middleware, LocalSigner\nStep 1 example END\n\nStep 2: Fill the Constructor:\n- choose an custody method to set up the adress of your wallet \n- creates the Eulith Web3 object (\"ew3\") with the EulithWeb3() function to on carry the protocol.\nStep 2 example START\nif __name__ == '__main__':\n    print_banner()\n\n    wallet = LocalSigner(\"<PRIVATE_KEY>\")\n    ew3 = EulithWeb3(\"https://eth-main.eulithrpc.com/v0\", \"<EULITH_REFRESH_TOKEN>\", construct_signing_middleware(wallet))\nStep 2 example END\n\nStep 3: Define transaction and its amounts:\n- define what tokens are involved in the transaction (the list of the available tokens is here: https://docs.eulith.com/v/hgbRx2t48xMLL5xhyh04/client-libraries/python/tokens)\n- define each token amounts and the total amount of the transaction\n- define the wallet or the wallets receivers adresses.\nStep 3 example START\n    weth = ew3.eulith_get_erc_token(TokenSymbol.WETH)\n        t1_send_amount = 0.0001\n        t2_send_amount = 0.0001\n        amount = t1_send_amount + t2_send_amount\n        t1_wallet_address = '<WALLET_ADRESS>'\n        t2_wallet_address = '<WALLET_ADRESS>'\nStep 3 example END\n\nStep 4: Check wallet's funds availability:\n- create a if-statement and check that the total amount of the tranasctions is lower than the wallet balance with the method get_balance()\n- if the total amount exceed the wallet balance, then print a message error and exit(1) for unsuccessful termination.\nStep 4 example START\n    if ew3.eth.get_balance(wallet.address) / 1e18 < amount + 0.003:\n            print(f'insufficient balance, deposit at least {amount + 0.002} ETH to perform operation')\n            exit(1)\nStep 4 example END\n\nThe Step 5,6, and 7 are optional for non-atomic transactions, but they are all required for atomic transaction.\n\nStep 5: Call and check funds availability in Eulith toolkit:\n- call the Eulith toolkit with the ensure_toolkit_contract() method, the method automatically checks if a toolkit already exist for this wallet\n- create a if-statement and check that the total amount of the tranasctions is lower than the toolkit balance with the balance_of_float() method\n- if the total amount exceed the toolkit balance, then wrap TokenSymbol from your wallet in a EulithERC20 format token with the deposit_eth() and send_transaction() methods and send it to the toolkit with the transfer_float() and send_transaction() methods.\nStep 5 example START\n    toolkit_address = ew3.v0.ensure_toolkit_contract(wallet.address)\n\n    if weth.balance_of_float(toolkit_address) < amount:\n        deposit_tx = weth.deposit_eth(amount, {'from': wallet.address, 'gas': 100000})\n        deposit_hash = ew3.eth.send_transaction(deposit_tx)\n        print(f'Converting ETH to WETH: {deposit_hash.hex()}')\n        ew3.eth.wait_for_transaction_receipt(deposit_hash)\n\n        transfer_to_toolkit_contract = weth.transfer_float(\n            toolkit_address, amount, {'from': wallet.address, 'gas': 100000})\n        transfer_hash = ew3.eth.send_transaction(transfer_to_toolkit_contract)\n        print(f'Sending enough WETH to the toolkit contract to cover the swap: {transfer_hash.hex()}')\n        ew3.eth.wait_for_transaction_receipt(transfer_hash)\nStep 5 example END\n\nStep 6: Open and append transactions to the atomic bundle\n- call the start_atomic_transaction() method to open the atomic bundle that is going to gather all the transactions you want to make\n- open a try-except-statement, include all the transactions you want to make in the try block with the send_transaction() method, in the except block, print a error message 'Error: Failed to execute transactions' and exit(1). \nStep 6 example START\n    ew3.v0.start_atomic_transaction(wallet.address)\n\n    try:\n        ew3.eth.send_transaction({'from': wallet.address,\n                                  'to': t1_wallet_address,\n                                  'value': hex(int(t1_send_amount * 1e18))})\n        ew3.eth.send_transaction({'from': wallet.address,\n                                  'to': t2_wallet_address,\n                                  'value': hex(int(t2_send_amount * 1e18))})\n    except Exception as e:\n        print(\"Error: Failed to execute transactions:\", str(e))\n        exit(1)\nStep 6 example END\n\nStep 7: Close bundle\n- open a try-except-statement, in the try block, call the commit_atomic_transaction() method to close the bundle, you won't be able to had new transactions in the atomic transaction after that, in the except block print a error message 'Failed to commit atomic transaction' and exit(1).\nStep 7 example START\n    try:\n        atomic_tx = ew3.v0.commit_atomic_transaction()\n    except Exception as e:\n        print(\"Error: Failed to commit atomic transaction:\", str(e))\n        exit(1)\nStep 7 example END\n\nStep 8 and 9 are required for every protocols.\n\nStep 8: Perform transaction:\n- open a try-except-statement, in the try block, call the send_transaction() method with the commit object as an argument, also call the wait_for_transaction_receipt() method to get the receipt of the transaction, in the except block, print a error message 'Transaction not found in the chain after 120 seconds. Try the atomic transaction again.' and exit(1).\nStep 8 example START\n    try:\n        tx_hash = ew3.eth.send_transaction(atomic_tx)\n        receipt = ew3.eth.wait_for_transaction_receipt(tx_hash)\n        print(f\"\\nTransaction hash: {receipt['transactionHash'].hex()}\")\n    except web3.exceptions.TimeExhausted:\n        print(\"Error: Transaction not found in the chain after 120 seconds. Try the atomic transaction again.\")\n        exit(1)\nStep 8 example END\n\nStep 9: Empty remaining balance:\n- do not forget to withdraw the remaining founds from the toolkit wit the transfer_from_float() and send_transaction() methods.\nStep 9 example START\n    withdraw_weth_from_toolkit_tx = weth.transfer_from_float(\n        toolkit_address, wallet.address, amount, {'from': wallet.address, 'gas': 100000})\n    tx_hash = ew3.eth.send_transaction(withdraw_weth_from_toolkit_tx)\n    print(f'Withdraw tx: {tx_hash.hex()}')\nStep 9 example END"},
                {role: "user", content: req.body.message}
            ]
        })
    }
    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', options)
        const data = await response.json()
        res.send(data)
    } catch(error) {
        console.error(error)
    }
})


app.listen(PORT, () => console.log('Your server is running on PORT ' + PORT))