pragma solidity 0.8.19;

contract C {

    // Listing constants that are not be used
    uint256 constant uc1 = 10;
    uint256 uc2 = 15;

    // Listing constants that are used
    uint256 constant c1 = 10;

    function getconstantused() public view returns (uint256) {
        return c1;
    }
}

