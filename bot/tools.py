import random

'''
## Roll XdY dice

DnD-style, X being number of dices to roll, Y being face of dice
Available dices: 4, 6, 8, 10, 12, 20
Limit number of dices to 10
'''
def roll_dice(x, y):
    # Available dices: d4, d6, d8, d10, d12, d20
    dices = [4, 6, 8, 10, 12, 20]
    
    # Error handling, early escape strategy
    ## If invalid dice (invalid y)
    if y not in dices:
        return (0, f'Invalid dice! Available: {dices}')
    ## If invalid number of dices (invalid x)
    if x > 10 or x < 1:
        return (0, f'Invalid number of dices! Input a number between 1-10.')
    
    diceList = []
    
    for count in range(x):
        diceList.append(random.randint(1, y))
    
    # For debugging
    print(f'Dices rolled: {diceList}')

    return (1, diceList)
    
'''
## Coinflip

Flip X number of coins, either heads or tails
Limit number of coins to 10
'''
def flip_coin(x):
    # Error handling, early escape
    ## If invalid number of coins
    if x > 10 or x < 1:
        return (0, f'Invalid number of coins! Input a number between 1-10.')
    
    coinList = []
    
    for count in range(x):
        coinList.append(random.choice(["Heads", "Tails"]))
    
    return (1, coinList)

'''
## 8-Ball

Roll 8-ball once
'''
def eightball():
    eightball_options = []
    
    return (1, random.choice(eightball_options))