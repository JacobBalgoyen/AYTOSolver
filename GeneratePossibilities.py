#!/usr/bin/python3

import time

def permutation( str ):
    permutations_file = open("permutations.txt", "w+", -1)

    perform_permutation( "", str, permutations_file )

    permutations_file.close()

def perform_permutation( prefix, str, file ):
    n = len( str )

    if n == 0:
        file.write( prefix )
        file.write( "\n" )

    else:
        for i in list( range( n ) ):
            perform_permutation( prefix + str[i], str[:i] + str[(i + 1):], file )

start_time = time.time()
permutation( "abcdefghij" )

copy = open("permutationsCopy.txt", 'w+')
with open("permutations.txt", 'r+') as file:
    data = file.readlines()
    for line in data:
        copy.write(line)
    file.close()
copy.close()


print("--- %s seconds ---" % (time.time() - start_time))
