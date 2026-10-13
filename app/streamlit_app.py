from pathlib import Path
import html

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# -----------------------------------------------------------------------------
# 1. Page setup and Swiggy-inspired styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Swiggy Customer Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

SWIGGY_ORANGE = "#FC8019"
SWIGGY_DARK = "#242424"
PAGE_BG = "#F7F8FA"
CARD_BG = "#FFFFFF"
TEXT = "#202124"
MUTED = "#5F6368"
RED = "#E84855"
YELLOW = "#F4B400"
GREEN = "#1C9B5F"

st.markdown(
    f"""
    <style>
      :root {{ color-scheme: light; }}
      html, body, [class*="stApp"] {{ background: {PAGE_BG}; color: {TEXT}; }}
      [data-testid="stAppViewContainer"] {{ background: {PAGE_BG}; }}
      [data-testid="stHeader"] {{ background: rgba(247,248,250,0.96); }}
      [data-testid="stSidebar"] {{ background: #FFF4E9; border-right: 1px solid #F3D7C1; }}
      [data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
      [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
      [data-testid="stSidebar"] h3 {{ color: {SWIGGY_ORANGE} !important; }}
      h1, h2, h3, h4, p, label, span, li {{ color: {TEXT}; }}
      h1, h2, h3 {{ letter-spacing: -0.25px; }}
      [data-testid="stMarkdownContainer"] p {{ line-height: 1.5; }}
      [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label {{ color: {TEXT} !important; }}
      div[data-baseweb="select"] *, div[data-baseweb="input"] *,
      div[data-baseweb="textarea"] * {{ color: {TEXT} !important; }}
      div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
      div[data-testid="stTextInput"] input,
      div[data-testid="stNumberInput"] input {{
        background: #FFFFFF !important; color: {TEXT} !important;
        border-color: #D6D9DE !important; border-radius: 9px !important;
      }}
      div[data-testid="stButton"] button {{
        background: {SWIGGY_ORANGE}; color: #FFFFFF !important;
        border: 1px solid {SWIGGY_ORANGE}; border-radius: 9px;
        font-weight: 650; min-height: 2.5rem;
      }}
      div[data-testid="stButton"] button:hover {{
        background: #E96F08; border-color: #E96F08; color: #FFFFFF !important;
      }}
      div[data-testid="stFormSubmitButton"] button {{
        background: {SWIGGY_ORANGE}; color: #FFFFFF !important;
      }}
      [data-testid="stMetric"] {{
        width: 96%; margin: 0 auto; box-sizing: border-box;
        background: {CARD_BG}; padding: 12px 12px; border-radius: 12px;
        border: 1px solid #E7E8EB; border-bottom: 4px solid {SWIGGY_ORANGE};
        box-shadow: 0 3px 10px rgba(20,25,30,0.04);
      }}
      [data-testid="stMetricLabel"] p {{ color: {MUTED} !important; font-size: 0.82rem; }}
      [data-testid="stMetricValue"] {{ color: {SWIGGY_ORANGE} !important; font-weight: 750; font-size: clamp(1.05rem, 1.35vw, 1.55rem); line-height: 1.2; overflow-wrap: anywhere; }}
      [data-testid="stMetricLabel"] {{ min-height: 2.1rem; }}
      .risk-note {{ color: {MUTED} !important; font-size: 0.78rem; line-height: 1.35; margin-top: -4px; }}
      .featured-offer {{ background: linear-gradient(125deg, #FFF0E2 0%, #FFFFFF 58%, #FFE0C2 100%); border: 1px solid #F4C49D; border-top: 6px solid {SWIGGY_ORANGE}; border-radius: 18px; padding: 22px; box-shadow: 0 8px 24px rgba(252,128,25,0.12); }}
      .offer-topline {{ color: #A64B00 !important; font-size: 0.78rem; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; }}
      .offer-discount {{ color: {SWIGGY_ORANGE} !important; font-size: 2rem; font-weight: 900; line-height: 1.1; margin: 8px 0; }}
      .offer-code {{ display: inline-block; background: {SWIGGY_DARK}; color: #FFFFFF !important; padding: 8px 14px; border-radius: 8px; font-weight: 800; letter-spacing: 1px; margin: 5px 0 12px 0; }}
      .offer-details {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0; }}
      .offer-chip {{ display: inline-block; background: #FFFFFF; border: 1px solid #F0C9A9; border-radius: 8px; padding: 7px 10px; color: {TEXT} !important; font-size: 0.82rem; font-weight: 650; }}
      .offer-reason {{ background: #FFFFFF; border-left: 4px solid {SWIGGY_ORANGE}; border-radius: 8px; padding: 12px 14px; margin-top: 12px; color: {TEXT} !important; }}
      .offer-reason p {{ color: {TEXT} !important; margin: 4px 0; }}
      .hero {{
        background: linear-gradient(115deg, #F96E0B, {SWIGGY_ORANGE}); color: #FFFFFF;
        padding: 18px 24px; border-radius: 15px; margin: 0 0 22px 0;
        box-shadow: 0 5px 16px rgba(252,128,25,0.17);
      }}
      .hero h1 {{ color: #FFFFFF !important; margin: 0; font-size: 1.75rem; }}
      .hero p {{ color: #FFFFFF !important; margin: 4px 0 0 0; font-size: 0.95rem; }}
      .section-title {{
        font-size: 1.2rem; font-weight: 750; color: {TEXT};
        border-bottom: 2px solid {SWIGGY_ORANGE}; padding-bottom: 8px;
        margin: 22px 0 13px 0;
      }}
      .rfm-card {{
        background: #FFFFFF; border: 1px solid #F1D7C3; border-left: 5px solid {SWIGGY_ORANGE};
        border-radius: 12px; padding: 15px 14px; margin-top: 8px;
      }}
      .rfm-card p {{ color: {TEXT} !important; margin: 5px 0 12px 0; font-size: 0.9rem; }}
      .rfm-card strong {{ color: {TEXT} !important; }}
      .insight-card {{
        background: #FFFFFF; border: 1px solid #E5E7EB; border-top: 4px solid {SWIGGY_ORANGE};
        border-radius: 12px; padding: 14px 15px; min-height: 138px;
        box-shadow: 0 3px 12px rgba(20,25,30,0.04);
      }}
      .insight-label {{ color: {SWIGGY_ORANGE} !important; font-size: 0.8rem; font-weight: 750; text-transform: uppercase; }}
      .insight-card h4 {{ margin: 6px 0; font-size: 1rem; color: {TEXT} !important; }}
      .insight-card p {{ color: {MUTED} !important; font-size: 0.88rem; margin: 0; }}
      .small-note {{ color: {MUTED} !important; font-size: 0.82rem; }}
      .offer-card {{ background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 13px; padding: 16px; height: 100%; }}
      .offer-card h3 {{ color: {SWIGGY_ORANGE} !important; margin: 0 0 6px 0; font-size: 1.05rem; }}
      .offer-card p {{ color: {TEXT} !important; margin: 4px 0; }}
      .pill {{ display: inline-block; border-radius: 20px; padding: 4px 10px; background: #FFF0E2; color: #A64B00 !important; font-size: 0.78rem; font-weight: 700; }}
      [data-testid="stDataFrame"] {{ background: #FFFFFF; border-radius: 10px; }}
      [data-testid="stAlert"] p {{ color: inherit !important; }}
      footer {{ visibility: hidden; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# 2. Load and prepare the customer dataset
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "customer_analytics_ready.csv"


@st.cache_data(show_spinner="Loading customer data...")
def load_customer_data(file_path: str) -> pd.DataFrame:
    """Read the processed CSV and standardise key numeric columns."""
    data = pd.read_csv(file_path)

    numeric_columns = [
        "user_id", "total_orders", "total_spend", "total_quantity",
        "average_order_value", "recency", "frequency", "monetary",
        "R_score", "F_score", "M_score", "RFM_score", "RFM_total",
    ]
    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")

    for column in ["rfm_segment", "risk_level", "customer_status"]:
        if column not in data.columns:
            data[column] = "Unknown"
        data[column] = data[column].fillna("Unknown").astype(str)

    if "user_id" not in data.columns:
        raise ValueError("The CSV must contain a 'user_id' column.")

    return data


def money(value: float) -> str:
    """Format rupee values using K, M, and B suffixes."""
    if pd.isna(value):
        return "₹0"
    value = float(value)
    absolute = abs(value)
    if absolute >= 1_000_000_000:
        return f"₹{value / 1_000_000_000:.2f}B"
    if absolute >= 1_000_000:
        return f"₹{value / 1_000_000:.2f}M"
    if absolute >= 1_000:
        return f"₹{value / 1_000:.2f}K"
    return f"₹{value:,.0f}"


def compact_number(value: float) -> str:
    """Format counts using K, M, and B suffixes."""
    if pd.isna(value):
        return "0"
    value = float(value)
    absolute = abs(value)
    if absolute >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if absolute >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if absolute >= 1_000:
        return f"{value / 1_000:.2f}K"
    return f"{value:,.0f}"


def chart_layout(fig, height: int = 340):
    """Apply consistent readable labels and light-theme chart styling."""
    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=TEXT, size=12),
        margin=dict(l=18, r=18, t=45, b=25),
        title_font=dict(color=TEXT, size=15),
        legend=dict(font=dict(color=TEXT)),
        hoverlabel=dict(bgcolor="white", font_color=TEXT),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, tickfont=dict(color=TEXT))
    fig.update_yaxes(gridcolor="#E9EAED", zeroline=False, tickfont=dict(color=TEXT))
    return fig


def add_value_labels(fig, color: str = TEXT):
    """Force chart data labels to use a dark, readable colour."""
    fig.update_traces(textfont_color=color)
    return fig


def section(title: str):
    st.markdown(f'<div class="section-title">{html.escape(title)}</div>', unsafe_allow_html=True)


def insight_card(label: str, heading: str, explanation: str):
    st.markdown(
        f'<div class="insight-card"><div class="insight-label">{html.escape(label)}</div>'
        f'<h4>{html.escape(heading)}</h4><p>{html.escape(explanation)}</p></div>',
        unsafe_allow_html=True,
    )


def calculate_assessment(
    recency: float,
    frequency: float,
    monetary: float,
    total_orders: float,
    segment: str = "Unknown",
):
    """Return transparent sample campaign suggestions, not ML predictions."""
    segment_text = str(segment or "").strip().lower()
    # Use the supplied RFM label when it clearly signals loyalty. For manual
    # entries, use a documented proxy rather than claiming proven loyalty.
    rfm_loyal = any(word in segment_text for word in ("loyal", "champion"))
    loyalty_proxy = total_orders >= 5 and recency <= 30 and monetary >= 5000
    is_loyal = rfm_loyal or loyalty_proxy

    if total_orders <= 0 or frequency <= 0:
        return "New / No Orders", "Insufficient history", {
            "coupon": "FIRSTDELIVERY",
            "discount": "Free delivery",
            "cap": "Delivery fee waived once (sample rule)",
            "minimum": "First order only",
            "eligibility": "For a customer placing their first order",
            "reason": "No previous orders are recorded, so there is not enough history to assess churn. A first-order free-delivery incentive is the suggested test.",
            "action": "Invite the customer to place a first order, then track whether they convert.",
            "offer_type": "First-order free delivery",
        }

    if recency <= 30:
        status, risk = "Active", "Low Risk"
    elif recency <= 60:
        status, risk = "Cooling", "Medium Risk"
    elif recency <= 90:
        status, risk = "At Risk", "High Risk"
    else:
        status, risk = "Inactive", "High Risk"

    if status == "Inactive":
        offer = {
            "coupon": "RETURN20", "discount": "20% off",
            "cap": "Maximum discount ₹100", "minimum": "Minimum order ₹399",
            "eligibility": "Illustrative win-back offer; subject to campaign terms",
            "reason": "The last order was more than 90 days ago. A capped win-back discount is suggested to encourage a return order.",
            "action": "Send a re-engagement message and measure repeat orders and discount cost.",
            "offer_type": "Inactive-customer win-back",
        }
    elif status == "At Risk":
        offer = {
            "coupon": "COMEBACK75", "discount": "₹75 off",
            "cap": "Fixed ₹75 discount", "minimum": "Minimum order ₹499",
            "eligibility": "Illustrative offer; minimum spend must be met",
            "reason": "The last order was 61–90 days ago. A fixed-value comeback incentive is suggested.",
            "action": "Send a win-back message and track redemption and repeat ordering.",
            "offer_type": "At-risk comeback coupon",
        }
    elif status == "Cooling":
        offer = {
            "coupon": "COOLING10", "discount": "10% off",
            "cap": "Maximum discount ₹50", "minimum": "Minimum order ₹299",
            "eligibility": "Illustrative offer; subject to campaign terms",
            "reason": "The last order was 31–60 days ago. A modest discount is suggested before the customer becomes inactive.",
            "action": "Send a reminder and compare repeat-order rate with a suitable control group.",
            "offer_type": "Cooling-customer reminder",
        }
   
    elif is_loyal:
        offer = {
            "coupon": "LOYALCASH",
            "discount": "Up to ₹100 cashback",
            "cap": "Maximum cashback ₹100",
            "minimum": "Minimum order ₹499",
            "eligibility": (
                "Illustrative conditional reward for eligible orders; "
                "cashback is not guaranteed on every order."
            ),
            "reason": (
                "The customer meets the sample loyalty criteria. "
                "A conditional cashback reward is suggested."
            ),
            "action": (
                "Check campaign eligibility and track actual redemption "
                "and repeat orders."
            ),
            "offer_type": "Conditional loyalty cashback",
        }
    else:
        offer = {
            "coupon": "NEXT5",
            "discount": "5% off",
            "cap": "Maximum discount ₹30",
            "minimum": "Minimum order ₹199",
            "eligibility": "Illustrative next-order incentive",
            "reason": (
                "The customer is recently active but does not match "
                "the sample loyalty criteria. A small next-order "
                "incentive is suggested."
            ),
            "action": (
                "Test a modest incentive and monitor whether it "
                "improves repeat ordering."
            ),
            "offer_type": "Active-customer next-order offer",
        }

    return status, risk, offer

@st.cache_data(show_spinner=False)
def create_demo_customer_data(rows: int = 500) -> pd.DataFrame:
    """Create fictional records for public demos when the private CSV is absent."""
    rng = np.random.default_rng(42)
    user_id = np.arange(1, rows + 1)
    total_orders = rng.integers(1, 26, size=rows)
    average_order_value = rng.uniform(180, 950, size=rows).round(2)
    total_spend = (total_orders * average_order_value).round(2)
    recency = rng.integers(0, 151, size=rows)

    customer_status = np.select(
        [recency <= 30, recency <= 60, recency <= 90],
        ["Active", "Cooling", "At Risk"],
        default="Inactive",
    )
    risk_level = np.select(
        [recency <= 30, recency <= 60],
        ["Low Risk", "Medium Risk"],
        default="High Risk",
    )
    rfm_segment = rng.choice(
        ["Champions", "Loyal Customers", "Potential Loyalists", "At Risk/Needs Attention"],
        size=rows,
        p=[0.16, 0.30, 0.30, 0.24],
    )
    r_score = np.select([recency <= 30, recency <= 60], [5, 3], default=1)
    f_score = np.select([total_orders >= 16, total_orders >= 8], [5, 3], default=1)
    m_score = np.select([total_spend >= 10000, total_spend >= 4000], [5, 3], default=1)

    return pd.DataFrame({
        "user_id": user_id,
        "total_orders": total_orders,
        "total_spend": total_spend,
        "total_quantity": total_orders * rng.integers(1, 4, size=rows),
        "average_order_value": average_order_value,
        "recency": recency,
        "frequency": total_orders,
        "monetary": total_spend,
        "R_score": r_score,
        "F_score": f_score,
        "M_score": m_score,
        "RFM_score": r_score * 100 + f_score * 10 + m_score,
        "RFM_total": r_score + f_score + m_score,
        "rfm_segment": rfm_segment,
        "risk_level": risk_level,
        "customer_status": customer_status,
    })


try:
    if DATA_FILE.exists():
        customers = load_customer_data(str(DATA_FILE))
    else:
        customers = create_demo_customer_data()
        st.warning(
            "Demo mode: the private customer CSV is not included in this public deployment. "
            "The dashboard is showing fictional sample customers, not real customer records."
        )
except Exception as error:
    st.error(f"Could not load the customer dataset: {error}")
    st.stop()


# -----------------------------------------------------------------------------
# 3. Sidebar: navigation and a plain-language RFM guide
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        f'<div style="font-size:1.65rem;font-weight:850;color:{SWIGGY_ORANGE};margin-bottom:2px;">'
        f'🍽️ SWIGGY</div><div style="font-size:0.82rem;color:{MUTED};margin-bottom:20px;">Customer Intelligence</div>',
        unsafe_allow_html=True,
    )
    st.markdown("## Navigation")
    page = st.radio(
        "Choose a page",
        ["Customer Dashboard", "Prediction Centre"],
        label_visibility="collapsed",
        key="page_navigation",
    )

    st.markdown("## RFM made simple")
    st.markdown(
        f"""
        <div class="rfm-card">
          <p><strong>R — Recency</strong><br>How many days since the customer's last order? A smaller number usually means a more recent visit.</p>
          <p><strong>F — Frequency</strong><br>How often does the customer order? More orders can indicate a stronger habit.</p>
          <p><strong>M — Monetary</strong><br>How much money has the customer spent? This shows the customer's spending value.</p>
          <p><strong>Easy way to remember</strong><br>Recent visits + ordering habit + spending value.</p>
          <p style="margin-bottom:0"><strong>Stakeholder takeaway</strong><br>Use RFM together to decide whom to retain, reward, or re-engage.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="small-note">Offers in the Prediction Centre are illustrative suggestions, not recorded Swiggy promotions.</p>',
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# 4. Compact title banner
# -----------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="hero">
      <h1>Swiggy Customer Analytics</h1>
      <p>Customer behaviour · Spending patterns · Retention opportunities</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# 5. Customer Dashboard
# -----------------------------------------------------------------------------
if page == "Customer Dashboard":
    filter1, filter2, filter3 = st.columns(3)

    segment_options = sorted(customers["rfm_segment"].dropna().unique().tolist())
    risk_options = sorted(customers["risk_level"].dropna().unique().tolist())
    status_options = sorted(customers["customer_status"].dropna().unique().tolist())

    with filter1:
        selected_segment = st.selectbox("RFM Segment", ["All segments"] + segment_options)
    with filter2:
        selected_risk = st.selectbox("Risk Level", ["All risk levels"] + risk_options)
    with filter3:
        selected_status = st.selectbox("Activity Status", ["All statuses"] + status_options)

    filtered = customers.copy()
    if selected_segment != "All segments":
        filtered = filtered[filtered["rfm_segment"] == selected_segment]
    if selected_risk != "All risk levels":
        filtered = filtered[filtered["risk_level"] == selected_risk]
    if selected_status != "All statuses":
        filtered = filtered[filtered["customer_status"] == selected_status]

    if filtered.empty:
        st.warning("No customers match these filters. Choose different filters to see results.")
        st.stop()

    total_customers = filtered["user_id"].nunique()
    total_orders = filtered["total_orders"].fillna(0).sum() if "total_orders" in filtered else 0
    total_spend = filtered["total_spend"].fillna(0).sum() if "total_spend" in filtered else filtered["monetary"].fillna(0).sum()
    high_risk_count = filtered[filtered["risk_level"].str.lower() == "high risk"]["user_id"].nunique()
    high_risk_share = (high_risk_count / total_customers * 100) if total_customers else 0
    avg_spend_customer = filtered.groupby("user_id")["total_spend"].first().mean() if "total_spend" in filtered else filtered.groupby("user_id")["monetary"].first().mean()
    avg_order_value = filtered["average_order_value"].mean() if "average_order_value" in filtered else 0
    avg_orders_customer = filtered.groupby("user_id")["total_orders"].first().mean() if "total_orders" in filtered else filtered.groupby("user_id")["frequency"].first().mean()

    kpis = st.columns(5)
    kpis[0].metric("Total Customers", compact_number(total_customers))
    kpis[1].metric("Total Orders", compact_number(total_orders))
    kpis[2].metric("Total Spending", money(total_spend))
    kpis[3].metric("High-Risk Customers", compact_number(high_risk_count))
    kpis[4].metric("High-Risk Share", f"{high_risk_share:.1f}%")

    kpis2 = st.columns(3)
    kpis2[0].metric("Average Spend / Customer", money(avg_spend_customer))
    kpis2[1].metric("Average Order Value", money(avg_order_value))
    kpis2[2].metric("Average Orders / Customer", f"{avg_orders_customer:.2f}" if pd.notna(avg_orders_customer) else "0")

    # Prepare category counts for charts.
    left, right = st.columns(2)
    with left:
        risk_counts = filtered.groupby("risk_level")["user_id"].nunique().reindex(["High Risk", "Medium Risk", "Low Risk"]).dropna()
        risk_counts = risk_counts[risk_counts > 0]
        if risk_counts.empty:
            st.info("No risk-level data for this selection.")
        else:
            fig = px.pie(
                names=risk_counts.index,
                values=risk_counts.values,
                hole=0.62,
                color=risk_counts.index,
                color_discrete_map={"High Risk": RED, "Medium Risk": YELLOW, "Low Risk": GREEN},
                title="Risk Level Distribution",
            )
            fig.update_traces(textposition="inside", textinfo="percent+label", textfont_color="#202124")
            chart_layout(fig, 350)
            st.plotly_chart(fig, use_container_width=True)

    with right:
        segment_counts = filtered.groupby("rfm_segment")["user_id"].nunique().sort_values()
        fig = px.bar(
            x=segment_counts.values,
            y=segment_counts.index,
            orientation="h",
            text=[compact_number(v) for v in segment_counts.values],
            title="Customers by RFM Segment",
            labels={"x": "Customers", "y": "RFM Segment"},
            color_discrete_sequence=[SWIGGY_ORANGE],
        )
        fig.update_traces(textposition="outside", textfont_color=TEXT, cliponaxis=False)
        chart_layout(fig, max(340, 35 * len(segment_counts) + 100))
        st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        status_counts = filtered.groupby("customer_status")["user_id"].nunique().sort_values(ascending=False)
        fig = px.bar(
            x=status_counts.index,
            y=status_counts.values,
            text=[compact_number(v) for v in status_counts.values],
            title="Customers by Activity Status",
            labels={"x": "Activity Status", "y": "Customers"},
            color=status_counts.index,
            color_discrete_map={"Active": GREEN, "Cooling": YELLOW, "At Risk": RED, "Inactive": "#8E44AD", "New Customer": "#4E79A7"},
        )
        fig.update_traces(textposition="outside", textfont_color=TEXT, cliponaxis=False)
        chart_layout(fig, 340)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        x_col = "frequency" if "frequency" in filtered else "total_orders"
        y_col = "monetary" if "monetary" in filtered else "total_spend"
        scatter_data = filtered[[x_col, y_col, "risk_level", "rfm_segment"]].dropna().copy()
        if len(scatter_data) > 5000:
            scatter_data = scatter_data.sample(5000, random_state=42)
        fig = px.scatter(
            scatter_data,
            x=x_col,
            y=y_col,
            color="risk_level",
            hover_data=["rfm_segment"],
            title="Order Frequency vs Spending",
            labels={x_col: "Order Frequency", y_col: "Customer Spending"},
            color_discrete_map={"High Risk": RED, "Medium Risk": YELLOW, "Low Risk": GREEN},
            opacity=0.65,
        )
        chart_layout(fig, 340)
        st.plotly_chart(fig, use_container_width=True)

    spending_col = "monetary" if "monetary" in filtered else "total_spend"
    fig = px.histogram(
        filtered,
        x=spending_col,
        nbins=35,
        title="How customer spending is distributed",
        labels={spending_col: "Customer Spending", "count": "Customers"},
        color_discrete_sequence=[SWIGGY_ORANGE],
    )
    fig.update_traces(marker_line_color="white", marker_line_width=0.6)
    chart_layout(fig, 320)
    st.plotly_chart(fig, use_container_width=True)

    # Automatically generated stakeholder-friendly insights.
    high_share = high_risk_share
    inactive_count = filtered[filtered["customer_status"].str.lower() == "inactive"]["user_id"].nunique()
    inactive_share = inactive_count / total_customers * 100 if total_customers else 0
    top_segment = filtered["rfm_segment"].value_counts().index[0] if not filtered["rfm_segment"].empty else "No segment"
    recent_median = filtered["recency"].median() if "recency" in filtered else float("nan")

    insights = st.columns(3)
    with insights[0]:
        if high_share >= 50:
            insight_card("Retention priority", f"{high_share:.1f}% high-risk share", "Prioritise a targeted win-back campaign and track whether customers place another order.")
        else:
            insight_card("Retention health", f"{high_share:.1f}% high-risk share", "Continue monitoring high-risk customers and test focused reminders before broad discounts.")
    with insights[1]:
        insight_card("Activity pattern", f"{inactive_share:.1f}% inactive", "Inactive customers may need a re-engagement message. Compare campaign response before increasing incentives.")
    with insights[2]:
        insight_card("Largest segment", str(top_segment), "This is the most common segment in the current filter. Tailor messaging to this group, while protecting high-value customers.")

    st.markdown(
        f'<p class="small-note">Additional context: median recency is {recent_median:.0f} days. Insights describe the filtered dataset and suggested actions; they do not prove that a campaign will cause a result.</p>',
        unsafe_allow_html=True,
    )

    # Customer details: exact ID search, with a clear button that restores all rows.
    section("Customer Details")
    st.caption("Search matches the complete customer ID, not a partial substring. Clear Search restores every customer in the current dashboard filters.")

    def clear_customer_search():
        st.session_state["customer_id_search"] = ""

    search_col, clear_col = st.columns([5, 1])
    with search_col:
        customer_search = st.text_input(
            "Customer ID",
            placeholder="Enter the exact user_id, for example 1",
            key="customer_id_search",
            label_visibility="collapsed",
        ).strip()
    with clear_col:
        st.button("Clear Search", on_click=clear_customer_search, use_container_width=True)

    table_data = filtered.copy()
    if customer_search:
        # String comparison keeps exact ID matching reliable across CSV numeric formats.
        ids = table_data["user_id"].map(lambda value: str(int(value)) if pd.notna(value) and float(value).is_integer() else str(value))
        table_data = table_data[ids == customer_search]

    st.caption(f"Showing {len(table_data):,} customer record(s)")
    if customer_search and table_data.empty:
        st.warning("No exact customer ID was found in the current filtered selection. Clear the search or adjust the filters.")
    else:
        preferred_columns = [
            "user_id", "rfm_segment", "customer_status", "risk_level", "recency",
            "frequency", "monetary", "total_orders", "total_spend", "average_order_value",
            "R_score", "F_score", "M_score", "RFM_score",
        ]
        display_columns = [column for column in preferred_columns if column in table_data.columns]
        st.dataframe(
            table_data[display_columns],
            use_container_width=True,
            hide_index=True,
            height=360,
        )
        csv_data = table_data.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download displayed customer records (CSV)",
            data=csv_data,
            file_name="swiggy_customer_details.csv",
            mime="text/csv",
        )


