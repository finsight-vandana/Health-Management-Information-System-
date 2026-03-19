import pandas as pd
import os
import re

# ---------------- PATH ----------------
parent_folder = r"C:\Users\goyal\Downloads\Key Performance Indicators\2012_13\csv_files"

# ---------------- STATE LIST ----------------
states = [
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh",
    "Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka",
    "Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram",
    "Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana",
    "Tripura","Uttar Pradesh","Uttarakhand","West Bengal"
]

all_data = []

# ---------------- LOOP THROUGH FILES ----------------
for root, dirs, files in os.walk(parent_folder):
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)

            try:
                # ---------------- LOAD ----------------
                df = pd.read_csv(file_path, header=None, low_memory=False)

                # ---------------- FIND HEADER ROW ----------------
                header_row = None
                for i in range(min(6, len(df))):
                    if df.iloc[i].astype(str).str.contains("Indicator", case=False, na=False).any():
                        header_row = i
                        break

                if header_row is None:
                    print(f"⚠️ Skipping (no header): {file}")
                    continue

                # set header
                df.columns = df.iloc[header_row]
                df = df.iloc[header_row + 1:]

                # ---------------- CLEAN COLUMN NAMES ----------------
                df.columns = df.columns.astype(str).str.strip()

                # keep ALL columns but rename duplicates safely
                new_cols = []
                col_count = {}

                for col in df.columns:
                    if col in col_count:
                        col_count[col] += 1
                        new_cols.append(f"{col}_{col_count[col]}")
                    else:
                        col_count[col] = 0
                        new_cols.append(col)

                df.columns = new_cols

                # ---------------- REMOVE YEAR COLUMNS ----------------
                df = df.loc[:, ~df.columns.str.contains("2011-12|2012-13", na=False)]

                # ---------------- REMOVE REPEATED HEADER ROWS ----------------
                df = df[
                    ~df.iloc[:, 0].astype(str).str.contains("Indicator|2012-13", na=False)
                ]

                # ---------------- EXTRACT STATE & DISTRICT ----------------
                name = file.replace(".csv", "")
                parts = name.split("_")

                # remove timestamp (last 2 parts)
                core_parts = parts[:-2]
                full_name = " ".join(core_parts)

                state = None
                district = None

                for s in states:
                    if full_name.startswith(s):
                        state = s
                        district = full_name.replace(s, "").strip()
                        break

                # fallback (just in case)
                if state is None:
                    state = core_parts[0]
                    district = " ".join(core_parts[1:])

                # clean formatting
                state = state.strip()
                district = district.strip()

                # ---------------- ADD COLUMNS ----------------
                df.insert(0, "district", district)
                df.insert(0, "state", state)

                all_data.append(df)

                print(f"✅ Processed: {file}")

            except Exception as e:
                print(f"❌ Error in file: {file}")
                print(e)

# ---------------- COMBINE ----------------
final_df = pd.concat(all_data, ignore_index=True)

# ---------------- SAVE ----------------
output_path = os.path.join(parent_folder, "FINAL_DATASET_CLEAN.csv")
final_df.to_csv(output_path, index=False)

print("🎉 FINAL DATASET CREATED SUCCESSFULLY!")