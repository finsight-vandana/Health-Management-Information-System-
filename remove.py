import pandas as pd

df = pd.read_csv("combined2_output.csv", header=None)

# STEP 1: Set header
df.columns = df.iloc[1]
df = df[2:]

# STEP 2: Remove 2018-19 columns (SAFE)
cols_to_keep = [col for col in df.columns if "2017-18" not in str(col)]
df = df[cols_to_keep]

# STEP 3: Remove duplicates but KEEP 'Sub District'
seen = set()
new_cols = []

for col in df.columns:
    if col == "Sub District":
        new_cols.append(col)  # always keep
    elif col not in seen:
        seen.add(col)
        new_cols.append(col)

df = df[new_cols]

# STEP 4: Remove extra header rows
df = df[~df.iloc[:, 0].astype(str).str.contains("Indicators", na=False)]

# STEP 5: Reset index
df.reset_index(drop=True, inplace=True)

# Save
df.to_csv("cleaned_output.csv", index=False)

print("✅ Done without error!")