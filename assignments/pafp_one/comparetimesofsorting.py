import time
import random

# Function for selection sort
def selection(lst):
	# Iterating variable i througn range 0 to length-1
	for i in xrange(len(lst)):
		# Setting min_i variable to the first unsorted element
		min_i = i
		# Iterating variable j through the unsorted portion of the array
		for j in xrange(i+1,len(lst)):
			# If element in index j is lesser than element in index min_i set min_i to value of j
			if lst[j] < lst[min_i]:
				min_i = j
		# Swap elements at minimum index and i
		lst[min_i], lst[i] = lst[i], lst[min_i]

# Function for insertion sort
def insertion(lst):
	# Iterating variable i througn range 1 to length-1
	for i in xrange(1,len(lst)):
		# Setting key element as i'th element of array
		key = lst[i]
		# Setting j as the index before i in array
		j = i - 1
		# Iterating while j remains greater than zero and key value is lesser than j'th element in array
		while j >= 0 and key < lst[j]:
			# Moving all elements after j to j+1
			lst[j+1] = lst[j]
			j -= 1
		# Setting the empty array space as key value
		lst[j+1] = key

# Function for bubble sort
def bubble(lst):
	# Iterating variable i through range 0 to length-1
	for i in xrange(len(lst)):
		# Iterating variable j through range 0 to length-i-1
		for j in xrange(0,len(lst)-i-1):
			# If j'th element is greater than it's succeeding element swap those two elements
			if lst[j] > lst[j+1]:
				lst[j], lst[j+1] = lst[j+1], lst[j]

# Function for quick sort
def quick(lst,low,high):
	# Check if indexes haven't crossed
	if low < high:
		# Setting sorted portion of array with less_ind
		less_ind = low - 1
		# Setting pivot
		pi_num = lst[high]
		# Iterating variable j through range from low to high-1
		for j in xrange(low,high):
			# If element in unsorted portion of array is lower than pivot then increment sorted index and swap elements with indexes j and less_ind
			if pi_num >= lst[j]:
				less_ind += 1
				lst[less_ind], lst[j] = lst[j], lst[less_ind]
		# Swap pivot and element at index where pivot should actually be
		lst[less_ind+1], lst[high] = lst[high], lst[less_ind+1]
		# Setting pivot index and recursively calling sorting function on subarrays to the left and right of the pivot element
		pi_ind = less_ind + 1
		quick(lst,low,pi_ind-1)
		quick(lst,pi_ind+1,high)

# Function for merge sort
def merge(lst,lft,rgt):

	# Helper function to merge two subarrays 
	def act_merge(lst,left,mid,right):
		# num_1 is number of elements of first subarray
		num_1 = mid - left + 1
		# num_2 is number of elements of second subarray
		num_2 = right - mid

		# Initialising temporary arrays with zeroes
		lst_left, lst_right = [0] * num_1, [0] * num_2

		# Copying elements from main array to temporary arrays
		for i in xrange(0,num_1):
			lst_left[i] = lst[left + i]
		for i in xrange(0,num_2):
			lst_right[i] = lst[mid + 1 + i]

		# Initialising indexes for subarrays
		ind_left, ind_right, ind_lst = 0, 0, left

		# Comparing two subarrays and check which one is smaller, and then insert the smaller element into the merged array, continue till either of the temporary arrays are emptied
		while ind_left < num_1 and ind_right < num_2:
			if lst_left[ind_left] <= lst_right[ind_right]:
				lst[ind_lst] = lst_left[ind_left]
				ind_left += 1
			else:
				lst[ind_lst] = lst_right[ind_right]
				ind_right += 1
			ind_lst += 1

		# Copy the rest of the elements that remain in the left temporary array 
		while ind_left < num_1:
			lst[ind_lst] = lst_left[ind_left]
			ind_left += 1
			ind_lst += 1

		# Copy the rest of the elements that remain in the right temporary array 
		while ind_right < num_2:
			lst[ind_lst] = lst_right[ind_right]
			ind_right += 1
			ind_lst += 1

	# Checking if indexes haven't crossed
	if lft < rgt:
		# Getting middle index
		mid = (lft+rgt-1)/2
		# Recursively calling merge function with left part of array
		merge(lst,lft,mid)
		# Recursively calling merge function with right part of array
		merge(lst,mid+1,rgt)
		# Calling helper function to merge left and right subarrays
		act_merge(lst,lft,mid,rgt)

# Function for heap sort
def heap(lst):

	# Helper function to build max or min heap based on requirement (minheap used here)
	def heapify(lst,size,par_ind):
		# Setting index of largest element and index of left and right children
		smlst_ind, lch_ind, rch_ind = par_ind, par_ind * 2 + 1, par_ind * 2 + 2
		# Checking between parent and left child to see which is smaller
		if lch_ind < size and lst[lch_ind] > lst[smlst_ind]:
			smlst_ind = lch_ind
		# Checking between parent and right child to see which is smaller
		if rch_ind < size and lst[rch_ind] > lst[smlst_ind]:
			smlst_ind = rch_ind
		# If index of smallest element does not match that of parent, then swap the elements and re-heapify the affected subtree by recursively calling heapify
		if smlst_ind != par_ind:
			lst[smlst_ind], lst[par_ind] = lst[par_ind], lst[smlst_ind]
			heapify(lst,size,smlst_ind)

	# Call heapify for all subtrees from bottom
	for i in xrange(len(lst)-1,-1,-1):
		heapify(lst,len(lst),i)
	# Remove each element from the top and then call heapify to rebuild the heap for remaining elements in heap
	for i in xrange(len(lst)-1,0,-1):
		lst[i], lst[0] = lst[0], lst[i]
		heapify(lst,i,0)

# Function to compute times of sorting, i.e. driver function for all sort functions
def comp_fn(func_name):
	# Dictionary to map string to function object
	dict_func = {
		"selection" : selection,
		"insertion" : insertion,
		"bubble" : bubble,
		"quick" : quick,
		"merge" : merge,
		"heap" : heap
	}
	# Iterating power through range from 1 to 20
	for power in xrange(1,25):
		# Using list comprehension to generate list with random elements with list size being 2 raised to power
		rand_lst = [random.randint(0,1000000) for x in range(2 ** power)]
		# Starting timer
		start_time = time.time()
		# Invocation logic, along with cutoff
		if func_name in ["quick", "merge"]:
			if func_name == "quick" and len(rand_lst) < 100:
				insertion(rand_lst)
			else:
				dict_func.get(func_name)(rand_lst,0,len(rand_lst)-1)
		else:
			dict_func.get(func_name)(rand_lst)
		# Finally print time
		print "Time taken to sort with {} elements is {} seconds.".format(len(rand_lst),(time.time() - start_time))
		# Clear list
		del rand_lst[:]
		# Check if user still wants to continue with next iteration
		if raw_input("Do you want to continue? (y/n)").lower() == 'y':
			continue
		else:
			break

comp_fn(raw_input("Enter the sorting function to test times with: "))