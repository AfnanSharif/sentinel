"""
Sentinel — Analytics Dashboard Component
Enterprise analytics widgets tracking customer support SLAs.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Any, Dict


def render_analytics_dashboard(metrics: Dict[str, Any]) -> None:
    """Render historical support statistics and metrics dashboards."""
    st.subheader("📊 Operational Analytics")

    # High level KPI columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tickets Processed", "1,248", "+12%")
    with col2:
        st.metric("Average Handling Time", "1.8s", "-15%")
    with col3:
        st.metric("SLA Compliance Rate", "98.7%", "+0.5%")
    with col4:
        st.metric("Customer Satisfaction (CSAT)", "4.82 / 5.0", "+2%")

    # Create dummy ticket category data for visualization
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.markdown("<p class='dashboard-card-title'>📦 Ticket Distribution by Category</p>", unsafe_allow_html=True)

    data = {
        "Category": ["Billing & Payments", "Shipping & Logistics", "Technical Support", "Product Inquiry"],
        "Tickets": [412, 385, 298, 153],
    }
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="Category",
        y="Tickets",
        color="Category",
        color_discrete_sequence=["#c5a880", "#3A506B", "#1C2541", "#5C6B73"],
        template="plotly_dark",
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Sentiment history card
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.markdown("<p class='dashboard-card-title'>🎭 Real-time Sentiment Trend</p>", unsafe_allow_html=True)

    sentiment_data = {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Negative %": [15, 12, 18, 10, 8, 14, 11],
        "Neutral %": [35, 38, 32, 40, 42, 36, 39],
        "Positive %": [50, 50, 50, 50, 50, 50, 50],
    }
    df_sent = pd.DataFrame(sentiment_data)
    fig_sent = px.line(
        df_sent,
        x="Day",
        y=["Negative %", "Neutral %", "Positive %"],
        color_discrete_sequence=["#ef4444", "#94a3b8", "#10b981"],
        template="plotly_dark",
    )
    fig_sent.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_sent, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
