"""
Execute script on server

Find nth prime number and write to text file
"""
from sys import argv, exit

# We need a number
if len(argv) < 2:
    print('ERROR: Number not specified!')
    print('$ python worker-script.py number')
    exit(1)
    
# Get number n
n = int(argv[1])

# Make sure n >= 1
if n < 1:
    print('ERROR: Number must be >= 1, got:', n)
    print('$ python worker-script.py number')
    exit(1)

# Allocate array for prime numbers
primes = [2]

# We initialize a value k, which we increment by 
# 1 continuously. For every increment, we check 
# if k is divisible by any of the prime numbers 
# we've discovered so far (that is if k % p == 0). 
# If k is not divisible by any of the prime numbers, 
# we add k to our list of primes. This is dependent 
# on the axiom that if k is not divisible by any prime 
# factors < k, then k is not divisible by any factors
# < k and is obviously not divisible by any numbers 
# that are greater than k
k = 3
while len(primes) < n:
    # Loop through our primes and check each prime for 
    # if k is divisibile by that prime
    indivisible = True
    for p in primes:
        if k % p == 0:
            indivisible = indivisible and False
            break
    
    # If k is indivisible, add it to primes list
    if indivisible:
        primes.append(k)
        
    # Increment k
    k += 1

# Print latest prime found
print(primes[-1])