# -----------------------------------------------------------------------------
# 6. Prediction Centre: existing customer or hypothetical customer
# -----------------------------------------------------------------------------
else:
    st.markdown("### Assess one customer")
    st.write(
        "Look up a real customer by ID, or enter example values for a hypothetical customer. "
        "The result uses simple project rules—not a trained machine-learning model. "
        "For a new customer with zero orders, the app will show **No order history** and a welcome offer, not falsely label them Active / Low Risk."
    )

    method = st.radio(
        "Assessment method",
        ["Existing Customer ID", "Enter Customer Metrics"],
        horizontal=True,
        key="assessment_method",
    )

    # Do not show a previous customer's results after switching assessment mode.
    if st.session_state.get("previous_assessment_method") != method:
        st.session_state.pop("last_assessment", None)
        st.session_state["previous_assessment_method"] = method

    assessment = None
    if method == "Existing Customer ID":
        id_col, value_col, button_col = st.columns([3, 1.5, 1.2])
        with id_col:
            existing_id = st.text_input("Enter exact Customer ID", placeholder="Enter the complete user_id", key="prediction_customer_id").strip()
        
            
        with button_col:
            st.write("")
            st.write("")
            assess_existing = st.button("Assess Customer", use_container_width=True)

        if assess_existing:
            st.session_state.pop("last_assessment", None)
            if not existing_id:
                st.warning("Enter a customer ID first.")
            else:
                ids = customers["user_id"].map(lambda value: str(int(value)) if pd.notna(value) and float(value).is_integer() else str(value))
                matches = customers[ids == existing_id]
                if matches.empty:
                    st.error("That exact customer ID was not found. Check the ID and try again.")
                else:
                    row = matches.iloc[0]
                    assessment = {
                        "customer_id": existing_id,
                        "recency": float(row.get("recency", 0) or 0),
                        "frequency": float(row.get("frequency", row.get("total_orders", 0)) or 0),
                        "monetary": float(row.get("monetary", row.get("total_spend", 0)) or 0),
                        "total_orders": float(row.get("total_orders", row.get("frequency", 0)) or 0),
                        "segment": str(row.get("rfm_segment", "Unknown")),
                        
                    }
                    st.session_state["last_assessment"] = assessment

    else:
        with st.form("manual_assessment_form"):
            metric1, metric2 = st.columns(2)
            with metric1:
                manual_orders = st.number_input("Total orders so far", min_value=0, value=0, step=1)
                manual_spend = st.number_input("Total spending so far (₹)", min_value=0.0, value=0.0, step=100.0)
            with metric2:
                manual_recency = st.number_input("Days since last order (recency)", min_value=0, value=0, step=1, help="Use 0 only if the last order was today. For a customer with no orders, leave Total orders at 0.")
                
                
            submit_manual = st.form_submit_button("Assess Sample Customer", use_container_width=True)

        if submit_manual:
            st.session_state.pop("last_assessment", None)
            assessment = {
                "customer_id": "Hypothetical customer",
                "recency": float(manual_recency),
                "frequency": float(manual_orders),
                "monetary": float(manual_spend),
                "total_orders": float(manual_orders),
                "segment": "Not assigned (sample inputs)",
               
                
            }
            st.session_state["last_assessment"] = assessment

    # Keep results visible after Streamlit reruns, until a new assessment is submitted.
    if assessment is None:
        assessment = st.session_state.get("last_assessment")

    if assessment is None:
        st.info("Choose an existing customer or enter sample metrics, then select Assess Customer to see the results.")
    else:
        status, risk, offer = calculate_assessment(
    assessment["recency"],
    assessment["frequency"],
    assessment["monetary"],
    assessment["total_orders"],
    assessment.get("segment", "Unknown"),
)
        st.markdown("### Assessment results")
        # Do not show a meaningless Customer ID KPI for manually entered sample metrics.
        if method == "Existing Customer ID":
            result_cols = st.columns([1.0, 1.0, 1.0, 1.35])
            result_cols[0].metric("Customer ID", str(assessment["customer_id"]))
            result_cols[1].metric("Days Since Last Order", f"{assessment['recency']:.0f} days")
            result_cols[2].metric("Activity Status", status)
            result_cols[3].metric("Rule-Based Risk Indicator", risk)
        else:
            result_cols = st.columns([1.0, 1.0, 1.4])
            result_cols[0].metric("Days Since Last Order", f"{assessment['recency']:.0f} days")
            result_cols[1].metric("Activity Status", status)
            result_cols[2].metric("Rule-Based Risk Indicator", risk)
        st.markdown(
            "<p class='risk-note'>Risk labels follow this project's recency cut-offs; they are not a trained model or a probability of churn.</p>",
            unsafe_allow_html=True,
        )

        st.markdown("### Customer snapshot")
        details_left, details_right = st.columns(2)
        with details_left:
            st.write(f"**RFM segment:** {assessment.get('segment', 'Unknown')}")
            st.write(f"**Order frequency:** {assessment['frequency']:.0f} orders")
        with details_right:
            st.write(f"**Total spending:** {money(assessment['monetary'])}")
           
        st.markdown("### Your suggested offer")
        st.markdown(
            f'<div class="featured-offer">'
            f'<div class="offer-topline">🍊 Personalised campaign idea · Suggested for this customer</div>'
            f'<div class="offer-discount">{html.escape(offer["discount"])}</div>'
            f'<div>Use this sample coupon code at checkout:</div>'
            f'<div class="offer-code">{html.escape(offer["coupon"])}</div>'
            f'<div class="offer-details">'
            f'<span class="offer-chip">{html.escape(offer["cap"])}</span>'
            f'<span class="offer-chip">{html.escape(offer["minimum"])}</span>'
            f'<span class="offer-chip">{html.escape(offer.get("offer_type", "Suggested offer"))}</span>'
            f'</div>'
            f'<div class="offer-reason"><strong>Eligibility</strong><p>{html.escape(offer.get("eligibility", "Illustrative sample rule"))}</p></div>'
            f'<div class="offer-reason"><strong>Why this offer?</strong><p>{html.escape(offer["reason"])}</p></div>'
            f'<div class="offer-reason"><strong>Recommended next action</strong><p>{html.escape(offer["action"])}</p></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.caption("This is a project demonstration. The coupon is not a live Swiggy code and has not been applied to a real account.")

        st.markdown("### Sample campaign rules")
        st.caption("These are illustrative project rules only—not live Swiggy promotions or recorded coupon outcomes.")
        coupon_options = [
            ("FIRSTDELIVERY", "Free delivery", "First order only", "New customers with no recorded orders"),
            (
    "LOYALCASH",
    "Up to ₹100 cashback",
    "Minimum order ₹499",
    "Conditional reward; eligible orders only, not guaranteed every time",
),
            ("COOLING10", "10% off · max ₹50", "Minimum order ₹299", "Customers whose last order was 31–60 days ago"),
            ("COMEBACK75", "₹75 off", "Minimum order ₹499", "Customers whose last order was 61–90 days ago"),
            ("RETURN20", "20% off · max ₹100", "Minimum order ₹399", "Customers whose last order was over 90 days ago"),
        ]
        for start_idx in range(0, len(coupon_options), 3):
            coupon_cols = st.columns(3)
            for column, (code, discount, minimum, purpose) in zip(coupon_cols, coupon_options[start_idx:start_idx + 3]):
                with column:
                    st.markdown(
                        f'<div class="offer-card"><h3>{html.escape(code)}</h3>'
                        f'<p><strong>{html.escape(discount)}</strong></p><p>{html.escape(minimum)}</p>'
                        f'<p class="small-note">{html.escape(purpose)}</p></div>',
                        unsafe_allow_html=True,
                    )

        st.markdown(
            '<p class="small-note">Important: the current app applies recency cut-offs to produce a risk indicator. A real churn model would need a defined churn label, a time-based validation split, model evaluation, and calibrated probabilities before presenting a numeric churn likelihood.</p>',
            unsafe_allow_html=True,
        )
