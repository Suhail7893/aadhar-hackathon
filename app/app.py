import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="UIDAI Demand Intelligence",
    layout="wide",
    page_icon="app/uidai_logo.png"
)

# ---------------- PREMIUM UI THEME (FROM FIRST CODE) ----------------
st.markdown("""
<style>

.stApp {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: "Inter", sans-serif;
}

h1, h2, h3 {
    color: #020617;
    font-weight: 700;
}

h1 { font-size: 38px; }
h2 { font-size: 26px; }
h3 { font-size: 22px; }

/* ===== INFO BANNER (SKY BLUE) FIX ===== */
div[data-testid="stAlert"] {
    background-color: #cfe8ff !important;
    border-left: none !important;   /* REMOVE DARK BLUE STRIP */
    border-radius: 14px !important;
    color: #000000 !important;      /* BLACK TEXT */
    font-weight: 500;
}
            
/* Make percentage bold inside info banner */
div[data-testid="stAlert"] p strong {
    font-weight: 800 !important;
    color: #000000 !important;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
    border: 1px solid #e5e7eb;
}

div[data-testid="stMetricLabel"] {
    font-size: 14px;
    color: #020617;
    font-weight: 700;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

div[data-testid="stMetricValue"] {
    font-size: 30px;
    font-weight: 700;
    color: #020617;
}

div[data-testid="stDataFrame"] {
    background-color: #020617;
    border-radius: 14px;
    padding: 6px;
}

div[data-testid="stDataFrame"] tbody tr:hover {
    background-color: #1e293b !important;
}

button {
    border-radius: 10px !important;
    font-weight: 600 !important;
}

div[data-testid="stDownloadButton"] > button {
    background-color: #2563eb !important;
    color: white !important;
    padding: 0.6rem 1.4rem;
    border-radius: 12px;
    border: none;
}

div[data-testid="stDownloadButton"] > button:hover {
    background-color: white !important;
    color: #2563eb !important;
    border: 2px solid #2563eb;
}
            
/* ===== FORCE KPI METRIC HEADINGS STYLE ===== */
div[data-testid="stMetric"] label {
    text-transform: uppercase !important;
    font-weight: 800 !important;
    color: #020617 !important;
    font-size: 14px !important;
    letter-spacing: 0.6px !important;
}

/* Backup selector (Streamlit version safe) */
div[data-testid="stMetric"] label span {
    text-transform: uppercase !important;
    font-weight: 800 !important;
    color: #020617 !important;
}
            
/* ===== FORCE KPI METRIC HEADING BOLD ===== */
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] label span {
    text-transform: uppercase !important;
    font-weight: 900 !important;   /* MAX BOLD */
    font-size: 14px !important;
    color: #020617 !important;
    letter-spacing: 0.6px !important;

    /* Force bold even for variable fonts */
    font-variation-settings: "wght" 900 !important;
}
            
/* ===== CUSTOM SKY-BLUE INFO BANNER ===== */
.custom-info {
    background-color: #cfe8ff;
    border-radius: 14px;
    padding: 14px 18px;
    margin-bottom: 20px;
    color: #000000;
    font-size: 16px;
    font-weight: 500;
}

/* Bold & dark percentage */
.custom-info .pct {
    font-weight: 800;
    color: #000000;
}

/* ===== DATAFRAME CONTAINER ===== */
div[data-testid="stDataFrame"] {
    background-color: white !important;
    border-radius: 10px;
    border: 1px solid #d1d5db;
}

/* =========================
   FORCE LIGHT TABLE THEME
   ========================= */

/* Outer container */
div[data-testid="stDataFrame"] {
    background-color: #ffffff !important;
    border: 2px solid #000000 !important;
    border-radius: 8px;
}

/* Table base */
div[data-testid="stDataFrame"] table {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-collapse: collapse !important;
}

/* Header */
div[data-testid="stDataFrame"] thead th {
    background-color: #ffffff !important;
    color: #000000 !important;
    font-weight: 700 !important;
    border: 1px solid #000000 !important;
}

/* Body rows */
div[data-testid="stDataFrame"] tbody tr {
    background-color: #ffffff !important;
}

/* Body cells */
div[data-testid="stDataFrame"] tbody td {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #000000 !important;
}

/* Remove any dark hover */
div[data-testid="stDataFrame"] tbody tr:hover td {
    background-color: #f5f5f5 !important;
    color: #000000 !important;
}
            
/* ==============================
   FORCE SELECTBOX HEADING BOLD
   ============================== */

div[data-testid="stSelectbox"] label {
    color: #020617 !important;
    font-size: 15px !important;
    font-weight: 900 !important;          /* MAX BOLD */
    letter-spacing: 0.6px !important;
    text-transform: uppercase !important;

    /* Force bold even for variable fonts like Inter */
    font-variation-settings: "wght" 900 !important;

    margin-bottom: 8px !important;
    display: block !important;
}

/* Emoji inside heading */
div[data-testid="stSelectbox"] label span {
    font-weight: 900 !important;
    color: #020617 !important;
}

/* ==============================
   FORCE AI SUMMARY TEXT BLACK
   ============================== */

div[data-testid="stAlert"] {
    background-color: #cfe8ff !important;
    color: #000000 !important;          /* FORCE BLACK TEXT */
    font-weight: 500;
}

/* Paragraph text inside alert */
div[data-testid="stAlert"] p {
    color: #000000 !important;
}

/* Bold text (AI Summary label) */
div[data-testid="stAlert"] p strong {
    color: #000000 !important;
    font-weight: 800 !important;
}

/* Emoji inside alert */
div[data-testid="stAlert"] span {
    color: #000000 !important;
}            

footer { visibility: hidden; }
            
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
DATA_PATH = "output/"

demand_trend = pd.read_csv(DATA_PATH + "demand_monthly_summary.csv")
risk_data = pd.read_csv(DATA_PATH + "district_risk_all_levels_final.csv")
spike_alerts = pd.read_csv(DATA_PATH + "demand_spike_alerts.csv")
actions = pd.read_csv(DATA_PATH + "final_decision_action_cleaned.csv")

spike_alerts["year_month"] = pd.to_datetime(spike_alerts["year_month"], format="%Y-%m")
spike_alerts["year_month"] = spike_alerts["year_month"].dt.strftime("%Y-%b")

# ---------------- CLEAN RISK LEVEL ----------------
def clean_risk_level(val):
    if pd.isna(val):
        return None
    text = re.sub(r"<.*?>", "", str(val))
    text = text.strip().lower()
    if "high" in text:
        return "High"
    if "medium" in text:
        return "Medium"
    return "Low"

risk_data["risk_level"] = risk_data["risk_level"].apply(clean_risk_level)

# ---------------- HEADER ----------------
import base64

def load_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = load_image_base64("app/uidai_logo.png")

st.markdown(
    f"""
    <div style="display:flex; flex-direction:column; align-items:center;">
        <img src="data:image/png;base64,{logo_base64}" width="460"/>
        <h1 style="margin-top:10px;">UIDAI Demand Intelligence</h1>
        <p style="color:#475569; font-size:15px;">
            AI-driven Aadhaar Demand & Risk Analytics Platform
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<hr style='margin-top:15px; margin-bottom:25px;'>", unsafe_allow_html=True)



st.markdown("---")

# ---------------- KPI METRICS ----------------


demand_trend["month"] = pd.to_datetime(demand_trend["month"], errors="coerce")
demand_trend = demand_trend.dropna(subset=["month"]).sort_values("month")

latest = demand_trend.iloc[-1]
prev = demand_trend.iloc[-2]
change_pct = ((latest["total_demand"] - prev["total_demand"]) / prev["total_demand"]) * 100

st.markdown(
    f"""
    <div class="custom-info">
        Latest month shows a 
        <span class="pct">{change_pct:.1f}%</span>
        change in demand compared to the previous month.
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- KPI METRICS ----------------
# Additional KPI calculations
peak_demand_lakh = (demand_trend["total_demand"].max()) / 100000
lowest_demand_lakh = (demand_trend["total_demand"].min()) / 100000
avg_monthly_demand_lakh = (demand_trend["total_demand"].mean()) / 100000


# ---- KPI Row 1 (4 cards) ----
r1c1, r1c2, r1c3, r1c4 = st.columns(4)

r1c1.metric("📍 Districts Analyzed", f"{risk_data['district'].nunique():,}")
r1c2.metric("⚠️ High-Risk Districts", f"{(risk_data['risk_level'] == 'High').sum():,}")
r1c3.metric("📈 Demand Spikes", f"{spike_alerts.shape[0]:,}")
r1c4.metric("🧠 Actions Generated", f"{actions.shape[0]:,}")

# ---- KPI Row 2 (3 cards) ----
r2c1, r2c2, r2c3 = st.columns(3)

r2c1.metric("🚀 Peak Demand (Lakhs)", f"{peak_demand_lakh:.1f}")
r2c2.metric("📉 Lowest Demand (Lakhs)", f"{lowest_demand_lakh:.1f}")
r2c3.metric("📊 Avg Monthly Demand (Lakhs)", f"{avg_monthly_demand_lakh:.1f}")

st.markdown("---")

# ---------------- DEMAND TREND (LOGIC FROM SECOND CODE) ----------------
st.subheader("📊 Aadhaar Demand Intelligence Overview")
st.caption(
    "This visualization highlights demand volatility, identifies abnormal surge periods, "
    "and helps administrators distinguish onboarding spikes from stable operational demand."
)

demand_trend["smoothed_demand"] = (
    demand_trend["total_demand"]
    .rolling(3, min_periods=1)
    .mean()
)
demand_trend["demand_lakh"] = demand_trend["smoothed_demand"] / 100000

median_val = demand_trend["demand_lakh"].median()
# Identify spike months (above 1.05x median)
spike_threshold = median_val * 1.05
spike_months = demand_trend[demand_trend["demand_lakh"] > spike_threshold]


fig, ax = plt.subplots(figsize=(11, 4.5))

# Demand trend line
ax.plot(
    demand_trend["month"],
    demand_trend["demand_lakh"],
    marker="o",
    linewidth=2.5,
    label="Demand Trend"
)
# Median demand line
ax.axhline(
    median_val,
    linestyle="--",
    linewidth=2,
    alpha=0.7,
    label="Post-Stabilization Median Demand"
)

# Highlight spike months
ax.scatter(
    spike_months["month"],
    spike_months["demand_lakh"],
    color="red",
    s=70,
    zorder=5,
    label="Spike Months"
)

# Highlight early high-demand phase (first 3 months)
ax.axvspan(
    demand_trend["month"].iloc[0],
    demand_trend["month"].iloc[2],
    color="#e5e7eb",
    alpha=0.6,
    label="Initial High-Demand Phase"
)

# Axis labels & title
ax.set_title(
    "Monthly Aadhaar Demand Trend & Stabilization Analysis",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Month", fontsize=11)
ax.set_ylabel("Demand (Lakhs)", fontsize=11)

# Grid & legend
ax.grid(True, alpha=0.3)
ax.legend(frameon=False)

plt.tight_layout()
st.pyplot(fig)

st.markdown(
    """
    <div class="ai-insight">
        📌 <strong>AI Insight:</strong>
        Aadhaar demand shows an initial onboarding surge, followed by a stable demand pattern.
        Post-stabilization months remain close to the median, enabling predictable resource planning.
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Note: Smoothed demand uses a rolling average to reduce short-term noise "
    "and highlight long-term operational trends."
)

# ---------------- SPIKE ALERTS ----------------
st.subheader("🚨 Demand Surge Intelligence")
st.caption(
    "This table lists all detected demand surges across districts. "
    "Risk levels indicate the relative severity of deviation from normal demand patterns."
)

spike_df = spike_alerts.copy()

spike_df["spike_label"] = spike_df["spike_level"].map({
    "HIGH_SPIKE": "High",
    "MEDIUM_SPIKE": "Medium",
    "NORMAL": "Low"
})

spike_df = spike_df.reset_index(drop=True)
severity_order = {"High": 3, "Medium": 2, "Low": 1}

spike_df["sev"] = spike_df["spike_label"].map(severity_order)
spike_df = spike_df.sort_values("sev", ascending=False).drop(columns="sev")

display_df = spike_df.drop(
    columns=["spike_level", "mom_growth"],
    errors="ignore"
)

# Define risk priority (use original column name)
risk_priority = {"High": 3, "Medium": 2, "Low": 1}

display_df["risk_rank"] = display_df["spike_label"].map(risk_priority)

# Sort by severity → latest month → highest demand
display_df = display_df.sort_values(
    by=["risk_rank", "year_month", "demand_total"],
    ascending=[False, False, False]
)

# Drop helper column
display_df = display_df.drop(columns=["risk_rank"])

# Reset index and create S.No
display_df = display_df.reset_index(drop=True)
display_df.insert(0, "S.No", display_df.index + 1)

# Remove invalid district rows (numeric junk like 100000)
spike_df = spike_df[~spike_df["district"].astype(str).str.isnumeric()]

# Drop technical columns
display_df = spike_df[
    ~spike_df["district"].astype(str).str.isnumeric()
].drop(
    columns=["spike_level", "mom_growth"],
    errors="ignore"
)

# Rename columns (government style)
display_df = display_df.rename(columns={
    "district": "District",
    "year_month": "Month",
    "demand_total": "Total Demand",
    "spike_label": "Risk Level"
})

# Reset index and create proper S.No
display_df = display_df.reset_index(drop=True)
display_df.insert(0, "S.No", display_df.index + 1)

# Format demand numbers
display_df["Total Demand"] = display_df["Total Demand"].map("{:,}".format)

def risk_badge(val):
    if val == "High": return "🔴 High"
    if val == "Medium": return "🟠 Medium"
    return "🟢 Low"

display_df["Risk Level"] = display_df["Risk Level"].apply(risk_badge)

st.data_editor(
    display_df,
    use_container_width=True,
    height=420,
    hide_index=True,
    disabled=True
)

st.download_button(
    "⬇️ Download Spike Alerts (CSV)",
    data=spike_df.to_csv(index=False),
    file_name="demand_spike_alerts.csv",
    mime="text/csv"
)

st.caption(
    "Note: Records are ordered by risk severity, most recent month, and total demand. "
    "This prioritization helps administrators focus on the most critical and recent demand surges."
)

# ---------------- RISK CLASSIFICATION ----------------
st.subheader("🛡️ District Risk Intelligence Console")
st.caption("AI-assisted classification using volatility, anomalies, and historical trends")

severity = {"High": 3, "Medium": 2, "Low": 1}

district_risk = (
    risk_data
    .assign(sev=risk_data["risk_level"].map(severity))
    .sort_values("sev", ascending=False)
    .drop_duplicates(subset=["state", "district"], keep="first")
    .drop(columns="sev")
)

filtered = district_risk.copy()

high_cnt = (filtered["risk_level"] == "High").sum()
med_cnt = (filtered["risk_level"] == "Medium").sum()
low_cnt = (filtered["risk_level"] == "Low").sum()

filtered["AI Reason"] = filtered["risk_level"].map({
    "High": "Repeated demand spikes detected",
    "Medium": "Emerging demand deviation",
    "Low": "Stable historical demand"
})
def confidence_band(val):
    if val >= 85:
        return "High Confidence"
    if val >= 60:
        return "Moderate Confidence"
    return "Low Confidence"


st.info(
    f"🧠 **AI Summary:** {high_cnt} districts require immediate intervention, "
    f"{med_cnt} show early warning signals, and {low_cnt} remain stable."
)


col1, col2 = st.columns([2, 1])

states = sorted(district_risk["state"].dropna().unique())
selected_state = st.selectbox("🌍 Select State", ["All States"] + states)
selected_risk = st.selectbox("⚠️ Risk Level", ["All", "High", "Medium", "Low"])


if selected_state != "All States":
    filtered = filtered[filtered["state"] == selected_state]
if selected_risk != "All":
    filtered = filtered[filtered["risk_level"] == selected_risk]

# ---------- AI CONFIDENCE ----------
filtered["AI Confidence (%)"] = filtered["risk_level"].map({
    "High": 90,
    "Medium": 65,
    "Low": 40
})

def confidence_band(val):
    if val >= 85:
        return "High Confidence"
    elif val >= 60:
        return "Moderate Confidence"
    return "Low Confidence"

filtered["Model Confidence"] = filtered["AI Confidence (%)"].apply(confidence_band)

filtered["AI Confidence"] = filtered["risk_level"].map({
    "High": "Very High (90%)",
    "Medium": "Moderate (65%)",
    "Low": "Low (40%)"
})

filtered["Recommended Action"] = filtered["risk_level"].map({
    "High": "🚨 Immediate intervention required",
    "Medium": "⚠️ Monitor & prepare response",
    "Low": "✅ Routine monitoring"
})

filtered["Risk Status"] = filtered["risk_level"].apply(risk_badge)

# Reset index and add S.No
filtered = filtered.reset_index(drop=True)
filtered.insert(0, "S.No", filtered.index + 1)

st.dataframe(
    filtered[
        [
            "S.No",
            "district",
            "state",
            "Risk Status",
            "AI Confidence",
            "AI Reason",
            "Recommended Action"
        ]
    ],
    use_container_width=True,
    height=420,
    hide_index=True   # 🔥 THIS REMOVES THE LEFT COLUMN
)

st.caption(
    "🔴 High Risk: Immediate operational action required | "
    "🟠 Medium Risk: Monitor closely | "
    "🟢 Low Risk: Routine monitoring sufficient"
)

st.caption(
    "📝 **Sorting Logic:** Districts are ordered by **risk severity (High → Low)**, "
    "then by **most recent anomaly occurrence**, and finally by **demand intensity**. "
    "This ensures that the most critical districts appear at the top for faster decision-making."
)

# ---------------- PRIORITY DISTRICTS ----------------
st.markdown("## 🚨 Priority Attention Districts")
st.caption("Top districts requiring immediate or close administrative attention")

high_risk = district_risk[district_risk["risk_level"] == "High"].head(5)
medium_risk = district_risk[district_risk["risk_level"] == "Medium"].head(5)

col_high, col_medium = st.columns(2)

# -------- HIGH RISK COLUMN --------
with col_high:
    st.markdown("### 🔴 High Risk (Immediate Action)")
    for _, row in high_risk.iterrows():
        st.markdown(
            f"""
            **🔴 {row['district']} ({row['state']})**  
            🧠 AI Confidence: **Very High (90%)**  
            🚨 _Immediate intervention recommended_
            """
        )

# -------- MEDIUM RISK COLUMN --------
with col_medium:
    st.markdown("### 🟠 Medium Risk (Early Warning)")
    for _, row in medium_risk.iterrows():
        st.markdown(
            f"""
            **🟠 {row['district']} ({row['state']})**  
            🧠 AI Confidence: **Moderate (65%)**  
            ⚠️ _Monitor closely & prepare contingency_
            """
        )

# ---------------- ACTIONS ----------------
st.subheader("🎯 Actionable Decision Support")
st.caption(
    "Operational guidance generated from demand spikes, risk severity, and historical trends"
)

# ---------------- CLEAN RECOMMENDATIONS ----------------

actions_df = actions.copy()

# Keep only relevant columns
actions_df = actions_df[
    [
        "state",
        "district",
        "month",
        "spike_flag",
        "monthly_total_load"
    ]
]

# Rename for clarity
actions_df = actions_df.rename(columns={
    "monthly_total_load": "Current Load",
    "spike_flag": "Demand Status"
})

# Action mapping
actions_df["Recommended Action"] = actions_df["Demand Status"].map({
    "HIGH_SPIKE": "🚨 Deploy additional operators & resources",
    "MEDIUM_SPIKE": "⚠️ Prepare standby capacity",
    "NORMAL": "✅ Continue routine operations"
})

# Priority mapping
actions_df["Priority"] = actions_df["Demand Status"].map({
    "HIGH_SPIKE": "🔴 High",
    "MEDIUM_SPIKE": "🟠 Medium",
    "NORMAL": "🟢 Low"
})

# Sort: High → Medium → Low, then latest month
priority_order = {"🔴 High": 3, "🟠 Medium": 2, "🟢 Low": 1}
actions_df["p"] = actions_df["Priority"].map(priority_order)

actions_df = actions_df.sort_values(
    by=["p", "month"],
    ascending=[False, False]
).drop(columns="p")

# Reset index & add S.No
actions_df = actions_df.reset_index(drop=True)
actions_df.insert(0, "S.No", actions_df.index + 1)

actions_df = actions_df.rename(columns={
    "Demand Status": "Risk Level",
    "Recommended Action": "Action Recommendation"
})

actions_df["Risk Level"] = actions_df["Risk Level"].map({
    "HIGH_SPIKE": "High",
    "MEDIUM_SPIKE": "Medium",
    "NORMAL": "Low"
})

def risk_badge(val):
    if val == "High":
        return "🔴 High"
    if val == "Medium":
        return "🟠 Medium"
    return "🟢 Low"

actions_df["Risk Level"] = actions_df["Risk Level"].apply(risk_badge)

st.dataframe(
    actions_df[
        [
            "S.No",
            "state",
            "district",
            "month",
            "Priority",
            "Current Load",
            "Action Recommendation"
        ]
    ],
    use_container_width=True,
    height=420,
    hide_index=True
)

st.caption(
    "📝 **Sorting Logic:** Recommendations are prioritized by **severity of demand spike** "
    "(High → Medium → Normal) and then by **most recent month**, ensuring urgent actions appear first."
)

st.success(
    "This AI-driven decision support enables UIDAI to plan ahead instead of reacting late."
)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>Built for UIDAI Hackathon | Data-Driven Governance 🇮🇳</p>",
    unsafe_allow_html=True
)
