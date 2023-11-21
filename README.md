### WELCOME!

If you enter this file it may be for curiosity or finding out who we are. We are the Prickly Port Pirates! (PPP) A starting team which is surfacing to the networks to complete tasks and be one step closer of gettig the "One Piece". Through their computer network advetures they will gain strenght and reach the "Wired Blue". 

It is said that the One Piece can be found through exploring networks and between all only the most experiences can enter the Wired Blue network. Would this team be able to get the an A-pass through their computer networks class to chace the One Piece? Stay tuned to find out!

## Running the Main code:
1. run:
```bash
pip install scikit-learn
pip install matplotlib
```
2. run the "generate_genesis.py" file to create the blockchain. (this will add the genesis block to the blockchain.json file.)
3. Open up the "BlockChain Code" folder
4. run the "RunEnterprises.bat" file to get both Enterprises running on two terminals.
5. Start chatting between terminals!

## Running the trials for spam messaging & graphing:
1. Make sure both peers are ready to message each other
2. choose one terminal and type in the following
```bash
   spam [number_of_messages] [duration_of_time]
```
3. After running these the csv files will be fille with information to be able to use TimeGraph.py
4. Open TimeGraph.py  (made for graphing and data collection therefore the code has to be hardcoded)
5. Modify P2PGraph so that the parameter matches the number of entries in the csv file. (at the bottom of the code)
``` bash
   graph = P2PGraph(number_of_data_collected)
```
