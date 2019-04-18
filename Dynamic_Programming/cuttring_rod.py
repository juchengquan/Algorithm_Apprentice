import numpy as np

def cutRod(n):
    # cutting a rod
    global lisp, counter, rod_length, rod_price, rod_count
    counter += 1
    for ele in rod_length:
        if n >= ele:
            lisp[ele] = rod_price[ele-1] # initialize known prices
            rod_dispatch[ele, ele] = 1

        if n-ele > 1 and n-ele not in rod_length:
            if lisp[int(n-ele)] == 0: # if this is not calculated yet:
                lisp[int(n-ele)] = cutRod(n-ele)[0] 
        else:
            pass
    
    lisp[n] = np.max([lisp[int(n-ele)]+rod_price[idx] if n-ele >=1 else 1e6 for idx, ele in enumerate(rod_length) ]) 
    location = np.argmax([lisp[int(n-ele)]+rod_price[idx] if n-ele >=1 else 1e6 for idx, ele in enumerate(rod_length) ]) 
    rod_dispatch[n,:] = rod_dispatch[location+1,:] + rod_dispatch[n-location-1,:]
    #print(location)

    return (lisp[n],  lisp ) # return the last one and whole sequence

if __name__ == "__main__" :
    rod_length = np.arange(10, dtype="int16")+1
    rod_price = np.array([1,5,8,9,10,17,17,20,24,30], dtype="int16")
    rod_count = np.zeros(10+1, dtype="int16")
    
    counter = 0
    N = 33
    rod_dispatch = np.zeros((N+1, 10+1), dtype="int16") # use a matrix to trace the dispatch
    
    lisp = np.zeros(N+1, dtype="int16")
    benefit , all_solution = cutRod(N)
    
    print("maximum benefit is {0}".format(int(benefit)))
    print("Cmoplexity is {0}".format(counter))
    print("The dispatch is {0}".format(rod_dispatch[N,:]))
