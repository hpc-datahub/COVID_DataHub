import pandas as pd

df1 = pd.read_csv("/Volumes/Apoorv/RA-PublicHealth/COVID_DataHub/update_data.csv", header=0)

df2 = pd.read_csv("/Volumes/Apoorv/RA-PublicHealth/COVID_DataHub/Prepandemic/Prepandemic_v2.csv", header=0)

merged_df = df2.merge(df1, left_on='FIPS', right_on='FIPS')

merged_df.to_csv("/Volumes/Apoorv/RA-PublicHealth/COVID_DataHub/Prepandemic/Prepandemic_v2_fin.csv", header=True)
print(merged_df.head())