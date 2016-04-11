"""
title::
    war

description::
    This file will perform 100000 and 1000000 simulations of the card game 
    War. It will shuffle and deal a 52 card deck between two players so that 
    each player has 26 cards in their respective hand. It will then begin
    playing the game. Following the rules of War, if the two players draw
    the same card during a battle, a "war" sequence starts. It will then count
    the number of war sequences that are played. Once the number of simulations
    have been reached the stats for the game are printed.

methods::
    shuffle_and_deal
        Creates a deck of 52 cards then shuffles and deals them to two players
        so that each player has 26 cards. The card numbers 11-14 represent
        Jacks, Queens, Kings, and Aces respectively.
        
    play
        Plays the game War. Each player puts down one card from the top of 
        their deck. The card with the highest number wins that "battle". If 
        both cards are equal to each other a war sequence starts. Once a player
        has all 52 cards the game is over.

    begin_war
        The players place down four cards each. The value of their fourth card
        determines the winner of the war (highest wins). If both cards are 
        equal to one another the process repeats until a winner is decided. If
        a player runs out of cards during the war, the other player is 
        considered the winner of the war.

author::
    Alex Perkins

copyright::
    Copyright (C) 2016, Rochester Institute of Technology

version::
    1.0.0

"""

import random

def shuffle_and_deal():

    """
    description::
        Creates a deck of 52 cards then shuffles and deals them to two players
        so that each player has 26 cards. The card numbers 11-14 represent
        Jacks, Queens, Kings, and Aces respectively.

    returns::
        player1Hand
            (list of integers) Player 1's hand of the 26 cards dealt to them

        player2Hand
            (list of integers) Player 2's hand of the 26 cards dealt to them
    """
    
    player1Hand = []
    player2Hand = []
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4

    # Shuffle the deck
    random.shuffle(deck)

    # Deal cards to each player
    for card in range(int(len(deck)/2)):
        player1Hand.append(deck.pop(0))
        player2Hand.append(deck.pop(0))

    return player1Hand, player2Hand


def play(player1Hand, player2Hand):

    """
    description::
        Plays the game War. Two players put down one card from the top of their
        deck. The card with the highest number wins that "battle". If the two
        cards are equal to each other a "war" sequence starts. When the war 
        sequence is complete the regular "battles" continue. Once a player has
        all 52 cards the game is over and that player wins.

    attributes::
        player1Hand
            (list of integers) Player 1's hand of 26 cards with values ranging
            from 2-14

        player2Hand
            (list of integers) Player 2's hand of 26 cards with values ranging
            from 2-14

    returns::
        winner
            (integer) The winner of the game. Either 1 or 2 representing 
            Player 1 or Player 2.

        numBattles
            (integer) The number of battles that took place during the game.
            Each war sequence is considered a battle

        numWars
            (integer) The number of wars that took place during the game.

        warHistogram
            (list of integers) Consists of six integers. Each number represents
            how many war sequences occurred in the game:
            0th position: 1-war sequence
            1st position: 2-war sequence
            2nd position: 3-war sequence
            3rd position: 4-war sequence
            4th position: 5-war sequence
            5th position: 6-war sequence
    """
   
    player1 = 1
    player2 = 2
    winner = 0
    numBattles = 0
    warHistogram = [0]*6

    while True:

        # Check which player wins the game
        if len(player1Hand) == 52:
            winner = player1
            break
        elif len(player2Hand) == 52:
            winner = player2
            break
        
        # Players begin a battle, each laying down a card
        winningDeck = []
        winningDeck.append(player1Hand.pop(0))
        winningDeck.append(player2Hand.pop(0))
        numBattles += 1

        # Check if Player 1's card value is greater than Player 2's card value
        if winningDeck[0] > winningDeck[1]:
            random.shuffle(winningDeck)
            player1Hand.extend(winningDeck)
        
        # Begin war sequence if both cards are equal
        elif winningDeck[0] == winningDeck[1]:
            player1Hand, player2Hand, numBattles, warHistogram = \
            begin_war(player1Hand, player2Hand, winningDeck, numBattles,\
            warHistogram)

        # Player 2 wins the battle if other checks are not met
        else:
            random.shuffle(winningDeck)
            player2Hand.extend(winningDeck)
    
    # Count number of wars that occurred during the game. Multipliers are added
    # to account for the fact that double wars and above are two wars or more
    # for each value.
    numWars = warHistogram[0] + warHistogram[1]*2 + warHistogram[2]*3 + \
              warHistogram[3]*4 + warHistogram[4]*5 + warHistogram[5]*6

    return winner, numBattles, numWars, warHistogram


