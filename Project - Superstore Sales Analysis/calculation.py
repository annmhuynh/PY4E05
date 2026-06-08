import data_process as dps
import pandas as pd

dir = "raw data"
dfs = dps.load_data(dir)

df_ords = dfs["Orders"] 
df_ppl  = dfs["People"]
df_rtns = dfs["Returns"]

df_ords = dps.process_data(df_ords)

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

def total_sales(condition=None, time=None):
    df = dfs["Orders"]
    if condition:
        df = apply_conditions(df, condition)
    if time is not None:
        return df.groupby(time)["Sales"].sum()
    return df["Sales"].sum()

def total_profit(condition=None, time=None):
    df = dfs["Orders"]
    if condition:
        df = apply_conditions(df, condition)
    if time is not None:
        return df.groupby(time)["Profit"].sum()
    return df["Profit"].sum()

def total_discount(condition=None, time=None):
    df = dfs["Orders"]
    if condition:
        df = apply_conditions(df, condition)
    if time is not None:
        return df.groupby(time)["Discount"].sum()
    return df["Discount"].sum()

def profit_margin(condition=None, time=None):
    df = dfs["Orders"]
    if condition:
        df = apply_conditions(df, condition)
    sales = total_sales(condition, time)
    profit = total_profit(condition, time)
    discount = total_discount(condition, time)
    return profit / (sales - discount) * 100

def total_customer(condition=None, time=None):
    df = dfs["Orders"]
    if condition:
        df = apply_conditions(df, condition)
    if time is not None:
        return df.groupby(time)["Customer ID"].nunique()
    return df["Customer ID"].nunique()

def total_order(condition=None, time=None):
    df = dfs["Orders"]
    if condition:
        df = apply_conditions(df, condition)
    if time is not None:
        return df.groupby(time)["Order ID"].count()
    return df["Order ID"].count()

def discount_analysis(condition=None):
    df = dfs["Orders"]
    if condition:
        df = apply_conditions(df, condition)   
    df["Net Sales"] = df["Sales"] * (1 - df["Discount"])
    df["Cost"] = df["Sales"] - df["Profit"]
    df["Adjusted Profit"] = df["Net Sales"] - df["Cost"]
    df["Profit Margin"] = df["Adjusted Profit"] / df["Net Sales"]
    discount_summary = df.groupby("Discount")[["Sales","Profit","Net Sales", "Adjusted Profit","Profit Margin"]].mean().reset_index()
    return discount_summary

# === PHÂN TÍCH DOANH THU ===
import plotly.graph_objects as go
import plotly.express as px

def kpi_dashboard(df_ords, condition=None): 
    kpis = {
        "Total Sales 💰"    : total_sales(condition),
        "Total Customers 👥": total_customer(condition),
        "Total Orders 📦"   : total_order(condition),
        "AOV 📊"            : (total_sales(condition) / total_order(condition)),
        "Profit Margin 📈"  : profit_margin(condition)
    }
    
    fig = go.Figure()
    n = len(kpis.items())
    fig.update_layout(
        autosize=True,
        height = 200,
        margin = dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white"
    )
    for i, (label, val) in enumerate(kpis.items()):
        x0 = i / n
        x1 = (i+1) / n       
        fig.add_shape(
            type="rect",
            xref="paper",
            yref="paper",
            x0=x0,
            x1=x1,
            y0=0,
            y1=1,
            fillcolor="#58867C",
            line=dict(color="#ffffff",width=10),
            layer="below"
        )
        fig.add_trace(go.Indicator(
            mode="number",
            value=val,
            number={
                "font": {
                    "color": "white",
                    "family": "Consolas",
                    "size": 47
                },
                "prefix": "$" if "Sales" in label or "AOV" in label else "",
                "suffix": "%" if "Margin" in label else ""
            },
            domain={'x': [x0, x1], 'y':[0,0.8]}
            )
        )
        fig.add_annotation(
            x=(x0+x1)/2,
            y=0.8,
            text=label,
            showarrow=False,
            font=dict(size=18, color="white"),
            xref="paper",
            yref="paper",
            xanchor="center"
        )
        
    return fig.to_html(full_html=False, include_plotlyjs="cdn", config={"responsive": True})

def fig_sales_by_year(condition=None):
    sales_by_year = total_sales(condition=condition,time="Year")
    if isinstance(sales_by_year, pd.Series):
        sales_by_year = sales_by_year.reset_index()
        sales_by_year.rename(columns={"index":"Year", "Sales": "Sales"}, inplace=True)
    fig = px.bar(
        sales_by_year,
        x="Year",
        y="Sales",
        text="Sales",
        color="Sales",
        color_continuous_scale="Turbo")
    fig.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        textfont=dict(
            size=13,
            color="#0F1B24",
            family="Helvetica"
        )
    )
    fig.update_layout( 
        font=dict(
            family="Tahoma",
            size=12,
            color="black"
        ),   
        xaxis=dict(
            title="Year",
            tickfont=dict(size=13, color="black", family="Tahoma"),
            type="category",
            tickmode="linear"
        ),
        yaxis=dict(
            title="Sales",
            tickfont=dict(size=13, color="black", family="Tahoma")
        ),
        hoverlabel=dict(
            font=dict(
                size=13,
                family="Arial"
            ),
            bgcolor="rgba(255,255,255,0.7)"
        ),
        
        autosize = True,
        xaxis_title_font=dict(size=15, color="black", family="Century Gothic"),
        yaxis_title_font=dict(size=15, color="black", family="Century Gothic"),
        margin=dict(l=20, r=20, t=25, b=20),
        paper_bgcolor="white"
    )
    fig.update_traces(
        hovertemplate=(
            "Year=%{x}<br>"
            "Sales=$%{y:,.0f}"
            "<extra></extra>"
        )
    )
    return fig.to_html(full_html=False, include_plotlyjs="cdn", config={"responsive": True})

