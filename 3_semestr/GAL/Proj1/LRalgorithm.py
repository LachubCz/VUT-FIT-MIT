"""
@author: Vladan Kudlac
@see: http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.217.9208
"""
from collections import defaultdict
from typing import Tuple, List, Dict
from ConflictPair import ConflictPair
from BucketSearch import bucket_sort
from graph import Graph
from graphs import *
import datetime

from Interval import Interval


class LRPlanarityCheck:

	parent_edge: defaultdict  # Dict[str, Tuple[str, str]]
	height: defaultdict  # Dict[str, int]
	orientedGraph: List[Tuple[str, str]]
	lowpt: Dict[Tuple[str, str], int]
	nesting_depth: Dict[Tuple[str, str], int]

	adj_list: defaultdict  # Dict[str, [List[str]]

	graph: Graph
	lowpt2: Dict[Tuple[str, str], int]

	s: List[ConflictPair]
	stack_bottom: Dict[Tuple[str, str], ConflictPair]
	lowpt_edge: Dict[Tuple[str, str], Tuple[str, str]]
	ref: defaultdict  # Dict[Tuple[str, str], Tuple[str, str]]
	side: defaultdict  # Dict[Tuple[str, str], int]

	def __init__(self, graph: Graph):
		v = len(graph.get_vertices())
		# Used in both DFS traversals
		self.parent_edge = defaultdict(lambda: None)
		self.height = defaultdict(lambda: None)
		self.orientedGraph = []
		self.lowpt = {}
		self.nesting_depth = {}

		self.adj_list = defaultdict(lambda: None)

		# Used in first DFS orientation, removed after that
		self.graph = graph
		self.lowpt2 = {}

		# Used in second DFS traversal
		self.s = []
		self.stack_bottom = {}
		self.lowpt_edge = {}
		self.ref = defaultdict(lambda: None)
		self.side = defaultdict(lambda: 1)

	def simple_check(self) -> bool:
		"""
		Euler's Relation planarity check
		@return: bool False when not planar, True when it still can be planar
		"""
		v = len(self.graph.get_vertices())
		e = len(self.graph.get_edges())

		return v < 3 or e <= (3 * v - 6)

	def run(self) -> bool:
		"""
		Left-Right planarity algorithm
		@return: bool False when not planar, True when planar
		"""

		roots = []

		# Orientation
		for s in self.graph.get_vertices():
			if self.height[s] is None:
				self.height[s] = 0
				roots.append(s)
				self.lr_orientation(s)
			# sort adjacency list according to non-decreasing nesting_depth O(n * log n)
			if self.adj_list[s] is not None:
				self.adj_list[s] = bucket_sort(self.adj_list[s], s, self.nesting_depth, len(self.adj_list)*2)
			else:
				self.adj_list[s] = []

		del self.graph
		del self.lowpt2

		# Testing
		for s in roots:
			if not self.lr_test(s):
				return False

		return True

	def lr_orientation(self, v: str) -> None:
		"""
		Phase 1 - DFS orientation and nesting order
		@param v: str vertex
		"""
		e = self.parent_edge[v]
		for w in self.graph.get_Adj(v):
			if not ((v, w) in self.orientedGraph or (w, v) in self.orientedGraph):
				if self.adj_list[v] is None:
					self.adj_list[v] = [w]
				else:
					self.adj_list[v].append(w)
				self.orientedGraph.append((v, w))
				self.lowpt[(v, w)] = self.height[v]
				self.lowpt2[(v, w)] = self.height[v]

				if self.height[w] is None:  # tree edge
					self.parent_edge[w] = (v, w)
					self.height[w] = self.height[v] + 1
					self.lr_orientation(w)
				else:  # back edge
					self.lowpt[(v, w)] = self.height[w]

				# determine nesting depth
				self.nesting_depth[(v, w)] = 2 * self.lowpt[(v, w)]
				if self.lowpt2[(v, w)] < self.height[v]:  # chordal
					self.nesting_depth[(v, w)] += 1

				# update lowpoints of parent edge e
				if e is not None:
					if self.lowpt[(v, w)] < self.lowpt[e]:
						self.lowpt2[e] = min(self.lowpt[e], self.lowpt2[(v, w)])
						self.lowpt[e] = self.lowpt[(v, w)]
					elif self.lowpt[(v, w)] > self.lowpt[e]:
						self.lowpt2[e] = min(self.lowpt2[e], self.lowpt[(v, w)])
					else:
						self.lowpt2[e] = min(self.lowpt2[e], self.lowpt2[(v, w)])

	def lr_test(self, v: str) -> bool:
		"""
		Phase 2 - Testing for LR partition
		@param v: str vertex
		@return: bool False when not planar, True when it still can be planar
		"""
		e = self.parent_edge[v]
		for w in self.adj_list[v]:
			ei = (v, w)
			self.stack_bottom[ei] = self.top_s()
			if ei == self.parent_edge[w]:  # tree edge
				if not self.lr_test(w):
					return False
			else:  # back edge
				self.lowpt_edge[ei] = ei
				self.s.append(ConflictPair(right=Interval(ei, ei)))
			if self.lowpt[ei] < self.height[v]:  # ei has return edge
				if w == self.adj_list[v][0]:
					self.lowpt_edge[e] = self.lowpt_edge[ei]
				else:
					# Add constraints of ei
					if not self.add_constraints(ei, e):
						return False

		if e is not None:  # v is not root
			u = e[0]
			# Trim back edges ending at parent u
			self.trim_back_edges(u)
			# Side of e is side of a highest return edge
			if self.lowpt[e] < self.height[u]:  # e has return edge
				hl = self.top_s().l.high
				hr = self.top_s().r.high
				if hl is not None and (hr is None or self.lowpt[hl] > self.lowpt[hr]):
					self.ref[e] = hl
				else:
					self.ref[e] = hr

		return True

	def add_constraints(self, ei: Tuple[str, str], e: Tuple[str, str]) -> bool:
		"""
		Add constraints of ei (phase 2)
		@param e: Tuple[str, str]
		@param ei: Tuple[str, str]
		@return: bool False when not planar, True when it still can be planar
		"""
		p = ConflictPair()
		# merge return edges of ei into p.r
		while True:
			q = self.s.pop()
			if not (q.l.empty()):
				q.swap()
			if not (q.l.empty()):
				return False  # HALT: not planar
			else:
				if self.lowpt[q.r.low] > self.lowpt[e]:  # merge intervals
					if p.r.empty():
						p.r.high = q.r.high
					else:
						self.ref[p.r.low] = q.r.high
					p.r.low = q.r.low
				else:  # make consistent
					self.ref[q.r.low] = self.lowpt_edge[e]
			if self.top_s() == self.stack_bottom[ei]:
				break

		# merge conflicting return edges of e(1), ... , e(i-1) into p.l
		while self.conflicting(self.top_s().l, ei) or self.conflicting(self.top_s().r, ei):
			q = self.s.pop()
			if self.conflicting(q.r, ei):
				q.swap()
			if self.conflicting(q.r, ei):
				return False  # HALT: not planar
			else:  # merge interval below lowpt[ei] into p.r
				self.ref[p.r.low] = q.r.high
				if q.r.low is not None:
					p.r.low = q.r.low
			if p.l.empty():
				p.l.high = q.l.high
			else:
				self.ref[p.l.low] = q.l.high
			p.l.low = q.l.low

		if not (p.l.empty() and p.r.empty()):
			self.s.append(p)

		return True

	def trim_back_edges(self, u: str):
		"""
		Remove back edges ending at parent u (phase 2)
		@param u:
		@return:
		"""
		# drop entire conflict pairs
		while len(self.s) and self.lowest(self.top_s()) == self.height[u]:
			p = self.s.pop()
			if p.l.low is not None:
				self.side[p.l.low] = -1

		# one more conflict pair to consider
		if len(self.s):
			p = self.s.pop()
			# trim left interval
			while p.l.high is not None and p.l.high[1] == u:
				p.l.high = self.ref[p.l.high]
			if p.l.high is None and p.l.low is not None:  # just emptied
				self.ref[p.l.low] = p.r.low
				self.side[p.l.low] = -1
				p.l = Interval(high=p.l.high)
			# trim right interval
			while p.r.high is not None and p.r.high[1] == u:
				p.r.high = self.ref[p.r.high]
			if p.r.high is None and p.r.low is not None:  # just emptied
				self.ref[p.r.low] = p.l.low
				self.side[p.r.low] = -1
				p.r = Interval(high=p.r.high)
			self.s.append(p)

	def conflicting(self, i: Interval, b: Tuple[str, str]) -> bool:
		"""
		Check conflicting edge against interval
		@param i: Interval interval
		@param b: Tuple[str, str] edge
		@return: bool True when conflicting, otherwise False
		"""
		return not (i.empty()) and self.lowpt[i.high] > self.lowpt[b]

	def top_s(self) -> ConflictPair:
		"""
		Return last item on stack or None when empty
		@return: ConflictPair | None
		"""
		return self.s[-1] if len(self.s) else None

	def lowest(self, p: ConflictPair) -> int:
		if p.l.empty():
			return self.lowpt[p.r.low]
		if p.r.empty():
			return self.lowpt[p.l.low]
		return min(self.lowpt[p.r.low], self.lowpt[p.l.low])


