import json

def load_abi(contract_name):
    abi_path = f'./abis/{contract_name}.json'
    with open(abi_path, 'r') as abi_file:
        return json.load(abi_file)
