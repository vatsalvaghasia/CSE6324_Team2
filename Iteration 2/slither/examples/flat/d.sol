pragma solidity 0.8.19;

contract D {
    event Transfer(address indexed addr1, address addr2, address addr3, uint256 value);

    function f1(address addr1, address addr2, address addr3, uint256 value) public{
       emit Transfer(addr1,addr2,addr3,10);
    }
}



