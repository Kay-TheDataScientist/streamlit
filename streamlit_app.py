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
# Add a drop-down for Category
categories = df['Category'].unique()
selected_category = st.selectbox("Select Category", categories)

st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
# Filter the dataframe based on the selected category
filtered_df_category = df[df['Category'] == selected_category]

# Add a multi-select for Sub-Category
sub_categories = filtered_df_category['Sub-Category'].unique().tolist() 
selected_sub_categories = st.multiselect("Select Sub-Category", sub_categories, default=sub_categories.tolist())
st.write("### (3) show a line chart of sales for the selected items in (2)")
# Filter data for selected sub-categories
filtered_df = df[df['Sub-Category'].isin(selected_sub_categories)]

# Group by date and sum sales
sales_by_date = filtered_df.groupby('Order_Date')['Sales'].sum()

# Display the line chart
st.line_chart(sales_by_date)

st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
# Calculate total sales and total profit for the selected sub-categories.
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()

# Calculate profit margin.  Avoid division by zero.
profit_margin = (total_profit / total_sales) * 100 if total_sales else 0

# Display the metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", total_sales)
col2.metric("Total Profit", total_profit)
col3.metric("Profit Margin (%)", f"{profit_margin:.2f}%")

st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
# Calculate overall profit margin for all products.
overall_total_sales = df['Sales'].sum()
overall_total_profit = df['Profit'].sum()
overall_profit_margin = (overall_total_profit / overall_total_sales) * 100 if overall_total_sales else 0

# Calculate the difference (delta) between the selected sub-category profit margin and the overall profit margin.
delta = profit_margin - overall_profit_margin

# Display the profit margin with the delta.
col3.metric("Profit Margin (%)", f"{profit_margin:.2f}%", delta=f"{delta:.2f}%")
