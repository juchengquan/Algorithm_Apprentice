import numpy as np

def get_coin_change(n):
    global lisp, counter, coin_set
    for ele in coin_set:
        if n >= ele:
            lisp[ele] = 1
            
        if n-ele in coin_set:
            lisp[int(n-ele)] = 1
        elif n-ele > 1 and n-ele not in coin_set:
            counter +=1
            lisp[int(n-ele)]= get_coin_change(n-ele)[0] 
        else:
            pass
    
    lisp[n] = np.min([lisp[int(n-ele)] if n-ele >=1 else 100 for ele in coin_set]) + 1
    
    return (lisp[n], lisp)
    
if __name__ == "__main__":
    coin_set = np.array([1,5,11],dtype=int)
    counter = 0 # set a global counter to calculate complexity 
    N = 16
    lisp = np.zeros(N+1) # relax the first index as invalid, e.g., 0
    min_no_of_coin , all_solution = get_coin_change(N)
    print("Min number of coin is {0}".format(int(min_no_of_coin)))
    print("Complexity is {0}".format(int(counter)))