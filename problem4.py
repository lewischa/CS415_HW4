class Node():
	def __init__(self, key):
		self.key = key
		self.edges = []
		self.populateEdges()

	def generateEdge(self, pos):
		key_digits = [int(char) for char in self.key]
		key_digits[pos] = key_digits[pos] - 1
		pos = pos + 1
		for digit in range(pos, len(key_digits)):
			key_digits[digit] = key_digits[digit] + 1
		edge = ''.join([str(digit) for digit in key_digits])
		return edge

	def populateEdges(self):
		for i, c in enumerate(self.key):
			if self.key[i] != "0":
				self.edges.append(self.generateEdge(i))
			else: continue

	def printNode(self):
		print("Vertex: {}".format(self.key))
		print("Edges: {}".format(self.edges))

x = Node('1111')
x.printNode()
x = Node('0222')
x.printNode()
x = Node('1022')
x.printNode()