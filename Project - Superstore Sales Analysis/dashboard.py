from flask import Blueprint, request, render_template
import data_process as dps
import visualization as vl
from config import CLEAN_DATA_PATH, TEMPLATES_PATH, STATIC_PATH

dashboard_bp = Blueprint("dashboard", __name__,
                         template_folder=TEMPLATES_PATH,
                         static_folder=STATIC_PATH)

dfs = dps.load_data(CLEAN_DATA_PATH)
df_ords = dfs["Orders_clean"]

@dashboard_bp.route("/", methods=["GET"])
def dashboard():
    regions = df_ords["Region"].unique().tolist()
    categories = df_ords["Category"].unique().tolist()
    segments = df_ords["Segment"].unique().tolist()
    min_date = df_ords["Order Date"].min().date()
    max_date = df_ords["Order Date"].max().date()
    
    start_date = request.args.get("start-date")
    end_date = request.args.get("end-date")
    region = request.args.get("region")
    segment = request.args.get("segment")
    category = request.args.get("category")

    conditions = {
        "start_date": start_date,
        "end_date"  : end_date,
        "Region"    : region,
        "Segment"   : segment,
        "Category"  : category,
    }

    kpi_html = vl.kpi_dashboard(df_ords, condition=conditions)
    sales_html = vl.fig_sales_by_year(df_ords, condition=conditions)
    top_items_html = vl.fig_top_items(df_ords, by="Profit", level=["Sub-Category", "Product ID", "Product Name"], top_n=15, condition=conditions)
    customer_segment = vl.fig_customer_segment(df_ords, by="Sales", condition=conditions)
    profit_margin = vl.fig_profit_and_margin_by_year(df_ords, condition=conditions)
    order_value = vl.fig_order_value(df_ords, condition=conditions)
    rfm_potential_customer = vl.fig_rfm_potential_customers(df_ords, condition=conditions)
    rfm_risky_customer = vl.fig_rfm_risky_customers(df_ords, condition=conditions)
    discount_impact_mean = vl.fig_discount_analysis_mean(df_ords, condition=conditions)
    discount_impact_sum = vl.fig_discount_analysis_sum(df_ords, condition=conditions)
    top_subcat_sales = vl.fig_top_subcat_sales(df_ords, condition=conditions)
    top_subcat_profit = vl.fig_top_subcat_profit(df_ords, condition=conditions)
    discount_impact_cat = vl.fig_product_profit_summary(df_ords, condition=conditions, by="Sub-Category")

    return render_template(
        "dashboard.html",
        region=region,
        regions=regions,
        category=category,
        categories=categories,
        segment=segment,
        segments=segments,
        min_date=min_date,
        max_date=max_date,
        start_date=start_date,
        end_date=end_date,
        kpi=kpi_html,
        sales=sales_html,
        top_items=top_items_html,
        customer_segment=customer_segment,
        profit_margin=profit_margin,
        order_value=order_value,
        rfm_potential_customer=rfm_potential_customer,
        rfm_risky_customer=rfm_risky_customer,
        discount_impact_mean=discount_impact_mean,
        discount_impact_sum=discount_impact_sum,
        top_subcat_sales=top_subcat_sales,
        top_subcat_profit=top_subcat_profit,
        discount_impact_cat=discount_impact_cat,
        conditions=conditions
    )