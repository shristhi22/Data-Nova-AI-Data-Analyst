import streamlit as st
import pandas as pd
from utils.csv_loader import (
    load_csv,
    dataset_summary,
    numerical_columns,
    categorical_columns
)

st.set_page_config(page_title="AI Data Analyst", layout="wide")

st.title("📊 AI Data Analyst Dashboard")
if "df" not in st.session_state:
    st.warning("⚠️ Please upload a CSV file from Home page.")
    st.stop()

df = st.session_state.df

if df is not None:

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([
        "📋 Overview",
        "📑 Dataset Info",
        "📈 Statistics"
    ])

    with tab1:

        st.subheader("Dataset Shape")

        col1, col2 = st.columns(2)

        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])

        st.subheader("First 10 Rows")
        st.dataframe(df.head(10), use_container_width=True)

    with tab2:

        dataset_summary(df)

    with tab3:

        st.subheader("Numerical Statistics")

        num_cols = numerical_columns(df)

        if len(num_cols) > 0:
            st.dataframe(df[num_cols].describe().T, use_container_width=True)
        else:
            st.warning("No numerical columns found.")

        st.subheader("Categorical Columns")

        cat_cols = categorical_columns(df)

        if len(cat_cols) > 0:
            selected = st.selectbox(
                "Select Column",
                cat_cols
            )

            st.dataframe(
                df[selected].value_counts().reset_index().rename(
                    columns={
                        "index": selected,
                        selected: "Count"
                    }
                ),
                use_container_width=True
            )
        else:
            st.warning("No categorical columns found.")