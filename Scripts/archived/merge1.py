import pandas as pd

df1 = pd.read_csv("/Users/apoorvdayal/Desktop/RA-PublicHealth/Suru_Data/acs.csv", header=1)

df2 = pd.read_csv("/Users/apoorvdayal/Desktop/RA-PublicHealth/Suru_Data/fina.csv", header=0)

merged_df = df2.merge(df1, left_on='FIPS', right_on='FIPS')

merged_df.to_csv("/Users/apoorvdayal/Desktop/RA-PublicHealth/Suru_Data/fin.csv", header=True)
print(merged_df.head())