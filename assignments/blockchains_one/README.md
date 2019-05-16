# [Blockchains and Cryptocurrencies](https://github.com/nocturnalbeast/assignments-n-stuff/tree/sem_two/assignments/blockchains_one) 

## Demonstration of Solidity contracts

### Contents

The assignment submission contains two folders:

* simple_bank - contains the Truffle project which has the Solidity contract for the SimpleBank example
* screenshots - contains the screenshots of the entire process

### Execution

Launch the development network:

`truffle develop`

This will start the development network with 10 different accounts.

Launch a different terminal and compile the contracts:

`truffle compile`

Then verify that there are no errors in compilation, and then deploy the contracts onto the development network:

`truffle migrate`

Then, run the included tests with:

`truffle test`