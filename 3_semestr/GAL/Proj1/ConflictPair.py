"""
@author: Vladan Kudlac
"""
from Interval import Interval


class ConflictPair:

	l: Interval
	r: Interval

	def __init__(self, left: Interval = None, right: Interval = None):
		if left is None:
			left = Interval()
		if right is None:
			right = Interval()
		self.l = left
		self.r = right

	def swap(self) -> None:
		tmp = self.l
		self.l = self.r
		self.r = tmp
