import data_process

dir = "raw data"
dfs = data_process.load_data(dir)

# ========= PHÂN TÍCH DỮ LIỆU =========

# Phân tích doanh thu và lợi nhuận:

total_sales = dfs["Orders"]["Sales"].sum()
total_profit = dfs["Orders"]["Profit"].sum()

print("Total Sales:", total_sales)
print("Total Profit:", total_profit)