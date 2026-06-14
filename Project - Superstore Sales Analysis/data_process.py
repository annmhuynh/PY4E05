import pandas as pd
import os
from config import BASE_PATH, RAW_DATA_PATH, CLEAN_DATA_PATH

def load_data(directory):
    dfs = {}
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            name = os.path.splitext(filename)[0]
            file_path = os.path.join(directory, filename)
            
            if "Orders" in name:
                df = pd.read_csv(file_path, parse_dates=["Order Date", "Ship Date"])
            else:
                df = pd.read_csv(file_path)
            
            dfs[name] = df
    return dfs

def report_data(dfs_dict: dict):
    "\n[ Print Basic Report For DataFrame ]\n"
    for name, df in dfs_dict.items():
        print(f"\n==== Report for [{name}] ===")
        print("\n> Info:")
        df.info()
        print("\n> Describe:")
        print(df.describe(include="all"))
        print("\n> Missing values:")
        print(df.isnull().sum())
        print("\n> Unique values:")
        for col in df.select_dtypes(include=["object", "string"]).columns:
            unique_count = df[col].nunique()
            top_values = df[col].value_counts().head(5)
            print(f"\n [{col}: {unique_count} unique values]")
            print(top_values)         
        print("-"*50)

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    "\n[ Clean Data And Add Date Time Column ]\n"
    if "Order Date" in df.columns:
        df["Quarter"] = df["Order Date"].dt.to_period("Q")
        df["Year"] = df["Order Date"].dt.year
        df["Month"] = df["Order Date"].dt.month

    date_cols = [c for c in ["Order Date", "Ship Date"] if c in df.columns]
    if date_cols:
        df = df.dropna(subset=date_cols)

    type_num_data = df.select_dtypes(include=["number"]).columns
    for col in type_num_data:
        df[col] = df[col].fillna(0)
    
    type_str_data = df.select_dtypes(include=["str"]).columns
    for col in type_str_data:
        if len(type_str_data) > 0:
            df = df.dropna(subset=type_str_data)
    return df

def save_processed(df: pd.DataFrame, name: str):
    "\n[ Save Processed DataFrame To Folder ]\n"
    os.makedirs(CLEAN_DATA_PATH, exist_ok=True)
    out_path = os.path.join(CLEAN_DATA_PATH, f"{name}_clean.csv")
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"Save cleaned data to {out_path}")

if __name__ == "__main__":
    dfs = load_data(RAW_DATA_PATH)
    report_data(dfs)
    
    for name, df in dfs.items():
        clean_df = process_data(df)
        save_processed(clean_df, name)
    
    dfs_clean = load_data(CLEAN_DATA_PATH)
    report_data(dfs_clean)