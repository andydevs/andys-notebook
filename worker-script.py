"""
Execute script on server

Find nth prime number and write to text file
"""
from sys import argv, exit

# Help message
help_message = '$ python worker-script.py number [number...]'

# We need at least one number
if len(argv) < 2:
    print('ERROR: At least one number must be specified!')
    print(help_message)
    exit(1)
    
# Get numbers n
ns = [int(n) for n in argv[1:]]

# Make sure all ns > 1
for n in ns:
    if n < 1:
        print('ERROR: All numbers must be >= 1! got:', n)
        print(help_message)
        exit(1)
        
# Get maximum n value from ns
# If we discover all primes up 
# to this number, we then have
# implicitly discovered all nth 
# primes for n < max n. So we 
# can filter for those
n = max(ns)

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

# Print the nth primes for all ns
print(*(primes[n - 1] for n in ns), sep='\n')