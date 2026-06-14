import data_process as dps
import pandas as pd
from config import CLEAN_DATA_PATH

dfs = dps.load_data(CLEAN_DATA_PATH)
df_ords = dfs["Orders_clean"]
df_ppl = dfs["People_clean"]
df_rtns = dfs["Returns_clean"]

def apply_conditions(df, condition):
    mask = pd.Series(True, index=df.index)
    for col, val in condition.items():
        if val:
            if col == "start_date":
                mask &= df["Order Date"] >= pd.to_datetime(val)
            elif col == "end_date":
                mask &= df["Order Date"] <= pd.to_datetime(val)
            else:
                mask &= df[col] == val
    return df[mask]

def format_currency(val):
    if val < 0:
        return f"$({abs(val):,.2f})"
    else:
        return f"${val:,.2f}"
 
def total_sales(df, condition=None, time=None):
    if condition:
        df = apply_conditions(df, condition)
    if time is not None:
        return df.groupby(time)["Sales"].sum()
    return df["Sales"].sum()

def total_profit(df, condition=None, time=None):
    if condition:
        df = apply_conditions(df, condition)
    if time is not None:
        return df.groupby(time)["Profit"].sum()
    return df["Profit"].sum()

def total_discount(df, condition=None, time=None):
    if condition:
        df = apply_conditions(df, condition)
    if time is not None:
        return df.groupby(time)["Discount"].sum()
    return df["Discount"].sum()

def profit_margin(df, condition=None, time=None):
    if condition:
        df = apply_conditions(df, condition)
    sales = total_sales(df, condition, time)
    profit = total_profit(df, condition, time)
    discount = total_discount(df, condition, time)
    return profit / (sales - discount) * 100

def total_customer(df, condition=None, time=None):
    if condition:
        df = apply_conditions(df, condition)
    if time is not None:
        return df.groupby(time)["Customer ID"].nunique()
    return df["Customer ID"].nunique()

def total_order(df, condition=None, time=None):
    if condition:
        df = apply_conditions(df, condition)
    if time is not None:
        return df.groupby(time)["Order ID"].count()
    return df["Order ID"].count()

def discount_analysis(df, condition=None, agg="mean", by=None):
    if condition:
        df = apply_conditions(df, condition)   
    df["Net Sales"] = df["Sales"] * (1 - df["Discount"])
    df["Cost"] = df["Sales"] - df["Profit"]
    df["Adjusted Profit"] = df["Net Sales"] - df["Cost"]
    df["Profit Margin"] = df["Adjusted Profit"] / df["Net Sales"]
    
    metrics = ["Sales", "Profit", "Net Sales", "Adjusted Profit", "Profit Margin"]

    if by:
        group_col = [by]
        if agg == "mean":
            discount_summary = df.groupby(group_col)[metrics].mean().reset_index()
        elif agg == "sum":
            discount_summary = df.groupby(group_col)[metrics].sum().reset_index()
        discount_summary["Average Discount"] = df.groupby(by)["Discount"].mean().values
        if by == "Sub-Category":
            discount_summary = discount_summary.merge(
                df[["Sub-Category", "Category"]].drop_duplicates(),
                on="Sub-Category",
                how="left"
            )
    else:
        group_col = ["Discount"]
        if agg == "mean":
            discount_summary = df.groupby(group_col)[metrics].mean().reset_index()
        elif agg == "sum":
            discount_summary = df.groupby(group_col)[metrics].sum().reset_index()   
    return discount_summary
