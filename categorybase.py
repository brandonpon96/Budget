import json

class SerializableNode:
	def __init__(self, name, subgroup, category = None):
		self.name = name
		self.category = category
		self.subgroup = subgroup

class CategoryNode:
	def __init__(self, category = None):
		self.words = {}
		self.category = category

	def loadWords(self, words):
		self.words = words

	def display(self, level):
		s = ""
		for l in range(level-1):
			s += '\t'
		if self.category != None:
			print s + ' - ' + self.category
		for word in self.words:
			s = ""
			for l in range(level):
				s += '\t'
			print s + word
			self.words[word].display(level+1)

class CategoryFinder:
	def __init__(self):
		self.node = CategoryNode()

	def __str__(self):
		self.node.display(0)
		return "\n"

	def loadFromNode(self, node):
		self.node = node

	def addCategory(self, business, category):
		business = business.lower()
		word_list = business.split()
		lastword = word_list[-1:][0]
		head = self.node
		for word in word_list:
			if word == lastword:
				if word not in head.words:
					head.words[word] = CategoryNode(category)
				else:
					if head.words[word].category != None and head.words[word].category != category:
						print "overwriting category " + head.words[word].category + " with " + category
					head.words[word].category = category
			else:
				if word not in head.words:
					head.words[word] = CategoryNode()
				head = head.words[word]
					

	def addKeyWord(self, keyword, category):
		keyword = keyword.lower()
		if keyword in self.node.words:
			if self.node.words[keyword].category != None and self.node.words[keyword].category != category:
				print "overwriting category " + self.node.words[keyword].category + " with " + category
			self.node.words[keyword].category = category
		else:
			self.node.words[keyword] = CategoryNode(category)

	def getCategory(self, business):
		verify_status = True
		business = business.lower()
		word_list = business.split()
		for i in range(len(word_list)):
			head = self.node
			business_match = ""
			for word in word_list[i:]:
				if word in head.words:
					business_match += word + " "
					if head.words[word].category != None:
						return (head.words[word].category, business_match[:-1], verify_status)
					head = head.words[word]
				else:
					verify_status = False
			if head == self.node:
				break
		return None

	def recurse_serialize(self, node, name):
		groups = []
		for word in node.words:
			groups.append(self.recurse_serialize(node.words[word], word))
		return SerializableNode(name, groups, node.category)

	def serialize(self):
		serialized = self.recurse_serialize(self.node, "base_node")
		fd = open("category_data.txt", 'w+')
		fd.write(json.dumps(vars(serialized), default=lambda o: o.__dict__, indent = 4))
		fd.close()

	def recurse_deserialize(self, data):
		words = {}
		for obj_data in data['subgroup']:
			words[obj_data['name']] = self.recurse_deserialize(obj_data)
		temp =  CategoryNode(data['category'])
		temp.loadWords(words)
		return temp

	def deserialize_category_finder(self, data):
		if 'category' in data and 'subgroup' in data:
			self.loadFromNode(self.recurse_deserialize(data))

	def deserialize(self):
		try:
			with open("category_data.txt", 'r+') as f:
				data = json.load(f)
				self.deserialize_category_finder(data)
		except:
			print "error opening category data"
			return




