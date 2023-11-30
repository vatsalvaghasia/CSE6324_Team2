// SPDX-License-Identifier: MIT 
pragma solidity 0.8.19;

contract D {
    function expectEmit(
        bool checkTopic1,
        bool checkTopic2,
        bool checkTopic3,
        bool checkData
    ) public{}

    event Transfer(address indexed addr1, address addr3, uint256 value);

    function f1(address addr1, address addr2, address addr3, uint value) public{
        expectEmit(false,false,true,true);
       emit Transfer(addr1,addr3,value);
    }   
}



