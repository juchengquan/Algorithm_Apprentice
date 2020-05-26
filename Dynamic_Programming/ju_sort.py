
# bubble sort
def bubble_sort(arr):
	N = len(arr)

	for i in range(N):
		early_termination = True
		for j in range(0, N-i-1):
			if arr[j] > arr[j+1]:
				arr[j], arr[j+1] = arr[j+1], arr[j]
				early_termination = False
			if early_termination == True:
				print("early termination")
				return arr
	return arr

# selection sort
def selection_sort(arr):
	N = len(arr)

	for i in range(N):
		for j in range(i+1, N):
			if arr[j] < arr[i]:
				arr[i], arr[j] = arr[j], arr[i]
	return arr

# insertion_sort(arr):
def insertion_sort(arr):
	N = len(arr)

	for i in range(N):
		curr = arr[i]
		j = i-1
		while j >= 0 and arr[j] > curr:
			arr[j+1] = arr[j]
			j -= 1
		
		arr[j+1] = curr
	return arr	

# merge_sort
def merge_sort(arr):
	N = len(arr)
	if N <= 1:
		return arr

	pivot = N // 2

	left = merge_sort(arr[0:pivot])
	right = merge_sort(arr[pivot:])
	res = []
	while left and right:
		if left[-1] > right[-1]:
			res.insert(0, left.pop())
		elif left[-1] <= right[-1]:
			res.insert(0, right.pop())
			
	# sort out rest
	if left:
		res = left + res
	if right:
		res = right + res

	return res

# quick_sort
def quick_sort(arr):
	N = len(arr)
	if N <=1:
		return arr

	pivot = 0
	for i in range(1, N):
		if arr[i] <= arr[0]:
			pivot += 1
			arr[pivot], arr[i] = arr[i], arr[pivot]

	# put pivot in place:
	arr[pivot], arr[0] = arr[0], arr[pivot]

	# in-place
	left = quick_sort(arr[:pivot])
	right = quick_sort(arr[pivot+1:])

	return left + [arr[pivot]] + right


if __name__ == "__main__":
	arr = [5, 4, 3, 2, 1, 8, 7, 6, 9]
	print(arr)

	arr = quick_sort(arr)

	print(arr)

