
import pandas as pd

df = pd.read_csv("FINAL_DATASET_CLEAN.csv")

# Step 1: Normalize column names (remove .1, .2, etc.)
df.columns = df.columns.str.replace(r"\.\d+$", "", regex=True)

# Step 2: Remove duplicates (now they match)
df = df.loc[:, ~df.columns.duplicated()]

# Save
df.to_csv("final_output.csv", index=False)

print("✅ Removed .1, .2 duplicate columns!")