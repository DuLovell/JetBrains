import random
user_name = input('Enter your name: ')
player_rating = 0
print('Hello, {0}'.format(user_name))
with open('rating.txt', 'r') as file_:
    for line in file_.readlines():
        if user_name in line:
            player_rating = int(line.split()[-1])
turns = input().split(',')
if turns == ['']:
    turns = ['rock', 'paper', 'scissors']
print("Okay, let's start")
while True:
    try:
        player_turn = input()
        defeated_by = []  # which results will defeat the player
        if player_turn == '!exit':
            print('Bye!')
            break
        elif player_turn == '!rating':
            print('Your rating: {0}'.format(player_rating))
        else:
            # Filling up defeated_by list
            for option in turns[turns.index(player_turn) + 1:]:
                defeated_by.append(option)
                if len(defeated_by) == (len(turns) - 1) // 2:
                    break
            else:
                for option2 in turns[:turns.index(player_turn)]:
                    defeated_by.append(option2)
                    if len(defeated_by) == (len(turns) - 1) // 2:
                        break
            
            computer_turn = turns[random.randint(0, len(turns) - 1)]

            if player_turn == computer_turn:
                print('There is a draw ({0})'.format(computer_turn))
                player_rating += 50
            elif computer_turn not in defeated_by:
                print('Well done. Computer chose {0} and failed'.format(computer_turn))
                player_rating += 100
            else:
                print('Sorry, but computer chose {0}'.format(computer_turn))
    except ValueError:
        print('Invalid input')
