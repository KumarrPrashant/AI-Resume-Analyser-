"""
🌌 GALAXY / COSMOS THEME ENGINE
--------------------------------
Centralised, self-contained styling layer for the AI Resume Analyzer.
Import `inject_theme()` once at the top of the app and use the helper
components below (hero, cards, alerts, badges, score orb, nav header)
to keep every page visually consistent with the space theme.
"""

import streamlit as st
from stars_data import STARS_SMALL, STARS_MED, STARS_LARGE

PRIMARY_FONT = "Poppins"
DISPLAY_FONT = "Orbitron"


def inject_theme():
    """Injects the full galaxy CSS + animated starfield background once per page."""

    st.markdown(
        f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800&display=swap');

    :root {{
        --space-black:   #05050f;
        --space-dark:    #0a0b1e;
        --space-dark-2:  #10122b;
        --nebula-purple: #8b5cf6;
        --nebula-violet: #a855f7;
        --nebula-pink:   #f72585;
        --cosmic-blue:   #3a86ff;
        --star-gold:     #ffd166;
        --aurora-green:  #06ffa5;
        --text-light:    #eef0fb;
        --text-dim:      #a4a8d1;
        --text-faint:    #767ab0;
        --glass-bg:      rgba(255,255,255,0.045);
        --glass-bg-2:    rgba(255,255,255,0.08);
        --glass-border:  rgba(255,255,255,0.14);
        --glow-purple:   0 0 24px rgba(139,92,246,0.55);
        --glow-pink:     0 0 24px rgba(247,37,133,0.45);
        --glow-blue:     0 0 24px rgba(58,134,255,0.45);
    }}

    /* ---------- BASE ---------- */
    html, body, [class^="css"], [class*=" css"] {{
        font-family: '{PRIMARY_FONT}', sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(ellipse 90% 60% at 15% -10%, rgba(139,92,246,0.28), transparent 60%),
            radial-gradient(ellipse 80% 55% at 110% 10%, rgba(247,37,133,0.18), transparent 55%),
            radial-gradient(ellipse 70% 50% at 50% 120%, rgba(58,134,255,0.20), transparent 55%),
            linear-gradient(180deg, var(--space-black) 0%, var(--space-dark) 45%, var(--space-dark-2) 100%);
        background-attachment: fixed;
        color: var(--text-light);
    }}

    /* ---------- ANIMATED STARFIELD ---------- */
    #cosmic-stars {{
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        overflow: hidden;
    }}
    .star-layer {{
        position: absolute;
        top: 0; left: 0;
        width: 1px; height: 1px;
        background: transparent;
        border-radius: 50%;
    }}
    .star-small  {{ box-shadow: {STARS_SMALL}; animation: twinkle 4s ease-in-out infinite; }}
    .star-med    {{ box-shadow: {STARS_MED}; width: 2px; height: 2px; animation: twinkle 6s ease-in-out infinite; animation-delay: 1s; }}
    .star-large  {{ box-shadow: {STARS_LARGE}; width: 3px; height: 3px; animation: twinkle 3.2s ease-in-out infinite; animation-delay: .5s; }}

    @keyframes twinkle {{
        0%, 100% {{ opacity: 0.35; }}
        50%      {{ opacity: 1; }}
    }}

    .nebula-blob {{
        position: absolute;
        border-radius: 50%;
        filter: blur(90px);
        opacity: 0.35;
        animation: drift 22s ease-in-out infinite;
    }}
    .nebula-blob.n1 {{ width: 420px; height: 420px; background: var(--nebula-purple); top: -120px; left: -100px; }}
    .nebula-blob.n2 {{ width: 380px; height: 380px; background: var(--nebula-pink); top: 40%; right: -140px; animation-delay: 6s; }}
    .nebula-blob.n3 {{ width: 320px; height: 320px; background: var(--cosmic-blue); bottom: -120px; left: 30%; animation-delay: 12s; }}

    @keyframes drift {{
        0%, 100% {{ transform: translate(0,0) scale(1); }}
        50%      {{ transform: translate(30px,-40px) scale(1.12); }}
    }}

    /* ---------- HERO ---------- */
    .hero-wrap {{
        text-align: center;
        padding: 2.4rem 1rem 1.6rem 1rem;
        position: relative;
        z-index: 1;
    }}
    .hero-badge {{
        display: inline-block;
        padding: 6px 18px;
        border-radius: 999px;
        background: var(--glass-bg-2);
        border: 1px solid var(--glass-border);
        color: var(--text-dim);
        font-size: 0.72rem;
        letter-spacing: 2.5px;
        font-weight: 600;
        margin-bottom: 18px;
        backdrop-filter: blur(6px);
    }}
    .hero-title {{
        font-family: '{DISPLAY_FONT}', sans-serif;
        font-weight: 800;
        font-size: 3.1rem;
        line-height: 1.15;
        letter-spacing: 1px;
        color: var(--text-light);
        margin: 0;
    }}
    .hero-title .grad {{
        background: linear-gradient(90deg, var(--nebula-purple), var(--cosmic-blue), var(--nebula-pink), var(--nebula-purple));
        background-size: 300% auto;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: shimmer 6s linear infinite;
    }}
    @keyframes shimmer {{
        0%   {{ background-position: 0% 50%; }}
        100% {{ background-position: 300% 50%; }}
    }}
    .hero-sub {{
        margin-top: 14px;
        color: var(--text-dim);
        font-size: 1.02rem;
        font-weight: 300;
        max-width: 620px;
        margin-left: auto;
        margin-right: auto;
    }}
    .hero-divider {{
        margin: 1.8rem auto 0 auto;
        width: 100%;
        max-width: 900px;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
    }}

    /* ---------- SECTION HEADERS ---------- */
    .cosmic-h {{
        font-family: '{DISPLAY_FONT}', sans-serif;
        font-weight: 700;
        font-size: 1.35rem;
        color: var(--text-light);
        letter-spacing: .5px;
        margin: 1.6rem 0 .9rem 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .cosmic-h::before {{
        content: "";
        width: 5px; height: 22px;
        border-radius: 3px;
        background: linear-gradient(180deg, var(--nebula-purple), var(--cosmic-blue));
        display: inline-block;
        box-shadow: var(--glow-purple);
    }}
    .cosmic-sub {{
        color: var(--text-faint);
        font-size: .88rem;
        margin-top: -6px;
        margin-bottom: 1rem;
    }}

    /* ---------- GLASS CARD ---------- */
    .glass-card {{
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 18px;
        padding: 1.3rem 1.4rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
        margin-bottom: 1.1rem;
    }}
    .glass-card:hover {{
        border-color: rgba(139,92,246,0.5);
        transition: border-color .3s ease;
    }}

    /* ---------- INFO CHIPS (basic info grid) ---------- */
    .chip-grid {{ display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 1.2rem; }}
    .info-chip {{
        flex: 1 1 200px;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 14px;
        padding: 14px 16px;
        backdrop-filter: blur(8px);
    }}
    .info-chip .chip-label {{
        font-size: .68rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: var(--text-faint);
        font-weight: 600;
    }}
    .info-chip .chip-value {{
        font-size: 1.02rem;
        color: var(--text-light);
        font-weight: 500;
        margin-top: 4px;
        word-break: break-word;
    }}

    /* ---------- ALERTS (replace default st.success/warning/error/info look) ---------- */
    .cosmic-alert {{
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 12px 16px;
        border-radius: 12px;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        margin: 8px 0;
        font-size: .93rem;
        color: var(--text-light);
        backdrop-filter: blur(6px);
    }}
    .cosmic-alert .a-icon {{ font-size: 1.0rem; line-height: 1.3; }}
    .alert-success {{ border-left: 3px solid var(--aurora-green); box-shadow: 0 0 18px rgba(6,255,165,0.10); }}
    .alert-warning {{ border-left: 3px solid var(--star-gold); box-shadow: 0 0 18px rgba(255,209,102,0.10); }}
    .alert-error   {{ border-left: 3px solid var(--nebula-pink); box-shadow: 0 0 18px rgba(247,37,133,0.12); }}
    .alert-info    {{ border-left: 3px solid var(--cosmic-blue); box-shadow: 0 0 18px rgba(58,134,255,0.12); }}
    .alert-tip     {{ border-left: 3px solid var(--text-faint); opacity: 0.85; }}

    /* ---------- SCORE ORB ---------- */
    .score-orb-wrap {{ display:flex; justify-content:center; margin: 1.6rem 0; }}
    .score-orb {{
        width: 190px; height: 190px;
        border-radius: 50%;
        display: flex; flex-direction: column; align-items:center; justify-content:center;
        background: radial-gradient(circle at 35% 30%, rgba(139,92,246,0.35), rgba(10,11,30,0.9) 70%);
        border: 2px solid rgba(139,92,246,0.55);
        box-shadow: 0 0 40px rgba(139,92,246,0.45), inset 0 0 30px rgba(139,92,246,0.15);
        animation: pulse-orb 3.5s ease-in-out infinite;
    }}
    @keyframes pulse-orb {{
        0%, 100% {{ box-shadow: 0 0 40px rgba(139,92,246,0.35), inset 0 0 30px rgba(139,92,246,0.12); }}
        50%      {{ box-shadow: 0 0 60px rgba(139,92,246,0.6), inset 0 0 40px rgba(139,92,246,0.22); }}
    }}
    .score-orb .val {{ font-family:'{DISPLAY_FONT}',sans-serif; font-size: 2.6rem; font-weight:800; color: var(--text-light); }}
    .score-orb .lbl {{ font-size: .68rem; letter-spacing:1.5px; text-transform:uppercase; color: var(--text-dim); margin-top:2px; }}

    /* ---------- BADGES ---------- */
    .cosmic-badge {{
        display:inline-block; padding: 5px 14px; border-radius: 999px;
        font-size: .78rem; font-weight:600; letter-spacing:.5px;
        background: linear-gradient(90deg, rgba(139,92,246,.25), rgba(58,134,255,.25));
        border: 1px solid var(--glass-border); color: var(--text-light);
    }}

    /* ---------- SIDEBAR ---------- */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(10,11,30,0.97), rgba(5,5,15,0.99));
        border-right: 1px solid var(--glass-border);
    }}
    [data-testid="stSidebar"] * {{ color: var(--text-light); }}
    .sidebar-title {{
        font-family: '{DISPLAY_FONT}', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 1px;
        background: linear-gradient(90deg, var(--nebula-violet), var(--cosmic-blue));
        -webkit-background-clip: text; background-clip: text; color: transparent;
        margin-bottom: 4px;
    }}
    .sidebar-caption {{ color: var(--text-faint); font-size: .78rem; margin-bottom: 18px; }}
    .sidebar-foot {{
        margin-top: 22px; padding-top: 14px;
        border-top: 1px solid var(--glass-border);
        font-size: .78rem; color: var(--text-faint);
    }}

    /* ---------- WIDGETS ---------- */
    .stButton>button, .stFormSubmitButton>button, .stDownloadButton>button {{
        background: linear-gradient(90deg, var(--nebula-purple), var(--cosmic-blue));
        color: white; border: none; border-radius: 999px;
        padding: 0.55rem 1.6rem; font-weight: 600; letter-spacing: .3px;
        box-shadow: 0 4px 20px rgba(139,92,246,0.35);
        transition: all .25s ease;
    }}
    .stButton>button:hover, .stFormSubmitButton>button:hover, .stDownloadButton>button:hover {{
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 6px 28px rgba(139,92,246,0.55);
        color: white;
    }}

    input, textarea, .stTextInput input, .stNumberInput input {{
        background: var(--glass-bg) !important;
        color: var(--text-light) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 10px !important;
    }}
    .stTextInput>div>div, .stNumberInput>div>div {{
        background: transparent !important;
    }}
    ::placeholder {{ color: var(--text-faint) !important; }}

    [data-baseweb="select"] > div {{
        background: var(--glass-bg) !important;
        border-color: var(--glass-border) !important;
        border-radius: 10px !important;
        color: var(--text-light) !important;
    }}

    .stSlider [data-baseweb="slider"] > div > div {{ background: var(--glass-border) !important; }}
    .stSlider [role="slider"] {{
        background: var(--nebula-purple) !important;
        box-shadow: 0 0 10px rgba(139,92,246,0.7) !important;
    }}

    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, var(--nebula-pink), var(--nebula-purple), var(--cosmic-blue)) !important;
        box-shadow: 0 0 12px rgba(139,92,246,0.6);
    }}
    .stProgress > div > div > div {{
        background: rgba(255,255,255,0.08) !important;
    }}

    [data-testid="stFileUploaderDropzone"] {{
        background: var(--glass-bg) !important;
        border: 1.5px dashed var(--glass-border) !important;
        border-radius: 16px !important;
    }}
    [data-testid="stFileUploaderDropzone"] * {{ color: var(--text-dim) !important; }}

    [data-testid="stDataFrame"] {{
        border-radius: 14px; overflow: hidden;
        border: 1px solid var(--glass-border);
    }}

    .streamlit-expanderHeader {{
        background: var(--glass-bg) !important;
        border-radius: 10px !important;
        color: var(--text-light) !important;
    }}

    /* default markdown headers */
    h1, h2, h3 {{ color: var(--text-light); font-family: '{DISPLAY_FONT}', sans-serif; }}
    p, span, label, li {{ color: var(--text-light); }}

    /* course pill list */
    .course-list {{ display:flex; flex-direction:column; gap:8px; margin-top: 6px; }}
    .course-pill {{
        display:flex; align-items:center; gap:10px;
        background: var(--glass-bg); border:1px solid var(--glass-border);
        padding: 10px 14px; border-radius: 12px;
        transition: all .2s ease;
    }}
    .course-pill:hover {{ border-color: rgba(139,92,246,.6); transform: translateX(3px); }}
    .course-pill a {{ color: var(--text-light) !important; text-decoration:none; font-weight:500; }}
    .course-pill .pill-num {{
        min-width: 24px; height:24px; border-radius:50%;
        background: linear-gradient(135deg, var(--nebula-purple), var(--cosmic-blue));
        display:flex; align-items:center; justify-content:center;
        font-size:.72rem; font-weight:700; color:white;
    }}

    /* footer */
    .cosmic-footer {{
        text-align:center; padding: 2rem 0 1rem 0;
        color: var(--text-faint); font-size: .82rem;
    }}
    .cosmic-footer a {{ color: var(--nebula-violet); text-decoration:none; font-weight:600; }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>

    <div id="cosmic-stars">
        <div class="star-layer star-small"></div>
        <div class="star-layer star-med"></div>
        <div class="star-layer star-large"></div>
        <div class="nebula-blob n1"></div>
        <div class="nebula-blob n2"></div>
        <div class="nebula-blob n3"></div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def hero(title_main="AI RESUME", title_grad="ANALYZER",
         subtitle="Navigate your career through the cosmos — parsed by AI, guided by the stars.",
         badge="✨ AI-POWERED CAREER INTELLIGENCE"):
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-badge">{badge}</div>
            <div class="hero-title">{title_main} <span class="grad">{title_grad}</span></div>
            <p class="hero-sub">{subtitle}</p>
        </div>
        <div class="hero-divider"></div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title, subtitle=None):
    st.markdown(f'<div class="cosmic-h">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="cosmic-sub">{subtitle}</div>', unsafe_allow_html=True)


