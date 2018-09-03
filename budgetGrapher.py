from transactionTree import TransactionTree
from transactionTree import TransactionNode
from transactionTree import Node
import matplotlib.pyplot as plt

class SpendGroup:
	def __init__(self):
		self.timeline = TransactionTree()

	def insertItem(self, node):
		month = int(node.val / 100)
		self.timeline.update(month, node.amount)

	def addDate(self, val):
		month = int(val / 100)
		if self.timeline.find(month) == None:
			self.timeline.update(month, 0)

	def get_timeline(self):
		costs = self.timeline.axis_array()
		print [x.amount for x in costs]
		return [x.amount for x in costs]


class BudgetGraph:
	def __init__(self):
		self.categories = {}
		self.populate_categories()

		self.master_timeline = TransactionTree()

	def populate_categories(self):
		categories = [
			"dining out",
			"transportation",
			"entertainment",
			"groceries",
			"hobby",
			"clothes",
			"personal care"
		]
		for c in categories:
			self.categories[c] = SpendGroup()

	def insert(self, node):
		if node.category not in self.categories:
			self.categories[node.category] = SpendGroup()

		self.addDate(node.val)
		for category in self.categories:
			self.categories[category].addDate(node.val)
		self.categories[node.category].insertItem(node)

	def addDate(self, val):
		month = int(val / 100)
		if self.master_timeline.find(month) == None:
			self.master_timeline.insert(Node(month))

	def get_timeline_axis(self):
		nodes = self.master_timeline.axis_array()
		timeline = [x.val for x in nodes]
		print timeline
		return [self.val_to_month(x) for x in timeline]

	def display_graph(self):
		category_totals = []
		x_axis = self.get_timeline_axis()
		for c in self.categories:
			print c
			y_axis = self.categories[c].get_timeline()
			category_totals.append(y_axis)
			plt.plot(x_axis, y_axis, label=c)
		total = [sum(x) for x in zip(*category_totals)]
		plt.plot(x_axis, total)
		plt.legend(loc='upper right')
		plt.show()


	def val_to_month(self, val):
		print val
		year = int(val / 100)
		month = int(val % 100)
		month_name = {
			1: "Jan\n" + str(year),
			2: "Feb",
			3: "Mar",
			4: "Apr",
			5: "May",
			6: "Jun",
			7: "Jul",
			8: "Aug",
			9: "Sep",
			10: "Oct",
			11: "Nov",
			12: "Dec"
		}
		return month_name.get(month, "invalid")




