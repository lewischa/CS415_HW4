
# Node class is essentially one line of an adjacency list
# Each Node has a key, such as '1111', to represent number of
# A2s, A3s, A4s, and A5s, respectively
# Creating new Node will also generate a list[] of that node's edges
class Node:
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

class NodeQueue:
	def __init__(self):
		self.queue = []

	# Add to end of queue
	def enqueue(self, key):
		self.queue.append(key)

	# Delete and return first element in queue
	def dequeue(self):
		first = self.queue[0]
		del self.queue[0]
		return str(first)

	# Does the 'key' exist in the queue already? returns True/False
	def isQueued(self, key):
		for each in self.queue:
			if each == key: return True
		return False

	# Is the queue empty? Returns True/False
	def isEmpty(self):
		return self.queue == []

	def length(self):
		return len(self.queue)


class AdjacencyList:
	def __init__(self, key):
		self.adjList = []
		self.nodeQueue = NodeQueue()
		self.addFirst(key)
		self.buildList()
	def addNode(self, key):
		if type(key) is Node:
			self.adjList.append(key)
		else:
			key = Node(key)
			self.adjList.append(key)
		return key

	# Add first row to adjacency list
	def addFirst(self, key):
		node1 = Node(key)
		self.addNode(node1)
		for each in node1.edges:
			if not self.nodeQueue.isQueued(each):
				self.nodeQueue.enqueue(each)

	# Add new vertices to queue that are not currently in it
	def addToQueue(self, node):
		for each in node.edges:
			if not self.nodeQueue.isQueued(each):
				if each != '0000':
					self.nodeQueue.enqueue(each)

	# Build the adjacency list after the first row
	def buildList(self):
		while not self.nodeQueue.isEmpty():
			nextNode = self.nodeQueue.dequeue()
			nextNode = self.addNode(nextNode)
			self.addToQueue(nextNode)

	def printList(self):
		for each in self.adjList:
			each.printNode()


x = AdjacencyList('1111')
i = 0
for each in x.adjList:
	each.printNode()
	i = i + 1
print("There are {} vertices.".format(i))

