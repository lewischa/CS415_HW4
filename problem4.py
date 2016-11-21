
# Node class is essentially one line of an adjacency list
# Each Node has a key, such as '1111', to represent number of
# A2s, A3s, A4s, and A5s, respectively
# Creating new Node will also generate a list[] of that node's edges
class Node:
	def __init__(self, key):
		self.key = key
		self.edges = []
		self.visited = False
		self.num_edges = 0
		self.populateEdges()

	def isLastEdge(self):
		if self.key == '0001': return True
		else: return False
		# key_digits = [int(char) for char in self.key]
		# last = len(key_digits) - 1
		# if key_digits[last] != 1: return False
		# else:
		# 	for i in range(last - 1):
		# 		if key_digits[i] != 0: return False
		# 	return True

	def generateEdge(self, pos):
		key_digits = [int(char) for char in self.key]
		key_digits[pos] = key_digits[pos] - 1
		pos = pos + 1
		for digit in range(pos, len(key_digits)):
			key_digits[digit] = key_digits[digit] + 1
		edge = ''.join([str(digit) for digit in key_digits])
		self.num_edges += 1
		return edge

	def populateEdges(self):
		if self.isLastEdge(): return
		for i, c in enumerate(self.key):
			if self.key[i] != "0":
				self.edges.append(self.generateEdge(i))
			else: continue

	def numEdges(self):
		return self.num_edges

	def printNode(self):
		print("Vertex: {}".format(self.key))
		print("Edges: {}".format(self.edges))

# This class is used to build the adjacency list
# Each node's edges are queued if they're not already there
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

# Stores the list of nodes (adjacency list) and
# the node queue to keep track of which nodes still
# need to be added to the list
class AdjacencyList:
	def __init__(self, key):
		self.adjList = []
		self.nodeQueue = NodeQueue()
		self.addFirst(key)
		self.buildList()

	# Add a node to the adjacency list
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

	# Find and return a node object based on its key
	def find(self, key):
		for each in self.adjList:
			if each.key == key:
				return each

	def printList(self):
		for each in self.adjList:
			each.printNode()

# Builds a graph (adjacency list) from given 'key'
# Topologically sorts the graph and stores it in 'sorted[]'
class Graph:
	def __init__(self, key):
		self.adjListObject = AdjacencyList(key)
		self.visited = []
		self.stack = []
		self.sorted = []
		self.top_sort()

	# Has the node associated with 'key' been visited? True/False
	def visited(self, key):
		return self.adjListObject.find(key).visited

	# Push a key/node onto the stack
	def push_stack(self, key):
		self.stack.append(key)

	# Delete and return most recently pushed element on stack
	def pop_stack(self):
		return self.stack.pop(len(self.stack) - 1)

	# Is the stack empty? True/False
	def empty_stack(self):
		return self.stack == []

	# Set visited to true for each node
	# If the node has no children, push to stack
	# Otherwise, explore each child recursively
	# Once all children are explored, push node to stack
	def explore(self, node):
		node.visited = True
		if node.numEdges() == 0:
			self.push_stack(node.key)
			return
		for edge in node.edges:
			if self.adjListObject.find(edge).visited:
				continue
			else:
				self.explore(self.adjListObject.find(edge))
		self.push_stack(node.key)
		return

	# Pop elements off stack into sorted[] array
	def fillSorted(self):
		while not self.empty_stack():
			self.sorted.append(self.pop_stack())

	# Top level topological sort handler
	def top_sort(self):
		for node in self.adjListObject.adjList:
			if node.visited:
				continue
			else: 
				self.explore(node)
		self.fillSorted()



x = Graph('1111')
print(x.sorted)

