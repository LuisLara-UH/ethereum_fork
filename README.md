## Development Assignment

For the Development Assignment, I implemented a local fork of the Ethereum network using Hardhat. This allowed me to replicate the mainnet environment for testing purposes. I developed the `AtomicSwaper.sol` contract, which encapsulates functionalities to deposit tokens, withdraw tokens, and execute an atomic swap. These functions were carefully designed to ensure secure and reliable interactions.

In my project structure, the contract code resides in the `contracts` folder. I also created a Python-based Brownie project to test the functionalities of the `AtomicSwaper` contract. The test file, `test_atomic_swap_contract.py`, was used to deploy the contract and validate its behavior. However, due to challenges in fully forking and simulating the actual tokens' behavior, I manually deployed the tokens required for testing. Additionally, I encountered difficulties deploying Uniswap and Sushiswap, which currently prevents a correct testing for the atomic swap method.

## EVM Challenge

In the EVM Challenge, I engaged in low-level Ethereum Virtual Machine (EVM) coding by manually creating bytecode to achieve specific functionality. I crafted an intricate piece of bytecode to execute mathematical operations based on input values. My bytecode effectively handled multiple scenarios, including returning 0 for input 0 and computing Fibonacci numbers for other inputs.

The crafted bytecode leverages various EVM opcodes, including `PUSH`, `DUP`, `SWAP`, and conditional jumps (`JUMPI`). This allowed me to construct complex control flow and arithmetic operations. This is the code:

```
// If input is 0, return 0
PUSH1 0x00 
PUSH1 0x00
CALLDATALOAD
DUP1
ISZERO
PUSH1 0x2c
JUMPI
// If input is 1, return 1
PUSH1 0x01
SWAP1
SUB
DUP1
ISZERO
PUSH1 0x2c
JUMPI
PUSH1 0x01
SWAP1
SUB
// Put the first two values on stack
PUSH1 0x01
PUSH1 0x00

// Loop for adding last two numbers
JUMPDEST
DUP2
ADD
DUP3
ISZERO
PUSH1 0x2c
JUMPI
PUSH1 0x01
DUP4
SUB
DUP2
DUP4
PUSH1 0x1b
JUMP

// Finish execution and return value at top
JUMPDEST
PUSH1 0x00
MSTORE
PUSH1 0x20
PUSH1 0x00
RETURN
```

## Solidity Assignment

For the Solidity Assignment, I delved into the analysis of a deployed smart contract to extract specific data encoded within its constructor. I began by extracting the contract ABI and using it to decode the input data of the contract creation transaction. I used this for decoding the input:

```python
contract = w3.eth.contract(address=contract_address, abi=abi)
constructor_inputs = contract.decode_function_input(calldata)
```

The result was:
```
[
'0x5260016000806101000a81548160ff0219169083151502179055504260015560',
'0x0a600260006101000a81548160ff021916908360ff16021790555060ff600260',
'0x016101000a81548160ff021916908360ff160217905550426002806101000a81'
]
```

By carefully examining the decoded input, I identified the crucial value stored at a particular position (`data[2][2]`).To further interpret this value, I transformed it into 16 bytes using a specific conversion process. The resulting value was 0x287936c44f499ef05be712da00399f12.

However, during the attempt to unlock the contract using this processed value via the `unlock.js` script(in the root of the project), I encountered an issue where the contract was reverting. Despite extensive debugging efforts, I was unable to pinpoint the root cause of this behavior.
