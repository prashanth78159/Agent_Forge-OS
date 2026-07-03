
import streamlit as st

def apply_theme():

    st.markdown("""
    <style>

    .stApp{
        background:#0D1117;
        color:white;
    }

    .main-title{
        font-size:3rem;
        font-weight:700;
        color:#58A6FF;
    }

    .card{
        background:#161B22;
        padding:20px;
        border-radius:12px;
        border:1px solid #30363D;
        margin-bottom:15px;
    }

    .metric-card{
        background:#161B22;
        padding:15px;
        border-radius:12px;
        text-align:center;
        border:1px solid #30363D;
    }

    .section-title{
        font-size:1.5rem;
        font-weight:600;
        margin-top:20px;
        margin-bottom:10px;
    }

    </style>
    """,
    unsafe_allow_html=True)
