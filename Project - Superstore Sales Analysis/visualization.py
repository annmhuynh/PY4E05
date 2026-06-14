import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import pandas as pd
import numpy as np
import calculation as cal

visualization_template = go.layout.Template(
    layout=dict(
        autosize = True,
        margin=dict(l=40, r=40, t=50, b=40),
        paper_bgcolor="rgba(250,250,250,0.54)",
        bargap=0.25,
        title=dict(
            font=dict(
                size=20,
                family="Roboto",
                color="darkred",
            ),
            x=0,
            xanchor="left",
            y=0.95,
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#EBE7E7",
            title=dict(
                font=dict(
                    size=15,
                    color="#101802",
                    family="Century Gothic"
                ),
                standoff=10,
            ),
            tickfont=dict(
                size=13,
                color="black",
                family="Tahoma",
            ),
            automargin=True,
            autorange=True,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#EBE7E7",
            title=dict(
                font=dict(
                    size=15,
                    color="#101802",
                    family="Century Gothic"
                ),
                standoff=10,
            ),
            tickfont=dict(
                size=13,
                color="black",
                family="Tahoma",
            ),
            automargin=True,
            autorange=True,
        ),
        hoverlabel=dict(
            bgcolor="rgba(255,255,255,0.7)",
            font_size=13,
            font_family="Arial"
        ),
        legend=dict(
            title=dict(
                font=dict(
                    family="Tahoma",
                    size=12
                ),
            ),
            bgcolor="rgba(200,200,200,0.3)",
            bordercolor="rgba(0,0,255,0.5)",
            borderwidth=1,
            itemwidth=30,
            font=dict(
                family="Arial",
                size=13
            )
        ),
    ),
    data=dict(
            bar=[dict(
                textfont=dict(
                    size=13.5,
                    family="Arial",
                ),
            )],
            indicator=[dict(
                mode="number",
                number=dict(
                    font=dict(
                    size=18,
                    color="#DCFFE7",
                    ),
                ),
            )],
        ),
)
pio.templates["template"] = visualization_template
pio.templates.default = "template"

def render(fig, full_html=False, include_plotlyjs="cdn"):
    return fig.to_html(
        full_html=full_html,
        include_plotlyjs=include_plotlyjs,
        config={"responsive": True}
    )

def kpi_dashboard(df, condition=None): 
    kpis = {
        "Total Sales 💰"    : cal.total_sales(df, condition),
        "Total Customers 👥": cal.total_customer(df, condition),
        "Total Orders 📦"   : cal.total_order(df, condition),
        "AOV 📊"            : (cal.total_sales(df, condition) / cal.total_order(df, condition)),
        "Profit Margin 📈"  : cal.profit_margin(df, condition)
    } 
    fig = go.Figure()
    n = len(kpis.items())
    fig.update_layout(
        autosize=True,
        height = 150,
        margin = dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(240,250,240,0.54)"
    )
    for i, (label, val) in enumerate(kpis.items()):
        if isinstance(val, pd.Series):
            val = val.sum()
        font_size = max(28, int(80 / n))
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
            fillcolor="#365C8D",
            line=dict(color="#ffffff",width=13),
            layer="below"
        )
        fig.add_trace(go.Indicator(
            mode="number",
            value=val,
            number={
                "font": dict(family="Comic Sans MS, Arial, sans-serif", size=font_size, color="white"),
                "prefix": "$" if "Sales" in label or "AOV" in label else "",
                "suffix": "%" if "Margin" in label else ""
            },
            domain={'x': [x0, x1], 'y':[0,0.8]}
        ))
        fig.add_annotation(
            x=(x0+x1)/2,
            y=0.8,
            text=label,
            showarrow=False,
            font=dict(size=font_size//2, color="white"),
            xref="paper",
            yref="paper",
            xanchor="center"
        )
        
    return render(fig)

def fig_sales_by_year(df, condition=None):
    sales_by_year = cal.total_sales(df, condition=condition,time="Year")
    if isinstance(sales_by_year, pd.Series):
        sales_by_year = sales_by_year.reset_index()
        sales_by_year.columns= ["Year", "Sales"]

    fig = px.bar(
        sales_by_year,
        x="Year",
        y="Sales",
        text="Sales",
        color="Sales",
        color_continuous_scale="agsunset"
    )
    fig.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside",
        hovertemplate=(
            "Year=%{x}<br>"
            "Sales=$%{y:,.0f}"
            "<extra></extra>"
        )
    )
    fig.update_layout(
        title=dict(
            text="Sales by Year",
        ),
        xaxis=dict(
            type="category",
            tickmode="linear",
        ),
        yaxis=dict(
            title="Sales ($)"
        )
    )
    return render(fig)

