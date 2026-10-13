import streamlit as st


def apply_2026_theme(page_title="Graduate Employment Analytics", page_icon="🎓"):
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

        :root {
            --bg-primary: #030712;
            --bg-card: rgba(15, 23, 42, 0.72);
            --bg-card-hover: rgba(30, 41, 59, 0.85);
            --border-subtle: rgba(148, 163, 184, 0.14);
            --border-glow: rgba(139, 92, 246, 0.55);
            --accent-purple: #8b5cf6;
            --accent-blue: #3b82f6;
            --accent-cyan: #06b6d4;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
        }

        /* Ambient Aurora + Cyber Grid Background */
        .stApp {
            background-color: #030712;
            background-image:
                radial-gradient(at 10% 10%, rgba(139, 92, 246, 0.16) 0px, transparent 45%),
                radial-gradient(at 90% 15%, rgba(59, 130, 246, 0.14) 0px, transparent 45%),
                radial-gradient(at 50% 90%, rgba(6, 182, 212, 0.10) 0px, transparent 50%),
                linear-gradient(to right, rgba(148, 163, 184, 0.04) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(148, 163, 184, 0.04) 1px, transparent 1px);
            background-size: 100% 100%, 100% 100%, 100% 100%, 36px 36px, 36px 36px;
            background-attachment: fixed;
        }

        /* Main Container Spacing */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1480px !important;
        }

        /* Typography */
        h1, h2, h3, h4 {
            font-family: 'Space Grotesk', sans-serif !important;
            letter-spacing: -0.025em;
            color: #f8fafc !important;
        }
        h1 {
            background: linear-gradient(135deg, #c084fc 0%, #60a5fa 50%, #34d399 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
        }

        /* Executive Hero Banner */
        .exec-hero {
            position: relative;
            background: linear-gradient(135deg, rgba(30, 27, 75, 0.82) 0%, rgba(15, 23, 42, 0.90) 60%, rgba(8, 47, 73, 0.78) 100%);
            border: 1px solid rgba(139, 92, 246, 0.35);
            border-radius: 20px;
            padding: 1.85rem 2.2rem;
            margin-bottom: 1.6rem;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.12);
            overflow: hidden;
        }
        .exec-hero::before {
            content: "";
            position: absolute;
            top: -50%;
            right: -10%;
            width: 380px;
            height: 380px;
            background: radial-gradient(circle, rgba(139, 92, 246, 0.25) 0%, transparent 70%);
            pointer-events: none;
        }
        .hero-badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-bottom: 0.75rem;
        }
        .hero-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.73rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            padding: 0.28rem 0.75rem;
            border-radius: 999px;
            background: rgba(139, 92, 246, 0.18);
            border: 1px solid rgba(167, 139, 250, 0.4);
            color: #ddd6fe;
        }
        .hero-pill.cyan {
            background: rgba(6, 182, 212, 0.16);
            border-color: rgba(34, 211, 238, 0.4);
            color: #a5f3fc;
        }
        .hero-pill.emerald {
            background: rgba(16, 185, 129, 0.16);
            border-color: rgba(52, 211, 153, 0.4);
            color: #a7f3d0;
        }
        .hero-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.15rem;
            font-weight: 800;
            line-height: 1.18;
            margin: 0 0 0.55rem 0;
            background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 55%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            font-size: 0.98rem;
            color: #cbd5e1;
            max-width: 920px;
            line-height: 1.55;
            margin: 0;
        }

        /* Custom Glass KPI Cards */
        .kpi-card {
            background: linear-gradient(160deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.88) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-top: 3px solid var(--accent-color, #8b5cf6);
            border-radius: 16px;
            padding: 1.25rem 1.35rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
            transition: all 0.25s ease;
            height: 100%;
        }
        .kpi-card:hover {
            transform: translateY(-4px);
            border-color: rgba(139, 92, 246, 0.45);
            box-shadow: 0 16px 36px rgba(139, 92, 246, 0.18);
        }
        .kpi-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.45rem;
        }
        .kpi-label {
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            color: #94a3b8;
        }
        .kpi-icon {
            font-size: 1.15rem;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            width: 34px;
            height: 34px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .kpi-value {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.95rem;
            font-weight: 700;
            color: #f8fafc;
            line-height: 1.15;
            margin-bottom: 0.4rem;
        }
        .kpi-delta {
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.15rem 0.55rem;
            border-radius: 6px;
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        .kpi-delta.purple {
            background: rgba(139, 92, 246, 0.16);
            color: #c4b5fd;
            border-color: rgba(139, 92, 246, 0.35);
        }
        .kpi-delta.blue {
            background: rgba(59, 130, 246, 0.16);
            color: #93c5fd;
            border-color: rgba(59, 130, 246, 0.35);
        }
        .kpi-delta.amber {
            background: rgba(245, 158, 11, 0.16);
            color: #fcd34d;
            border-color: rgba(245, 158, 11, 0.35);
        }

        /* Legacy .metric-card & .theory-box support across pages */
        .metric-card {
            background: linear-gradient(160deg, rgba(30, 41, 59, 0.78) 0%, rgba(15, 23, 42, 0.90) 100%) !important;
            border: 1px solid rgba(148, 163, 184, 0.18) !important;
            border-left: 4px solid #8b5cf6 !important;
            border-radius: 16px !important;
            padding: 1.35rem 1.5rem !important;
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35) !important;
            color: #f8fafc !important;
        }
        .metric-card h3, .metric-card h4 {
            color: #f8fafc !important;
            margin-top: 0 !important;
        }
        .metric-card p {
            color: #cbd5e1 !important;
            margin-bottom: 0.4rem !important;
        }
        .metric-card strong {
            color: #ffffff !important;
        }
        .metric-label {
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #94a3b8;
            margin-bottom: 0.35rem;
        }
        .metric-value {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.85rem;
            font-weight: 700;
            color: #f8fafc;
        }
        .theory-box {
            background: rgba(15, 23, 42, 0.78) !important;
            border: 1px solid rgba(139, 92, 246, 0.28) !important;
            border-left: 4px solid #3b82f6 !important;
            padding: 1.15rem 1.4rem !important;
            border-radius: 14px !important;
            margin-top: 0.9rem !important;
            font-size: 0.94rem !important;
            color: #e2e8f0 !important;
            line-height: 1.6 !important;
        }
        .theory-box strong {
            color: #93c5fd !important;
        }

        /* Section Header Strip */
        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 0.25rem 0 0.75rem 0;
            padding-bottom: 0.45rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.14);
        }
        .section-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.18rem;
            font-weight: 700;
            color: #f8fafc;
            margin: 0;
        }
        .section-tag {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            color: #94a3b8;
            background: rgba(30, 41, 59, 0.7);
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            border: 1px solid rgba(148, 163, 184, 0.15);
        }

        /* Native stMetric Glassmorphism */
        div[data-testid="stMetric"] {
            background: linear-gradient(160deg, rgba(30, 41, 59, 0.72) 0%, rgba(15, 23, 42, 0.86) 100%);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 16px;
            padding: 1.25rem 1.35rem !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.32);
            transition: transform 0.25s ease, border-color 0.25s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            border-color: rgba(139, 92, 246, 0.5);
        }
        div[data-testid="stMetricValue"] {
            font-size: 2.15rem !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            color: #f8fafc !important;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 0.82rem !important;
            color: #94a3b8 !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        /* Bordered Containers (Cards) */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(15, 23, 42, 0.68) !important;
            backdrop-filter: blur(14px) !important;
            border: 1px solid rgba(148, 163, 184, 0.15) !important;
            border-radius: 18px !important;
            padding: 1.2rem 1.35rem !important;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.28) !important;
        }

        /* Tabs Styling */
        button[data-baseweb="tab"] {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            color: #94a3b8 !important;
            padding: 0.6rem 1.15rem !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #f8fafc !important;
            background: rgba(139, 92, 246, 0.15) !important;
            border-radius: 10px 10px 0 0 !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(10, 15, 30, 0.95) 0%, rgba(15, 23, 42, 0.92) 100%) !important;
            border-right: 1px solid rgba(148, 163, 184, 0.12);
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.16) !important;
            border-radius: 12px !important;
            padding: 0.7rem 1.4rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.02em !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 6px 20px rgba(139, 92, 246, 0.28) !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 28px rgba(139, 92, 246, 0.45), 0 0 15px rgba(59, 130, 246, 0.4) !important;
            filter: brightness(1.08);
        }

        /* Dataframes */
        [data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.18);
        }

        /* Gallery Caption */
        .gallery-caption {
            text-align: center;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            font-size: 0.92rem;
            color: #e2e8f0;
            padding-top: 0.5rem;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )


