import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on March 31th")

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
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")

st.write("### (1) Add a drop down for Category")
categories = df['Category'].unique().tolist()
selected_category = st.selectbox("Select a Category", categories)

st.write("### (2) Add a multi-select for Sub_Category in the selected Category")
df1 = df[df['Category'] == selected_category]
subcategories = df1['Sub_Category'].unique() 
selected_subcategories = st.multiselect("Select Subcategories", subcategories)

st.write("### (3) Show a line chart of sales for the selected items in (2)")
df2 =df1[df1['Sub_Category'].isin(selected_subcategories)]
sales_by_month1 = df2.groupby(['Sub_Category', pd.Grouper(freq='M')])['Sales'].sum().stack(level=0)
st.line_chart(sales_by_month1)

st.write("### (4) Show three metrics for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.metric("Total Sales", df2['Sales'].sum())
st.metric("Total Profit" , df2['Profit'].sum())
avg_num = df['Profit'].sum() / df['Sales'].sum()
avg_num1 = df2['Profit'].sum() / df2['Sales'].sum()
st.metric("Average Profit Margin", avg_num1, delta=avg_num1-avg_num)

st.write("### (5) Use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
# Calculate overall average profit margin
overall_total_sales = df['Sales'].sum()
overall_total_profit = df['Profit'].sum()
overall_profit_margin = (overall_total_profit / overall_total_sales) if overall_total_sales else 0
# Calculate delta
delta = avg_num1 - overall_profit_margin if selected_subcategories else -overall_profit_margin
# Display metric with delta
st.metric("Average Profit Margin", avg_num1, delta=delta)


st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
