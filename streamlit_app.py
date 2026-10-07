import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='ME')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

# My Additions
# (1) Drop down for Category
category = st.selectbox("Select a Category", df["Category"].unique())

# (2) Multi-select for Sub_Category, only showing sub-categories in the chosen Category
sub_options = df[df["Category"] == category]["Sub_Category"].unique()
sub_categories = st.multiselect("Select Sub-Categories", sub_options)

# Only show results once at least one sub-category is picked
if sub_categories:
    # Keep only the rows that match the selected sub-categories
    filtered = df[df["Sub_Category"].isin(sub_categories)]

    # (3) Line chart of sales by month for the selected items
    filtered_by_month = filtered.filter(items=["Sales"]).groupby(pd.Grouper(freq="ME")).sum()
    st.line_chart(filtered_by_month, y="Sales")

    # (4) Three metrics: total sales, total profit, profit margin
    total_sales = filtered["Sales"].sum()
    total_profit = filtered["Profit"].sum()
    margin = total_profit / total_sales * 100

    # (5) Overall margin across ALL products, used for the delta
    overall_margin = df["Profit"].sum() / df["Sales"].sum() * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Profit Margin", f"{margin:.2f}%", delta=f"{margin - overall_margin:.2f}%")
else:
    st.write("Select at least one sub-category to see results.")

#st.write("## Instructions: Your additions")
#st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
#st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
#st.write("### (3) show a line chart of sales for the selected items in (2)")
#st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
#st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