if __name__ == '__main__':
	graph = Graph(g_1)
	lrTest = LRPlanarityCheck(graph)
	print("Simple check: ", lrTest.simple_check())
	print("LR test: ", lrTest.run(), "\n")
	graph = Graph(g_2)
	lrTest = LRPlanarityCheck(graph)
	print("Simple check: ", lrTest.simple_check())
	print("LR test: ", lrTest.run(), "\n")
	graph = Graph(g_3)
	lrTest = LRPlanarityCheck(graph)
	print("Simple check: ", lrTest.simple_check())
	print("LR test: ", lrTest.run(), "\n")
	graph = Graph(g_4)
	lrTest = LRPlanarityCheck(graph)
	print("Simple check: ", lrTest.simple_check())
	print("LR test: ", lrTest.run(), "\n")
	graph = Graph(g_5)
	lrTest = LRPlanarityCheck(graph)
	print("Simple check: ", lrTest.simple_check())
	print("LR test: ", lrTest.run(), "\n")
	graph = Graph(g_6)
	lrTest = LRPlanarityCheck(graph)
	print("Simple check: ", lrTest.simple_check())
	print("LR test: ", lrTest.run(), "\n")
	'''
	print("\nGraph by Dylan Emery (planar)")
	graph = numpy.empty((9, 9))
	graph.fill(0)
	graph[0][1] = 1
	graph[0][3] = 1
	graph[0][8] = 1
	graph[2][1] = 1
	graph[2][3] = 1
	graph[2][5] = 1
	graph[4][3] = 1
	graph[4][5] = 1
	graph[4][8] = 1
	graph[6][1] = 1
	graph[6][5] = 1
	graph[7][5] = 1
	graph[7][8] = 1
	graph += graph.T - numpy.diag(graph.diagonal())
	lrTest = LRPlanarityCheck(graph)
	print("Simple check: ", lrTest.simple_check())
	print("LR test: ", lrTest.run())
	print(graph)

	print("\nK3,3 (not planar)")
	graph = numpy.empty((6, 6))
	graph.fill(0)
	graph[0][3] = 1
	graph[0][4] = 1
	graph[0][5] = 1
	graph[1][3] = 1
	graph[1][4] = 1
	graph[1][5] = 1
	graph[2][3] = 1
	graph[2][4] = 1
	graph[2][5] = 1
	graph += graph.T - numpy.diag(graph.diagonal())
	lrTest = LRPlanarityCheck(graph)
	print("Simple check: ", lrTest.simple_check())
	print("LR test: ", lrTest.run())
	print(graph)
	'''

	alphabet = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
	for k in range(1, len(alphabet)):
		graph = {}
		for i in range(k):
			adj = []
			for j in range(k):
				if i != j:
					adj.append(alphabet[j])
			graph[alphabet[i]] = adj
		print("K", k, ":")
		lrTest = LRPlanarityCheck(Graph(graph))
		print("Simple check: ", lrTest.simple_check())
		start = datetime.datetime.now()
		result = lrTest.run()
		stop = datetime.datetime.now()
		print("LR test: ", result)
		print(stop-start, "\n")
