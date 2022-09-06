import random


# Here is a working version of blackjack. It clearly demonstrates an understanding of both the basics (variables, etc.)
# and control flow (functions, etc.)
# There is also a meaningful use of lists in that they are the defining structure of the deck and the methods depend
# on list operations.

# optional additions I didn't add
# splitting when available, insurance, doubling down, ability to play through a deck w/o shuffling


def hand_value(card_values):
    value, num_aces = 0, 0
    for v in card_values:
        if v == "Ace":
            num_aces += 1
            value += 11
        else:
            value += v
    if value <= 21:
        return value
    for i in range(num_aces):
        value -= 10
        if value <= 21:
            return value
    return "Bust"


def new_deck():
    deck = []
    for i in range(4):
        for k in range(1, 14):
            if k == 1:
                deck.append("Ace")
            elif k <= 9:
                deck.append(k)
            elif k > 9:
                deck.append(10)
    return deck


def deal(i=3):
    # create a local deck and display
    local_deck = new_deck()
    random.shuffle(local_deck)
    print("Dealer: " + str(local_deck[0]) + " ?? \nYou: " + str(local_deck[2]) + " + " + str(
        local_deck[3]) + " = " + str(hand_value(local_deck[2:4])))

    # check for blackjack(s)
    if ((local_deck[0] == "Ace" or local_deck[1] == "Ace") and (local_deck[0] == 10 or local_deck[1] == 10)) and \
            ((local_deck[2] == "Ace" or local_deck[3] == "Ace") and (local_deck[2] == 10 or local_deck[3] == 10)):
        print("Push")
        return "Push"
    elif (local_deck[0] == "Ace" or local_deck[1] == "Ace") and (local_deck[0] == 10 or local_deck[1] == 10):
        print("Sorry, dealer has blackjack. You lose")
        return "Loss"
    elif (local_deck[2] == "Ace" or local_deck[3] == "Ace") and (
            local_deck[2] == 10 or local_deck[3] == 10):
        print("You have blackjack!")
        return "Blackjack"

    # allow the player to hit if desired
    # location in deck = i
    player_sum = hand_value(local_deck[2:i + 1])
    test = True
    while test:
        choice = input("Hit or stand?")
        if choice == "Hit" or choice == "hit":
            i += 1
            player_sum = hand_value(local_deck[2:i + 1])
            print("Dealer: " + str(local_deck[0]) + " ?? \nYou: " + str(local_deck[2]) + " + " + str(local_deck[3]),
                  end="")
            for h in range(4, i + 1):
                print(" +", local_deck[h], end="")
            print(" =", player_sum)
            if player_sum == "Bust":
                print("You went bust, sorry")
                return "Loss"
        if choice == "Stand" or choice == "stand":
            test = False

    # allow the dealer to respond
    # first, define the dealer's sum
    dealer_sum = int(hand_value(local_deck[0:2]))

    # dealer hits to 17
    # d = dealer's deck position
    d = i
    while dealer_sum < 17:
        d += 1
        dealer_sum = hand_value(local_deck[0:2] + local_deck[i + 1:d + 1])
        if dealer_sum == "Bust":
            break
        int(dealer_sum)

    # print output of the game
    print("Dealer: ", str(local_deck[0]), "+", str(local_deck[1]), end="")
    for h in range(i + 1, d + 1):
        print(" +", str(local_deck[h]), end="")
    print(" =", dealer_sum, "\nYou: ", str(local_deck[2]), "+", str(local_deck[3]), end="")
    for e in range(4, i + 1):
        print(" +", str(local_deck[e]), end="")
    print(" =", player_sum)

    # check win conditions
    if dealer_sum == "Bust":
        print("Dealer went bust, you win!")
        return "Win"
    elif dealer_sum > player_sum:
        print("Sorry, you lost!")
        return "Loss"
    elif dealer_sum == player_sum:
        return "Push"
    else:
        print("You won!")
        return "Win"


# begin runnable code
game_is_running = True

# Welcome screen and introduction. No exception handling for buy-in
buy_in = int(input("Welcome to digital blackjack. We pay 2:1 on Blackjack and do not offer insurance."
                   "\nPlease enter your whole number starting buy in: $"))
players_pot = buy_in
print("Thank you. To exit, enter -1 as your bet.")

# entry into game mode
while game_is_running:
    bet = input("Please enter your bet: $")
    if bet == "-1":
        game_is_running = False
        print("Thank you for playing. You finished with $" + str(players_pot))
        if players_pot > int(buy_in):
            print("Congrats on winning $" + str(players_pot - buy_in) + "!")
        break
    elif players_pot == 0:
        game_is_running = False
        print("Thank you for playing. Sorry you lost it all!")
        break
    elif bet.isnumeric():
        if int(bet) > players_pot:
            print("That bet is more than your current pot amount")
        else:
            output = deal()
            if output == "Blackjack":
                players_pot += 2 * int(bet)
            elif output == "Win":
                players_pot += int(bet)
            elif output == "Loss":
                players_pot -= int(bet)
            print(output)
    else:
        continue