def fig_profit_and_margin_by_year(df, condition=None):
    profit_year = cal.total_profit(df, condition=condition, time="Year")
    if isinstance(profit_year, pd.Series):
        profit_year = profit_year.reset_index()
        profit_year.columns = ["Year", "Profit"]

    pm_data = cal.profit_margin(df, condition=condition, time="Year")
    if isinstance(pm_data, pd.Series):
        pm_data = pm_data.reset_index()
        pm_data.columns = ["Year", "Profit Margin"]

    merged = profit_year.merge(pm_data, on="Year")


    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=merged["Year"],
        y=merged["Profit"],
        name="Profit",
        text=merged["Profit"],
        texttemplate="$%{text:,.0f}",
        marker_color="#ffc6f6",
        hovertemplate=(
            "Year=%{x}<br>"
            "Profit=$%{y:,.0f}<br>"
            "<extra></extra>"
        ),
    ))
    fig.add_trace(go.Scatter(
        x=merged["Year"],
        y=merged["Profit Margin"],
        name="Profit Margin",
        text=merged["Profit Margin"],
        texttemplate="%{text:,.2f}%",
        mode="lines+markers+text",
        textposition="top right",
        marker=dict(
            color="#3c0763",
            size=8,
        ),
        yaxis="y2",
        hovertemplate=(
            "Year=%{x}<br>"
            "Profit Margin=%{y:,.2f}%"
            "<extra></extra>"
        ),
    ))
    fig.update_layout(
        title="Profit & Profit Margin by Year",
        xaxis=dict(
            type="category",
            tickmode="linear",
        ),
        yaxis=dict(
            title="Profit ($)",
        ),
        yaxis2=dict(
            title="Profit Margin (%)",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        legend=dict(
            orientation="h",
            y=-0.2,
        )
    )
    return render(fig)
   
def fig_discount_analysis_mean(df, condition=None):
    summary_mean = cal.discount_analysis(df, condition=condition, agg="mean")
    cols = ["Sales", "Profit", "Net Sales", "Adjusted Profit"]
    fmt_cols = []
    for col in cols:
        fmt_cols.append(summary_mean[col].apply(cal.format_currency))
    customdata = list(zip(*fmt_cols))
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=summary_mean["Discount"],
        y=summary_mean["Profit Margin"],
        name="Profit Margin",
        customdata=customdata,
        marker_color="#6a0dad",
        hovertemplate=(
            "Discount=%{x}<br>"
            "Profit Margin=%{y}<br>"
            "Sales=%{customdata[0]}<br>"
            "Profit=%{customdata[1]}<br>"
            "Net Sales=%{customdata[2]}<br>"
            "Adjusted Profit=%{customdata[3]}"
            "<extra></extra>"
        )
    ))
    fig.update_layout(
        title=dict(
            text="Impact of Discounts on Profit Margin (Average Order Value)",
        ),
        xaxis=dict(
            title="Discount(%)",
            tickformat=".0%",
        ),
        yaxis=dict(
            title="Profit Margin(%)",
            tickformat=".0%",
        ),
    )
    return render(fig)

