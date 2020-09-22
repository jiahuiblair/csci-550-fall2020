import itertools
import numpy as np
import pandas as pd 

import sys

MINSUP =  15# int(sys.argv[1])
MINCONF = 0.1 # float(sys.argv[2])
k = 5 # int(sys.argv[3])

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
	def __init__(self, dept_name = set(), sup = 0, parent = "", children = [],c=0,r_sup=0):
		self.dept_name = dept_name
		self.sup = sup
		self.children = children
		self.parent = parent
		self.c=c
		self.r_sup=r_sup
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
	def __init__(self, X = set(), Y = set(), sup_Y = 0, sup_Z = 0, c = 0, r_sup=0, lift=0):
		self.X = X
		self.Y = Y
		self.sup_Y = sup_Y
		self.sup_Z = sup_Z
		self.c = c
		self.r_sup=r_sup
		self.lift=lift

	def set_X(self, X):
		self.X = X
	def set_Y(self, Y):
		self.Y = Y
	def set_sup_Y(self, sup_Y):
		self.sup_Y = sup_Y
	def set_sup_Z(self, sup_Z):
		self.sup_Z = sup_Z
	def set_c(self, c):
		self.c = c
	def set_r_sup(self, r_sup):
		self.r_sup = r_sup
	def set_lift(self, lift):
		self.lift = lift

def run(file_path, MINSUP, MINCONF, k):

	data, colnames = read_csv(file_path)

	unique_txns = set([data[i][0] for i in range(len(data))] )
	unique_depts = set([data[i][1] for i in range(len(data))] )

	unique_txns  = list(unique_txns)
	unique_depts = list(unique_depts)
	df_mat = np.zeros([len(unique_txns),len(unique_depts)]).astype(int)

	df = pd.DataFrame(np.array(df_mat), index = unique_txns, columns = unique_depts)

	for item in data: 
		row_index = item[0]
		column_index = item[1]

		df.loc[row_index, column_index] += 1

	transaction_db = []
	# for each transaction id
	for row in df.index.values:
		row_data = []

		for col in df.columns.values:
			if df.loc[row, col] == 1:
				row_data.append(col)
		row_data = {row: row_data}
		transaction_db.append(row_data)

	D = transaction_db
	with open("transaction_db.txt", 'w') as file:
		for item in D:
			for key,values in item.items():
				file.write(key + "," + ",".join(values) + "\n")



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

				A.remove(max_elem)
				if (len(A) == 0):
					continue
				c = Z.sup / find_support(max_elem, F)
			
				if (c > MINCONF):

					# sup_Y = find_support(set(A.copy()), F)

					Y = Z.dept_name.copy()
					
					for item in max_elem:
						Y.remove(item)

					sup_Y = find_support(Y, F)

					newRule = Rule(X = set(max_elem).copy(), Y = Y.copy(), sup_Y = sup_Y, sup_Z = Z.sup, c = c)
					rules.append(newRule)
				else:
					if (len(max_elem) > 1):
						for i in range(1,len(max_elem)):
							tempset=[]
							tempset=set(itertools.combinations(max_elem,i))
							for aSet in tempset:
								A.remove(aSet)


	rule_list_for_ranking_lift = {}
	rule_list_for_ranking_rsup = {}

	for i,rule in enumerate(rules):
		rule.set_r_sup(rule.sup_Z / len(unique_txns))
		rule.set_lift(rule.c / rule.sup_Y)
		print("This is a rule >>>>>>>>>>>>>>>>>>>")
		print("X is " + str(rule.X) + " and Y is " + str(rule.Y))

		print("sup(Y) is " + str(rule.sup_Y))
		print("sup(Z) is " + str(rule.sup_Z))

		print("c is " + str(rule.c))
		lift = rule.c /(rule.sup_Y / len(unique_txns))
		print("lift is " + str(lift) + "\n\n\n")

		# temp_dict = {}
		# temp_dict[abs(lift -1)] = str(rule.X) + "---->" + str(rule.Y)
		rule_list_for_ranking_lift[str(abs(lift -1))] = str(rule.X) + "---->" + str(rule.Y)
		rule_list_for_ranking_rsup[str(rule.sup_Z)] = str(rule.X) + "---->" + str(rule.Y)


	rule_list_lift = sorted(rule_list_for_ranking_lift, reverse = True)
	rule_list_rsup = sorted(rule_list_for_ranking_rsup, reverse = False)

	# print(rule_list_for_ranking_lift)
	print("Ranking based on lift value >>>>>>>>>>>>>>")
	i = 0
	for rule in rule_list_lift:
		if i < k:
			print(str(rule) + ":" + rule_list_for_ranking_lift[rule])
			i += 1

	print("Ranking based on relative support value >>>>>>>>>>>>>>")
	j = 0
	for rule in rule_list_rsup:
		if (j < k):
			print(str(rule) + ":" + rule_list_for_ranking_rsup[rule])
			j += 1
if __name__ == '__main__':
	run("txn_by_dept.csv", MINSUP, MINCONF, k)