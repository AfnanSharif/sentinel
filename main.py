"""
Sentinel — Main Streamlit Application
Enterprise AI Customer Support Platform powered by OpenAI + FAISS + Azure ML
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.openai_config import openai_settings
from pipeline.data_loader import TicketDataLoader
from rag.rag_engine import RAGEngine
from nlp.sentiment_analyzer import SentimentAnalyzer
from nlp.ticket_classifier import TicketClassifier
from ui.dashboard import render_analytics_dashboard
from ui.ticket_view import render_ticket_interface
from ui.styles import inject_custom_css
from utils.logger import setup_logger

logger = setup_logger(__name__)


def initialize_session_state() -> None:
    """Initialize Streamlit session state."""
    defaults = {
        "rag_engine": None,
        "classifier": None,
        "analyzer": None,
        "tickets_loaded": False,
        "query_history": [],
        "selected_response": None,
        "metrics": {
            "total_queries": 0,
            "avg_response_time": 0,
            "satisfaction_score": 0,
        },
        "active_tab": "support",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


@st.cache_resource(show_spinner=False)
def initialize_rag_engine() -> RAGEngine:
    """Initialize and cache the RAG engine."""
    return RAGEngine()


@st.cache_resource(show_spinner=False)
def initialize_classifier() -> TicketClassifier:
    """Initialize and cache the ticket classifier."""
    return TicketClassifier()


@st.cache_resource(show_spinner=False)
def initialize_analyzer() -> SentimentAnalyzer:
    """Initialize and cache the sentiment analyzer."""
    return SentimentAnalyzer()


def main() -> None:
    """Main Sentinel application."""
    st.set_page_config(
        page_title="Sentinel | Enterprise Support",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_custom_css()
    initialize_session_state()

    # Initialize components
    if st.session_state.rag_engine is None:
        with st.spinner("🛡️ Initializing Sentinel AI..."):
            st.session_state.rag_engine = initialize_rag_engine()
            st.session_state.classifier = initialize_classifier()
            st.session_state.analyzer = initialize_analyzer()

    # Header
    st.markdown("""
        <div class="sentinel-header">
            <div class="shield-icon">🛡️</div>
            <h1 class="sentinel-title">SENTINEL</h1>
            <p class="sentinel-subtitle">Enterprise AI Customer Support Platform</p>
            <div class="sentinel-badges">
                <span class="badge">OpenAI GPT-4</span>
                <span class="badge">FAISS Vector DB</span>
                <span class="badge">Azure ML</span>
                <span class="badge">RAG Pipeline</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["🎫 Support Agent", "📊 Analytics", "⚙️ Configuration"])

    with tab1:
        render_ticket_interface(
            rag_engine=st.session_state.rag_engine,
            classifier=st.session_state.classifier,
            analyzer=st.session_state.analyzer,
            query_history=st.session_state.query_history,
        )

    with tab2:
        render_analytics_dashboard(metrics=st.session_state.metrics)

    with tab3:
        _render_config_tab()


def _render_config_tab() -> None:
    """Render the configuration tab."""
    st.subheader("⚙️ System Configuration")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🤖 AI Model Settings**")
        st.code(f"""
Model: {openai_settings.OPENAI_CHAT_MODEL}
Embedding: {openai_settings.OPENAI_EMBEDDING_MODEL}
Temperature: {openai_settings.OPENAI_TEMPERATURE}
Max Tokens: {openai_settings.OPENAI_MAX_TOKENS}
        """)
    with col2:
        st.markdown("**📦 Vector Database**")
        st.code(f"""
Index Path: {openai_settings.FAISS_INDEX_PATH}
Top-K Results: {openai_settings.FAISS_TOP_K}
Embedding Dim: {openai_settings.EMBEDDING_DIMENSION}
        """)


if __name__ == "__main__":
    main()
