import streamlit as st

from utils.data_loader import load_data
from analysis.funnel_analysis import *
from components.charts import *
from ml.lead_model import train_lead_model

st.set_page_config(
    page_title="Marketing Funnel Analytics",
    layout="wide"
)

# ================= DARK MODE STYLE =================
st.markdown("""
<style>

html, body, [class*="css"] {
    background-color:#0b0f1a;
    color:white;
}

.metric-card{
background:linear-gradient(135deg,#1f2937,#111827);
padding:20px;
border-radius:12px;
text-align:center;
}

.metric-title{
color:#9ca3af;
}

.metric-value{
font-size:28px;
font-weight:bold;
color:#22c55e;
}

</style>
""", unsafe_allow_html=True)

st.title("🚀 Marketing Funnel & Conversion Intelligence")

# ================= LOAD DATA =================
df = load_data()

# ================= TOP FILTER BAR =================
st.markdown("### Dashboard Filters")

f1, f2 = st.columns(2)

with f1:
    channel = st.multiselect(
        "Contact Channel",
        df["contact"].unique(),
        default=df["contact"].unique()
    )

with f2:
    campaign = st.slider(
        "Campaign Range",
        int(df["campaign"].min()),
        int(df["campaign"].max()),
        (int(df["campaign"].min()), int(df["campaign"].max()))
    )

# ================= APPLY FILTERS =================
df = df[
(df["contact"].isin(channel)) &
(df["campaign"] >= campaign[0]) &
(df["campaign"] <= campaign[1])
]

# ================= KPI METRICS =================
visitors, leads, customers, v_l, l_c, overall = funnel_metrics(df)

k1,k2,k3 = st.columns(3)

k1.metric("Visitors", visitors)
k2.metric("Leads", leads)
k3.metric("Customers", customers)

k4,k5,k6 = st.columns(3)

k4.metric("Visitor → Lead %", v_l)
k5.metric("Lead → Customer %", l_c)
k6.metric("Overall Conversion %", overall)

st.divider()

# ================= FUNNEL =================
st.subheader("Marketing Funnel")

funnel = dropoff_data(df)

fig_funnel = funnel_chart(funnel)
fig_funnel.update_layout(template="plotly_dark")

st.plotly_chart(fig_funnel, use_container_width=True)

st.divider()

# ================= CHANNEL + CAMPAIGN =================
col1, col2 = st.columns(2)

with col1:

    st.subheader("Channel Performance")

    channel_perf = channel_performance(df)

    fig_channel = channel_chart(channel_perf)
    fig_channel.update_layout(template="plotly_dark")

    st.plotly_chart(fig_channel, use_container_width=True)

with col2:

    st.subheader("Campaign Conversion")

    campaign_perf = campaign_performance(df)

    fig_campaign = campaign_chart(campaign_perf)
    fig_campaign.update_layout(template="plotly_dark")

    st.plotly_chart(fig_campaign, use_container_width=True)

st.divider()

# ================= TREND =================
st.subheader("Monthly Conversion Trend")

trend = monthly_conversion(df)

fig_trend = conversion_trend(trend)
fig_trend.update_layout(template="plotly_dark")

st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# ================= ML MODEL =================
st.subheader("🤖 Lead Conversion Prediction Model")

model, accuracy, importance = train_lead_model(df)

st.success("Lead scoring model trained")

st.metric("Model Accuracy", str(round(accuracy*100,2))+"%")

st.markdown("### Feature Importance")

st.bar_chart(importance.set_index("Feature"))

st.divider()

# ================= INSIGHTS =================
st.subheader("📌 Key Insights")

st.markdown("""
• Large drop-off occurs at **Visitor → Lead stage**

• Some **contact channels convert significantly better**

• Campaign frequency influences **conversion probability**
""")

st.subheader("🚀 Recommendations")

st.markdown("""
• Improve landing page lead capture

• Invest more budget in high-performing channels

• Optimize campaigns with low conversion rates
""")