def render_hero_banner(title: str, subtitle: str, badges=None):
    if badges is None:
        badges = [
            ("🎓 IT3081 Statistical Modeling", ""),
            ("⚡ R 4.6 + Streamlit Engine", "cyan"),
            ("📊 N = 299,984 Graduates", "emerald"),
        ]
    pills_html = "".join(
        f'<span class="hero-pill {cls}">{text}</span>' for text, cls in badges
    )
    st.markdown(
        f"""
        <div class="exec-hero">
            <div class="hero-badge-row">{pills_html}</div>
            <div class="hero-title">{title}</div>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_card(
    label: str,
    value: str,
    delta: str = "",
    icon: str = "📊",
    accent: str = "#8b5cf6",
    delta_cls: str = "",
):
    delta_html = f'<div class="kpi-delta {delta_cls}">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="kpi-card" style="--accent-color: {accent};">
            <div class="kpi-top">
                <span class="kpi-label">{label}</span>
                <span class="kpi-icon">{icon}</span>
            </div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_plotly_chart(fig, height=360, show_legend=True):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.35)",
        font=dict(family="Inter, sans-serif", color="#e2e8f0", size=12),
        showlegend=show_legend,
        height=height,
        margin=dict(t=28, b=36, l=36, r=24),
        legend=dict(
            bgcolor="rgba(15, 23, 42, 0.65)",
            bordercolor="rgba(148, 163, 184, 0.15)",
            borderwidth=1,
            font=dict(color="#e2e8f0", size=11),
        ),
        xaxis=dict(
            gridcolor="rgba(148, 163, 184, 0.08)",
            zerolinecolor="rgba(148, 163, 184, 0.15)",
            tickfont=dict(color="#cbd5e1"),
            title_font=dict(color="#94a3b8", size=12),
        ),
        yaxis=dict(
            gridcolor="rgba(148, 163, 184, 0.08)",
            zerolinecolor="rgba(148, 163, 184, 0.15)",
            tickfont=dict(color="#cbd5e1"),
            title_font=dict(color="#94a3b8", size=12),
        ),
        hoverlabel=dict(
            bgcolor="#0f172a",
            bordercolor="#8b5cf6",
            font_size=12,
            font_family="Inter, sans-serif",
            font_color="#f8fafc",
        ),
    )
    return fig
