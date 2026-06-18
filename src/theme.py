"""
RetentionAI — Y2K Retro Windows Theme
"""

import streamlit as st

# ─── Colour Palette ───────────────────────────────────────────────────────────
BG       = "#f0eaff"
CARD     = "#ffffff"
TITLEBAR = "#c8b8f0"
BORDER   = "#2d2040"
PINK     = "#f0b8d4"
LIME     = "#c8e88a"
PURPLE   = "#9b72d4"
TEXT     = "#2d2040"
MUTED    = "#7a6a9a"
GREEN    = "#5ab85a"
AMBER    = "#e8a020"
RED      = "#d43050"
ACCENT   = PURPLE


def apply_retro_theme():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&family=Press+Start+2P&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    background-color: #f0eaff !important;
    color: #2d2040 !important;
}
.stApp {
    background-color: #f0eaff !important;
    background-image: radial-gradient(circle, #c8b8f022 1px, transparent 1px);
    background-size: 22px 22px;
}

[data-testid="stSidebar"] {
    background-color: #e8d8ff !important;
    border-right: 3px solid #2d2040 !important;
    box-shadow: 4px 0 0 0 #2d2040;

    min-width: 280px !important;
    max-width: 280px !important;
}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span { color: #2d2040 !important; }
/* ───────── Professional Sidebar Navigation ───────── */

[data-testid="stSidebar"] .stRadio > div {
    gap: 12px !important;
}

[data-testid="stSidebar"] .stRadio label {
    width: 100% !important;
    min-height: 58px !important;

    display: flex !important;
    align-items: center !important;

    background: #ffffff !important;

    border: 2px solid #2d2040 !important;
    border-radius: 8px !important;

    padding: 14px 18px !important;

    font-size: 0.92rem !important;
    font-weight: 600 !important;

    box-shadow: 3px 3px 0 #2d2040 !important;

    transition: all 0.15s ease !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: #f7f3ff !important;
    transform: translateY(-2px);
    box-shadow: 5px 5px 0 #2d2040 !important;
}

[data-testid="stSidebar"] .stRadio label[data-selected="true"] {
    background: linear-gradient(
        90deg,
        #c8b8f0,
        #f0b8d4
    ) !important;

    border-left: 8px solid #9b72d4 !important;

    color: #2d2040 !important;

    box-shadow: 5px 5px 0 #2d2040 !important;
}

/* radio dot */
[data-testid="stSidebar"] .stRadio input {
    transform: scale(0.85);
}

.retro-window {
    background: #ffffff;
    border: 2.5px solid #2d2040;
    box-shadow: 5px 5px 0 #2d2040;
    margin-bottom: 18px;
    overflow: hidden;
}
.retro-titlebar {
    background: linear-gradient(90deg, #c8b8f0, #f0b8d4);
    border-bottom: 2.5px solid #2d2040;
    padding: 6px 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-weight: 700;
    font-size: 0.82rem;
    color: #2d2040;
}
.retro-titlebar-buttons { display: flex; gap: 4px; }
.retro-btn-dot {
    width: 14px; height: 14px;
    border: 2px solid #2d2040;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: 900;
    background: #f0eaff;
    cursor: pointer;
    line-height: 1;
}
.retro-window-body { padding: 16px 18px; }

.metric-card {
    background: #ffffff;
    border: 2.5px solid #2d2040;
    box-shadow: 4px 4px 0 #2d2040;
    padding: 18px 16px;
    text-align: center;
    position: relative;
}
.metric-card::before {
    content: '';
    display: block;
    height: 8px;
    background: linear-gradient(90deg, #c8b8f0, #f0b8d4, #c8e88a);
    margin: -18px -16px 12px -16px;
    border-bottom: 2px solid #2d2040;
}
.metric-value {
    font-family: 'VT323', monospace;
    font-size: 2.6rem;
    color: #9b72d4;
    line-height: 1.1;
}
.metric-label {
    font-size: 0.72rem;
    color: #7a6a9a;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
    margin-top: 4px;
}

.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #2d2040;
    background: linear-gradient(90deg, #c8b8f0 0%, #f0b8d4 60%, transparent 100%);
    border: 2px solid #2d2040;
    border-left: 6px solid #9b72d4;
    padding: 7px 14px;
    margin: 1.4rem 0 0.8rem 0;
    box-shadow: 3px 3px 0 #2d2040;
    letter-spacing: 0.02em;
}

.stButton > button {
    background: #c8b8f0 !important;
    color: #2d2040 !important;
    border: 2.5px solid #2d2040 !important;
    border-radius: 0 !important;
    padding: 10px 22px !important;
    font-weight: 700 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.88rem !important;
    box-shadow: 4px 4px 0 #2d2040 !important;
    transition: all 0.1s !important;
}
.stButton > button:hover {
    background: #9b72d4 !important;
    color: #ffffff !important;
    transform: translate(-2px, -2px) !important;
    box-shadow: 6px 6px 0 #2d2040 !important;
}
.stButton > button:active {
    transform: translate(2px, 2px) !important;
    box-shadow: 2px 2px 0 #2d2040 !important;
}

[data-testid="stDownloadButton"] > button {
    background: #c8e88a !important;
    color: #2d2040 !important;
    border: 2.5px solid #2d2040 !important;
    border-radius: 0 !important;
    font-weight: 700 !important;
    box-shadow: 4px 4px 0 #2d2040 !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #a8d860 !important;
    transform: translate(-2px, -2px) !important;
    box-shadow: 6px 6px 0 #2d2040 !important;
}

[data-testid="stFileUploader"] {
    border: 2.5px dashed #9b72d4 !important;
    background: #faf5ff !important;
    box-shadow: 4px 4px 0 #c8b8f0;
}

.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: #faf5ff !important;
    border: 2px solid #2d2040 !important;
    border-radius: 0 !important;
    color: #2d2040 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #e8d8ff;
    border: 2px solid #2d2040;
    border-bottom: none;
    gap: 0;
    box-shadow: 4px -4px 0 #2d2040;
}
.stTabs [data-baseweb="tab"] {
    background: #f0eaff;
    border-right: 2px solid #2d2040 !important;
    border-bottom: 2px solid #2d2040 !important;
    padding: 8px 20px;
    font-weight: 700;
    font-size: 0.82rem;
    color: #7a6a9a !important;
    border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
    background: #c8b8f0 !important;
    color: #2d2040 !important;
    border-bottom: 2px solid #c8b8f0 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    border: 2px solid #2d2040;
    border-top: none;
    background: #ffffff;
    padding: 18px;
    box-shadow: 4px 4px 0 #2d2040;
}

[data-testid="stDataFrame"] {
    border: 2.5px solid #2d2040 !important;
    box-shadow: 4px 4px 0 #2d2040;
}
[data-testid="stDataFrame"] thead th {
    background: #c8b8f0 !important;
    color: #2d2040 !important;
    font-weight: 700;
    border-bottom: 2px solid #2d2040 !important;
}

[data-testid="stAlert"] {
    border: 2.5px solid #2d2040 !important;
    border-radius: 0 !important;
    box-shadow: 4px 4px 0 #2d2040 !important;
    font-weight: 600;
}

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 2.5px solid #2d2040;
    box-shadow: 4px 4px 0 #2d2040;
    padding: 16px 18px;
    border-radius: 0 !important;
}
div[data-testid="stMetric"] label { color: #7a6a9a !important; font-weight: 600; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #9b72d4 !important;
    font-family: 'VT323', monospace !important;
    font-size: 2.2rem !important;
}

.risk-badge {
    display: inline-block;
    padding: 5px 16px;
    border: 2.5px solid #2d2040;
    font-weight: 700;
    font-size: 0.9rem;
    box-shadow: 3px 3px 0 #2d2040;
    letter-spacing: 0.05em;
}

.rec-card {
    background: #faf5ff;
    border: 2px solid #2d2040;
    border-left: 6px solid #c8e88a;
    padding: 11px 16px;
    margin: 6px 0;
    color: #2d2040;
    font-size: 0.92rem;
    font-weight: 500;
    box-shadow: 3px 3px 0 #2d2040;
}

.explain-pos {
    background: #f0fff4;
    border: 2px solid #2d2040;
    border-left: 6px solid #5ab85a;
    padding: 10px 14px;
    margin: 5px 0;
    box-shadow: 3px 3px 0 #2d2040;
    color: #2d2040;
}
.explain-neg {
    background: #fff0f4;
    border: 2px solid #2d2040;
    border-left: 6px solid #d43050;
    padding: 10px 14px;
    margin: 5px 0;
    box-shadow: 3px 3px 0 #2d2040;
    color: #2d2040;
}

.logo-text {
    font-family: 'Press Start 2P', monospace;
    font-size: 1.1rem;
    color: #9b72d4;
    line-height: 1.6;
    text-shadow: 2px 2px 0 #c8b8f0;
}
.subtitle-text {
    font-size: 0.72rem;
    color: #7a6a9a;
    font-weight: 600;
    margin-top: 4px;
    letter-spacing: 0.04em;
}

hr { border: none; border-top: 2px solid #c8b8f0; margin: 12px 0; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #f0eaff; }
::-webkit-scrollbar-thumb { background: #c8b8f0; border: 2px solid #2d2040; }
</style>
""", unsafe_allow_html=True)


def retro_window(title: str, icon: str = "🖥️", body_html: str = ""):
    st.markdown(f"""
    <div class="retro-window">
        <div class="retro-titlebar">
            <span>{icon} {title}</span>
            <div class="retro-titlebar-buttons">
                <span class="retro-btn-dot">_</span>
                <span class="retro-btn-dot">□</span>
                <span class="retro-btn-dot">✕</span>
            </div>
        </div>
        <div class="retro-window-body">{body_html}</div>
    </div>""", unsafe_allow_html=True)


def metric_card(label: str, value: str, sub: str = ""):
    sub_html = f'<div style="color:#7a6a9a;font-size:0.72rem;margin-top:3px;">{sub}</div>' if sub else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {sub_html}
    </div>""", unsafe_allow_html=True)


def section_header(text: str):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def speech_bubble(text: str, color: str = "#c8b8f0"):
    st.markdown(f"""
    <div style="
        background:{color};border:2.5px solid #2d2040;padding:12px 16px;
        margin:8px 0 22px 0;box-shadow:4px 4px 0 #2d2040;position:relative;
        font-weight:500;color:#2d2040;">
        {text}
        <div style="position:absolute;bottom:-14px;left:18px;width:0;height:0;
            border-left:10px solid transparent;border-right:10px solid transparent;
            border-top:14px solid #2d2040;"></div>
        <div style="position:absolute;bottom:-10px;left:20px;width:0;height:0;
            border-left:8px solid transparent;border-right:8px solid transparent;
            border-top:12px solid {color};"></div>
    </div>""", unsafe_allow_html=True)


def pixel_divider():
    st.markdown("""
    <div style="height:10px;margin:14px 0;
        background:repeating-linear-gradient(
            90deg,#c8b8f0 0,#c8b8f0 8px,#f0b8d4 8px,#f0b8d4 16px,
            #c8e88a 16px,#c8e88a 24px,#f0eaff 24px,#f0eaff 32px);
        border-top:2px solid #2d2040;border-bottom:2px solid #2d2040;">
    </div>""", unsafe_allow_html=True)


def retro_alert(text: str, kind: str = "info"):
    cfg = {
        "info":    ("#e8d8ff", "#9b72d4", "ℹ️"),
        "success": ("#d8f8d8", "#5ab85a", "✅"),
        "warning": ("#fff8d8", "#e8a020", "⚠️"),
        "error":   ("#ffd8e0", "#d43050", "❌"),
    }.get(kind, ("#e8d8ff", "#9b72d4", "ℹ️"))
    bg, border, icon = cfg
    st.markdown(f"""
    <div style="background:{bg};border:2.5px solid {border};border-left:8px solid {border};
         padding:12px 16px;box-shadow:4px 4px 0 #2d2040;margin:8px 0;
         color:#2d2040;font-weight:600;font-size:0.9rem;">
        {icon} {text}
    </div>""", unsafe_allow_html=True)