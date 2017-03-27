#for each round
#Truth Booth
	#If TRUE
		#remove all combinations without that pair
	#If FALSE
		#remove all combinations with that pair
#Matching Ceremony
	#If enough new lights to equal 10 total
		#WIN
	#If Blackout
		#for every guessed pair
			#remove all combinations with that pair
	#If 1 - 9 new lights
		#remove combinations which would not result in the
		#the same number of new lights
#output size of possibilities array
#output probabilities for each match
	#for each available match the probability is
		#= (number of possibilities with that match)/(total remaining possibilities)
#if less than 20 possible combinations
	#output probability of each full guess
		#= SUM(probability of each couple in that guess) (from above)

import time
import numpy as np
import pandas as pd
import tkinter as tk

def reset_permutations():
    print( "...reseting possible permutations...\n" )
    permutations = open("permutations.txt", 'r+')

    with open("permutationsCopy.txt", "r+") as file:
        data = file.readlines()
        for i in data:
            permutations.write(i)
        permutations.truncate()
        file.close()

    permutations.close()

def setup_game():
    players = []
    for i in list( range( 10 ) ):
        players.append( input( "Name of Guy #%s:" % (i + 1) ) )
    for i in list( range( 10 ) ):
        players.append( input( "Name of Girl #%s:" % (i + 1) ) )
    print('\n')

    return players

def match(man, woman):
    with open("permutations.txt", 'r+') as file:
        data = file.readlines()
        temp_data = []
        for line in data:
            if line[man] is woman:
                temp_data.append(line)
        file.seek(0)
        for i in temp_data:
            file.write(i)
        file.truncate()
        file.close()

def not_a_match(man, woman):
    with open("permutations.txt", 'r+') as file:
        data = file.readlines()
        temp_data = []
        for line in data:
            if line[man] is not woman:
                temp_data.append(line)
        file.seek(0)
        for i in temp_data:
            file.write(i)
        file.truncate()
        file.close()

def calculate_probability_of_match(man_number, woman_letter):
    count = 0
    with open("permutations.txt", "r+") as file:
        data = file.readlines()
        for line in data:
            if line[man_number] == woman_letter:
                count += 1
        return count / len(data)
        file.close()

def passes_number_of_lights_test(guess, compareTo, num_lights_cutoff):
    num_lights = 0

    for i in range( len( compareTo ) ):
        if num_lights >= num_lights_cutoff:
            return True
        elif guess[i] == compareTo[i]:
            num_lights += 1

    return False

def print_number_of_possibilities():
    with open("permutations.txt") as file:
        data = file.readlines()
        print("The Number of Possibilities Left is: %s" % len( data ))

def print_players(players, is_men, is_sideways):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    if is_sideways is False:
        for i in list(range(10)):
            if is_men:
                print("{}. {}".format(i, players[i]))
            else:
                print("{}. {}".format(letters[i], players[i + 10]))
    else:
        for i in list(range(10)):
            if is_men:
                print("{}. {}".format(i, players[i]), end=' ')
            else:
                print("{}.{}".format(letters[i], players[i + 10]), end=' ')
        print('\n')

def play_truth_booth(players):
    print( "~~~~ In the Truth Booth ~~~~" )

    print_players(players, True, False)
    man = int( input( "which man is entering the Truth Booth? (Enter digit 0 through 9)" ) ) #0-9
    print_players(players, False, False)
    woman = input( "which woman is entering the Truth Booth? (Enter letter a through j)" ) #a-j
    result = input( "is it a match? ('yes' or 'no')" ) #'yes' or 'no'
    print("calculating *Bleep *Bloop...")

    start_time = time.time()

    if result == 'yes':
        match(man, woman)

    else:
        not_a_match(man, woman)

    print("--- %s seconds ---\n" % (time.time() - start_time))

def play_matching_ceremony(players):
    print("~~~~ In the Matching Ceremony ~~~~")
    print( "Time to put in the pairs..." )
    print("Enter letter a through j")
    print('\n')
    print_players(players, False, True)
    permutation = ""
    for i in list( range( 10 ) ):
        permutation += input( "Who matched with man #%s?" % players[i])
    print( "the guess is %s" % permutation )
    num_lights = int( input( "How many total lights were there?" ) )

    if num_lights == 10:
        print( "YAAAAAAASSSSS THEY WON!" )

    elif num_lights == 0:
        print( "BLA BLA BLA BLACKOOOOOOOUT!" )
        print( "...deleting all these loser pairs..." )
        for i in list( range( 10 ) ):
            not_a_match(i, permutation[i])

    else:
        print( "...analyzing based on number of lights..." )
        print('\n')
        with open("permutations.txt", 'r+') as file:
            data = file.readlines()
            temp_data = []
            for line in data:
                if passes_number_of_lights_test(line, permutation, num_lights):
                    temp_data.append(line)
            file.seek(0)
            for i in temp_data:
                file.write(i)
            file.truncate()
            file.close()

def show_end_round_analysis(players):
    men = players[0:10]
    women = players[10:20]
    print( "~~~~ End of Round Analysis ~~~~" )

    print_number_of_possibilities()
    print('\n')

    match_probabilities = np.zeros(shape=(10, 10), dtype=float)

    letters = "abcdefghij"

    print("...calculating match probabilities...")
    for man in range(10):
        for woman in range(10):\
            match_probabilities[man][woman] = format(calculate_probability_of_match(man, letters[woman]), ".2f")

    df = pd.DataFrame(match_probabilities, index=men, columns=women)
    print(df)

def play_are_you_the_one():
    reset_permutations()

    players = setup_game()

    for round in list( range( 10 ) ):
        print( ">>>>STARTING ROUND %s<<<<\n" % (round + 1) )

        play_truth_booth(players)

        play_matching_ceremony(players)

        show_end_round_analysis(players)

play_are_you_the_one()
