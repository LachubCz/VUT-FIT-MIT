"""
@author: Vladan Kudlac
"""
from typing import Tuple


class Interval:

	low: Tuple[str, str]
	high: Tuple[str, str]

	def __init__(self, low: Tuple[str, str] = None, high: Tuple[str, str] = None):
		self.low = low
		self.high = high

	def empty(self):
		return self.low is None and self.high is None
