import pytest
from brownie import AtomicSwapContract, accounts, Contract, Token, Wei
from brownie.convert import to_address
from abis.abi_utils import load_abi


@pytest.fixture(scope="module")
def usdt_token():
    # yield Contract.from_abi("USDT", to_address("0xdAC17F958D2ee523a2206206994597C13D831ec7"), load_abi("UsdtToken"))
    yield Token.deploy("USDT token", "USDT", 6, Wei("100 ether"), {'from': accounts[0], 'gas_price': '50 gwei'})

@pytest.fixture(scope="module")
def usdc_token():
    # yield Contract.from_abi("USDC", to_address("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"), load_abi("UsdcToken"))
    yield Token.deploy("USDC token", "USDC", 6, Wei("100 ether"), {'from': accounts[0], 'gas_price': '50 gwei'})

@pytest.fixture(scope="module")
def weth9_token():
    # yield Contract.from_abi("WETH9", to_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"), load_abi("Weth9Token"))
    yield Token.deploy("WETH9 token", "WETH9", 6, Wei("100 ether"), {'from': accounts[0], 'gas_price': '50 gwei'})

@pytest.fixture(scope="module")
def atomic_swap_contract(usdt_token, usdc_token, weth9_token):
    owner = accounts[0]
    return AtomicSwapContract.deploy(owner, usdc_token, usdt_token, weth9_token, {'from': owner, 'gas_price': '50 gwei'})

def test_deposit_tokens(atomic_swap_contract, usdt_token):
    owner = accounts[0]
    amount = 100

    initial_balance = usdt_token.balanceOf(atomic_swap_contract)
    usdt_token.approve(atomic_swap_contract, amount, {'from': owner, 'gas_price': '50 gwei'})
    atomic_swap_contract.depositTokens(usdt_token, amount, {'from': owner, 'gas_price': '50 gwei'})
    final_balance = usdt_token.balanceOf(atomic_swap_contract)

    assert final_balance - initial_balance == amount

def test_withdraw_tokens(atomic_swap_contract, usdt_token):
    owner = accounts[0]
    amount = 10 

    initial_balance = usdt_token.balanceOf(owner)
    atomic_swap_contract.withdrawTokens(usdt_token, amount, {'from': owner, 'gas_price': '50 gwei'})
    final_balance = usdt_token.balanceOf(owner)

    assert final_balance - initial_balance == amount

def test_swap_and_send(atomic_swap_contract, usdc_token, usdt_token, weth9_token):
    owner = accounts[0]
    recipient = accounts[1]
    initial_balance = usdt_token.balanceOf(recipient)
    
    eth_amount = Wei("1 ether")
    weth9_token.approve(atomic_swap_contract, eth_amount, {'from': owner, 'gas_price': '50 gwei'})
    tx = atomic_swap_contract.swapAndSend(recipient, {'from': owner, 'value': eth_amount, 'gas_price': '50 gwei'})

    final_balance = usdt_token.balanceOf(recipient)
    expected_balance_increase = final_balance - initial_balance
    
    assert expected_balance_increase > 0
    assert tx.return_value == expected_balance_increase
