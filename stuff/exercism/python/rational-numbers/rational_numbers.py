from __future__ import division
from fractions import gcd


class Rational(object):
	def __init__(self, numer, denom):
		self.numer = numer
		self.denom = denom
		self.simplify()

	def simplify(self):
		divi = gcd(self.numer,self.denom)
		self.numer /= divi
		self.denom /= divi

	def __eq__(self, other):
		return self.numer == other.numer and self.denom == other.denom

	def __repr__(self):
		return '{}/{}'.format(self.numer, self.denom)

	def __add__(self, other):
		self.numer = (self.numer * other.denom) + (other.numer * self.denom)
		self.denom = self.denom * other.denom
		self.simplify()
		return self

	def __sub__(self, other):
		self.numer = (self.numer * other.denom) - (other.numer * self.denom)
		self.denom = self.denom * other.denom
		self.simplify()
		return self

	def __mul__(self, other):
		self.numer = self.numer * other.numer
		self.denom = self.denom * other.denom
		self.simplify()
		return self

	def __truediv__(self, other):
		self.numer = self.numer * other.denom
		self.denom = self.denom * other.numer
		self.simplify()
		return self

	def __abs__(self):
		self.numer = abs(self.numer)
		self.denom = abs(self.denom)
		self.simplify()
		return self

	def __pow__(self, power):
		self.numer = self.numer ** power
		self.denom = self.denom ** power
		self.simplify()
		return self

	def __rpow__(self, base):
		return base**(self.numer/self.denom)
