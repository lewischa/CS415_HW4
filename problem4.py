
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
		self.expectedA5 = 0
		self.A5isDone = False
		self.populateEdges()

	def isLastEdge(self, edge):
		numEdges = len(self.edges)
		if numEdges > 1:
			if self.edges[numEdges - 1] == edge:
				return True
			else:
				return False
		else:
			key_digits = [int(char) for char in self.key]
			lastDigit = len(key_digits) - 1
			if key_digits[lastDigit] != 0:
				return True
			else:
				return False


	def isFinalEdge(self):
		if self.key == '0001': return True
		else: return False
		# key_digits = [int(char) for char in self.key]
		# last = len(key_digits) - 1
		# if key_digits[last] != 1: return False
		# else:
		# 	for i in range(last - 1):
		# 		if key_digits[i] != 0: return False
		# 	return True

	# Calculates and returns the weight of the edge that is
	# currently being generated
	def getEdgeWeight(self, key_digits, pos):
		node_sum = 0
		for digit in key_digits:
			node_sum += digit
		edge_weight = key_digits[pos] / node_sum
		return edge_weight

	def generateEdge(self, pos):
		if type(self.key) is list:
			self.key = self.key[0]
		key_digits = [int(char) for char in self.key]
		edge_weight = self.getEdgeWeight(key_digits, pos)
		key_digits[pos] = key_digits[pos] - 1
		pos = pos + 1
		for digit in range(pos, len(key_digits)):
			key_digits[digit] = key_digits[digit] + 1
		edge = ''.join([str(digit) for digit in key_digits])
		self.num_edges += 1
		return [edge, edge_weight]

	def populateEdges(self):
		if self.isFinalEdge(): return
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
		if type(key) is list:
			self.queue.append(key[0])
		else:
			self.queue.append(key)

	# Delete and return first element in queue
	def dequeue(self):
		first = self.queue[0]
		del self.queue[0]
		return str(first)

	# Does the 'key' exist in the queue already? returns True/False
	def isQueued(self, key):
		if type(key) is list:
			key = key[0]
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
		self.initKey = key

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
		self.addFirst(self.initKey)
		while not self.nodeQueue.isEmpty():
			nextNode = self.nodeQueue.dequeue()
			nextNode = self.addNode(nextNode)
			self.addToQueue(nextNode)

	# Find and return a node object based on its key
	def find(self, key):
		if type(key) is list:
			key = key[0]
		for each in self.adjList:
			if each.key == key:
				return each

	def printList(self):
		for each in self.adjList:
			each.printNode()

# Builds a graph (adjacency list) from given 'key'
# Topologically sorts the graph and stores it in 'sorted[]'
# Provides the ability to calculate the number of A5's one
	# is expected to draw starting with 1 of each size sheet
class Graph:
	def __init__(self, key):
		self.adjListObject = AdjacencyList(key)
		self.adjListObject.buildList()
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

	# Recursively and iteratively calculate expected number of A5's
	def _calc_expectedA5(self, key):
		node = self.adjListObject.find(key)
		numEdges = len(node.edges)

		# Recursive 'break' condition:
			# Return if you're at the very last node ('0001')
		if numEdges == 0:
			self.adjListObject.find(key).expectedA5 = 0
			self.adjListObject.find(key).A5isDone = True
			return 0
		tempTotal = 0

		# Iterate through edges of every Node, recursively calculating
			# expected A5's for each node that Node points to
		for edge in node.edges:
			tempNode = self.adjListObject.find(edge[0])

			# If we've already calculated A5's for the node in edge[0], just use that instead
				# of making another recursive call
			if tempNode.A5isDone:
				if node.isLastEdge(edge):
					self.adjListObject.find(key).expectedA5 += (0 + tempNode.expectedA5) * edge[1]
				else:
					self.adjListObject.find(key).expectedA5 += tempNode.expectedA5 * edge[1]

			# Check if we need to add 1 to the calculation (if the edge corresponds to
				# pulling an A5)
			elif node.isLastEdge(edge):
				self.adjListObject.find(key).expectedA5 += (1 + self._calc_expectedA5(edge[0])) * edge[1]
			else:
				self.adjListObject.find(key).expectedA5 += self._calc_expectedA5(edge[0]) * edge[1]

		# We've iterated through each of Node's edges after the for loop,
			# so we are done calculating Node's expected A5. Set 'A5isDone' to True
			# and return expected A5.
		self.adjListObject.find(key).A5isDone = True
		return self.adjListObject.find(key).expectedA5

	# Top-level handler to call internal function w/ proper key
	# to calculate expected number of A5's
	def calc_expectedA5(self):
		tempNode = self.adjListObject.find('1111')
		if tempNode.A5isDone:
			return tempNode.expectedA5
		return self._calc_expectedA5('1111')
##########################    END CLASSES    ######################################



# Print list of options that user can enter
def printOptions():
	print(" ")
	print("***  OPTIONS  ***")
	print("1. Print adjacency list")
	print("2. Print topologically sorted dag")
	print("3. Calculate and print expected number of A5\'s")
	print(" ")

# Ask user for specific option (invalid input will be handled)
def gatherInput():
	printOptions()
	option = input("Enter your option (1, 2, or 3): ")
	while (option != '1') and (option != '2') and (option != '3'):
		print("That is not a valid option. Only 1, 2, or 3 are accepted.")
		option = input("Try again: ")
	return option

# Do the actual option that user selected (invalid option will be handled)
def runOption(option, graph):
	if option == '1':
		print("Adjacency List: ")
		graph.adjListObject.printList()
		return
	elif option == '2':
		print("\nTopologically Sorted Graph: \n")
		print(graph.sorted)
		return
	elif option == '3':
		print("\nExpected Number of A5\'s: \n")
		print(graph.calc_expectedA5())
		return
	else:
		print("There was an error with the option selected.\n")
		return

def main():
	print("\nCreating directed, acyclic graph beginning with node \'1111\'. . .")
	dag = Graph('1111')
	print("The graph has been created.\n")
	option = gatherInput()
	runOption(option, dag)
	again = input("\nWould you like to choose a different option (y/n)? ")
	again = again.lower()
	while again != 'n':
		while again != 'y':
			again = input("I didn't recognize that. Would you like to continue (y/n)? ")
			again = again.lower()
			if again == 'n':
				print("All done. Exiting . . .")
				exit()
		option = gatherInput()
		runOption(option, dag)
		again = input("\nWould you like to choose a different option (y/n)? ")
		again = again.lower()
	print("All done. Exiting . . .")
	exit()


if __name__ == "__main__":
	main()