def top_product(df, by="by", level="Product Name", top_n = 10, condition=None, time=None):
    if condition:
        df = apply_conditions(df, condition)
    if time is not None:
        grouped = df.groupby([time, level]).agg(
            **{
                "Sales": ("Sales", "sum"),
                "Profit": ("Profit", "sum"),
                "Discount": ("Discount", "sum"),
                "Total Orders": ("Order ID", "count")
            }).reset_index()
        grouped = grouped.sort_values(by=time)
        top_items = grouped.groupby(time).apply(
            lambda g: g.sort_values(by=by, ascending=False).head(top_n)
        ).reset_index(level=0)
    else:
        grouped = df.groupby(level).agg(
            **{
            "Sales": ("Sales", "sum"),
            "Profit": ("Profit", "sum"),
            "Discount": ("Discount", "sum"),
            "Total Orders": ("Order ID", "count")
            }).reset_index()
        grouped["Profit Margin"] = (grouped["Profit"] / (grouped["Sales"] - grouped["Discount"])) * 100
        top_items = grouped.sort_values(by=by, ascending=False).head(top_n)
    top_items.index = range(1, len(top_items)+1)
    return top_items

def fig_top_items(df, by="Sales", level="Product Name", top_n=5, condition=None, time=None):
    df = top_product(df, by=by, level=level, top_n=top_n, condition=condition, time=time)
    df = df.reset_index(drop=True)
    df["Rank"] = df.groupby(time).cumcount() + 1

    pivot = df.pivot(index="Rank", columns=time, values=level)

    fill_colors = []
    for i in pivot.index:
        shade = 255 - i*5 if 255 - i*5 > 80 else 80
        row_color = [f"rgb({shade}, {shade}, {255})"] * len(pivot.columns)
        fill_colors.append(row_color)

    fig = go.Figure(data = [go.Table(
        header = dict(
            values = ["Rank"] + list(pivot.columns),
            fill_color = "#467B9E",
            font = dict(color="white", size=13, family="Helvetica"),
            align = "center"
        ),
        cells = dict(
            values = [pivot.index] + [pivot[col].tolist() for col in pivot.columns],
            fill_color = [["#F9F9F9"] * len(pivot.index)] + fill_colors,
            align = "left",
            font = dict(size=13, family="Arial")
        )
    )])
    fig.update_layout(
        margin=dict(l=20, r=20, t=25, b=20),
        autosize = True,
        height = 450,
        paper_bgcolor = "white"
    )
    return fig.to_html(full_html=False, include_plotlyjs="cdn", config={"responsive": True})

def customer_segment(df, by="Sales", condition=None):
    df = apply_conditions(df, condition)
    df = df.groupby(["Year","Segment"])[by].sum().reset_index()
    df["%Segment"] = (
        df.groupby("Year")[by]
        .transform(lambda x: x/x.sum() * 100))
    df["Label"] = (
        df[by].map("${:,.0f}".format) 
        + " (" 
        + df["%Segment"].map("{:,.2f}".format) 
        + "%)"
    )
    fig = px.bar(
        df,
        x = "Year",
        y = "%Segment",
        color = "Segment",
        barmode = "stack",
        text = "Label"
    )
    for trace in fig.data:
        seg = trace.name
        seg_data = df[df["Segment"] == seg][["Segment", by, "%Segment"]].to_numpy()
        trace.customdata = seg_data
        trace.hovertemplate = (
            f"Year=%{{x}}<br>"
            f"Segment=%{{customdata[0]}}<br>"
            f"{by}=$%{{customdata[1]:,.0f}}<br>"
            f"%Segment=%{{customdata[2]:.2f}}%"
            "<extra></extra>"
        )
    fig.update_traces(
        texttemplate="%{text}",
        textposition="inside",
        textfont=dict(size=13, family="Helvetica")
        )
    fig.update_yaxes(title="Percent", ticksuffix="%")
    fig.update_layout(
        xaxis=dict(
            title="Year",
            tickfont=dict(size=13, color="black", family="Tahoma"),
            type="category",
            tickmode="linear"
        ),
        yaxis=dict(
            title="Percent",
            tickfont=dict(size=13, color="black", family="Tahoma")
        ),
        hoverlabel=dict(
            font=dict(
                size=13,
                family="Arial"
            ),
            bgcolor="rgba(255,255,255,0.7)"
        ),
        autosize = True,
        xaxis_title_font=dict(size=15, color="black", family="Century Gothic"),
        yaxis_title_font=dict(size=15, color="black", family="Century Gothic"),
        margin=dict(l=20, r=20, t=25, b=20),
        paper_bgcolor="white",
        legend=dict(
            title=dict(
                text="  Customer Segment  ",
                font=dict(
                    family="Tahoma",
                    size=12
                )
            ),
            orientation="v",
            bgcolor="rgba(200,200,200,0.3)",
            bordercolor="rgba(0,0,255,0.5)",
            borderwidth=1,
            itemwidth=30,
            font=dict(
                family="Arial",
                size=12
            )
        )
    )
    return fig.to_html(full_html=False, include_plotlyjs="cdn", config={"responsive":True})
