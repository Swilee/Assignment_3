








#setup

pot = 0
NumberOfPlayers = int(input('Number of players'))
Playername=[None]*NumberOfPlayers
for i in range(0, NumberOfPlayers):
    Playername[i] = input('Player %d name' %(i+1))

print(type(Playername))
STARTINGSTACK = float(input('Set starting stack amount'))




ActivePlayers = NumberOfPlayers
