"""
Sentinel — Custom CSS
Enterprise blueprint, navy blue & gold premium styling for Sentinel support agent.
"""
import streamlit as st

SENTINEL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Montserrat:wght@300;400;500;600;700&family=Source+Code+Pro:wght@400;600&display=swap');

:root {
    --sentinel-navy: #0B132B;
    --sentinel-gold: #c5a880;
    --sentinel-gold-light: #e5cfa8;
    --sentinel-card: #1C2541;
    --sentinel-border: #3A506B;
    --text-primary: #F4F5F6;
    --text-secondary: #A9B2C3;
}

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif !important;
}

.stApp {
    background-color: var(--sentinel-navy) !important;
    color: var(--text-primary) !important;
}

.sentinel-header {
    text-align: center;
    padding: 3rem 0;
    margin-bottom: 2.5rem;
    background: linear-gradient(180deg, #1C2541 0%, #0B132B 100%);
    border: 1px solid var(--sentinel-border);
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    position: relative;
}

.sentinel-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--sentinel-gold), #fff, var(--sentinel-gold));
}

.shield-icon {
    font-size: 3.5rem;
    color: var(--sentinel-gold);
    filter: drop-shadow(0 0 10px rgba(197,168,128,0.5));
}

.sentinel-title {
    font-family: 'Cinzel', serif !important;
    font-size: 3.2rem;
    font-weight: 700;
    letter-spacing: 4px;
    color: var(--sentinel-gold) !important;
    margin: 0.5rem 0 0;
}

.sentinel-subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 1.5rem;
}

.sentinel-badges {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
    flex-wrap: wrap;
}

.sentinel-badges .badge {
    background: rgba(197, 168, 128, 0.1);
    color: var(--sentinel-gold-light);
    border: 1px solid rgba(197, 168, 128, 0.3);
    padding: 0.3rem 0.8rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.5px;
}

/* Card layout components */
.dashboard-card {
    background: var(--sentinel-card);
    border: 1px solid var(--sentinel-border);
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.dashboard-card-title {
    font-family: 'Cinzel', serif;
    font-size: 1.1rem;
    color: var(--sentinel-gold);
    border-bottom: 1px solid rgba(197, 168, 128, 0.2);
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}
</style>
"""


def inject_custom_css() -> None:
    """Inject custom CSS for Sentinel project."""
    st.markdown(SENTINEL_CSS, unsafe_allow_html=True)
