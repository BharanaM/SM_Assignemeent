import streamlit as st

def apply_2026_theme(page_title="Analytics", page_icon="🚀"):
    st.set_page_config(
        page_title=page_title, 
        page_icon=page_icon, 
        layout="wide", 
        initial_sidebar_state="expanded"
    )

    st.markdown("""
        <style>
        /* 2026 Futuristic & Glassmorphism UI */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Space+Grotesk:wght@400;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #020617;
        }

        /* 2026 Cyber Grid Background */
        .stApp {
            background-image: 
                linear-gradient(to right, rgba(139, 92, 246, 0.05) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(139, 92, 246, 0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            background-position: center center;
            background-attachment: fixed;
        }
        
        /* Typography */
        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif !important;
            letter-spacing: -0.03em;
        }
        h1 {
            background: linear-gradient(135deg, #a855f7 0%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            margin-bottom: 0.5rem !important;
        }

        /* Container padding */
        .block-container { 
            padding-top: 3rem !important; 
            padding-bottom: 3rem !important; 
            max-width: 1400px;
        }

        /* Metrics Glassmorphism styling */
        div[data-testid="stMetric"] {
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1.5rem !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(139, 92, 246, 0.5);
        }
        div[data-testid="stMetricValue"] { 
            font-size: 2.5rem !important; 
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            color: #f8fafc !important; 
        }
        div[data-testid="stMetricLabel"] {
            font-size: 1rem !important;
            color: #94a3b8 !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.6) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        [data-testid="stSidebarNav"] {
            background: transparent !important;
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 12px !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.02em !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2) !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5), 0 0 15px rgba(59, 130, 246, 0.5) !important;
            filter: brightness(1.1);
        }

        /* Expanders */
        .streamlit-expanderHeader {
            background-color: rgba(30, 41, 59, 0.4) !important;
            backdrop-filter: blur(10px);
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            font-weight: 600 !important;
            color: #e2e8f0 !important;
        }
        div[data-testid="stExpander"] {
            background: transparent !important;
            border: none !important;
        }

        /* Dataframes & Tables */
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Containers */
        div[data-testid="stVerticalBlock"] > div[style*="border"] {
            background: rgba(30, 41, 59, 0.3) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
        }
        
        /* Info/Warning/Error boxes */
        div.stAlert {
            background: rgba(30, 41, 59, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(10px);
        }
        </style>
    """, unsafe_allow_html=True)
