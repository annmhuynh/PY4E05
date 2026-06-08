from flask import Flask, request, render_template
import data_process as dps
import calculation as cal
import pandas as pd

app = Flask(__name__)

dfs = dps.load_data("raw data")
df_ords = dps.process_data(dfs["Orders"])

@app.route("/", methods=["GET"])
def dashboard():
    regions = df_ords["Region"].unique().tolist()
    categories = df_ords["Category"].unique().tolist()
    min_date = df_ords["Order Date"].min().date()
    max_date = df_ords["Order Date"].max().date()
    
    start_date = request.args.get("start-date")
    end_date = request.args.get("end-date")
    region = request.args.get("region")
    category = request.args.get("category")

    conditions = {
        "start_date": start_date,
        "end_date": end_date,
        "Region": region,
        "Category": category
    }

    kpi_html = cal.kpi_dashboard(df_ords, condition=conditions)
    sales_html = cal.fig_sales_by_year(condition=conditions)
    top_items_html = cal.fig_top_items(df_ords, by="Profit", level="Product Name", top_n=5, condition=conditions, time="Year")
    customer_segment = cal.customer_segment(df_ords, by="Sales", condition=conditions)
    
    return render_template(
        "dashboard.html",
        kpi=kpi_html,
        sales=sales_html,
        top_items=top_items_html,
        regions=regions,
        categories=categories,
        min_date=min_date,
        max_date=max_date,
        customer_segment=customer_segment,
        conditions=conditions
    )
if __name__ == "__main__":
    app.run(debug=True)