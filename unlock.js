const { Web3 } = require('web3');
var Tx = require('ethereumjs-tx').Transaction;

// Connect to an Ethereum node
var web3 = new Web3('https://sepolia.infura.io/v3/709562f1d7a04802800f2e07204a131b');

const contractAddress = '0xA456f5b661C222E0e58Fd2133d365d6ac2d92F2e';
const contractABI = [
    {
        "inputs": [
        {
            "internalType": "bytes32[3]",
            "name": "_data",
            "type": "bytes32[3]"
        }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [
        {
            "internalType": "bytes16",
            "name": "_key",
            "type": "bytes16"
        }
        ],
        "name": "unlock",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "awkwardness",
        "outputs": [
        {
            "internalType": "uint16",
            "name": "",
            "type": "uint16"
        }
        ],
        "inputs": []
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "data",
        "outputs": [
        {
            "internalType": "bytes32[][]",
            "name": "",
            "type": "bytes32[][]"
        }
        ],
        "inputs": []
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "denomination",
        "outputs": [
        {
            "internalType": "uint8",
            "name": "",
            "type": "uint8"
        }
        ],
        "inputs": []
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "foo",
        "outputs": [
        {
            "internalType": "bytes32",
            "name": "",
            "type": "bytes32"
        }
        ],
        "inputs": []
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "locked",
        "outputs": [
        {
            "internalType": "bool",
            "name": "",
            "type": "bool"
        }
        ],
        "inputs": []
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "ID",
        "outputs": [
        {
            "internalType": "uint256",
            "name": "",
            "type": "uint256"
        }
        ],
        "inputs": []
    }
];

// The private key of the sender account
var privateKey = Buffer.from('I erased the private key here', 'hex');

// The value to unlock (bytes16 format)
const dataToUnlock = '0x287936c44f499ef05be712da00399f12';

const contract = new web3.eth.Contract(contractABI, contractAddress);

// Get the sender's account nonce
const senderAddress = '0x9E6159C2cE3c9e13c0B575F26377f57143f81AFd'; // Replace with the sender's address
var rawTx = {
    nonce: '0x00',
    gasPrice: '0x09184e72a000',
    gasLimit: 35000,
    from: senderAddress,
    to: contractAddress,
    value: '0x00',
    data: contract.methods.unlock(dataToUnlock).encodeABI()
    }

var tx = new Tx(rawTx, {'chainId': 11155111});
tx.sign(privateKey);

var serializedTx = tx.serialize();
web3.eth.sendSignedTransaction('0x' + serializedTx.toString('hex'))
    .on('transactionHash', hash => {
        console.log('Transaction Hash:', hash);
    })
    .on('receipt', receipt => {
        console.log('Transaction Receipt:', receipt);
    })
    .on('error', error => {
        console.error('Error:', error);
    });

