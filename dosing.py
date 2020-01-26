import pandas as pd


#Read the following files into a dataframe
data_ec = pd.read_csv("./t2_ec 20190619.csv")
data_registry = pd.read_csv("./t2_registry 20190619.csv")

print(data_ec.head())
print(data_registry.head())

#Merge the dataframes:
merge_result_data = pd.merge(data_registry[['ID', 'RID', 'USERID', 'VISCODE', 'SVDOSE']], 
                        data_ec[['ECSDSTXT', 'RID', 'VISCODE']], 
                        on=['RID', 'VISCODE'], 
                        how='left')

print(merge_result_data.head())

#Filter records where:
merge_result_data = merge_result_data[(merge_result_data.VISCODE == 'w02') & (merge_result_data.SVDOSE == 'Y') & (merge_result_data.ECSDSTXT != 280)]

#Create and output a .csv file of the filtered records:
merge_result_data.to_csv("./results.csv", index = None, header = True)

print(merge_result_data.head())
