import random

'''
## Roll XdY dice

DnD-style, X being number of dices to roll, Y being face of dice
Available dices: 4, 6, 8, 10, 12, 20
Limit number of dices to 10
'''
def roll_dice(args):
    # Available dices: d4, d6, d8, d10, d12, d20
    dices = [4, 6, 8, 10, 12, 20]
    
    arglist = args.split('d')
    
    # Error handling, early escape strategy
    ## If wrong arglist length
    if len(arglist) != 2:
        return (0, f'Invalid argument!\nPlease use the format !roll XdY, where X is a number between 1-10 and dY is a valid dice: {dices}.')
    ## If x or y is not an integer
    for arg in arglist:
        if not arg.isdigit():
            return (0, f'Invalid argument!\nPlease use the format !roll XdY, where X is a number between 1-10 and dY is a valid dice: {dices}.')
        
    # Parse ints
    x = int(arglist[0])
    y = int(arglist[1])
    
    ## If invalid dice (invalid y)
    if y not in dices:
        return (0, f'Invalid dice!\nAvailable: {dices}')
    ## If invalid number of dices (invalid x)
    if x > 10 or x < 1:
        return (0, f'Invalid number of dices!\nInput a number between 1-10.')
    
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
def flip_coin(arg):
    # Error handling, early escape
    ## If arg is not an int
    if not arg.isdigit():
        return (0, 'Invalid argument!\nPlease use the format !flip X, where X is a number between 1-10')
    
    # Parse int
    x = int(arg)
    
    ## If invalid number of coins
    if x > 10 or x < 1:
        return (0, f'Invalid number of coins!\nInput a number between 1-10.')
    
    coinList = []
    
    for count in range(x):
        coinList.append(random.choice(["Heads", "Tails"]))
    
    return (1, coinList)

'''
## 8-Ball

Roll 8-ball once
'''
def eightball(arg):
    print("8Ball Function Called")
    eightball_options = ["It is certain",
                    "It is decidedly so",
                    "Without a doubt",
                    "Yes definitely",
                    "You may rely on it",
                    "As I see it, yes",
                    "Most likely",
                    "Outlook good",
                    "Yes",
                    "Signs point to yes",
                    "Reply hazy, try again",
                    "Ask again later",
                    "Better not tell you now",
                    "Cannot predict now",
                    "Concentrate and ask again",
                    "Don't count on it",
                    "My reply is no",
                    "My sources say no",
                    "Outlook not so good",
                    "Very doubtful"]

    if not arg or arg.strip() == '':
        return (0, "You cannot consult the 8-ball without a question!")

    else:
        return (1, random.choice(eightball_options))