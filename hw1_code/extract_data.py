############### load data into dataframe, output being df #######################


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


import numpy as np

df_mat = np.zeros([len(unique_txns),len(unique_depts)]).astype(int)



import pandas as pd 

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


# 	row = []
# 	for each column index, 
# 		if df[transaction id, column index] == 1
# 			row.append(df{})


# print(df.loc["16120100160021008773"].values)
# print(type(df["0369:YOUNG MENS"].values))

# df.to_csv("out.csv")


# data = pd.read_csv("txn_by_dept.csv")

# print(data.columns.values)
# print(data.index)
# print(data["POS Txn"][8])