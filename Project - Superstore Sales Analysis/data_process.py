import pandas as pd
import os

base_path = os.path.dirname(os.path.abspath(__file__))
dir_path = os.path.join(base_path,"raw data")

def load_data(directory):
    dfs = {}
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            name = os.path.splitext(filename)[0]
            df = pd.read_csv(os.path.join(directory, filename))
            dfs[name] = df
    return dfs

def report_data(dfs_dict):
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

def process_data(df):
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"])
    df["Quarter"] = df["Order Date"].dt.to_period("Q")
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    return df

dfs = load_data(dir_path)

if __name__ == "__main__":
    report_data(dfs)