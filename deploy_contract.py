from web3 import Web3
import requests

def init_web3():
    '''
    initialize web3 instance
    :return: web3 instance
    '''
    w3 = Web3(Web3.WebsocketProvider('wss://rinkeby.infura.io/ws/v3/800054c370de4aa7907af5b45273c7fd'))
    assert w3.isConnected(), '!! Attention !! The node is not connected !!!'
    return w3

def get_abi(address):
    '''
    get ABI of certain smart contract, marked by its address
    :param address: address of certain smart contract
    :return: abi for this contract
    '''
    # address = '0x60aE616a2155Ee3d9A68541Ba4544862310933d4'
    MAX_TRIAL = 5
    error_count = 0
    api_key = 'UCJ24GP9ICCR28QNPDNCXZ27VHWIG442F6'
    url = f'https://api-rinkeby.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={api_key}'
    while error_count < MAX_TRIAL:
        try:
            # print('Retrieving:', url.format(address=address, api_key=api_key))
            response = requests.get(url.format(address=address, api_key=api_key))
            if response.status_code == 200:
                json_response = response.json()
                if json_response['status'] == '1': # Valid data returned
                    return json_response['result']
                else:
                    error_count += 1
            else:
                error_count += 1
        except Exception as e:
            print('Error happened when asking for ABI', e)
            error_count += 1
    else:
        return ''

def init_contract(w3, address, abi_info) -> dict:
    '''
    initialize instance for certain smart contract
    :param w3: web3 instance
    :param address: address for this contract
    :param abi: abi for this contract
    :return: dict consisting of
        -- address: smart contract address
        -- abi: smart contract abi
        -- contract: smart contract instance
    '''
    # address = '0x9Ad6C38BE94206cA50bb0d90783181662f0Cfa10'
    single_contract = w3.eth.contract(address=w3.toChecksumAddress(address), abi=abi_info)
    return {
        'address': address,
        'abi': abi_info,
        'contract': single_contract
    }

def call_uploadData(contract, data_hash, price, description, gas, gasPrice, account, private_key):
    uploadData = contract.functions.uploadData(data_hash, price, description).buildTransaction(
        {
            'gas': gas,
            'gasPrice': w3.toWei(gasPrice, 'gwei'),
            'from': account,
            'nonce': w3.eth.getTransactionCount(account)
        }
    )
    signed_tx = w3.eth.account.sign_transaction(uploadData, private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(w3.toHex(tx_hash))

def call_purchaseData(contract, data_hash, gas, gasPrice, account, private_key):
    uploadData = contract.functions.purchaseData(data_hash).buildTransaction(
        {
            'gas': gas,
            'gasPrice': w3.toWei(gasPrice, 'gwei'),
            'from': account,
            'nonce': w3.eth.getTransactionCount(account)
        }
    )
    signed_tx = w3.eth.account.sign_transaction(uploadData, private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(w3.toHex(tx_hash))

w3 = init_web3()

# fulfill address info and abi info
address = '0x3b937e9741f51bebc17e9c3a1bad32ace4264e73'  # Deployed 
abi_info = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "data_hash",
				"type": "string"
			}
		],
		"name": "purchaseData",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "data_hash",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "price",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "description",
				"type": "string"
			}
		],
		"name": "uploadData",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

# initialize smart contract obj
certain_contract = init_contract(w3, address, abi_info)['contract']
list(certain_contract.functions)

# load public & private key
account = '0xc834E96DD8788Ce1702c589dd56cA7415a041177'  # Jason's account
# import configobj
# private_key = configobj.ConfigObj('.env')['key']
private_key = ''  # Jason's account

