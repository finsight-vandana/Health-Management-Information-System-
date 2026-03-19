import pandas as pd
import glob
import os

folder = r"C:\Users\goyal\Downloads\Key Performance Indicators\2018_19\csv_files"

# get all csv files
files = glob.glob(os.path.join(folder, "*.csv"))

dataframes = []

for file in files:
    try:
        df = pd.read_csv(file)
        dataframes.append(df)
        print("Loaded:", os.path.basename(file))
    except Exception as e:
        print("Error:", file, e)

# merge all files
final_df = pd.concat(dataframes, ignore_index=True)

output = os.path.join(folder, "all_districts_merged.csv")

final_df.to_csv(output, index=False)

print("Merged dataset saved at:", output)