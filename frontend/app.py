import streamlit as st
import pandas as pd
import requests
from pathlib import Path


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="GreenOps",
    page_icon="🌱",
    layout="wide"
)


# -----------------------------
# Project Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ACTUAL_PREDICTED_IMAGE = (
    BASE_DIR
    / "ml"
    / "actual_vs_predicted.png"
)

FEATURE_IMPORTANCE_IMAGE = (
    BASE_DIR
    / "ml"
    / "feature_importance.png"
)


# -----------------------------
# Custom Styling
# -----------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f8f5;
}

[data-testid="stSidebar"] {
    background-color: #173d28;
}

[data-testid="stSidebar"] * {
    color: white;
}

h1, h2, h3 {
    color: #24352a;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e2e9e3;
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
}

.metric-title {
    color: #6d786f;
    font-size: 14px;
}

.metric-value {
    color: #24352a;
    font-size: 28px;
    font-weight: bold;
}

.metric-description {
    color: #87918a;
    font-size: 12px;
}

.analyzer {
    background-color: white;
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #e2e9e3;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Backend Connection
# -----------------------------

BACKEND_URL = "http://127.0.0.1:8000"


@st.cache_data(ttl=30)
def get_dashboard():

    response = requests.get(
        f"{BACKEND_URL}/dashboard",
        timeout=5
    )

    response.raise_for_status()

    return response.json()


# -----------------------------
# Get Dashboard Data
# -----------------------------

try:

    dashboard = get_dashboard()

except Exception as e:

    st.error("Could not connect to GreenOps backend.")

    st.code(
        str(e),
        language="text"
    )

    st.write(
        "Backend URL:",
        BACKEND_URL
    )

    st.stop()


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.markdown(
        "# 🌱 GreenOps"
    )

    st.markdown(
        "### Cloud Efficiency Platform"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Workloads",
            "Optimization",
            "Analytics"
        ]
    )

    st.divider()

    st.caption(
        "AI-powered cloud cost and carbon optimization"
    )


# -----------------------------
# Header
# -----------------------------

st.markdown(
    "<p style='color:#4c7a5c; font-weight:600;'>"
    "CLOUD EFFICIENCY"
    "</p>",
    unsafe_allow_html=True
)

st.title("GreenOps Dashboard")

st.write(
    "Monitor cloud cost, carbon emissions "
    "and optimization opportunities."
)

