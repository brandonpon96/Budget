import re
import json
from categorybase import CategoryFinder
from transactionTree import TransactionTree
from transactionTree import TransactionNode
from budgetGrapher import BudgetGraph

category_list = {'d': 'dining out','t':'transportation','e': 'entertainment', 'g': 'groceries', 'h': 'hobbies', 'c': 'clothes', 'p': 'personal care'}

def parse_statement(statement):
	fd = open(statement, 'r')
	lines = fd.readlines()
	fd.close()

	begin = 0
	end = 0
	findstart = True

	for i in range(len(lines)):
		if findstart:
			if len(lines[i]) > 11 and lines[i][:11].lower() == "transaction":
				begin = i
				findstart = False
		else:
			if lines[i] == '\n':
				end = i
				break
	return lines[begin:end]

chase_regex = r"^([0-1]\d/[0-3]\d)\s(.+)\s(\d+\.\d\d)$"
starone_regex = r"^([0-1]\d/[0-3]\d/\d\d)\s[0-1]\d/[0-3]\d/\d\d\s(\d+\.\d\d)\s(.+)\s\d+$"
# s = "04/22 DENNY'S #7328 18007336 LOS ANGELES CA 21.05"
# m = re.match(chase_regex, s)
# # print m.group
# if m:
# 	print m.group(1)
# 	print m.group(2)
# 	print m.group(3)

def sanitize_input(text):
	clean = ''.join(i for i in text if ord(i)<128)
	clean.replace('*', ' ').replace(',', ' ')
	return clean

def parse_transactions(transactions, bank):

	regex = chase_regex
	if bank == "starone":
		regex = starone_regex
	for transaction in transactions:
		transaction = sanitize_input(transaction)
		m = re.match(regex, transaction)
		if m:
			business = m.group(2)
			category, business_match = determine_category(business)
			# print categoryFinder
			budget.insert(TransactionNode(m.group(1) + "/18", m.group(2), m.group(3), business_match, category))


def determine_category(business):
	# conn = sqlite3.connect('spending_tracker.db')
	# c = conn.cursor()
	category, business_match, verify_status = categoryFinder.getCategory(business)
	if category == None:
		category_input = raw_input("What is the category of " + business + "? [d] dining out [t] transportation [e] entertainment [g] groceries [h] hobbies [c] clothes [p] personal care: ")
		if category_input in category_list:
			category = category_list[category_input]
		else:
			while category_input not in category_list:
				category_input = raw_input("Please enter valid category. What is the category of " + business + "? [d] dining out [t] transportation [e] entertainment [g] groceries [h] hobbies [c] clothes [p] personal care: ")
			category = category_list[category_input]

		real_business = raw_input("actual name of business? ")
		keyword = raw_input("is there a keyword? n for none: ")

		categoryFinder.addCategory(real_business, category)

		if keyword != 'n' and keyword != 'N':
			categoryFinder.addKeyWord(keyword, category)
		return category
	return (category, business_match)

fd = open('input.txt', 'r')
transactions = fd.readlines()
fd.close()

categoryFinder = CategoryFinder()
categoryFinder.deserialize()

transaction_history = TransactionTree()
transaction_history.deserialize()

budget = BudgetGraph()
# parse_transactions(transactions, "chase")

for transaction in transaction_history.traverse():
	budget.insert(transaction)

budget.display_graph()


# transaction_history.serialize()
# categoryFinder.serialize()

# print categoryFinder




