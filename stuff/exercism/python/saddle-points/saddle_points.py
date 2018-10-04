def max_row(matrix,index):
	return max(matrix[index])

def min_col(matrix,index):
	col = []
	for i in range(len(matrix)):
		col.append(matrix[i][index])
	return min(col)

def saddle_points(matrix):
	sdle_pts = []
	if len(set([len(row) for row in matrix])) > 1:
		raise ValueError("Irregular matrix!")
	for i in xrange(len(matrix)):
		for j in xrange(len(matrix[i])):
			if (matrix[i][j] == max_row(matrix,i)) & (matrix[i][j] == min_col(matrix,j)):
				sdle_pts.append((i,j))
	return set(sdle_pts)