def fig_discount_analysis_sum(df, condition=None):
    summary_sum = cal.discount_analysis(df, condition=condition, agg="sum")
    cols = ["Sales", "Profit", "Net Sales", "Adjusted Profit"]
    fmt_cols = []
    for col in cols:
        fmt_cols.append(summary_sum[col].apply(cal.format_currency))
    customdata = list(zip(*fmt_cols))
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=summary_sum["Discount"],
        y=summary_sum["Profit Margin"],
        name="Profit Margin",
        customdata=customdata,
        marker_color="#6a0dad",
        hovertemplate=(
            "Discount=%{x}<br>"
            "Profit Margin=%{y}<br>"
            "Sales=%{customdata[0]}<br>"
            "Profit=%{customdata[1]}<br>"
            "Net Sales=%{customdata[2]}<br>"
            "Adjusted Profit=%{customdata[3]}"
            "<extra></extra>"
        )
    ))
    fig.update_layout(
        title=dict(
            text="Impact of Discounts on Profit Margin (Total Sales Contribution)",
        ),
        xaxis=dict(
            title="Discount(%)",
            tickformat=".0%",
        ),
        yaxis=dict(
            title="Profit Margin(%)",
            tickformat=".0%",
        ),
        bargap=0.1,
    )
    return render(fig)


# ===========================
# CUSTOMERS ANALYSIS
# ===========================

customer_color_map = {
        "Consumer": "#C1FFE7",
        "Corporate": "#FFC6A6",
        "Home Office": "#C5EAFD"
    }

# Customer Segments:
def fig_customer_segment(df, by="Sales", condition=None):
    df = cal.apply_conditions(df, condition)
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
        text = "Label",
        title="Customer Segment",
        color_discrete_map=customer_color_map
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
        textposition="inside",
        )
    fig.update_yaxes(
        title="Percent(%)",
        ticksuffix="%",
        )
    fig.update_layout(
        xaxis=dict(
           type="category",
            tickmode="linear"
        ),
        yaxis=dict(
            title="Percent(%)",
        ),
        legend=dict(
            title=dict(
                text="  Customer Segment  ",
            ),
            orientation="v",
        ),
    ),
    return render(fig)

def fig_order_value(df, condition=None):
    df = cal.apply_conditions(df, condition)
    df = df.groupby(["Segment", "Order ID"])["Sales"].sum().reset_index()
    df.rename(columns={"Sales": "Order Value"}, inplace=True)
    fig = px.box(
        df,
        x="Segment",
        y="Order Value",
        color="Segment",
        title="Order Value by Customer Segment",
        color_discrete_map=customer_color_map
    )
    fig.update_layout(
        legend=dict(
            title=dict(
                text="  Customer Segment  ",
            ),
        )
    )
    fig.update_traces(
    hovertemplate=(
        "Segment=%{x}<br>"
        "Order Value=$%{y:,.0f}<extra></extra>"
        )
    )
    return render(fig)

def rfm_data(df):
    rfm = df.groupby("Customer ID").agg({
        "Order Date": lambda x: (df["Order Date"].max() - x.max()).days,
        "Order ID": "count",
        "Sales": "sum"
    }).reset_index()
    rfm.columns = ["Customer ID", "Recency", "Frequency", "Monetary"]
    return rfm

def assign_segment(row, freq_thr, rec_thr, mon_thr):
    if row["Frequency"] >= freq_thr:
        if row["Monetary"] >= mon_thr:
            return "High-Value Customers"
        else:
            return "Loyal Customers"
    elif row["Recency"] < rec_thr and row["Frequency"] < freq_thr:
        return "Potential Customers"
    elif row["Recency"] > rec_thr and row["Frequency"] < freq_thr:
        if row["Monetary"] >= mon_thr:
            return "At-Risk Customers"
        else:
            return "Sleeping Customers"
    else:
        return "Others"

