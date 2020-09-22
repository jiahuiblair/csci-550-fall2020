import itertools

MINSUP = 15
MINCONF = 0.01

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
	def __init__(self, dept_name = set(), sup = 0, parent = "", children = [],c=0,rsup=0):
		self.dept_name = dept_name
		self.sup = sup
		self.children = children
		self.parent = parent
		self.c=c
		self.rsup=rsup
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
# root_node.print_children()

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

# for node in F:
# 	print(node.dept_name)



def find_support(dept_name, Frequent_set):
	for node in Frequent_set:
		if(len(node.dept_name.intersection(dept_name)) == len(dept_name)):
			return node.sup

def find_max_elem_len(setOfSets):
	max_elem_len = 0
	for aSet in setOfSets:
		if len(aSet) > max_elem_len:
			max_elem_len = len(aSet)
	return max_elem_len

class Rule:
	def __init__(self, X = set(), Y = set(), sup_Z = 0, c = 0, rsup=0, lift=0):
		self.X = X
		self.Y = Y
		self.sup_Z = sup_Z
		self.c = c
		self.rsup=rsup
		self.lift=lift

	def set_X(self, X):
		self.X = X
	def set_Y(self, Y):
		self.Y = Y
	def set_sup_Z(self, sup_Z):
		self.sup_Z = sup_Z
	def set_c(self, c):
		self.c = c
	def set_rsup(self, rsup):
		self.rsup = rsup
	def set_lift(self, lift):
		self.lift = lift


# generate set of strong rules
rules = []
# def associationRules(F,minconf):
for Z in F:

	if (len(Z.dept_name)>=2):
		# A = set(itertools.combinations(Z.dept_name))
		A = set()
		num_sets = len(Z.dept_name)
		
		for i in range(1,len(Z.dept_name)):
			tempset=[]
			tempset=set(itertools.combinations(Z.dept_name,i))
			A = A | (tempset)
		# print("The Z length is " + str(len(Z.dept_name)))
		while (len(A) > 0):

			# find the maximal element in A
			max_elem = set()
			max_elem_len = find_max_elem_len(A)
			for aSet in A:
				if (len(aSet) == max_elem_len):
					max_elem = aSet
					break
			# print("Z dept name is ") 
			# print(Z.dept_name)
			# print("max_elem is ")
			# print(max_elem)
			# print("A is ")
			# print(A)
			A.remove(max_elem)
			if (len(A) == 0):
				continue
			c = Z.sup / find_support(max_elem, F)
		
			if (c > MINCONF):
				newRule = Rule(X = set(max_elem).copy(), Y = A.copy(), sup_Z = Z.sup, c = c)
				rules.append(newRule)
			else:
				if (len(max_elem) > 1):
					for i in range(1,len(max_elem)):
						tempset=[]
						tempset=set(itertools.combinations(max_elem,i))
						for aSet in tempset:
							A.remove(aSet)
			# print("c value is " + str(c))


for rule in rules:
	print("This is a new rule >>>>>>>>>>>>>>>>>>>")
	print("X is " + str(rule.X) + " and Y is " + str(rule.Y))
	print("sup(Z) is " + str(rule.sup_Z))
	print("c is " + str(rule.c))

#print(str())
