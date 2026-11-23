import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setting
st.set_page_config(page_title="University Pro Dashboard", layout="wide")

# --- DARK PURPLE THEME (Jaise us photo me tha) ---
st.markdown("""
<style>
.stApp { background-color: #161126; color: white; }
div[data-testid="stMetric"] { background-color: #241B3D; border: 1px solid #7B61FF; padding: 15px; border-radius: 15px; }
div[data-testid="stMetricLabel"] { color: #CFC6FF; }
div[data-testid="stMetricValue"] { color: white; }
h1, h2, h3 { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- DATA LOAD ---
df = pd.read_excel('University_Data.xlsx')

# --- SIDEBAR (Left side - Photo jaisa) ---
st.sidebar.title("🎓 University")
st.sidebar.write("Navigation")
menu = st.sidebar.radio("Jao:", ["Overview", "Students", "Fees", "Performance"])
st.sidebar.divider()
st.sidebar.write("Filter")
# Agar tumhari file me koi Category wala column hai to wo yahan aa jayega
cat_cols = df.select_dtypes(include='object').columns.tolist()
selected = "All"
if len(cat_cols) > 0:
    selected = st.sidebar.selectbox("Select:", ["All"] + df[cat_cols[0]].dropna().unique().tolist())
    if selected != "All":
        df = df[df[cat_cols[0]] == selected]

# --- TITLE ---
st.title("💜 University Analytics")
st.write(f"Overview  |  Total Records: {len(df)}")

# --- KPI CARDS (Upar wale 4 Cards) ---
numeric_cols = df.select_dtypes(include='number').columns.tolist()
total_val = df[numeric_cols[0]].sum() if len(numeric_cols) > 0 else 0
avg_val = df[numeric_cols[0]].mean() if len(numeric_cols) > 0 else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Students", f"{len(df)}", "+12%")
c2.metric("Total Value", f"{total_val:,.0f}", "+8.5%")
c3.metric("Average", f"{avg_val:,.1f}", "+2.1%")
c4.metric("Total Columns", f"{len(df.columns)}", "Active")

st.divider()

# --- CHARTS ROW 1 ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Monthly Trend (Bar Chart)")
    if len(numeric_cols) > 0:
        fig1 = px.bar(df.head(12), y=numeric_cols[0], color_discrete_sequence=["#7B61FF"])
        fig1.update_layout(plot_bgcolor="#161126", paper_bgcolor="#161126", font_color="white")
        st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🥧 Distribution (Pie Chart)")
    if len(cat_cols) > 0:
        fig2 = px.pie(df, names=cat_cols[0], color_discrete_sequence=px.colors.sequential.Purp)
        fig2.update_layout(paper_bgcolor="#161126", font_color="white")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.write("Pie ke liye Text wala column chahiye")

# --- CHARTS ROW 2 ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("📈 Performance Line")
    if len(numeric_cols) > 0:
        fig3 = px.line(df.head(20), y=numeric_cols[0], markers=True, color_discrete_sequence=["#FF6EC7"])
        fig3.update_layout(plot_bgcolor="#161126", paper_bgcolor="#161126", font_color="white")
        st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("🏆 Top 5 Records")
    if len(numeric_cols) > 0:
        top5 = df.sort_values(by=numeric_cols[0], ascending=False).head(5)
        fig4 = px.bar(top5, x=numeric_cols[0], y=cat_cols[0] if len(cat_cols)>0 else top5.index, orientation='h', color_discrete_sequence=["#7B61FF"])
        fig4.update_layout(plot_bgcolor="#161126", paper_bgcolor="#161126", font_color="white")
        st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.subheader("📋 Full Data Table")
st.dataframe(df, use_container_width=True)