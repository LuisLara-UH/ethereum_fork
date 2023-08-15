// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";
import '@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router01.sol';
import "solmate/src/auth/Owned.sol";

contract AtomicSwapContract is Owned {
    ISwapRouter public constant uniswapRouter = ISwapRouter(0xE592427A0AEce92De3Edee1F18E0157C05861564);
    IUniswapV2Router01 public constant sushiSwapRouter = IUniswapV2Router01(0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F);
    address private USDC;
    address private USDT;
    address private WETH9;

    constructor(address _owner,
                address _usdc,
                address _usdt,
                address _weth9) 
                Owned(_owner) {
        USDC = _usdc;
        USDT = _usdt;
        WETH9 = _weth9;
    }
    
    function depositTokens(address token, uint256 amount) external onlyOwner {
        IERC20(token).transferFrom(msg.sender, address(this), amount);
    }
    
    function withdrawTokens(address token, uint256 amount) external onlyOwner {
        IERC20(token).transfer(owner, amount);
    }

    function withdrawEther(uint256 amount) external onlyOwner {
        require(amount <= address(this).balance, "Insufficient contract balance");
        payable(owner).transfer(amount);
    }

    function swapAndSend(address recipient) external payable {
        // Swap ETH to USDC on Uniswap
        uint256 amount = uniswapRouter.exactInputSingle{ value: msg.value }(
            ISwapRouter.ExactInputSingleParams(
                WETH9,
                USDC,
                3000,
                address(this),
                block.timestamp + 15,
                msg.value,
                1,
                0
        ));

        // Swap USDC to USDT on SushiSwap
        address[] memory pathUsdcToUsdt = new address[](2);
        pathUsdcToUsdt[0] = USDC;
        pathUsdcToUsdt[1] = USDT;
        IERC20(USDC).approve(address(sushiSwapRouter), amount);
        uint[] memory amountsUsdt = sushiSwapRouter.swapExactTokensForTokens(
            amount,
            0,
            pathUsdcToUsdt,
            address(this),
            block.timestamp + 120
        );
        uint256 usdtAmount = amountsUsdt[1];

        // Send output to external owned address
        require(!isContract(recipient), "Recipient must be an EOA");
        IERC20(USDT).transfer(recipient, usdtAmount);
    }

    function isContract(address _addr) internal view returns (bool) {
        uint256 size;
        assembly {
            size := extcodesize(_addr)
        }
        return size > 0;
    }
}
