import streamlit as st

st.title("📈 Data Explorer")
st.write("Welcome to Page 1! This page is ideal for your data visualizations.")

# Example interactive element
user_input = st.text_input("Enter a label for your chart:", "Sample Data")
st.line_chart([1, 2, 3, 5, 8, 13])
st.caption(f"Showing: {user_input}")