def fig_rfm_potential_customers(df, condition=None):
    df = cal.apply_conditions(df, condition=condition)
    sample_customers = rfm_data(df)
    n = min(200, len(sample_customers))
    rfm = sample_customers.sample(n, random_state=50)
    frequency_threshold = rfm["Frequency"].quantile(0.85)
    recency_threshold = rfm["Recency"].quantile(0.85)
    monetary_threshold = rfm["Monetary"].quantile(0.85)
    rfm["Segmentation"] = rfm.apply(
        assign_segment,
        axis=1,
        args=(frequency_threshold, recency_threshold, monetary_threshold)
    )
    loyal_customers = rfm[rfm["Segmentation"] == "Loyal Customers"]
    high_value_customers = rfm[rfm["Segmentation"] == "High-Value Customers"]
    potential_customers = rfm[rfm["Segmentation"] == "Potential Customers"]

    fig = px.scatter(
        rfm,
        x="Frequency",
        y="Monetary",
        color="Recency",
        size="Monetary",
        hover_data=["Customer ID", "Recency", "Segmentation"],
        title="RFM Top Customers (Potential Customers)",
        color_continuous_scale="Viridis",
    )
    fig.add_scatter(
        x=loyal_customers["Frequency"],
        y=loyal_customers["Monetary"],
        mode="markers",
        marker=dict(color="#FF7575", size=10, symbol="star"),
        name="Loyal Customers",
        customdata=loyal_customers[["Customer ID", "Recency", "Segmentation"]],
        hovertemplate=(
            "Customer ID=%{customdata[0]}<br>"
            "Segmentation=%{customdata[2]}<br>"
            "Frequency=%{x}<br>"
            "Monetary=$%{y:,.2f}<br>"
            "Recency=%{customdata[1]}}"
            "<extra></extra>"
        ),
    )
    fig.add_scatter(
        x=high_value_customers["Frequency"],
        y=high_value_customers["Monetary"],
        mode="markers",
        marker=dict(color="#89EDFF", size=10, symbol="diamond"),
        name="High-Value Customers",
        customdata=loyal_customers[["Customer ID", "Recency", "Segmentation"]],
        hovertemplate=(
            "Customer ID=%{customdata[0]}<br>"
            "Segmentation=%{customdata[2]}<br>"
            "Frequency=%{x}<br>"
            "Monetary=$%{y:,.2f}<br>"
            "Recency=%{customdata[1]}}"
            "<extra></extra>"
        ),
    )
    fig.add_scatter(
        x=potential_customers["Frequency"],
        y=potential_customers["Monetary"],
        mode="markers",
        marker=dict(color="#E999F7", size=10, symbol="cross"),
        name="Potential Customers",
        customdata=potential_customers[["Customer ID", "Recency", "Segmentation"]],
        hovertemplate=(
        "Customer ID=%{customdata[0]}<br>"
        "Segmentation=%{customdata[2]}<br>"
        "Frequency=%{x}<br>"
        "Monetary=$%{y:,.2f}<br>"
        "Recency=%{customdata[1]}}"
        "<extra></extra>"
        ),
    )
    fig.update_layout(
        legend=dict(
            title=dict(
                text=" Customer Segmentation ",
            ),
            orientation="h",
            y=-0.2,
            xanchor="center",
            x=0.5,            
        ),
    )
    fig.update_traces(
        hovertemplate=(
            "Customer ID=%{customdata[0]}<br>"
            "Segmentation=%{customdata[2]}<br>"    
            "Frequency=%{x}<br>"
            "Monetary=$%{y:,.2f}<br>"
            "Recency=%{customdata[1]}"
            "<extra></extra>"
        ),
    )
    return render(fig)

