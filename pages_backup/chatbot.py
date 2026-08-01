import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Chatbot", layout="wide")

st.title("🤖 AI Data Analyst Chatbot")

# Get dataset from session_state
if "df" not in st.session_state:
    st.warning("⚠️ Please upload a CSV file from the Home page.")
    st.stop()

df = st.session_state.df

st.success("✅ Dataset Loaded")

question = st.text_input("Ask a question about your dataset")

if question:

    q = question.lower()

    if "rows" in q:
        st.success(f"📊 Dataset has {df.shape[0]} rows.")

    elif "columns" in q:
        st.success(f"📋 Dataset has {df.shape[1]} columns.")

    elif "missing" in q:
        st.success(f"❗ Missing values: {df.isnull().sum().sum()}")

    elif "sales" in q:
        if "Sales" in df.columns:
            st.success(f"💰 Total Sales = {df['Sales'].sum():,.2f}")
        else:
            st.warning("Sales column not found.")

    elif "highest" in q:
        numeric = df.select_dtypes(include="number")

        if len(numeric.columns) > 0:
            col = numeric.columns[0]
            st.success(f"📈 Highest value in '{col}' = {df[col].max()}")
        else:
            st.warning("No numeric columns found.")

    else:
        st.info("""
I can answer questions like:

• How many rows?
• How many columns?
• Missing values?
• Total sales?
• Highest value?
""")