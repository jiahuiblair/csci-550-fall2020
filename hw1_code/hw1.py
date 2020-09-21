def read_csv(file_path):
	colnames = ""
	temp_mat = []
	with open(file_path, 'r') as file:
		lines = file.readlines()
	
	colnames = lines[0].strip().split(",")
	lines = lines[1:]
	for line in lines:
		row = line.strip().split(",")
		temp_mat.append(row)
	return temp_mat,colnames

data, colnames = read_csv("txn_by_dept.csv")

unique_txns = set([data[i][0] for i in range(len(data))] )
unique_depts = set([data[i][1] for i in range(len(data))] )

unique_txns  = list(unique_txns)
unique_depts = list(unique_depts)


def load_tranc_db(file_path):
	D = []
	with open(file_path, 'r') as file:
		lines = file.readlines()
	for line in lines:
		row_data = line.strip().split(",")
		transac_id = row_data[0]
		depts = row_data[1:]
		row_data = {transac_id: depts}
		D.append(row_data)
	return D


############################### generate frequent itemset
############   input: dataframe df, unique_depts, minsup
############   output: Frequent item set
class Node:
	def __init__(self, dept_name = "", sup = 0, parent = "", children = []):
		self.dept_name = dept_name
		self.sup = sup
		self.children = children
		self.parent = ""

	def set_dept_name(self, name):
		self.dept_name = name 
	def set_sup(self,sup):
		self.sup = sup
	def incre_sup(self):
		self.sup += 1
	def clean_sup(self):
		self.sup =0 

	def append_child(self, aNode):
		self.children.append(aNode)

	def print_children(self):

		for child in self.children:
			print(child.dept_name)

# def compute_support(node_list, data_frame):
# 	for 



D = load_tranc_db("transaction_db.txt")

F = []

root_node = Node(dept_name = "root_node")
root_node.print_children()

unique_level1_nodes = []
for unique_dept in unique_depts:
	root_node.append_child(Node(dept_name= unique_dept, parent = root_node))

# root_node.print_children()
k = 1

Ck = root_node.children

# while(len(Ck) != 0): 
	# compute support
	# check removal of X from Ck
	# extend tree 
	# k = k + 1




# generate set of strong rules


# rank rules 