st.success("● System Online")


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown("## Overview")

    st.markdown("---")

    st.markdown("## 🤖 AI Workload Analyzer")

    st.write(
        "Enter workload details to get an ML-based "
        "resource optimization recommendation."
    )

    with st.container(border=True):

        col1, col2, col3 = st.columns(3)

        with col1:

            cpu_usage = st.number_input(
                "CPU Usage (%)",
                min_value=0.0,
                max_value=100.0,
                value=18.0,
                step=1.0
            )

        with col2:

            ram_usage = st.number_input(
                "RAM Usage (%)",
                min_value=0.0,
                max_value=100.0,
                value=25.0,
                step=1.0
            )

        with col3:

            runtime_hours = st.number_input(
                "Runtime (hours)",
                min_value=0.1,
                value=24.0,
                step=1.0
            )

        col1, col2 = st.columns(2)

        with col1:

            workload_type = st.selectbox(
                "Workload Type",
                [
                    "database",
                    "machine_learning",
                    "batch",
                    "web",
                    "analytics"
                ]
            )

        with col2:

            current_instance = st.selectbox(
                "Current Instance",
                [
                    "m5.large",
                    "m5.xlarge",
                    "m5.2xlarge"
                ],
                index=2
            )

        analyze_button = st.button(
            "🔍 Analyze Workload",
            type="primary",
            use_container_width=True
        )

        if analyze_button:

            try:

                response = requests.post(
                    f"{BACKEND_URL}/analyze",
                    json={
                        "cpu_usage": cpu_usage,
                        "ram_usage": ram_usage,
                        "runtime_hours": runtime_hours,
                        "hour": 14,
                        "day_of_week": 2,
                        "workload_type": workload_type,
                        "current_instance": current_instance
                    },
                    timeout=10
                )

                response.raise_for_status()

                result = response.json()

                st.success(
                    "Analysis completed successfully."
                )

                st.markdown("### 📊 Recommendation")

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Predicted CPU",
                        f"{result['predicted_cpu']:.1f}%"
                    )

                with col2:

                    st.metric(
                        "Recommended Instance",
                        result["recommended_instance"]
                    )

                with col3:

                    # -----------------------------------------
                    # Calculate Analyzer Green Score
                    # -----------------------------------------

                    analyzer_utilization = (
                        float(cpu_usage) +
                        float(ram_usage)
                    ) / 2

                    if analyzer_utilization <= 25:
                        analyzer_score = 90
                    elif analyzer_utilization <= 40:
                        analyzer_score = 80
                    elif analyzer_utilization <= 60:
                        analyzer_score = 65
                    elif analyzer_utilization <= 80:
                        analyzer_score = 50
                    else:
                        analyzer_score = 35

                    if result["cost_saving"] > 0:
                        analyzer_score += 5

                    if result["carbon_saving"] > 0:
                        analyzer_score += 5

                    analyzer_score = min(
                        analyzer_score,
                        100
                    )

                    if analyzer_score >= 80:
                        analyzer_label = "Excellent"
                    elif analyzer_score >= 60:
                        analyzer_label = "Good"
                    elif analyzer_score >= 40:
                        analyzer_label = "Needs Improvement"
                    else:
                        analyzer_label = "Poor"

                    st.metric(
                        "Green Score",
                        f"{analyzer_score}/100",
                        analyzer_label
                    )

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.metric(
                        "Current Cost",
                        f"₹{result['current_cost']:.2f}"
                    )

                with col2:

                    st.metric(
                        "Optimized Cost",
                        f"₹{result['optimized_cost']:.2f}"
                    )

                with col3:

                    st.metric(
                        "Cost Saving",
                        f"₹{result['cost_saving']:.2f}"
                    )

                with col4:

                    st.metric(
                        "Carbon Saving",
                        f"{result['carbon_saving']:.2f} kg"
                    )

                st.info(
                    f"💡 {result['reason']}"
                )

                # -----------------------------------------
                # Carbon Impact
                # -----------------------------------------

                st.markdown("### 🌱 Carbon Impact")

                current_details = result.get(
                    "current_carbon_details",
                    {}
                )

                optimized_details = result.get(
                    "optimized_carbon_details",
                    {}
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.markdown("#### Current Instance")

                    st.metric(
                        "Power",
                        f"{current_details.get('power_watts', 0)} W"
                    )

                    st.metric(
                        "Estimated Energy",
                        f"{current_details.get('energy_kwh', 0):.4f} kWh"
                    )

                    st.metric(
                        "Estimated Carbon",
                        f"{current_details.get('carbon_kg', 0):.2f} kg CO₂"
                    )

                with col2:

                    st.markdown("#### Recommended Instance")

                    st.metric(
                        "Power",
                        f"{optimized_details.get('power_watts', 0)} W"
                    )

                    st.metric(
                        "Estimated Energy",
                        f"{optimized_details.get('energy_kwh', 0):.4f} kWh"
                    )

                    st.metric(
                        "Estimated Carbon",
                        f"{optimized_details.get('carbon_kg', 0):.2f} kg CO₂"
                    )

                st.success(
                    f"🌱 Estimated carbon reduction: "
                    f"{result['carbon_saving']:.2f} kg CO₂"
                )

                with st.expander("How is this calculated?"):

                    st.write(
                        "GreenOps first estimates energy consumption "
                        "from power, CPU utilization and runtime."
                    )

                    st.latex(
                        r"E = \frac{P \times U \times T}{1000}"
                    )

                    st.write(
                        "It then estimates carbon emissions by "
                        "multiplying energy by the selected carbon "
                        "intensity factor."
                    )

                    st.latex(
                        r"C = E \times CI"
                    )

                    st.write(
                        f"Carbon intensity used: "
                        f"{result.get('carbon_intensity', 0.7):.2f} "
                        f"kg CO₂/kWh"
                    )

            except Exception as e:

                st.error(
                    "Could not analyze workload."
                )

                st.code(
                    str(e)
                )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Workloads</div>
                <div class="metric-value">
                    {dashboard["total_workloads"]}
                </div>
                <div class="metric-description">
                    Active workloads
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Current Cost</div>
                <div class="metric-value">
                    ₹{dashboard["total_cost"]}
                </div>
                <div class="metric-description">
                    Estimated cloud cost
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Carbon Emissions
                </div>
                <div class="metric-value">
                    {dashboard["total_carbon"]}
                </div>
                <div class="metric-description">
                    kg CO₂ estimated
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Potential Savings
                </div>
                <div class="metric-value">
                    ₹{dashboard["potential_cost_saving"]}
                </div>
                <div class="metric-description">
                    Through optimization
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"🌱 Potential Carbon Reduction: "
            f"{dashboard['potential_carbon_reduction']} kg CO₂"
        )

    with col2:

        st.info(
            f"⚡ Optimization Opportunities: "
            f"{dashboard['optimization_opportunities']}"
        )

    st.markdown("---")

    st.markdown("## Workload Overview")

    workloads_df = pd.DataFrame(
        dashboard["workloads"]
    )

    st.dataframe(
        workloads_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# WORKLOADS
# =========================================================

elif page == "Workloads":

    st.markdown("## All Workloads")

    st.write(
        "A simple view of the workloads currently being "
        "tracked by GreenOps."
    )

    workloads_df = pd.DataFrame(
        dashboard["workloads"]
    )

    st.dataframe(
        workloads_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# OPTIMIZATION
# =========================================================

elif page == "Optimization":

    st.markdown("## Optimization Opportunities")

    st.write(
        "GreenOps compares workload utilization with the "
        "current instance and highlights possible savings."
    )

    for workload in dashboard["workloads"]:

        cpu = float(workload["cpu_usage"])
        ram = float(workload["ram_usage"])

        # -----------------------------------------
        # Calculate Green Score
        # -----------------------------------------

        utilization = (cpu + ram) / 2

        cost_saving = float(
            workload.get("cost_saving", 0)
        )

        carbon_saving = float(
            workload.get("carbon_saving", 0)
        )

        if utilization <= 25:
            utilization_score = 90
        elif utilization <= 40:
            utilization_score = 80
        elif utilization <= 60:
            utilization_score = 65
        elif utilization <= 80:
            utilization_score = 50
        else:
            utilization_score = 35

        optimization_bonus = 0

        if cost_saving > 0:
            optimization_bonus += 5

        if carbon_saving > 0:
            optimization_bonus += 5

        green_score = min(
            utilization_score + optimization_bonus,
            100
        )

        if green_score >= 80:
            score_label = "Excellent"
        elif green_score >= 60:
            score_label = "Good"
        elif green_score >= 40:
            score_label = "Needs Improvement"
        else:
            score_label = "Poor"

        # -----------------------------------------
        # Optimization Card
        # -----------------------------------------

        with st.container(border=True):

            st.subheader(
                f"🌱 {workload['workload']}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Current Instance",
                    workload["instance"]
                )

            with col2:

                st.metric(
                    "Recommended",
                    workload["recommended_instance"]
                )

            with col3:

                st.metric(
                    "Green Score",
                    f"{green_score}/100",
                    score_label
                )

            st.divider()

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Current Cost",
                    f"₹{workload['current_cost']}"
                )

            with col2:

                st.metric(
                    "Optimized Cost",
                    f"₹{workload['current_cost'] - workload['cost_saving']:.2f}"
                )

            with col3:

                st.metric(
                    "Cost Saving",
                    f"₹{workload['cost_saving']}"
                )

            with col4:

                st.metric(
                    "Carbon Saving",
                    f"{workload.get('carbon_saving', 0):.2f} kg"
                )

            st.markdown("### Resource Utilization")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.write(
                    f"**CPU Usage:** {cpu:.1f}%"
                )

            with col2:

                st.write(
                    f"**RAM Usage:** {ram:.1f}%"
                )

            with col3:

                st.write(
                    f"**Runtime:** {workload['runtime_hours']} hours"
                )

            st.progress(
                min(int(utilization), 100),
                text=f"Average Resource Utilization: {utilization:.1f}%"
            )

            if workload["recommended_instance"] != workload["instance"]:

                st.success(
                    "🌱 Optimization recommended"
                )

                st.info(
                    f"💡 This workload is using relatively low "
                    f"CPU and RAM compared with its current "
                    f"instance. Moving from "
                    f"**{workload['instance']}** to "
                    f"**{workload['recommended_instance']}** "
                    f"could reduce cloud cost and resource "
                    f"consumption."
                )

            else:

                st.success(
                    "✓ Current instance is appropriate"
                )

            st.divider()


# =========================================================
# ANALYTICS
# =========================================================

elif page == "Analytics":

    st.markdown("## Analytics")

    st.write(
        "This page combines workload data with the performance "
        "of the ML model used by GreenOps."
    )

    # -----------------------------------------
    # ML Model Performance
    # -----------------------------------------

    st.markdown("### 🤖 ML Model Performance")

    st.caption(
        "Results from the latest evaluation on the 20% test split."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "MAE",
            "6.37",
            help="Average absolute prediction error in CPU percentage points."
        )

    with col2:

        st.metric(
            "RMSE",
            "7.91",
            help="Root Mean Squared Error. Larger errors have more influence."
        )

    with col3:

        st.metric(
            "R² Score",
            "0.90",
            help="Shows how well the model explains variation in future CPU usage."
        )

    st.info(
        "In simple terms, the model's average prediction error "
        "is about 6.37 CPU percentage points on the test data. "
        "The R² score of 0.90 indicates a strong fit on this "
        "prototype dataset."
    )

    st.warning(
        "These results are based on synthetic workload data "
        "created for the GreenOps prototype. They should not "
        "be treated as production accuracy."
    )

    # -----------------------------------------
    # Actual vs Predicted
    # -----------------------------------------

    st.markdown("### 📈 Actual vs Predicted CPU")

    if ACTUAL_PREDICTED_IMAGE.exists():

        st.image(
            str(ACTUAL_PREDICTED_IMAGE),
            use_container_width=True
        )

        st.caption(
            "Points closer to the diagonal reference line "
            "represent predictions closer to the actual future CPU."
        )

    else:

        st.warning(
            "Actual-vs-predicted graph was not found. "
            "Run: python ml\\evaluate_model.py"
        )

    # -----------------------------------------
    # Feature Importance
    # -----------------------------------------

    st.markdown("### 🔎 Feature Importance")

    if FEATURE_IMPORTANCE_IMAGE.exists():

        st.image(
            str(FEATURE_IMPORTANCE_IMAGE),
            use_container_width=True
        )

        st.caption(
            "Feature importance shows how much each input feature "
            "contributes to the Random Forest's predictions."
        )

    else:

        st.warning(
            "Feature importance graph was not found. "
            "Run: python ml\\evaluate_model.py"
        )

    st.markdown("---")

    # -----------------------------------------
    # Cost Analysis
    # -----------------------------------------

    workloads_df = pd.DataFrame(
        dashboard["workloads"]
    )

    st.markdown("### 💰 Cost Comparison")

    if "current_cost" in workloads_df.columns:

        cost_data = workloads_df[
            ["workload", "current_cost", "cost_saving"]
        ].copy()

        # Convert the saving into the actual optimized cost.
        cost_data["optimized_cost"] = (
            cost_data["current_cost"]
            - cost_data["cost_saving"]
        )

        cost_chart = cost_data[
            ["workload", "current_cost", "optimized_cost"]
        ].set_index("workload")

        st.bar_chart(
            cost_chart
        )

        total_current_cost = float(
            cost_data["current_cost"].sum()
        )

        total_optimized_cost = float(
            cost_data["optimized_cost"].sum()
        )

        total_cost_saving = max(
            total_current_cost - total_optimized_cost,
            0
        )

        if total_current_cost > 0:

            cost_reduction_percent = (
                total_cost_saving
                / total_current_cost
                * 100
            )

        else:

            cost_reduction_percent = 0

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Current Cost",
                f"₹{total_current_cost:.2f}"
            )

        with col2:

            st.metric(
                "Optimized Cost",
                f"₹{total_optimized_cost:.2f}"
            )

        with col3:

            st.metric(
                "Potential Saving",
                f"₹{total_cost_saving:.2f}",
                f"{cost_reduction_percent:.1f}%"
            )

        st.caption(
            "The optimized cost is calculated after applying "
            "the savings identified by the GreenOps optimizer."
        )

    # -----------------------------------------
    # Carbon Analysis
    # -----------------------------------------

    st.markdown("### 🌱 Carbon Comparison")

    carbon_columns = [
        "workload",
        "current_carbon",
        "carbon_saving"
    ]

    if all(
        column in workloads_df.columns
        for column in carbon_columns
    ):

        carbon_data = workloads_df[
            carbon_columns
        ].copy()

        # Convert carbon saving into the remaining
        # estimated optimized carbon.
        carbon_data["optimized_carbon"] = (
            carbon_data["current_carbon"]
            - carbon_data["carbon_saving"]
        )

        carbon_chart = carbon_data[
            ["workload", "current_carbon", "optimized_carbon"]
        ].set_index("workload")

        st.bar_chart(
            carbon_chart
        )

        total_current_carbon = float(
            carbon_data["current_carbon"].sum()
        )

        total_optimized_carbon = float(
            carbon_data["optimized_carbon"].sum()
        )

        total_carbon_saving = max(
            total_current_carbon
            - total_optimized_carbon,
            0
        )

        if total_current_carbon > 0:

            carbon_reduction_percent = (
                total_carbon_saving
                / total_current_carbon
                * 100
            )

        else:

            carbon_reduction_percent = 0

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Current Carbon",
                f"{total_current_carbon:.2f} kg"
            )

        with col2:

            st.metric(
                "Optimized Carbon",
                f"{total_optimized_carbon:.2f} kg"
            )

        with col3:

            st.metric(
                "Carbon Reduction",
                f"{total_carbon_saving:.2f} kg",
                f"{carbon_reduction_percent:.1f}%"
            )

        st.caption(
            "Carbon values are estimates based on the prototype's "
            "power-consumption and carbon-intensity assumptions."
        )

    else:

        st.info(
            "Carbon analysis data is not available for all workloads yet."
        )

    # -----------------------------------------
    # Resource Utilization
    # -----------------------------------------

    st.markdown("### ⚡ Resource Utilization")

    utilization_data = workloads_df[
        ["workload", "cpu_usage", "ram_usage"]
    ].set_index("workload")

    st.bar_chart(
        utilization_data
    )

    # -----------------------------------------
    # Workload Data
    # -----------------------------------------

    st.markdown("### 📋 Workload Data")

    st.dataframe(
        workloads_df,
        use_container_width=True,
        hide_index=True
    )
