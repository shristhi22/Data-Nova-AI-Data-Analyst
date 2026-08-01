import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from utils.pdf_generator import generate_pdf
from utils.file_manager import (
    save_uploaded_file,
    load_history,
    get_file_path
)
# ------------------ PAGE CONFIG ------------------

st.set_page_config(
    page_title="DataNova - AI Data Analyst",
    page_icon="📊",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------

st.markdown("""
<style>

body{
    background:#0B1120;
}

.main{
    background:#0B1120;
}
h1,h2,h3,h4{
    color:white;
}

.metric-box{
    background:#1e293b;
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;
}
div[data-testid="stMetric"]{
    background:#1E293B;
    border:1px solid #334155;
    padding:20px;
    border-radius:16px;
    box-shadow:0 4px 15px rgba(0,0,0,.25);
}

}
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#111827,#1E293B);
}
}

.stButton>button{
    background: linear-gradient(135deg,#7C3AED,#2563EB);
    color: white;
    border: none;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton>button:hover{
    transform: scale(1.03);
    box-shadow: 0 0 15px rgba(124,58,237,0.5);
}

</style>
""",unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style="
text-align:center;
font-size:48px;
font-weight:800;
background:linear-gradient(90deg,#7C3AED,#2563EB,#06B6D4);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:0px;">
📊 DataNova
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style="
text-align:center;
font-size:18px;
color:#CBD5E1;
margin-top:-10px;">
Analyze Smarter • Visualize Better • Decide Faster 🚀
</p>
""", unsafe_allow_html=True)


st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🤖 AI Quick Tools")
if "tool" not in st.session_state:
    st.session_state.tool = "None"

st.sidebar.markdown("### Choose a Tool")

if st.sidebar.button("📊 Statistics"):
    st.session_state.tool = "📊 Statistics"
if st.sidebar.button("📈 Correlation"):
    st.session_state.tool = "📈 Correlation"

if st.sidebar.button("🔍 Missing Values"):
    st.session_state.tool = "🔍 Missing Values"

if st.sidebar.button("📋 Column Information"):
    st.session_state.tool = "📋 Column Information"

if st.sidebar.button("📈 Data Visualizer"):
    st.session_state.tool = "📈 Data Visualizer"

if st.sidebar.button("💡 AI Insights"):
    st.session_state.tool = "💡 AI Insights"

if st.sidebar.button("🤖 Smart Query"):
    st.session_state.tool = "🤖 Smart Query"
tool = st.session_state.tool



# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader(
    "📂 Upload CSV File",
    type=["csv"]
)

# Upload new file
if uploaded_file is not None:

    filepath = save_uploaded_file(uploaded_file)

    try:
        st.session_state.df = pd.read_csv(filepath)
    except:
        st.session_state.df = pd.read_csv(filepath, encoding="latin1")

    st.session_state.current_file = uploaded_file.name


# Load recent history
history = load_history()
st.sidebar.markdown("---")
st.sidebar.subheader("📂 Current Dataset")

if "current_file" in st.session_state:
    st.sidebar.success(st.session_state.current_file)

    rows = st.session_state.df.shape[0]
    cols = st.session_state.df.shape[1]

    c1, c2 = st.sidebar.columns(2)
    c1.metric("Rows", rows)
    c2.metric("Cols", cols)
else:
    st.sidebar.info("No dataset selected")
# Show recent files
if history:

    st.sidebar.markdown("### 🕒 Recent Files")

    for file in history:

        if st.sidebar.button(f"📄 {file}", use_container_width=True):

            path = get_file_path(file)

            try:
                st.session_state.df = pd.read_csv(path)
            except:
                st.session_state.df = pd.read_csv(path, encoding="latin1")

            st.session_state.current_file = file

# Check dataset
if "df" not in st.session_state:

    st.info("👆 Upload a CSV file to continue.")

    st.stop()

df = st.session_state.df
st.sidebar.markdown("---")
st.sidebar.subheader("📄 Export Report")

if st.sidebar.button("📥 Download PDF Report"):

    pdf_file = generate_pdf(df)

    with open(pdf_file, "rb") as file:

        st.sidebar.download_button(
            label="⬇ Download Now",
            data=file,
            file_name="DataNova_Report.pdf",
            mime="application/pdf"
        )
if tool == "None":

    st.header("🤖 AI Analysis Center")

    col1, col2 = st.columns(2)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📄 Rows", df.shape[0])

    col2.metric("📑 Columns", df.shape[1])

    col3.metric(
    "🔢 Numeric",
    len(df.select_dtypes(include="number").columns)
)

    col4.metric(
    "📝 Categorical",
    len(df.select_dtypes(exclude="number").columns)
)
    st.divider()

st.subheader("📂 Current Dataset")

if "current_file" in st.session_state:
    st.success(f"✅ {st.session_state.current_file}")
else:
    st.warning("No dataset uploaded")
    st.info("📊 Statistics")
    st.info("📈 Correlation Matrix")
    st.info("🔍 Missing Value Analysis")
    st.info("📋 Column Information")
    st.info("📈 Data Visualizer")

    st.stop()
# ---------------- AI QUICK TOOLS ----------------

if tool == "📊 Statistics":


    st.header("📊 Dataset Statistics")

    st.dataframe(df.describe(include="all"))

    st.stop()

if tool == "📈 Correlation":

    st.header("📈 Correlation Matrix")

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        st.warning("At least 2 numeric columns are required.")
    else:
        corr = numeric_df.corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="Blues",
            aspect="auto"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.stop()
if tool == "🔍 Missing Values":

    st.header("🔍 Missing Value Analysis")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Percentage": (
            df.isnull().sum() / len(df) * 100
        ).round(2).values
    })

    st.dataframe(missing_df, use_container_width=True)

    st.stop()
if tool == "📋 Column Information":

    st.header("📋 Column Information")

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Non-Null Values": df.count().values,
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })

    st.dataframe(column_info, use_container_width=True)

    st.stop()  
if tool == "📈 Data Visualizer":

    st.header("📈 Data Visualizer")

    themes = {
        "Plotly": "plotly",
        "Dark": "plotly_dark",
        "GGPlot2": "ggplot2",
        "Seaborn": "seaborn",
        "Simple White": "simple_white"
    }

    selected_theme = st.selectbox(
        "🎨 Select Color Theme",
        list(themes.keys())
    )

    chart_type = st.selectbox(
        "📊 Select Chart Type",
        ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"]
    )

    x_axis = st.selectbox(
        "📌 Select X-Axis",
        df.columns
    )

    if chart_type != "Pie Chart":

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if not numeric_cols:
            st.error("❌ No numeric columns found in the dataset.")
            st.stop()

        y_axis = st.selectbox(
            "📌 Select Y-Axis",
            numeric_cols
        )

    if st.button("🚀 Generate Chart"):

        if chart_type == "Bar Chart":

            fig = px.bar(
                df,
                x=x_axis,
                y=y_axis,
                template=themes[selected_theme]
            )

        elif chart_type == "Line Chart":

            fig = px.line(
                df,
                x=x_axis,
                y=y_axis,
                template=themes[selected_theme]
            )

        elif chart_type == "Scatter Plot":

            fig = px.scatter(
                df,
                x=x_axis,
                y=y_axis,
                template=themes[selected_theme]
            )

        elif chart_type == "Pie Chart":

            fig = px.pie(
                df,
                names=x_axis,
                template=themes[selected_theme]
            )

        st.plotly_chart(fig, use_container_width=True)

    st.stop()
if tool == "💡 AI Insights":

    st.header("💡 AI Dataset Insights")

    st.success(f"📄 Total Rows: {df.shape[0]}")
    st.success(f"📑 Total Columns: {df.shape[1]}")

    st.info(f"🔢 Numeric Columns: {len(df.select_dtypes(include='number').columns)}")
    st.info(f"📝 Categorical Columns: {len(df.select_dtypes(exclude='number').columns)}")

    missing = df.isnull().sum().sum()

    if missing == 0:
        st.success("✅ No Missing Values Found")
    else:
        st.warning(f"⚠ {missing} Missing Values Found")

    duplicate = df.duplicated().sum()

    if duplicate == 0:
        st.success("✅ No Duplicate Records")
    else:
        st.warning(f"⚠ {duplicate} Duplicate Records Found")

    st.subheader("📌 Recommendations")

    st.write("• Clean missing values before analysis.")
    st.write("• Remove duplicate records if present.")
    st.write("• Use correlation analysis to identify relationships.")
    st.write("• Create visualizations to identify trends.")

    st.stop()  
if tool == "🤖 Smart Query":

    st.header("🤖 Smart Query")

    query = st.text_input(
        "Ask something about your dataset"
    )

    if query:


        q = query.lower()
        st.markdown("## 🧠 AI Analysis")

        if "rows" in q:
            st.success(f"Total Rows : {df.shape[0]}")

        elif "columns" in q:
            st.success(f"Total Columns : {df.shape[1]}")

        elif "missing" in q:
            st.success(f"Missing Values : {df.isnull().sum().sum()}")

        elif "duplicate" in q:
            st.success(f"Duplicate Rows : {df.duplicated().sum()}")
        elif "highest" in q or "max" in q:

         numeric_cols = df.select_dtypes(include="number").columns.tolist()

         found = False

        for col in numeric_cols:

         if col.lower() in q:

            st.success(f"Highest {col}: {df[col].max()}")

            found = True

            break

        if not found:

         st.warning("Please mention the numeric column name.")

        elif "average" in q or "mean" in q:

         numeric_cols = df.select_dtypes(include="number").columns.tolist()

         found = False

        for col in numeric_cols:

         if col.lower() in q:

            st.success(f"Average {col}: {round(df[col].mean(),2)}")

            found = True

            break

    if not found:

        st.warning("Please mention the numeric column name.")

        

    st.stop()       
# ---------------- KPI ----------------

rows=df.shape[0]

cols=df.shape[1]

missing=df.isnull().sum().sum()

duplicate=df.duplicated().sum()

numeric=df.select_dtypes(include=np.number).shape[1]

categorical=df.select_dtypes(exclude=np.number).shape[1]

health=100

health-=duplicate

health-=missing*0.1

health=max(0,min(100,int(health)))

# ---------------- DASHBOARD ----------------

