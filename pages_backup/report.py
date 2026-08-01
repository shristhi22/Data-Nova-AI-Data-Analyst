import streamlit as st
import pandas as pd

st.set_page_config(page_title="Report", layout="wide")

st.title("📄 AI Data Analysis Report")

# Get dataset from session_state
if "df" not in st.session_state:
    st.warning("⚠️ Please upload a CSV file from the Home page.")
    st.stop()

df = st.session_state.df

st.success("✅ Dataset Loaded Successfully")

st.header("📊 Dataset Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", int(df.isnull().sum().sum()))

st.markdown("---")

st.subheader("Column Information")

info = pd.DataFrame({
    "Column": df.columns,
    "Datatype": df.dtypes.astype(str),
    "Missing": df.isnull().sum(),
    "Unique": df.nunique()
})

st.dataframe(info, use_container_width=True)

st.subheader("Statistical Summary")
st.dataframe(df.describe(include="all"), use_container_width=True)

report = f"""
AI DATA ANALYSIS REPORT

Rows : {df.shape[0]}
Columns : {df.shape[1]}
Missing Values : {df.isnull().sum().sum()}

Numerical Columns:
{', '.join(df.select_dtypes(include='number').columns)}

Categorical Columns:
{', '.join(df.select_dtypes(include='object').columns)}
"""

st.download_button(
    "📥 Download Report",
    report,
    file_name="AI_Report.txt",
    mime="text/plain"
)