def fig_rfm_risky_customers(df, condition=None):
    df = cal.apply_conditions(df, condition=condition)
    sample_customers = rfm_data(df)
    n = min(200, len(sample_customers))
    rfm = sample_customers.sample(n, random_state=50)
    frequency_threshold = rfm["Frequency"].quantile(0.85)
    recency_threshold = rfm["Recency"].quantile(0.85)
    monetary_threshold = rfm["Monetary"].quantile(0.85)
    rfm["Segmentation"] = rfm.apply(
        assign_segment,
        axis=1,
        args=(frequency_threshold, recency_threshold, monetary_threshold)
    )
    sleeping_customers = rfm[rfm["Segmentation"] == "Sleeping Customers"] 
    at_risk_customers = rfm[rfm["Segmentation"] == "At-Risk Customers"]
    fig = px.scatter(
        rfm,
        x="Frequency",
        y="Monetary",
        color="Recency",
        size="Monetary",
        hover_data=["Customer ID", "Recency", "Segmentation"],
        title="RFM Top Customers (Risky Customers)",
        color_continuous_scale="Viridis",
    )
    fig.add_scatter(
        x=sleeping_customers["Frequency"],
        y=sleeping_customers["Monetary"],
        mode="markers",
        marker=dict(color="#FFFB00", size=10, symbol="hexagon"),
        name="Sleeping Customers",
        customdata=sleeping_customers[["Customer ID", "Recency", "Segmentation"]],
        hovertemplate=(
        "Customer ID=%{customdata[0]}<br>"
        "Segmentation=%{customdata[2]}<br>"
        "Frequency=%{x}<br>"
        "Monetary=$%{y:,.2f}<br>"
        "Recency=%{customdata[1]}}"
        "<extra></extra>"
        ),
    )
    fig.add_scatter(
        x=at_risk_customers["Frequency"],
        y=at_risk_customers["Monetary"],
        mode="markers",
        marker=dict(color="#FF0000", size=10, symbol="pentagon"),
        name="At-Risk Customers",
        customdata=at_risk_customers[["Customer ID", "Recency", "Segmentation"]],
        hovertemplate=(
        "Customer ID=%{customdata[0]}<br>"
        "Segmentation=%{customdata[2]}<br>"
        "Frequency=%{x}<br>"
        "Monetary=$%{y:,.2f}<br>"
        "Recency=%{customdata[1]}}"
        "<extra></extra>"
        ),
    )
    fig.update_layout(
        legend=dict(
            title=dict(
                text=" Customer Segmentation ",
            ),
            orientation="h",
            y=-0.2,
            xanchor="center",
            x=0.5,
        ),
    )
    fig.update_traces(
        hovertemplate=(
            "Customer ID=%{customdata[0]}<br>"
            "Segmentation=%{customdata[2]}<br>"
            "Frequency=%{x}<br>"
            "Monetary=$%{y:,.2f}<br>"
            "Recency=%{customdata[1]}"
            "<extra></extra>"
        ),
    )
    return render(fig)

# ===========================
# PRODUCTS ANALYSIS
# ===========================
def top_product(df, by="by", level="Product Name", top_n = 10, condition=None):
    if condition:
        df = cal.apply_conditions(df, condition)
    
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

def fig_top_items(df, by="Sales", level=["Sub-Category", "Product ID", "Product Name"], top_n=5, condition=None):
    df_top = top_product(df, by=by, level=level, top_n=top_n, condition=condition)
    df_top = df_top.reset_index(drop=True)

    fig = px.treemap(
        df_top,
        path=["Sub-Category", "Product ID"],
        values=by,
        color=by,
        color_continuous_scale="matter",
        title=f"Top {top_n} Products by {by}",
    )
    fig.update_traces(
        textinfo="label",
        texttemplate="%{label}",
        customdata=df_top["Product Name"],
        hovertemplate=(
            "Node=%{label}<br>"
            "Product Name=%{customdata}<br>"
            f"{by}=%{{value:,.0f}}<br>"
            "Percent of Total=%{percentParent:.1%}<br>"
            "Percent of Root=%{percentRoot:.1%}"
            "<extra></extra>"
        )
    )
    fig.update_layout(
        uniformtext=dict(
            minsize=10,
            mode="show",
        )
    )
    return render(fig)

