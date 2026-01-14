import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="Indian Crop Production Analytics",
    layout="wide"
)

# Load Data
@st.cache_data
def load_data():
    crop = pd.read_csv("data/analytical_tables/crop_summary.csv")
    state = pd.read_csv("data/analytical_tables/state_summary.csv")
    year = pd.read_csv("data/analytical_tables/yearly_summary.csv")
    season = pd.read_csv("data/analytical_tables/season_summary.csv")
    return crop, state, year, season

crop_summary, state_summary, yearly_summary, season_summary = load_data()

# Sidebar (Clean & Professional)
st.sidebar.markdown("## 📊 Dashboard Controls")
st.sidebar.markdown("Choose analysis type and view insights")

top_n = st.sidebar.slider(
    "Top Records",
    min_value=5,
    max_value=15,
    value=8
)

st.sidebar.markdown("---")
st.sidebar.caption("Indian Crop Analytics")


# Main Title
st.title("🌾 Indian Crop Production Analytics")
st.write("Interactive dashboard for agricultural production insights")

# KPI Section
col1, col2, col3, col4 = st.columns(4)

col1.metric("🌱 Crops", crop_summary.shape[0])
col2.metric("📍 States", state_summary.shape[0])
col3.metric("📅 Years", yearly_summary['Crop_Year'].nunique())
col4.metric("📦 Total Production", int(crop_summary['Production'].sum()))

st.markdown("---")

# BUTTON NAVIGATION (SEQUENCE)
st.markdown("### 🔍 Select Analysis View")

btn1, btn2, btn3, btn4 = st.columns(4)

if "view" not in st.session_state:
    st.session_state.view = "Crop"

if btn1.button("🌾 Crop-wise"):
    st.session_state.view = "Crop"

if btn2.button("📍 State-wise"):
    st.session_state.view = "State"

if btn3.button("📈 Year-wise"):
    st.session_state.view = "Year"

if btn4.button("🌦 Season-wise"):
    st.session_state.view = "Season"

st.markdown("---")


# VISUALIZATION SECTION
if st.session_state.view == "Crop":
    st.subheader("Top Crops by Production")

    data = crop_summary.sort_values(
        by="Production", ascending=False
    ).head(top_n)

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(data['Crop'], data['Production'])
    ax.set_xlabel("Crop")
    ax.set_ylabel("Production")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

elif st.session_state.view == "State":
    st.subheader("Top States by Production")

    data = state_summary.sort_values(
        by="Production", ascending=False
    ).head(top_n)

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(data['State_Name'], data['Production'])
    ax.set_xlabel("State")
    ax.set_ylabel("Production")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

elif st.session_state.view == "Year":
    st.subheader("Year-wise Production Trend")

    data = yearly_summary.sort_values(by="Crop_Year")

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(data['Crop_Year'], data['Production'])
    ax.set_xlabel("Year")
    ax.set_ylabel("Production")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

elif st.session_state.view == "Season":
    st.subheader("Season-wise Production Distribution")

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(season_summary['Season'], season_summary['Production'])
    ax.set_xlabel("Season")
    ax.set_ylabel("Production")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

# INSIGHTS
st.markdown("### 📌 Key Insights")
st.write("""
• Few crops dominate India's total production  
• Agricultural output is regionally concentrated  
• Long-term production growth is visible  
• Seasonal variation plays a major role  
""")

# Footer
st.markdown("---")
st.caption("Developed by Akash ")