def cosmic_alert(message, kind="info"):
    icons = {"success": "✅", "warning": "🛰️", "error": "🚫", "info": "🔭", "tip": "💡"}
    clean = str(message).replace("**", "").strip()
    st.markdown(
        f'<div class="cosmic-alert alert-{kind}"><span class="a-icon">{icons.get(kind, "ℹ️")}</span>'
        f'<span>{clean}</span></div>',
        unsafe_allow_html=True,
    )


def cosmic_success(msg):
    cosmic_alert(msg, "success")


def cosmic_warning(msg):
    cosmic_alert(msg, "warning")


def cosmic_error(msg):
    cosmic_alert(msg, "error")


def cosmic_info(msg):
    cosmic_alert(msg, "info")


def cosmic_tip(msg):
    cosmic_alert(msg, "tip")


def info_chips(chips):
    """chips: list of (label, value) tuples"""
    html = '<div class="chip-grid">'
    for label, value in chips:
        html += (
            f'<div class="info-chip"><div class="chip-label">{label}</div>'
            f'<div class="chip-value">{value}</div></div>'
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def score_orb(score, max_score=100, label="COSMIC SCORE"):
    st.markdown(
        f"""
        <div class="score-orb-wrap">
            <div class="score-orb">
                <div class="val">{score}</div>
                <div class="lbl">{label} / {max_score}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge(text):
    st.markdown(f'<span class="cosmic-badge">{text}</span>', unsafe_allow_html=True)


def glass_card_open():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)


def glass_card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def course_list_html(items):
    """items: list of (name, link) already numbered"""
    html = '<div class="course-list">'
    for i, (name, link) in enumerate(items, start=1):
        html += (
            f'<div class="course-pill"><span class="pill-num">{i}</span>'
            f'<a href="{link}" target="_blank">{name}</a></div>'
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def footer():
    st.markdown(
        """
        <div class="cosmic-footer">
            Built with 🤍 across the galaxy · Powered by AI &amp; Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )
