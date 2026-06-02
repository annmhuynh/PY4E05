import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__)) 
raw_path = os.path.join(base_dir,"raw data")
                         
def load_data(dir):
    dfs = {}
    for filename in os.listdir(dir):
        if filename.endswith(".csv"):
            name = os.path.splitext(filename)[0]
            df = pd.read_csv(os.path.join(dir, filename))
            dfs[name] = df
    return dfs

dfs = load_data(raw_path)

def report_data(dfs_dict):
    for name, df in dfs_dict.items():
        print(f"\n=== Read file [{name}] ===")
        print(df.info())
        print(df.describe(include="all"))
        print("-"*50)

def convert_datetime(dfs_dict):
    report = {}
    for name, df in dfs_dict.items():
        for col in df.columns:
            if "Date" in col:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        report[name] = {
            "rows": df.shape[0],
            "cols": df.shape[1],
            "dtypes": df.dtypes.to_dict()
        }
    return dfs_dict

if __name__ == "__main__":
    dfs = load_data(raw_path)
    report_data(dfs)

    dfs = convert_datetime(dfs)
    report_data(dfs)