def fig_top_subcat_sales(df, condition=None):
    df = cal.apply_conditions(df, condition=condition)
    profit_by_subcat = df.groupby("Sub-Category")["Sales"].sum().reset_index().reset_index()

    profit_by_subcat["Sales_fmt"] = profit_by_subcat["Sales"].apply(cal.format_currency)
    customdata = profit_by_subcat["Sales_fmt"].apply(lambda x: [x]).tolist()
    fig = px.bar(
        profit_by_subcat,
        x="Sales",
        y="Sub-Category",
        orientation="h",
        color="Sales",
        text="Sales_fmt",
        color_continuous_scale="tropic",
        title="Sales by Sub-Category",
    )
    fig.update_layout(
        xaxis=dict(
            title="Sales",
        ),
        yaxis=dict(
            title="Sub-Category",
        ),
        bargap=0.1,
    )
    fig.update_traces(
        customdata=customdata,
        texttemplate="%{text}",
        textposition="auto",
        textfont=dict(
            size=12,
            family="Arial",
            color="black",
        ),
        hovertemplate=(
            "Sub-Category=%{y}<br>"
            "Sales=%{customdata[0]}"
            "<extra></extra>"
        )
    )
    return render(fig)

def fig_top_subcat_profit(df, condition=None):
    df = cal.apply_conditions(df, condition=condition)
    profit_by_subcat = df.groupby("Sub-Category")["Profit"].sum().reset_index().reset_index()

    profit_by_subcat["Profit_fmt"] = profit_by_subcat["Profit"].apply(cal.format_currency)
    customdata = profit_by_subcat["Profit_fmt"].apply(lambda x: [x]).tolist()
    fig = px.bar(
        profit_by_subcat,
        x="Profit",
        y="Sub-Category",
        orientation="h",
        color="Profit",
        text="Profit_fmt",
        color_continuous_scale="tropic",
        title="Profit by Sub-Category",
    )
    fig.update_layout(
        xaxis=dict(
            title="Profit",
        ),
        yaxis=dict(
            title="Sub-Category",
        ),
        bargap=0.1,
    )
    fig.update_traces(
        customdata=customdata,
        texttemplate="%{text}",
        textposition="auto",
        textfont=dict(
            size=12,
            family="Arial",
            color="black",
        ),
        hovertemplate=(
            "Sub-Category=%{y}<br>"
            "Profit=%{customdata[0]}"
            "<extra></extra>"
        ),
    )
    return render(fig)

def fig_product_profit_summary(df, condition=None, by="Sub-Category"):
    summary_by_cat = cal.discount_analysis(df, condition=condition, agg="mean", by=by)    
    metrics = ["Sales", "Profit", "Net Sales", "Adjusted Profit", "Profit Margin", "Average Discount"]
    
    df_fmt = summary_by_cat.copy()
    for col in metrics:
        if col == "Profit Margin" or col == "Average Discount":
            df_fmt[col] = df_fmt[col].apply(lambda x: f"{x:.1%}")
        else:
            df_fmt[col] = df_fmt[col].apply(cal.format_currency)
    
    pivot_value = summary_by_cat[metrics + [by]].set_index(by)
    pivot_text = df_fmt[metrics + [by]].set_index(by)
    
    fig = px.imshow(
        pivot_value,
        aspect="auto",
        color_continuous_scale="ylorbr",
        title=f"Impact of Discount on Profit by {by}"
    )
    fig.update_layout(
        xaxis_title="Metrics",
        yaxis_title=by,
    )
    fig.update_traces(
        xgap=2,
        ygap=2,
        zsmooth=False,
        text=pivot_text.values,
        texttemplate="%{text}",
        hovertemplate=(
            f"{by}=%{{y}}<br>"
            "Metrics=%{x}<br>"
            "Value=%{z:.2f}<br>"
            "<extra></extra>"
        )
    )
    return render(fig)