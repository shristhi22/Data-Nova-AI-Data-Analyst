import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Insights", layout="wide")

st.title("📊 Data Insights & Visualization")

if "df" not in st.session_state:
    st.warning("⚠️ Please upload a CSV file from Home page.")
    st.stop()

df = st.session_state.df

st.success("✅ Dataset Loaded")

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

chart = st.selectbox(
    "Select Chart",
    [
        "Bar Chart",
        "Line Chart",
        "Histogram",
        "Pie Chart",
        "Box Plot"
    ]
)

if chart == "Bar Chart":

        x = st.selectbox("X Axis", categorical_cols)

        y = st.selectbox("Y Axis", numeric_cols)

        fig = px.bar(df, x=x, y=y)

        st.plotly_chart(fig, use_container_width=True)

elif chart == "Line Chart":

        x = st.selectbox("X Axis", df.columns)

        y = st.selectbox("Y Axis", numeric_cols)

        fig = px.line(df, x=x, y=y)

        st.plotly_chart(fig, use_container_width=True)

elif chart == "Histogram":

        col = st.selectbox("Column", numeric_cols)

        fig = px.histogram(df, x=col)

        st.plotly_chart(fig, use_container_width=True)

elif chart == "Pie Chart":

        names = st.selectbox("Category", categorical_cols)

        values = st.selectbox("Values", numeric_cols)

        fig = px.pie(df, names=names, values=values)

        st.plotly_chart(fig, use_container_width=True)

elif chart == "Box Plot":

        x = st.selectbox("Category", categorical_cols)

        y = st.selectbox("Numeric", numeric_cols)

        fig = px.box(df, x=x, y=y)

        st.plotly_chart(fig, use_container_width=True)