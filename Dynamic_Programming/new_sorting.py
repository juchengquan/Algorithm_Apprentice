
def bubble_sort(arr):
	N = len(arr)

	# i, j = 0, N-1:
	for i in range(N-1, 0, -1):
		early_termination = True
		for j in range(0, i):
			if arr[j] > arr[j+1]:
				arr[j], arr[j+1] = arr[j+1], arr[j]
				early_termination = False
		if early_termination:
			print("early_termination")
			return arr
	return arr

def selection_sort(arr):
	N = len(arr)
	for i in range(N-1, 0, -1):
		for j in range(0, i):
			if arr[i] < arr[j]:
				arr[i], arr[j] = arr[j], arr[i]
	return arr

def cocktail_sort(arr):
	N = len(arr)
	for i in range(0, N):
		early_termination = True
		for j in range(i, N-i-1):
			if arr[j] > arr[j+1]:
				arr[j], arr[j+1] = arr[j+1], arr[j]
				early_termination = False
		for j in range(N-i-2, i, -1):
			if arr[j-1] > arr[j]:
				arr[j], arr[j-1] = arr[j-1], arr[j]
				early_termination = False
	return arr

def insert_sort(arr):
	N = len(arr)
	for i in range(0, N):
		j = i-1 
		cur = arr[i]
		while j >= 0 and arr[j] > cur:
			arr[j+1] = arr[j]
			j -= 1
			
		arr[j+1] = cur
	return arr

def merge_sort(arr):
	N = len(arr)
	if N <= 1:
		return arr

	pivot = N // 2
	left = merge_sort(arr[:pivot])
	right = merge_sort(arr[pivot:])
	# print(left, right)

	# return merge_aux(left, right)

	# def merge_aux(left, right):
	res = []
	while left and right:
		if left[-1] >= right[-1]:
			res.insert(0, left.pop())
		else:
			res.insert(0, right.pop())

	if left:
		res = left + res 
	if right:
		res = right + res

	return res

def quick_sort(arr):
	N = len(arr)
	if N <= 1:
		return arr

	pivot = 0
	idx = 0
	for i in range(N):
		if arr[i] < arr[0]:
			idx += 1
			arr[idx], arr[i] = arr[i], arr[idx]

	# get pivot in place
	arr[pivot], arr[idx] = arr[idx], arr[pivot]

	# non-in-place
	left = quick_sort(arr[0:pivot])
	right = quick_sort(arr[pivot+1:])
	return left + [arr[pivot]] + right


if __name__  == "__main__":
	arr = [5, 4, 3, 2, 1, 8, 7, 6, 9]
	print(arr)

	arr = quick_sort(arr)

	print(arr)
