#coding=utf-8
### Sorting
from random import randint, seed
import numpy as np
import timeit
seed(1)


def generateRandomArray(n, *args):
    if args:
        minNum = args[0] 
        maxNum = args[1]
    else:
        minNum = 0
        maxNum = n
    arr = np.array([randint(minNum, maxNum) for x in range(n)])
    return arr

def check_Input_Type(arr):
    if type(arr) != np.ndarray:
        raise Exception("input type is wrong.")


###  bubbleSort
def bubble_Sort(arr):
    check_Input_Type(arr)
    
    N = arr.shape[0]
    for i in range(N-1, 0, -1):
        early_termination = True
        for j in range(0, i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                early_termination = False
        if early_termination == True:
            print("Early termination at i={0}, j={1}".format(i, j))
            break
    return arr


### selectionSort
def selection_Sort(arr):
    check_Input_Type(arr)
    
    N = arr.shape[0]
    for i in range(0, N-1):
        for j in range(i+1, N):
            j_pos = i
            if arr[j] < arr[j_pos]:
                j_pos = j
            arr[j_pos], arr[i] = arr[i], arr[j_pos]
    return arr


### insertionSort
def insertion_Sort(arr):
    check_Input_Type(arr)
    
    N = arr.shape[0]
    for i in range(1, N):
        temp_arr = arr[i]
        for j in range(i, 0, -1):
            if temp_arr < arr[j-1]:  # move
                arr[j] = arr[j-1]  # move on the right
            else:
                break  # till the right place since thr left has been sorted
            #insert:
            arr[j-1] = temp_arr
    return arr

###cocktail_Shaker_Sort
def cocktail_Shaker_Sort(arr):
    check_Input_Type(arr)
    N = arr.shape[0]
    for i in range(0, N):
        early_termination = True
        for j in range(i+1, N-i):
            if arr[j-1] > arr[j]:
                arr[j], arr[j-1] = arr[j-1], arr[j]
                early_termination = False
        for j in range(N-i-2, i, -1):
            if arr[j-1] > arr[j]:
                arr[j], arr[j-1] = arr[j-1], arr[j]
                early_termination = False
        if early_termination == True:
            print("Early termination at i={0}, j={1}".format(i, j))
            break
    return arr

# quick sort
def quick_sort(arr):
    check_Input_Type(arr)

    pass


def partition(arr):
    N = arr.shape[0]
    i = 1
    j = N-1
    pivot = arr[0]
    while True:
        if i >= N-1 or j <= 1:
            break
        if i >= j:
            break
        if arr[i] > pivot or arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]

        if arr[i] <= pivot:  # first add i
            i = i + 1
        else:
            pass
        if arr[j] >= pivot:
            j = j - 1
        else:
            pass
    # put pivot into right place:
    value = arr[0]
    arr = np.delete(arr, 0, axis=0)
    arr = np.insert(arr, i-1, value, axis=0)

    # TODO
    arr[0:i-1] = bubble_Sort(arr[0:i-1])
    arr[i:] = bubble_Sort(arr[i:])

    return arr


if __name__ == "__main__":
    arr = generateRandomArray(8)
    t_start = timeit.timeit()
    # arr = bubble_Sort(arr)
    
    #arr = selection_Sort(arr)
   
    #arr = insertion_Sort(arr)
    
    # arr = cocktail_Shaker_Sort(arr)

    arr = partition(arr)
    t_end= timeit.timeit()
    
    print(t_end - t_start)


    print(arr)
    



    