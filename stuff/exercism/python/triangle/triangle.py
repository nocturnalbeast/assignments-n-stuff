def is_equilateral(sides):
	return sides[0] == sides[1] == sides [2] != 0

def is_isosceles(sides):
	return (sorted(sides)[0] == sorted(sides)[1] or sorted(sides)[1] == sorted(sides)[2]) and triangle_inequality(sides)

def is_scalene(sides):
	return sides[0] != sides[1] != sides [2] and triangle_inequality(sides)

def triangle_inequality(sides):
	return sides[0] + sides[1] > sides[2] and sides[1] + sides[2] > sides[0] and sides[2] + sides[0] > sides[1]
