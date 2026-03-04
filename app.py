import streamlit as st

from utils.data_loader import load_data
from analysis.funnel_analysis import *
from components.charts import *
from ml.lead_model import train_lead_model

st.set_page_config(
    page_title="Marketing Funnel Analytics",
    layout="wide"
)

st.title("🚀 Marketing Funnel & Conversion Analytics")

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")

channel = st.sidebar.selectbox(
    "Contact Channel",
    ["All"] + list(df["contact"].unique())
)

if channel != "All":
    df = df[df["contact"]==channel]

# KPIs
visitors, leads, customers, v_l, l_c, overall = funnel_metrics(df)

col1,col2,col3 = st.columns(3)

col1.metric("Visitors", visitors)
col2.metric("Leads", leads)
col3.metric("Customers", customers)

st.markdown("---")

col4,col5,col6 = st.columns(3)

col4.metric("Visitor → Lead %", v_l)
col5.metric("Lead → Customer %", l_c)
col6.metric("Overall Conversion %", overall)

st.markdown("---")

# Funnel
st.subheader("Marketing Funnel")

funnel = dropoff_data(df)

st.plotly_chart(
    funnel_chart(funnel),
    use_container_width=True
)

st.markdown("---")

# Channel Analysis
st.subheader("Channel Performance")

channel_perf = channel_performance(df)

st.plotly_chart(
    channel_chart(channel_perf),
    use_container_width=True
)

st.markdown("---")

# Campaign Analysis
st.subheader("Campaign Conversion")

campaign_perf = campaign_performance(df)

st.plotly_chart(
    campaign_chart(campaign_perf),
    use_container_width=True
)

st.markdown("---")

# Conversion Trend
st.subheader("Monthly Conversion Trend")

trend = monthly_conversion(df)

st.plotly_chart(
    conversion_trend(trend),
    use_container_width=True
)

st.markdown("---")

# ML Model
st.subheader("Lead Conversion Prediction Model")

model, accuracy, importance = train_lead_model(df)

st.success("Lead scoring model trained")

st.metric("Model Accuracy", str(round(accuracy*100,2))+"%")

st.markdown("### Feature Importance")

st.bar_chart(
    importance.set_index("Feature")
)

st.markdown("---")

st.subheader("Key Insights")

st.write("• Large drop-off occurs at Visitor → Lead stage.")

st.write("• Certain contact channels convert significantly better.")

st.write("• Campaign frequency influences conversion probability.")

st.subheader("Recommendations")

st.write("• Improve landing page lead capture.")

st.write("• Focus marketing budget on high converting channels.")

st.write("• Optimize campaigns with low performance.")