def begin_war(player1Hand, player2Hand, winningDeck, numBattles, warHistogram):

    """
    description::
        Starts a war sequence. Both players put down four cards from the top of
        their decks. The value of the fourth card determines the winner of the
        war. Whichever card has the highest value, the player that put down
        that card wins the war. If the fourth cards equal each other another 
        war sequence begins until a winner is determined. Only up to six wars
        can be played in this version of war. If a player runs out of cards
        during a war sequence, the other player is determined the winner of the
        war sequence.

    attributes::
        player1Hand
            (list of integers) Player 1's hand of cards. Values of cards range
            from 2-14.

        player2Hand
            (list of integers) Player 2's hand of cards. Values of cards range
            from 2-14.
    
        winningDeck
            (list of integers) The deck that both players place cards into 
            during a battle. 

        numBattles
            (integer) The number of battles that occurred before the start of 
            the war sequence. Wars are counted as battles.

        warHistogram
            (list of integers) Consists of six integers. Each number represents
            how many war sequences occurred in the game:
            0th position: 1-war sequence
            1st position: 2-war sequence
            2nd position: 3-war sequence
            3rd position: 4-war sequence
            4th position: 5-war sequence
            5th position: 6-war sequence

    returns::
        player1Hand
            (list of integers) Player 1's hand of cards. Value of cards range
            from 2-14
        
        player2Hand
            (list of integers) Player 2's hand of cards. Value of cards range
            from 2-14

        numBattles
            (integer) The number of battles that occurred during the war 
            sequence. A war is considered a battle

        warHistogram
            (list of integers) Consists of six integers. Each number represents
            how many war sequences occurred in the game:
            0th position: 1-war sequence
            1st position: 2-war sequence
            2nd position: 3-war sequence
            3rd position: 4-war sequence
            4th position: 5-war sequence
            5th position: 6-war sequence
    """
    
    warSequence = 0
    continueWar = True

    while continueWar:

        numBattles += 1

        # Players lay down 4 cards
        for i in range(4):
            try:
                winningDeck.append(player1Hand.pop(0))
                winningDeck.append(player2Hand.pop(0))

            # If a player runs out of cards the other player wins the war
            except IndexError:
                random.shuffle(winningDeck)
                if len(player1Hand) == 0:
                    player2Hand.extend(winningDeck)
                else:
                    player1Hand.extend(winningDeck)

                # If six war sequences have occurred, the war ends
                if warSequence > 5:
                    return player1Hand, player2Hand, numBattles, warHistogram
                else:
                    warHistogram[warSequence] += 1
                    return player1Hand, player2Hand, numBattles,  warHistogram

        # Check if Player 1's 4th card is of greater value than Player 2's 4th
        # card
        if winningDeck[-2] > winningDeck[-1]:
            random.shuffle(winningDeck)
            player1Hand.extend(winningDeck)
            warHistogram[warSequence] += 1
            continueWar = False
            break

        # Check if Player 2's 4th card is of greater value than Player 1's 4th
        # card
        elif winningDeck[-2] < winningDeck[-1]:
            random.shuffle(winningDeck)
            player2Hand.extend(winningDeck)
            warHistogram[warSequence] += 1
            continueWar = False
            break

        # Continues war sequence if both of the 4th cards are equal to each 
        # other
        else:
            warSequence += 1

    return player1Hand, player2Hand, numBattles,  warHistogram


if __name__ == '__main__':

    import os
    import time
    from operator import add

    simulations = [100000, 1000000]

    for games in simulations:

        winnerStat = {1:0, 2:0}
        numBattlesStat = 0
        numWarsStat = 0
        warHistogramStat = [0] * 6

        start = time.time()
        for i in range(games):

            print('Simulating {0} games... {1:.2f}% complete'\
                  .format(games, (i/games)*100), end='\r')

            player1Hand, player2Hand = shuffle_and_deal()
            winner, numBattles, numWars, warHistogram = play(player1Hand,\
                                                             player2Hand)
            winnerStat[winner] += 1
            numBattlesStat += numBattles
            numWarsStat += numWars
            warHistogramStat = list(map(add, warHistogramStat, warHistogram))

        elapsedTime = time.time() - start
        print('\nPlayer 1 wins = {0}\n'\
              'Player 2 wins = {1}\n'\
              'Average battles/game = {2:.3f}\n'\
              'Average wars/game = {3:.3f}\n'\
              'Average 1-war sequences/game = {4:.6f}\n'\
              'Average 2-war sequences/game = {5:.6f}\n'\
              'Average 3-war sequences/game = {6:.6f}\n'\
              'Average 4-war sequences/game = {7:.6f}\n'\
              'Average 5-war sequences/game = {8:.6f}\n'\
              'Average 6-war sequences/game = {9:.6f}\n'\
              'The elapsed time to complete {10} simulations was {11:.2f} '\
              'seconds\n'\
              .format(winnerStat[1], winnerStat[2],\
                      numBattlesStat/games,\
                      numWarsStat/games,\
                      warHistogramStat[0]/games,\
                      warHistogramStat[1]/games,\
                      warHistogramStat[2]/games,\
                      warHistogramStat[3]/games,\
                      warHistogramStat[4]/games,\
                      warHistogramStat[5]/games,\
                      games, elapsedTime))
