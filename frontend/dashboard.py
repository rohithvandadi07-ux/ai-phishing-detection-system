import os

import streamlit as st
from streamlit_autorefresh import st_autorefresh

import pandas as pd

import plotly.express as px

from sqlalchemy import create_engine

from dotenv import load_dotenv

# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(

    page_title="AI Phishing Shield",

    page_icon="🛡️",

    layout="wide",

    initial_sidebar_state="expanded"

)

# ---------------------------------------------------
# AUTO REFRESH
# ---------------------------------------------------

st_autorefresh(

    interval=5000,

    key="dashboard_refresh"

)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""

<style>

.main {

    background-color: #0f172a;
    color: white;
}

section[data-testid="stSidebar"] {

    background-color: #111827;
}

h1, h2, h3, h4 {

    color: white !important;
}

div[data-testid="metric-container"] {

    background-color: #1e293b;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #334155;
}

.stDataFrame {

    background-color: white;
}

</style>

""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🛡️ AI Phishing Shield")

st.sidebar.markdown(
    "### Enterprise Security Dashboard"
)

st.sidebar.divider()

st.sidebar.success("System Status: ACTIVE")

st.sidebar.info(
    "Cloud Threat Monitoring Enabled"
)

st.sidebar.divider()

st.sidebar.markdown("""
### Dashboard Modules

- 📊 Threat Analytics
- 🚨 Live Threat Feed
- 📈 Detection Timeline
- 📄 Detection Logs
- ⬇️ Export Reports
- ☁️ PostgreSQL Telemetry
""")

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🛡️ AI Phishing Shield")

st.markdown(
    "## Enterprise Threat Intelligence Dashboard"
)

st.divider()

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------

engine = create_engine(
    DATABASE_URL
)

query = """

    SELECT *

    FROM detections

    ORDER BY id DESC

"""

df = pd.read_sql_query(
    query,
    engine
)

# ---------------------------------------------------
# EMPTY CHECK
# ---------------------------------------------------

if df.empty:

    st.warning(
        "No detections found yet."
    )

    st.stop()

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------

total_scans = len(df)

malicious_count = len(
    df[df["prediction"] == "malicious"]
)

safe_count = len(
    df[df["prediction"] == "safe"]
)

critical_count = len(
    df[df["risk_level"] == "CRITICAL"]
)

high_count = len(
    df[df["risk_level"] == "HIGH"]
)

avg_risk = round(
    df["risk_score"].mean(),
    2
)

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

st.subheader("📊 Security Analytics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Scans",
    total_scans
)

col2.metric(
    "Malicious URLs",
    malicious_count
)

col3.metric(
    "Safe URLs",
    safe_count
)

col4, col5, col6 = st.columns(3)

col4.metric(
    "Critical Threats",
    critical_count
)

col5.metric(
    "High Risk Threats",
    high_count
)

col6.metric(
    "Average Risk Score",
    avg_risk
)

st.divider()

# ---------------------------------------------------
# CHARTS
# ---------------------------------------------------

left_col, right_col = st.columns(2)

# PIE CHART
with left_col:

    pie_chart = px.pie(

        names=[
            "Safe",
            "Malicious"
        ],

        values=[
            safe_count,
            malicious_count
        ],

        title="Threat Distribution"

    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )

# RISK DISTRIBUTION
with right_col:

    risk_chart = px.histogram(

        df,

        x="risk_level",

        title="Risk Level Distribution"

    )

    st.plotly_chart(
        risk_chart,
        use_container_width=True
    )

st.divider()

# ---------------------------------------------------
# TIMELINE
# ---------------------------------------------------

st.subheader("📈 Detection Timeline")

timeline_df = (

    df.groupby("timestamp")
    .size()
    .reset_index(name="detections")

)

timeline_chart = px.line(

    timeline_df,

    x="timestamp",

    y="detections",

    markers=True,

    title="Threat Activity"

)

st.plotly_chart(
    timeline_chart,
    use_container_width=True
)

st.divider()

# ---------------------------------------------------
# LIVE THREAT FEED
# ---------------------------------------------------

st.subheader("🚨 Live Threat Feed")

live_threats = df[
    df["prediction"] == "malicious"
]

for _, row in live_threats.head(5).iterrows():

    st.error(

        f"""
        🚨 {row['risk_level']} Threat

        URL: {row['url']}

        Risk Score: {row['risk_score']}

        Time: {row['timestamp']}
        """

    )

st.divider()

# ---------------------------------------------------
# FILTERS
# ---------------------------------------------------

st.subheader("🔍 Detection Filters")

search_term = st.text_input(
    "Search URL"
)

risk_filter = st.selectbox(

    "Filter by Risk Level",

    [
        "ALL",
        "SAFE",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ]

)

filtered_df = df.copy()

# URL SEARCH
if search_term:

    filtered_df = filtered_df[
        filtered_df["url"]
        .str.contains(
            search_term,
            case=False,
            na=False
        )
    ]

# RISK FILTER
if risk_filter != "ALL":

    filtered_df = filtered_df[
        filtered_df["risk_level"]
        == risk_filter
    ]

# ---------------------------------------------------
# EXPORT CSV
# ---------------------------------------------------

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(

    label="⬇️ Export Detection Logs CSV",

    data=csv_data,

    file_name="phishing_detection_logs.csv",

    mime="text/csv"

)

st.divider()

# ---------------------------------------------------
# DETECTION LOG TABLE
# ---------------------------------------------------

st.subheader("📄 Detection Logs")

st.dataframe(

    filtered_df,

    use_container_width=True,

    height=400

)

st.divider()

# ---------------------------------------------------
# RECENT MALICIOUS URLS
# ---------------------------------------------------

st.subheader("⚠️ Recent Malicious URLs")

recent_threats = df[
    df["prediction"] == "malicious"
]

st.dataframe(

    recent_threats.head(10),

    use_container_width=True,

    height=300

)

st.divider()

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown(
    "## 🛡️ AI Phishing Shield — Enterprise Monitoring Platform"
)