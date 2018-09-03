
class MonthNode:
    def __init__(self, val, amount):
        #val is the month
        self.val = val
        self.transactions = []
        self.amount = amount
        self.leftChild = None
        self.rightChild = None

    def addCost(self, cost):
        self.amount += cost

class TransactionNode:
    def __init__(self, date, name, amount, business_match, category, val = None):
        self.date = date
        self.name = name
        self.amount = float(amount)
        self.business_match = business_match
        self.category = category
        self.leftChild = None
        self.rightChild = None

        self.val = int(val) if val != None else self.getValFromDate()

    def __str__(self):
        return self.date + "," + self.name + "," + str(self.amount) + "," + self.business_match + "," + self.category + "," + str(self.val) + '\n'
    
    def getValFromDate(self):
        date_split = self.date.split('/')
        return int(date_split[2] + date_split[0] + date_split[1])

    def get(self):
        return self.val
    
    def set(self, val):
        self.val = val
        
    def getChildren(self):
        children = []
        if(self.leftChild != None):
            children.append(self.leftChild)
        if(self.rightChild != None):
            children.append(self.rightChild)
        return children

class Node:
    def __init__(self, val):
        self.val = val
        self.leftChild = None
        self.rightChild = None

class TransactionTree:
    def __init__(self):
        self.root = None

    def setRoot(self, root_node):
        self.root = root_node

    def insert(self, node):
        # node = self.node_from_text(transaction_text)
        if(self.root is None):
            self.setRoot(node)
        else:
            self.insertNode(self.root, node)

    def insertNode(self, currentNode, node):
        if(node.val <= currentNode.val):
            if(currentNode.leftChild):
                self.insertNode(currentNode.leftChild, node)
            else:
                currentNode.leftChild = node
        elif(node.val > currentNode.val):
            if(currentNode.rightChild):
                self.insertNode(currentNode.rightChild, node)
            else:
                currentNode.rightChild = node

    def update(self, val, amount):
        m = self.find(val)
        if m != None:
            m.addCost(amount)
        else:
            self.insert(MonthNode(val, amount))

    def find(self, val):
        return self.findNode(self.root, val)

    def findNode(self, currentNode, val):
        if(currentNode is None):
            return None
        elif(val == currentNode.val):
            return currentNode
        elif(val < currentNode.val):
            return self.findNode(currentNode.leftChild, val)
        else:
            return self.findNode(currentNode.rightChild, val)

    def recurse_serialize(self, node, fd):
        if node == None:
            return
        if node.leftChild != None:
            self.recurse_serialize(node.leftChild, fd)
        fd.write(str(node))
        if node.rightChild != None:
            self.recurse_serialize(node.rightChild, fd)

    def serialize(self):
        fd = open('transaction_data.txt', 'w+')
        self.recurse_serialize(self.root, fd)
        fd.close()

    def helper(self, node):
        if node == None:
            return
        if node.leftChild != None:
            self.helper(node.leftChild)
        print node.val
        if node.rightChild != None:
            self.helper(node.rightChild)

    def print_nodes(self):
        self.helper(self.root)

    def axis_array(self):
        array = []
        node_stack = []
        current = self.root
        done = 0
        while not done:
            if current != None:
                node_stack.append(current)
                current = current.leftChild
            else:
                if len(node_stack) > 0:
                    current = node_stack.pop()
                    array.append(current)
                    current = current.rightChild
                else:
                    done = 1

        return array


    def node_from_text(self, text):
        properties = text.split(',')
        return TransactionNode(properties[0], properties[1], properties[2], properties[3], properties[4], int(properties[5]))


    def recurse_deserialize(self, begin, end, transaction_text):
        if begin > end:
            return None
        middle = (begin + end) / 2
        node = self.node_from_text(transaction_text[middle])
        node.leftChild = self.recurse_deserialize(begin, middle - 1, transaction_text)
        node.rightChild = self.recurse_deserialize(middle + 1, end, transaction_text)
        return node

    def deserialize(self):
        try:
            fd = open('transaction_data.txt', 'r+')
            transaction_text = fd.readlines()
            fd.close()

            node = self.recurse_deserialize(0, len(transaction_text)-1, transaction_text)
            self.setRoot(node)
        except:
            print "error opening transaction data"
            return

    def traverse_recurse(self, node):
        if node is None:
            return
        if node.leftChild is not None:
            for x in self.traverse_recurse(node.leftChild) :
                # you need to *re-yield* the elements of the left and right child
                yield x
        yield node
        if node.rightChild is not None:
            for x in self.traverse_recurse(node.rightChild) :
                yield x

    def traverse(self):
        return self.traverse_recurse(self.root)
        




        


