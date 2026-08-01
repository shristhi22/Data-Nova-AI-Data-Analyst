import pandas as pd
import streamlit as st


def load_csv(uploaded_file):
    """
    Load uploaded CSV file safely.
    Returns dataframe if successful, else None.
    """

    if uploaded_file is None:
        st.info("📂 Please upload a CSV file.")
        return None

    try:
        with st.spinner("Loading dataset..."):
            df = pd.read_csv(uploaded_file)

        st.success("✅ Dataset Loaded Successfully!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows", df.shape[0])

        with col2:
            st.metric("Columns", df.shape[1])

        st.subheader("Dataset Preview")
        st.dataframe(df.head(), use_container_width=True)

        return df

    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def dataset_summary(df):
    """
    Display dataset summary.
    """

    st.subheader("Dataset Information")

    info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum(),
        "Unique Values": df.nunique()
    })

    st.dataframe(info, use_container_width=True)


def numerical_columns(df):
    """
    Return numerical columns.
    """

    return df.select_dtypes(include=["int64", "float64"]).columns.tolist()


def categorical_columns(df):
    """
    Return categorical columns.
    """

    return df.select_dtypes(include=["object", "category"]).columns.tolist()