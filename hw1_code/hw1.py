import itertools

MINSUP = 20

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
	def __init__(self, dept_name = {}, sup = 0, parent = "", children = []):
		self.dept_name = dept_name
		self.sup = sup
		self.children = children
		self.parent = parent

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

def compute_support(k, node_list, data_frame):
	for aDict in data_frame:
		for key in aDict:
			# print("++++++++++++++++++++++++++++")
			# print(aDict[key])
			k_subset = itertools.combinations(aDict[key], k)
			for subset in k_subset:
				# print(set(subset))
				for node in node_list:
					if set(subset) == node.dept_name:
						node.sup += 1
	return node_list



D = load_tranc_db("transaction_db.txt")

F = []

root_node = Node(dept_name = {"root_node"})
root_node.print_children()

unique_level1_nodes = []
for unique_dept in unique_depts:
	root_node.append_child(Node(dept_name= {unique_dept}, sup = 0,parent = {"root_node"}))


# root_node.print_children()
k = 1

Ck = root_node.children

# for node in root_node.children:
# 	print("Dept name is " + str(node.dept_name) + ", sup is " + str(node.sup) + ", parent is " + str(node.parent))

while (len(Ck) != 0):
	updated_Ck = []
	Ck = compute_support(k, Ck, D)

	for node in Ck:
		if(node.sup >= MINSUP):
			F.append(node)
			updated_Ck.append(node)

	Ck = updated_Ck
	
	# put sibling nodes into same list
	groups = []
	existing_parent = []
	for i in range(len(Ck)):
		group = []
		current_parent = Ck[i].parent
		if current_parent not in existing_parent:
			group.append(Ck[i])
			existing_parent.append(Ck[i].parent)

			for j in range(i+1, len(Ck)):
				if Ck[j].parent == current_parent:
					group.append(Ck[j])
			groups.append(group)
		else:
			continue

	Ck = []
	for siblings in groups:
		for i in range(len(siblings)):
			for j in range(i+1, len(siblings)):
				temp = siblings[i].dept_name | siblings[j].dept_name
				if len(temp) == len(siblings[i].dept_name):
					continue
				else:
					temp_node = Node(dept_name = temp, sup = 0, parent = siblings[i].dept_name)
					Ck.append(temp_node)

	k = k + 1

for node in F:
	print(node.sup)





# generate set of strong rules


# rank rules 

