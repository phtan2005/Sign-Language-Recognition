import streamlit as st
import json
import os
import re
import requests

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TikTok Viral Detector",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:      #08090f;
    --bg2:     #0e1018;
    --bg3:     #13151f;
    --bg4:     #1a1c28;
    --border:  rgba(255,255,255,0.08);
    --border2: rgba(255,255,255,0.15);
    --red:     #ff3358;
    --red2:    #ff7090;
    --cyan:    #00cfff;
    --gold:    #ffcc00;
    --green:   #2ecc71;
    --green2:  #27ae60;
    --orange:  #ff9500;
    --purple:  #bf5af2;
    --text:    #eceaf6;
    --text2:   rgba(236,234,246,0.65);
    --text3:   rgba(236,234,246,0.40);
    --fh:      'Plus Jakarta Sans', sans-serif;
    --fm:      'JetBrains Mono', monospace;
    --r-sm:    8px;
    --r-md:    14px;
    --r-lg:    20px;
}
*, *::before, *::after { box-sizing: border-box; }
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--fh) !important;
}
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse 65% 40% at 10% 0%,   rgba(255,51,88,0.09)  0%, transparent 55%),
        radial-gradient(ellipse 45% 30% at 90% 100%, rgba(0,207,255,0.06)  0%, transparent 55%);
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stSidebar"] { display: none !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.wrap {
    max-width: 1080px;
    margin: 0 auto;
    padding: 2rem 2rem 6rem;
    position: relative; z-index: 1;
}

/* ── TOPBAR ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.5rem 0 1.75rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}
.topbar-brand { display: flex; align-items: center; gap: 1rem; }
.topbar-icon {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, var(--red), #ff6080);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    box-shadow: 0 4px 20px rgba(255,51,88,0.4);
}
.topbar-name { font-family: var(--fh); font-size: 1.1rem; font-weight: 800; color: var(--text); letter-spacing: -0.02em; }
.topbar-name span { background: linear-gradient(120deg, var(--red), var(--cyan)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.topbar-sub { font-family: var(--fm); font-size: 0.7rem; color: var(--text3); letter-spacing: 0.04em; }
.topbar-pills { display: flex; gap: 0.6rem; }
.pill {
    display: flex; align-items: center; gap: 0.45rem;
    background: var(--bg3); border: 1px solid var(--border);
    border-radius: 999px; padding: 0.35rem 0.85rem;
    font-family: var(--fm); font-size: 0.7rem; color: var(--text2); white-space: nowrap;
}
.pill strong { color: var(--text); font-weight: 600; }
.pill.red-pill { background: rgba(255,51,88,0.1); border-color: rgba(255,51,88,0.3); color: var(--red2); }
.pill.red-pill::before {
    content: ''; width: 5px; height: 5px;
    background: var(--red); border-radius: 50%;
    animation: blink 1.8s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.15;} }

/* ── TABS ── */
div[data-testid="stTabs"] [data-testid="stTabsTabList"] {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-md) !important;
    padding: 0.35rem !important;
    gap: 0.25rem !important;
    margin-bottom: 1.5rem !important;
}
div[data-testid="stTabs"] button[data-testid="stTabsTab"] {
    background: transparent !important;
    border: none !important;
    border-radius: 10px !important;
    color: var(--text3) !important;
    font-family: var(--fh) !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.3rem !important;
    transition: all 0.2s !important;
}
div[data-testid="stTabs"] button[data-testid="stTabsTab"]:hover {
    color: var(--text) !important;
    background: rgba(255,255,255,0.05) !important;
}
div[data-testid="stTabs"] button[data-testid="stTabsTab"][aria-selected="true"] {
    background: var(--red) !important;
    color: white !important;
    box-shadow: 0 2px 12px rgba(255,51,88,0.4) !important;
}
div[data-testid="stTabs"] [data-testid="stTabsTabList"]::before { display: none !important; }

/* ── TEXT INPUT (URL box) ── */
div[data-testid="stTextInput"] {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-md) !important;
    padding: 0.9rem 1.1rem 0.75rem !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stTextInput"]:focus-within {
    border-color: rgba(255,51,88,0.5) !important;
    box-shadow: 0 0 0 3px rgba(255,51,88,0.1) !important;
}
div[data-testid="stTextInput"] label p {
    font-family: var(--fm) !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--text3) !important;
    margin-bottom: 0.4rem !important;
}
div[data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important;
    color: var(--text) !important;
    font-family: var(--fm) !important;
    font-size: 0.88rem !important;
    padding: 0 !important;
    box-shadow: none !important;
}

/* ── NUMBER INPUT ── */
div[data-testid="stNumberInput"] {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-md) !important;
    padding: 1rem 1.1rem 0.8rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stNumberInput"]:focus-within {
    border-color: rgba(255,51,88,0.5) !important;
    box-shadow: 0 0 0 3px rgba(255,51,88,0.1) !important;
}
div[data-testid="stNumberInput"] label p {
    font-family: var(--fm) !important; font-size: 0.68rem !important;
    letter-spacing: 0.1em !important; text-transform: uppercase !important;
    color: var(--text3) !important; margin-bottom: 0.5rem !important;
}
div[data-testid="stNumberInput"] input {
    background: transparent !important; border: none !important;
    color: var(--text) !important; font-family: var(--fh) !important;
    font-size: 1.5rem !important; font-weight: 700 !important;
    padding: 0 !important; box-shadow: none !important; letter-spacing: -0.02em;
}
div[data-testid="stNumberInput"] button {
    background: transparent !important; border: none !important; color: var(--text3) !important;
}
div[data-testid="stNumberInput"] button:hover {
    color: var(--red) !important;
    background: rgba(255,51,88,0.1) !important; border-radius: 6px !important;
}

/* ── BUTTON ── */
div[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #ff3358 0%, #ff5577 100%) !important;
    color: #fff !important; border: none !important;
    border-radius: var(--r-md) !important; padding: 1rem !important;
    font-family: var(--fh) !important; font-size: 1rem !important;
    font-weight: 700 !important; letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(255,51,88,0.38) !important;
    margin-top: 0.5rem !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 36px rgba(255,51,88,0.52) !important;
}
div[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* ── CARD ── */
.card {
    background: var(--bg2); border: 1px solid var(--border);
    border-radius: var(--r-lg); padding: 1.75rem;
    margin-bottom: 1.25rem; position: relative; overflow: hidden;
}
.card::before {
    content: ''; position: absolute; top: 0; left: 1.5rem; right: 1.5rem; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
}
.card-label {
    font-family: var(--fm); font-size: 0.68rem; font-weight: 500;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--text3); margin-bottom: 1.25rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.card-label .dot { width: 4px; height: 4px; background: var(--red); border-radius: 50%; }

/* ── SEC TITLE ── */
.sec-title {
    font-family: var(--fh); font-size: 1.3rem; font-weight: 700;
    color: var(--text); letter-spacing: -0.02em; margin-bottom: 0.4rem;
}
.sec-sub {
    font-family: var(--fm); font-size: 0.72rem;
    color: var(--text3); margin-bottom: 1.5rem; line-height: 1.6;
}

/* ── THRESHOLD INFO ── */
.threshold-info {
    background: rgba(255,149,0,0.06); border: 1px solid rgba(255,149,0,0.2);
    border-radius: var(--r-md); padding: 1.1rem 1.3rem; margin-bottom: 1.5rem;
    display: flex; gap: 1rem; align-items: flex-start;
}
.ti-icon { font-size: 1.2rem; flex-shrink: 0; margin-top: 1px; }
.ti-body { font-family: var(--fm); font-size: 0.72rem; color: var(--text2); line-height: 1.7; }
.ti-body strong { color: var(--orange); font-weight: 600; }
.ti-body .ti-val {
    font-family: var(--fh); font-size: 1.4rem; font-weight: 800; color: var(--orange);
    letter-spacing: -0.02em; display: block; margin: 0.3rem 0 0.1rem;
}

/* ── URL FETCH BOX ── */
.url-hint {
    background: rgba(0,207,255,0.05); border: 1px solid rgba(0,207,255,0.15);
    border-radius: var(--r-md); padding: 0.9rem 1.1rem;
    font-family: var(--fm); font-size: 0.7rem; color: var(--text2);
    line-height: 1.7; margin-bottom: 1.25rem;
    display: flex; gap: 0.75rem; align-items: flex-start;
}
.url-hint-icon { font-size: 1.1rem; flex-shrink: 0; }

.fetched-info {
    background: rgba(46,204,113,0.07); border: 1px solid rgba(46,204,113,0.2);
    border-radius: var(--r-md); padding: 1.1rem 1.3rem; margin-bottom: 1.25rem;
}
.fi-title {
    font-family: var(--fh); font-size: 0.9rem; font-weight: 700;
    color: var(--green); margin-bottom: 0.35rem;
}
.fi-meta {
    font-family: var(--fm); font-size: 0.68rem; color: var(--text3);
    line-height: 1.6; margin-bottom: 0.75rem;
}
.fi-stats {
    display: grid; grid-template-columns: repeat(4,1fr); gap: 0.6rem;
}
.fi-stat {
    background: var(--bg3); border: 1px solid var(--border);
    border-radius: var(--r-sm); padding: 0.7rem; text-align: center;
}
.fi-stat .fis-icon { font-size: 1rem; margin-bottom: 0.2rem; }
.fi-stat .fis-val {
    font-family: var(--fh); font-size: 1.1rem; font-weight: 700;
    color: var(--green); letter-spacing: -0.02em;
}
.fi-stat .fis-lbl {
    font-family: var(--fm); font-size: 0.58rem;
    letter-spacing: 0.1em; text-transform: uppercase; color: var(--text3);
}

.fetch-error {
    background: rgba(255,51,88,0.07); border: 1px solid rgba(255,51,88,0.25);
    border-radius: var(--r-md); padding: 1rem 1.2rem;
    font-family: var(--fm); font-size: 0.72rem; color: var(--red2); line-height: 1.7;
}
.fetch-error strong { color: var(--red); }

/* ── VALIDATION ERROR ── */
.val-error {
    background: rgba(255,51,88,0.08); border: 1px solid rgba(255,51,88,0.3);
    border-radius: var(--r-md); padding: 1.1rem 1.3rem; margin-top: 1rem;
}
.val-error .ve-title { font-family: var(--fh); font-size: 0.95rem; font-weight: 700; color: var(--red2); margin-bottom: 0.5rem; }
.val-error .ve-item {
    font-family: var(--fm); font-size: 0.72rem; color: var(--text2);
    line-height: 1.8; padding-left: 0.5rem;
    border-left: 2px solid rgba(255,51,88,0.3); margin-top: 0.3rem;
}

/* ── RESULT ── */
.result-viral {
    border-radius: var(--r-lg); border: 1.5px solid rgba(255,51,88,0.4);
    background: linear-gradient(140deg, rgba(255,51,88,0.12) 0%, rgba(255,112,144,0.05) 60%, rgba(0,207,255,0.03) 100%);
    padding: 2rem; animation: fadeUp 0.45s cubic-bezier(0.22,1,0.36,1) both; margin-bottom: 1.25rem;
}
.result-safe {
    border-radius: var(--r-lg); border: 1.5px solid rgba(150,150,200,0.2);
    background: linear-gradient(140deg, rgba(80,80,130,0.1) 0%, rgba(50,50,90,0.05) 100%);
    padding: 2rem; animation: fadeUp 0.45s cubic-bezier(0.22,1,0.36,1) both; margin-bottom: 1.25rem;
}
@keyframes fadeUp { from{opacity:0;transform:translateY(16px);} to{opacity:1;transform:translateY(0);} }
.result-head { display:flex; align-items:center; gap:1.1rem; margin-bottom:1.5rem; }
.res-icon { font-size:3rem; line-height:1; }
.res-title { font-family:var(--fh); font-size:2.2rem; font-weight:800; letter-spacing:-0.03em; line-height:1.1; }
.result-viral  .res-title { background:linear-gradient(120deg,var(--red),var(--red2)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.result-safe   .res-title { color:rgba(236,234,246,0.6); }
.res-sub { font-family:var(--fm); font-size:0.75rem; color:var(--text3); margin-top:0.3rem; line-height:1.5; }

/* ── METRICS GRID ── */
.m4-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:0.75rem; margin-bottom:1.25rem; }
.m-tile { background:var(--bg3); border:1px solid var(--border); border-radius:var(--r-md); padding:1rem 0.75rem; text-align:center; }
.m-tile .mi { font-size:1.3rem; margin-bottom:0.4rem; }
.m-tile .ml { font-family:var(--fm); font-size:0.65rem; letter-spacing:0.1em; text-transform:uppercase; color:var(--text3); margin-bottom:0.3rem; }
.m-tile .mv { font-family:var(--fh); font-size:1.3rem; font-weight:700; color:var(--text); letter-spacing:-0.02em; }

/* ── ER GAUGE ── */
.er-gauge { background:var(--bg3); border:1px solid var(--border); border-radius:var(--r-md); padding:1.3rem 1.5rem; margin-bottom:1rem; }
.er-row { display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:0.9rem; }
.er-left .erl-title { font-family:var(--fm); font-size:0.68rem; letter-spacing:0.12em; text-transform:uppercase; color:var(--text3); margin-bottom:0.15rem; }
.er-left .erl-sub { font-family:var(--fm); font-size:0.65rem; color:var(--text3); opacity:0.55; }
.er-num { font-family:var(--fh); font-size:2.6rem; font-weight:800; color:var(--text); letter-spacing:-0.04em; line-height:1; }
.er-num sub { font-size:1rem; font-weight:500; color:var(--text3); }
.er-track { background:rgba(255,255,255,0.06); border-radius:999px; height:6px; overflow:hidden; margin-bottom:0.6rem; }
.er-bar { height:100%; border-radius:999px; }
.er-track-wrap { position:relative; margin-bottom:0.6rem; }
.er-marker { position:absolute; top:-4px; width:2px; height:14px; background:rgba(255,255,255,0.35); border-radius:1px; }
.er-axis { display:flex; justify-content:space-between; font-family:var(--fm); font-size:0.62rem; color:var(--text3); }
.er-axis .axis-mid { color:var(--red2); font-weight:500; }

/* ── FORMULA BOX ── */
.fbox { background:rgba(0,207,255,0.04); border:1px solid rgba(0,207,255,0.12); border-radius:var(--r-md); padding:1.1rem 1.3rem; margin-top:0.75rem; }
.fbox-title { font-family:var(--fm); font-size:0.65rem; letter-spacing:0.12em; text-transform:uppercase; color:var(--cyan); margin-bottom:0.5rem; }
.fbox-body { font-family:var(--fm); font-size:0.75rem; color:var(--text2); line-height:1.9; }
.fbox-body strong { color:var(--text); font-weight:600; }
.fbox-body .verdict-ok { color:var(--green); font-weight:700; }
.fbox-body .verdict-no { color:var(--red2); font-weight:700; }

/* ── MODEL STRIP ── */
.model-strip {
    display:flex; align-items:center; gap:1.2rem;
    background:rgba(255,204,0,0.04); border:1px solid rgba(255,204,0,0.12);
    border-radius:var(--r-md); padding:1rem 1.3rem; margin-top:0.75rem;
}
.ms-icon { font-size:1.2rem; flex-shrink:0; }
.ms-label { font-family:var(--fm); font-size:0.7rem; color:var(--text3); line-height:1.6; flex:1; }
.ms-label strong { color:rgba(255,204,0,0.85); font-weight:600; }
.ms-metrics { display:flex; gap:1.5rem; }
.ms-m { text-align:center; }
.ms-m .msv { font-family:var(--fh); font-size:1.15rem; font-weight:700; color:var(--gold); letter-spacing:-0.02em; }
.ms-m .msl { font-family:var(--fm); font-size:0.58rem; letter-spacing:0.1em; text-transform:uppercase; color:var(--text3); }

/* ── WHAT-IF SECTION ── */
.whatif-box {
    background: linear-gradient(140deg, rgba(191,90,242,0.08) 0%, rgba(0,207,255,0.04) 100%);
    border: 1.5px solid rgba(191,90,242,0.25);
    border-radius: var(--r-lg);
    padding: 1.75rem;
    margin-top: 1.25rem;
    animation: fadeUp 0.5s cubic-bezier(0.22,1,0.36,1) both;
}
.wi-header {
    display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;
}
.wi-badge {
    background: rgba(191,90,242,0.15); border: 1px solid rgba(191,90,242,0.3);
    border-radius: 999px; padding: 0.3rem 0.85rem;
    font-family: var(--fm); font-size: 0.63rem;
    letter-spacing: 0.1em; text-transform: uppercase; color: var(--purple);
    flex-shrink: 0;
}
.wi-title { font-family: var(--fh); font-size: 1.1rem; font-weight: 700; color: var(--text); }
.wi-sub { font-family: var(--fm); font-size: 0.68rem; color: var(--text3); margin-top: 0.2rem; }

.wi-rows { display: flex; flex-direction: column; gap: 0.75rem; }
.wi-row {
    display: grid; grid-template-columns: 2rem 1fr auto;
    gap: 1rem; align-items: center;
    background: var(--bg3); border: 1px solid var(--border);
    border-radius: var(--r-md); padding: 1rem 1.2rem;
}
.wi-row.wi-done {
    border-color: rgba(46,204,113,0.3);
    background: rgba(46,204,113,0.05);
}
.wi-row.wi-focus {
    border-color: rgba(191,90,242,0.4);
    background: rgba(191,90,242,0.06);
}
.wi-icon { font-size: 1.2rem; text-align: center; }
.wi-info {}
.wi-metric { font-family: var(--fh); font-size: 0.88rem; font-weight: 700; color: var(--text); margin-bottom: 0.2rem; }
.wi-current { font-family: var(--fm); font-size: 0.65rem; color: var(--text3); }
.wi-action { text-align: right; }
.wi-need {
    font-family: var(--fh); font-size: 1rem; font-weight: 800;
    color: var(--purple); letter-spacing: -0.02em;
}
.wi-need.done { color: var(--green); }
.wi-need-lbl { font-family: var(--fm); font-size: 0.6rem; color: var(--text3); text-transform: uppercase; letter-spacing: 0.08em; }

.wi-summary {
    background: rgba(191,90,242,0.08); border: 1px solid rgba(191,90,242,0.2);
    border-radius: var(--r-md); padding: 1rem 1.2rem; margin-top: 1rem;
    font-family: var(--fm); font-size: 0.72rem; color: var(--text2); line-height: 1.8;
}
.wi-summary strong { color: var(--purple); font-weight: 600; }
.wi-summary .wi-best {
    font-family: var(--fh); font-size: 1rem; font-weight: 700;
    color: var(--purple); margin-top: 0.5rem; display: block;
}

/* ── GUIDE ── */
.guide-desc {
    font-family: var(--fm); font-size: 0.73rem; color: var(--text2);
    line-height: 1.75; margin-bottom: 1.5rem; padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border);
}
.guide-desc strong { color: var(--text); font-weight: 600; }
.g-header {
    display: grid; grid-template-columns: 2.5rem 1fr 110px 150px;
    gap: 1rem; padding: 0 1.2rem 0.6rem;
    font-family: var(--fm); font-size: 0.63rem;
    letter-spacing: 0.14em; text-transform: uppercase; color: var(--text3);
}
.g-header .right { text-align: center; }
.g-rows { display: flex; flex-direction: column; gap: 0.6rem; }
.g-row {
    display: grid; grid-template-columns: 2.5rem 1fr 110px 150px;
    gap: 1rem; align-items: center;
    background: var(--bg3); border: 1px solid var(--border);
    border-radius: var(--r-md); padding: 1.1rem 1.2rem;
    transition: border-color 0.2s; cursor: default;
}
.g-row:hover { border-color: var(--border2); }
.g-icon { font-size: 1.3rem; text-align: center; }
.g-name { font-family: var(--fh); font-size: 0.9rem; font-weight: 700; color: var(--text); margin-bottom: 0.25rem; }
.g-desc { font-family: var(--fm); font-size: 0.65rem; color: var(--text3); line-height: 1.55; }
.g-target { text-align: center; }
.g-val { font-family: var(--fh); font-size: 1rem; font-weight: 700; color: var(--green); letter-spacing: -0.01em; margin-bottom: 0.15rem; }
.g-unit { font-family: var(--fm); font-size: 0.6rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text3); }
.g-weight { text-align: center; }
.wbar-wrap { background: rgba(255,255,255,0.06); border-radius: 999px; height: 4px; overflow: hidden; margin-bottom: 0.35rem; }
.wbar { height: 100%; border-radius: 999px; }
.wlabel { font-family: var(--fm); font-size: 0.62rem; color: var(--text3); text-align: center; }

/* ── EXAMPLE CARD ── */
.ex-card {
    background: linear-gradient(140deg, rgba(46,204,113,0.07) 0%, rgba(0,207,255,0.03) 100%);
    border: 1px solid rgba(46,204,113,0.2); border-radius: var(--r-lg);
    padding: 1.5rem; margin-top: 1.5rem;
}
.ex-head { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.25rem; }
.ex-badge {
    background: rgba(46,204,113,0.15); border: 1px solid rgba(46,204,113,0.3);
    border-radius: 999px; padding: 0.3rem 0.85rem;
    font-family: var(--fm); font-size: 0.63rem;
    letter-spacing: 0.1em; text-transform: uppercase; color: var(--green); flex-shrink: 0;
}
.ex-title { font-family: var(--fh); font-size: 0.95rem; font-weight: 700; color: var(--text); }
.ex-title small { display: block; font-family: var(--fm); font-size: 0.63rem; color: var(--text3); font-weight: 400; margin-top: 0.2rem; }
.ex-stats { display: grid; grid-template-columns: repeat(5,1fr); gap: 0.6rem; margin-bottom: 1.25rem; }
.ex-s { background: var(--bg3); border: 1px solid var(--border); border-radius: var(--r-sm); padding: 0.8rem 0.5rem; text-align: center; }
.ex-s .esi { font-size: 1.1rem; margin-bottom: 0.25rem; }
.ex-s .esv { font-family: var(--fh); font-size: 1rem; font-weight: 700; color: var(--green); letter-spacing: -0.02em; }
.ex-s .esl { font-family: var(--fm); font-size: 0.58rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text3); }
.ex-result {
    display: flex; align-items: center; justify-content: space-between;
    background: rgba(46,204,113,0.06); border: 1px solid rgba(46,204,113,0.15);
    border-radius: var(--r-md); padding: 1rem 1.3rem;
}
.exr-val { font-family: var(--fh); font-size: 1.8rem; font-weight: 800; color: var(--green); letter-spacing: -0.03em; }
.exr-label { font-family: var(--fm); font-size: 0.63rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text3); }
.exr-calc { font-family: var(--fm); font-size: 0.65rem; color: var(--text3); text-align: center; line-height: 1.7; }
.exr-chip {
    display: flex; align-items: center; gap: 0.5rem;
    background: rgba(46,204,113,0.15); border: 1px solid rgba(46,204,113,0.3);
    border-radius: 999px; padding: 0.55rem 1.1rem;
    font-family: var(--fh); font-size: 0.82rem; font-weight: 700; color: var(--green);
}

/* ── FOOTER ── */
.footer {
    margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid var(--border);
    display: flex; justify-content: space-between; align-items: center;
}
.fl { font-family: var(--fm); font-size: 0.68rem; color: var(--text3); line-height: 1.8; }
.fr { font-family: var(--fm); font-size: 0.68rem; color: var(--text3); text-align: right; line-height: 1.8; }

/* ══════════════════════════════════════════
   FLOATING CHAT WIDGET
══════════════════════════════════════════ */
#fcw-btn {
    position: fixed;
    bottom: 28px; right: 28px;
    width: 58px; height: 58px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ff3358 0%, #bf5af2 100%);
    box-shadow: 0 4px 20px rgba(255,51,88,0.45), 0 0 0 0 rgba(255,51,88,0.3);
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    z-index: 9999;
    animation: fcw-pulse 2.5s ease-in-out infinite;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
#fcw-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 28px rgba(255,51,88,0.6);
}
#fcw-btn svg { width: 26px; height: 26px; fill: #fff; transition: opacity 0.2s; }
#fcw-btn .fcw-icon-open  { display: flex; }
#fcw-btn .fcw-icon-close { display: none; }
#fcw-btn.open .fcw-icon-open  { display: none; }
#fcw-btn.open .fcw-icon-close { display: flex; }

/* Badge thông báo */
#fcw-badge {
    position: absolute; top: -3px; right: -3px;
    width: 18px; height: 18px; border-radius: 50%;
    background: var(--gold); color: #000;
    font-family: var(--fm); font-size: 0.6rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    border: 2px solid var(--bg);
    animation: fcw-badge-pop 0.4s cubic-bezier(0.34,1.56,0.64,1) both;
}

@keyframes fcw-pulse {
    0%,100% { box-shadow: 0 4px 20px rgba(255,51,88,0.45), 0 0 0 0   rgba(255,51,88,0.3); }
    50%      { box-shadow: 0 4px 20px rgba(255,51,88,0.45), 0 0 0 10px rgba(255,51,88,0); }
}
@keyframes fcw-badge-pop {
    from { transform: scale(0); opacity: 0; }
    to   { transform: scale(1); opacity: 1; }
}

/* Panel popup */
#fcw-panel {
    position: fixed;
    bottom: 100px; right: 28px;
    width: 370px;
    max-height: 580px;
    background: #0e1018;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    box-shadow: 0 24px 60px rgba(0,0,0,0.7), 0 0 0 1px rgba(255,51,88,0.15);
    display: none;
    flex-direction: column;
    overflow: hidden;
    z-index: 9998;
    animation: fcw-slide-in 0.28s cubic-bezier(0.34,1.2,0.64,1) both;
}
#fcw-panel.open {
    display: flex;
}
@keyframes fcw-slide-in {
    from { opacity: 0; transform: translateY(16px) scale(0.96); }
    to   { opacity: 1; transform: translateY(0)   scale(1); }
}

/* Header panel */
#fcw-header {
    display: flex; align-items: center; gap: 0.7rem;
    padding: 1rem 1.1rem;
    background: linear-gradient(135deg, rgba(255,51,88,0.15) 0%, rgba(191,90,242,0.10) 100%);
    border-bottom: 1px solid rgba(255,255,255,0.08);
    flex-shrink: 0;
}
.fcw-avatar {
    width: 36px; height: 36px; border-radius: 50%;
    background: linear-gradient(135deg,#ff3358,#bf5af2);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}
.fcw-hinfo { flex: 1; }
.fcw-hname { font-family: var(--fh); font-size: 0.88rem; font-weight: 700; color: #eceaf6; }
.fcw-hsub  { font-family: var(--fm); font-size: 0.62rem; color: rgba(236,234,246,0.5); margin-top: 1px; }
.fcw-hdot  { width: 8px; height: 8px; border-radius: 50%; background: #2ecc71;
             box-shadow: 0 0 6px rgba(46,204,113,0.7); flex-shrink: 0; }

/* Messages area */
#fcw-msgs {
    flex: 1; overflow-y: auto; padding: 1rem;
    display: flex; flex-direction: column; gap: 0.65rem;
    scroll-behavior: smooth;
}
#fcw-msgs::-webkit-scrollbar { width: 3px; }
#fcw-msgs::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 2px; }

.fcw-msg { display: flex; gap: 0.5rem; align-items: flex-end; }
.fcw-msg.bot  { flex-direction: row; }
.fcw-msg.user { flex-direction: row-reverse; }

.fcw-av-sm {
    width: 24px; height: 24px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg,#ff3358,#bf5af2);
    display: flex; align-items: center; justify-content: center; font-size: 0.7rem;
}

.fcw-bubble {
    max-width: 82%; padding: 0.6rem 0.85rem;
    font-family: var(--fh); font-size: 0.82rem; line-height: 1.6;
    word-break: break-word; border-radius: 14px;
}
.fcw-bubble.bot {
    background: #13151f; border: 1px solid rgba(255,255,255,0.08);
    color: #eceaf6; border-bottom-left-radius: 4px;
}
.fcw-bubble.user {
    background: linear-gradient(135deg,rgba(255,51,88,0.2),rgba(191,90,242,0.15));
    border: 1px solid rgba(255,51,88,0.2);
    color: #eceaf6; border-bottom-right-radius: 4px;
}
.fcw-bubble strong { color: #fff; font-weight: 700; }
.fcw-bubble code {
    background: rgba(0,207,255,0.12); color: #00cfff;
    padding: 0.1rem 0.3rem; border-radius: 3px;
    font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;
}

/* Typing indicator */
.fcw-typing { display: flex; align-items: center; gap: 5px; padding: 0.5rem 0.75rem; }
.fcw-dot { width: 6px; height: 6px; border-radius: 50%; background: rgba(236,234,246,0.4);
    animation: fcw-bounce 1.2s ease-in-out infinite; }
.fcw-dot:nth-child(2) { animation-delay: 0.2s; }
.fcw-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes fcw-bounce {
    0%,60%,100% { transform: translateY(0);    opacity: 0.4; }
    30%          { transform: translateY(-5px); opacity: 1;   }
}

/* Quick chips */
#fcw-chips {
    padding: 0.5rem 0.85rem 0;
    display: flex; flex-wrap: wrap; gap: 0.4rem;
}
.fcw-chip {
    font-family: var(--fh); font-size: 0.71rem;
    padding: 0.3rem 0.65rem; border-radius: 20px; cursor: pointer;
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
    color: rgba(236,234,246,0.8);
    transition: all 0.18s ease; white-space: nowrap;
}
.fcw-chip:hover {
    background: rgba(255,51,88,0.12); border-color: rgba(255,51,88,0.35);
    color: #eceaf6;
}

/* Input area */
#fcw-input-row {
    display: flex; gap: 0.5rem; align-items: center;
    padding: 0.75rem 0.85rem;
    border-top: 1px solid rgba(255,255,255,0.07);
    flex-shrink: 0;
}
#fcw-input {
    flex: 1; background: #1a1c28; border: 1px solid rgba(255,255,255,0.1);
    border-radius: 22px; padding: 0.55rem 1rem;
    font-family: var(--fh); font-size: 0.82rem; color: #eceaf6;
    outline: none; transition: border-color 0.2s;
    -webkit-text-fill-color: #eceaf6;
}
#fcw-input::placeholder { color: rgba(236,234,246,0.35); -webkit-text-fill-color: rgba(236,234,246,0.35); }
#fcw-input:focus { border-color: rgba(255,51,88,0.45); }
#fcw-send {
    width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg,#ff3358,#bf5af2);
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: transform 0.18s ease, opacity 0.18s;
}
#fcw-send:hover { transform: scale(1.08); }
#fcw-send:disabled { opacity: 0.4; cursor: not-allowed; }
#fcw-send svg { width: 16px; height: 16px; fill: #fff; }

/* Powered by footer */
#fcw-powered {
    padding: 0.35rem 1rem 0.55rem;
    text-align: center;
    font-family: var(--fm); font-size: 0.58rem;
    color: rgba(236,234,246,0.25);
    flex-shrink: 0;
}

/* ── CHATBOT ── */
.chat-status {
    display: flex; align-items: center; gap: 0.6rem;
    background: var(--bg3); border: 1px solid var(--border);
    border-radius: var(--r-md); padding: 0.75rem 1.1rem;
    margin-bottom: 1.25rem;
}
.chat-status-dot {
    width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
}
.chat-status-dot.online  { background: var(--green); box-shadow: 0 0 6px rgba(46,204,113,0.6); animation: blink 2s ease-in-out infinite; }
.chat-status-dot.offline { background: var(--red2); }
.chat-status-dot.loading { background: var(--orange); animation: blink 0.8s ease-in-out infinite; }
.chat-status-text { font-family: var(--fm); font-size: 0.72rem; color: var(--text2); }
.chat-status-text strong { color: var(--text); }

.chat-window {
    background: var(--bg2); border: 1px solid var(--border);
    border-radius: var(--r-lg); padding: 1.25rem;
    min-height: 320px; max-height: 520px;
    overflow-y: auto; margin-bottom: 1rem;
    display: flex; flex-direction: column; gap: 0.75rem;
    scroll-behavior: smooth;
}
.chat-window::-webkit-scrollbar { width: 4px; }
.chat-window::-webkit-scrollbar-track { background: transparent; }
.chat-window::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

.msg-row { display: flex; gap: 0.6rem; align-items: flex-end; animation: fadeUp 0.3s ease both; }
.msg-row.user  { flex-direction: row-reverse; }
.msg-row.bot   { flex-direction: row; }

.msg-avatar {
    width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; line-height: 1;
}
.msg-avatar.bot-av  { background: linear-gradient(135deg,#1F4E79,#2E75B6); }
.msg-avatar.user-av { background: linear-gradient(135deg,#ff3358,#ff7090); }

.msg-bubble {
    max-width: 78%; padding: 0.75rem 1rem;
    border-radius: 16px; font-family: var(--fh);
    font-size: 0.875rem; line-height: 1.65; word-break: break-word;
}
.msg-bubble.bot {
    background: var(--bg3); border: 1px solid var(--border);
    color: var(--text); border-bottom-left-radius: 4px;
}
.msg-bubble.user {
    background: linear-gradient(135deg,rgba(255,51,88,0.18),rgba(255,112,144,0.1));
    border: 1px solid rgba(255,51,88,0.25);
    color: var(--text); border-bottom-right-radius: 4px;
}
.msg-bubble.bot  code { background: rgba(0,207,255,0.1); color: var(--cyan); padding: 0.1rem 0.35rem; border-radius: 4px; font-family: var(--fm); font-size: 0.8rem; }
.msg-bubble.bot  strong { color: var(--text); font-weight: 700; }
.msg-time { font-family: var(--fm); font-size: 0.58rem; color: var(--text3); margin-top: 0.2rem; text-align: right; }

.typing-bubble {
    background: var(--bg3); border: 1px solid var(--border);
    border-radius: 16px; border-bottom-left-radius: 4px;
    padding: 0.75rem 1rem; display: inline-flex; gap: 5px; align-items: center;
}
.typing-dot {
    width: 7px; height: 7px; border-radius: 50%; background: var(--text3);
    animation: typing-bounce 1.2s ease-in-out infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing-bounce { 0%,60%,100%{transform:translateY(0);opacity:0.4;} 30%{transform:translateY(-5px);opacity:1;} }

.quick-btns {
    display: flex; flex-wrap: wrap; gap: 0.5rem;
    margin-bottom: 1rem;
}
.quick-btn-label { font-family: var(--fm); font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text3); margin-bottom: 0.5rem; }

.chat-input-row { display: flex; gap: 0.6rem; align-items: flex-end; }
div[data-testid="stTextInput"].chat-input-wrap input {
    font-size: 0.9rem !important;
}

.ollama-setup {
    background: rgba(255,149,0,0.06); border: 1px solid rgba(255,149,0,0.25);
    border-radius: var(--r-lg); padding: 1.5rem 1.75rem; margin-bottom: 1.25rem;
}
.setup-title { font-family: var(--fh); font-size: 1.05rem; font-weight: 700; color: var(--orange); margin-bottom: 1rem; }
.setup-step {
    display: flex; gap: 0.85rem; align-items: flex-start; margin-bottom: 0.9rem;
}
.setup-num {
    width: 24px; height: 24px; border-radius: 50%; flex-shrink: 0;
    background: rgba(255,149,0,0.2); border: 1px solid rgba(255,149,0,0.4);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--fm); font-size: 0.72rem; color: var(--orange); font-weight: 700;
}
.setup-text { font-family: var(--fm); font-size: 0.75rem; color: var(--text2); line-height: 1.7; }
.setup-text code { background: rgba(255,255,255,0.08); color: var(--cyan); padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.78rem; }
.setup-text strong { color: var(--text); }
</style>
""", unsafe_allow_html=True)


# ─── Load Config ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_config():
    path = os.path.join(os.path.dirname(__file__), "model_config.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"p80_threshold": 6.0, "metrics": {}}

config  = load_config()
P80     = config.get("p80_threshold", 6.0)
metrics = config.get("metrics", {})

# Đọc API key từ secrets hoặc config
RAPIDAPI_KEY = config.get("rapidapi_key", "")


# ─── Helpers ──────────────────────────────────────────────────────────────────
def calc_er(views, likes, comments, shares):
    if views <= 0: return 0.0
    return ((likes * 1.0) + (comments * 1.5) + (shares * 2.0)) / views * 100.0

def fmt(n):
    if n >= 1_000_000: return f"{n/1_000_000:.2f}M"
    if n >= 1_000:     return f"{n/1_000:.1f}K"
    return f"{n:,}"

def validate(views, likes, comments, shares):
    errors = []
    if views <= 0:
        errors.append("Lượt xem phải lớn hơn 0")
    if views > 0 and views < 1000:
        errors.append(f"Lượt xem quá thấp ({views:,}) — cần ít nhất 1,000 views để phân tích có ý nghĩa thống kê")
    if views > 0 and likes > views:
        errors.append(f"Lượt thích ({fmt(likes)}) không thể lớn hơn lượt xem ({fmt(views)})")
    if views > 0 and comments > views:
        errors.append(f"Bình luận ({fmt(comments)}) không thể lớn hơn lượt xem ({fmt(views)})")
    if views > 0 and shares > views:
        errors.append(f"Lượt chia sẻ ({fmt(shares)}) không thể lớn hơn lượt xem ({fmt(views)})")
    if views > 0 and (likes + comments + shares) == 0:
        errors.append("Video có 0 tương tác — không thể phân tích")
    return errors


# ─── TikTok Fetch ─────────────────────────────────────────────────────────────
# Dùng tikwm.com API trực tiếp — miễn phí, không cần API key, không giới hạn quota
# Tài liệu: https://www.tikwm.com/  |  Endpoint: POST https://www.tikwm.com/api/

def is_tiktok_url(url: str) -> bool:
    return bool(re.search(r'(tiktok\.com|vm\.tiktok\.com|vt\.tiktok\.com)', url, re.I))

def fetch_tiktok_stats(url: str, api_key: str = ""):
    """
    Lấy thông số video từ tikwm.com API (miễn phí, không cần key).
    - Dùng POST request với form data {'url': ..., 'hd': '0'}
    - tikwm là backend thực của tiktok-scraper7 trên RapidAPI
    - Không giới hạn quota, không cần đăng ký
    """
    # Bước 1: clean URL — xóa query params thừa
    clean_url = url.strip().split('?')[0].rstrip('/')

    # Bước 2: resolve short link vm/vt.tiktok.com nếu cần
    if 'vm.tiktok.com' in clean_url or 'vt.tiktok.com' in clean_url:
        try:
            r = requests.head(clean_url, allow_redirects=True, timeout=10,
                              headers={'User-Agent': 'Mozilla/5.0'})
            clean_url = r.url.split('?')[0].rstrip('/')
        except Exception:
            pass  # tiếp tục với url gốc nếu resolve thất bại

    # Bước 3: gọi tikwm API bằng POST (KHÔNG dùng GET — form data mới đúng)
    endpoint = "https://www.tikwm.com/api/"
    headers  = {
        "User-Agent":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer":      "https://www.tikwm.com/",
    }
    payload = {"url": clean_url, "hd": "0"}

    resp = requests.post(endpoint, data=payload, headers=headers, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    # code = 0 là thành công
    if data.get("code") != 0:
        msg = data.get("msg") or data.get("message") or "Lỗi không xác định"
        if "private" in msg.lower():
            raise ValueError("Video này đang để chế độ Private — không thể lấy dữ liệu")
        if "deleted" in msg.lower() or "removed" in msg.lower():
            raise ValueError("Video đã bị xóa hoặc không tồn tại")
        raise ValueError(f"API lỗi: {msg}")

    video = data.get("data", {})

    def safe_int(val):
        try: return int(val or 0)
        except: return 0

    # tikwm trả về trực tiếp trong data (không lồng trong 'statistics')
    views    = safe_int(video.get("play_count")    or video.get("playCount"))
    likes    = safe_int(video.get("digg_count")    or video.get("diggCount"))
    comments = safe_int(video.get("comment_count") or video.get("commentCount"))
    shares   = safe_int(video.get("share_count")   or video.get("shareCount"))

    author_info = video.get("author") or {}
    if isinstance(author_info, dict):
        author = author_info.get("nickname") or author_info.get("uniqueId") or "Unknown"
    else:
        author = str(author_info) or "Unknown"

    raw_title = video.get("title") or video.get("desc") or ""
    title = raw_title[:80] + ("..." if len(raw_title) > 80 else "")

    if views == 0:
        raise ValueError(
            "Video trả về 0 lượt xem — có thể video bị private hoặc đã xóa.\n"
            "Thử dùng link đầy đủ từ trình duyệt máy tính."
        )

    return {
        "views":    views,
        "likes":    likes,
        "comments": comments,
        "shares":   shares,
        "title":    title or "Video TikTok",
        "author":   author,
    }


# ─── What-If Engine ───────────────────────────────────────────────────────────
def whatif_suggestions(views, likes, comments, shares, p80, er):
    """
    Tính toán cụ thể bạn cần tăng thêm bao nhiêu ở mỗi chỉ số để đạt viral.
    Trả về list gợi ý, sắp xếp theo chi phí tăng ít nhất trước.
    """
    if er >= p80:
        return []  # Đã viral rồi

    # Weighted cần đạt = p80/100 * views
    weighted_target = (p80 / 100.0) * views
    weighted_now    = (likes * 1.0) + (comments * 1.5) + (shares * 2.0)
    delta_needed    = weighted_target - weighted_now  # lượng weighted cần thêm

    suggestions = []

    # Cách 1: Chỉ tăng Shares (hiệu quả nhất vì ×2)
    need_shares = delta_needed / 2.0
    suggestions.append({
        "icon":    "🔁",
        "metric":  "Lượt Chia sẻ",
        "current": shares,
        "need":    int(need_shares) + 1,
        "target":  shares + int(need_shares) + 1,
        "weight":  "×2.0",
        "er_new":  calc_er(views, likes, comments, shares + int(need_shares) + 1),
        "label":   f"Tăng thêm {fmt(int(need_shares)+1)} shares",
        "effort":  need_shares,  # dùng để sort
    })

    # Cách 2: Chỉ tăng Comments (×1.5)
    need_comments = delta_needed / 1.5
    suggestions.append({
        "icon":    "💬",
        "metric":  "Bình Luận",
        "current": comments,
        "need":    int(need_comments) + 1,
        "target":  comments + int(need_comments) + 1,
        "weight":  "×1.5",
        "er_new":  calc_er(views, likes, comments + int(need_comments) + 1, shares),
        "label":   f"Tăng thêm {fmt(int(need_comments)+1)} comments",
        "effort":  need_comments,
    })

    # Cách 3: Chỉ tăng Likes (×1.0)
    need_likes = delta_needed / 1.0
    suggestions.append({
        "icon":    "❤️",
        "metric":  "Lượt Thích",
        "current": likes,
        "need":    int(need_likes) + 1,
        "target":  likes + int(need_likes) + 1,
        "weight":  "×1.0",
        "er_new":  calc_er(views, likes + int(need_likes) + 1, comments, shares),
        "label":   f"Tăng thêm {fmt(int(need_likes)+1)} likes",
        "effort":  need_likes,
    })

    # Cách 4: Kết hợp tối ưu — tăng đều cả 3 theo tỉ lệ trọng số
    # Phân bổ delta theo tỉ lệ 2:1.5:1 → shares:comments:likes = 4:3:2
    total_weight = 4 + 3 + 2
    combo_shares   = int(delta_needed * 4 / total_weight / 2.0) + 1
    combo_comments = int(delta_needed * 3 / total_weight / 1.5) + 1
    combo_likes    = int(delta_needed * 2 / total_weight / 1.0) + 1
    suggestions.append({
        "icon":    "⚡",
        "metric":  "Kết hợp cả 3",
        "current": None,
        "need":    None,
        "target":  None,
        "weight":  "Tối ưu",
        "er_new":  calc_er(views, likes + combo_likes, comments + combo_comments, shares + combo_shares),
        "label":   f"+{fmt(combo_shares)} shares · +{fmt(combo_comments)} comments · +{fmt(combo_likes)} likes",
        "effort":  (combo_shares + combo_comments + combo_likes),
        "combo":   True,
        "combo_shares":   combo_shares,
        "combo_comments": combo_comments,
        "combo_likes":    combo_likes,
    })

    # Sort: phương án dễ nhất (effort thấp nhất) lên trên
    suggestions.sort(key=lambda x: x["effort"])
    return suggestions



# ─── RAG Chatbot Engine ────────────────────────────────────────────────────────
OLLAMA_MODEL    = "qwen2.5:3b"
OLLAMA_ENDPOINT = "http://localhost:11434/api/chat"

# ── Knowledge Base — toàn bộ tri thức dự án, chia thành chunks nhỏ ──────────
KB_CHUNKS = [
    {
        "id": "app_overview",
        "tags": ["app", "tổng quan", "giới thiệu", "là gì", "gồm gì", "tính năng"],
        "content": """Tên ứng dụng: TikTok Viral Detector.
Mục tiêu: Dự đoán khả năng viral của video TikTok dựa trên số liệu tương tác.
Công nghệ: Streamlit (giao diện web) + Random Forest (mô hình AI) + tikwm.com (lấy dữ liệu TikTok).
Dataset huấn luyện: 10.000.000 video TikTok thực tế từ HuggingFace.
App có 3 tab: Tab 1 phân tích từ link, Tab 2 nhập thủ công, Tab 3 trợ lý AI RAG."""
    },
    {
        "id": "weighted_er_formula",
        "tags": ["er", "weighted er", "công thức", "tính", "engagement rate", "trọng số"],
        "content": f"""Công thức Weighted Engagement Rate (Weighted ER):
Weighted ER = (Likes × 1 + Comments × 1.5 + Shares × 2) / Views × 100

Lý do trọng số khác nhau:
- Shares (×2.0): tín hiệu lan truyền mạnh nhất, đưa video ra ngoài vòng follower, TikTok algorithm ưu tiên cao nhất.
- Comments (×1.5): phản ánh mức độ kích thích cảm xúc, người dùng dừng lại tương tác — giá trị hơn like đơn thuần.
- Likes (×1.0): tín hiệu cơ bản nhất, dễ bấm nhất nên trọng số thấp nhất.
- Views không cộng vào weighted vì là mẫu số — nhiều views mà ít tương tác = ER thấp.

Ví dụ tính toán thực tế:
Video: 1.000.000 views, 6.500 likes, 3.300 comments, 104 shares
Weighted = (6.500×1) + (3.300×1.5) + (104×2) = 6.500 + 4.950 + 208 = 11.658
ER = 11.658 / 1.000.000 × 100 = 1,1658%
Kết luận: 1,1658% < {P80:.2f}% → Chưa Viral"""
    },
    {
        "id": "viral_threshold",
        "tags": ["p80", "ngưỡng", "viral", "threshold", "phân vị", "top 20", "bao nhiêu"],
        "content": f"""Ngưỡng Viral được tính từ dữ liệu 10 triệu video thực tế:
Ngưỡng P80 = {P80:.4f}%

Ý nghĩa P80:
- P80 = phân vị thứ 80 → chỉ 20% video hàng đầu đạt mức này.
- Video có ER >= {P80:.2f}% → VIRAL (top 20% toàn dataset).
- Video có ER <  {P80:.2f}% → Chưa Viral (thuộc nhóm 80% còn lại).
- P80 được tính bằng Apache Spark trên toàn bộ 10M video, lưu trong model_config.json.
- Ngưỡng này cố định, không thay đổi theo từng video."""
    },
    {
        "id": "tab1_link_analysis",
        "tags": ["tab 1", "link", "dán link", "url", "fetch", "lấy dữ liệu", "tikwm", "phân tích link"],
        "content": """Tab 1 — Phân tích từ Link TikTok:
Cách dùng: Dán link video → bấm nút "LẤY SỐ LIỆU & PHÂN TÍCH" → xem kết quả.

Hỗ trợ 3 dạng link:
- https://www.tiktok.com/@username/video/1234567890 (link đầy đủ từ trình duyệt)
- https://vm.tiktok.com/XXXXXXX/ (link rút gọn)
- https://vt.tiktok.com/XXXXXXX/ (link share từ app điện thoại)

Quy trình xử lý tự động:
1. Validate link — kiểm tra có chứa domain TikTok không.
2. Resolve short link — vm/vt.tiktok.com sẽ được theo redirect để lấy link thật.
3. Clean URL — xóa query params thừa (?is_copy_link=1...).
4. Gọi tikwm.com API (POST /api/) — miễn phí, không cần API key, không giới hạn quota.
5. Parse response — lấy views, likes, comments, shares, author, title.
6. Tính Weighted ER → so sánh P80 → hiển thị kết quả.

Kết quả hiển thị: banner (VIRAL/Chưa Viral) + 4 ô số liệu + thanh ER gauge + công thức chi tiết."""
    },
    {
        "id": "tab2_manual_input",
        "tags": ["tab 2", "nhập thủ công", "manual", "nhập tay", "số liệu"],
        "content": """Tab 2 — Nhập thủ công:
Cách dùng: Nhập 4 số liệu vào 4 ô → bấm "PHÂN TÍCH NGAY".

4 trường nhập liệu:
- Views (Lượt xem): tối thiểu 1.000 — bắt buộc > 0.
- Likes (Lượt thích): phải <= Views.
- Comments (Bình luận): phải <= Views.
- Shares (Lượt chia sẻ): phải <= Views.

Validation tự động:
- Báo lỗi nếu views < 1.000 (không đủ để phân tích có ý nghĩa thống kê).
- Báo lỗi nếu likes/comments/shares > views (không thể xảy ra thực tế).
- Báo lỗi nếu tổng tương tác = 0.

Dùng tab này khi: không có link, hoặc muốn thử với số liệu giả định."""
    },
    {
        "id": "whatif_engine",
        "tags": ["gợi ý", "cải thiện", "what-if", "tăng er", "cần thêm", "bao nhiêu shares", "phương án"],
        "content": f"""Tính năng Gợi ý cải thiện (What-If Engine):
Tự động xuất hiện khi video Chưa Viral (ER < P80).
Tính chính xác cần tăng thêm bao nhiêu tương tác để đạt ngưỡng viral.

Công thức cốt lõi:
delta_needed = (P80/100 × views) - weighted_hiện_tại
→ Đây là lượng "điểm tương tác có trọng số" còn thiếu.

4 phương án được đề xuất (sắp xếp từ dễ nhất):
1. ★ Chỉ tăng Shares: need = delta_needed / 2.0 — ít nhất vì trọng số ×2.
2. Chỉ tăng Comments: need = delta_needed / 1.5 — cần nhiều hơn Shares.
3. Chỉ tăng Likes: need = delta_needed / 1.0 — tốn nhất vì trọng số thấp nhất.
4. Kết hợp cả 3 (tỉ lệ 4:3:2): phân bổ đều theo trọng số, thực tế nhất.

Ví dụ: Video 1M views, ER = 1,1658%, thiếu 12,13% để viral:
- Chỉ shares: cần thêm ~60.659 shares
- Chỉ comments: cần thêm ~80.878 comments
- Chỉ likes: cần thêm ~121.317 likes
- Combo: +26.965 shares + ~26.965 comments + ~26.965 likes"""
    },
    {
        "id": "random_forest_model",
        "tags": ["random forest", "mô hình", "model", "ai", "thuật toán", "machine learning", "auc", "accuracy", "f1"],
        "content": """Mô hình Random Forest Classifier:
Thư viện: scikit-learn
Số cây: n_estimators=100
Độ sâu tối đa: max_depth=15
Lá tối thiểu: min_samples_leaf=100
Features tại mỗi nút: max_features='sqrt' (√16 ≈ 4 features)
Xử lý mất cân bằng: class_weight='balanced' (80% Non-Viral vs 20% Viral)
Tái tạo kết quả: random_state=42

Kết quả đánh giá trên tập test 1.997.108 bản ghi:
- AUC-ROC: 0.9964 (Xuất sắc — thang 0.90-1.00)
- Accuracy: 95.41%
- F1-Score: 95.57%
- Precision: 96.16%
- Recall: 95.41%

Tại sao chọn Random Forest:
- Kháng overfitting tốt hơn Decision Tree đơn lẻ.
- Xử lý được tương tác phi tuyến giữa các features.
- Cung cấp feature importance để giải thích kết quả."""
    },
    {
        "id": "data_preprocessing",
        "tags": ["tiền xử lý", "dữ liệu", "spark", "pyspark", "làm sạch", "feature", "16 features"],
        "content": """Tiền xử lý dữ liệu bằng Apache Spark (PySpark):
Dataset gốc: 10.000.000 video, 56 cột → sau xử lý: 9.985.538 bản ghi, 16 features.
Chỉ 0.14% dữ liệu bị loại (14.462 bản ghi không hợp lệ).

4 bước làm sạch chính:
1. Cast kiểu dữ liệu: LongType, DoubleType, IntegerType.
2. Filter: play_count > 0, các cột không âm, loại duplicate.
3. IQR Capping P1-P99: giới hạn outlier cực đoan.
4. Tạo time features: post_hour, post_dow, is_weekend, is_peak_hour.

16 features cuối cùng:
log_play_count, log_digg_count, log_comment_count, log_share_count, log_collect_count,
duration, vq_score, user_verified, music_original, duet_enabled, stitch_enabled, is_ad,
post_hour, post_dow, is_weekend, is_peak_hour.

Lưu ý: Các cột engagement_rate, weighted_engagement bị loại để tránh data leakage."""
    },
    {
        "id": "train_test_split",
        "tags": ["train test", "phân chia", "80/20", "tập train", "tập test", "stratify"],
        "content": """Phân chia dữ liệu Train/Test:
Tỉ lệ: 80% train / 20% test (stratify=y — giữ nguyên tỉ lệ Viral/Non-Viral).
random_state=42 đảm bảo tái tạo kết quả.

Số bản ghi:
- Tổng: 9.985.538
- Train: 7.988.430 (80%)
- Test: 1.997.108 (20%)
- Viral trong train: ~1.597.686 (20% of train)
- Viral trong test:  ~399.422 (20% of test)

Tham số stratify=y quan trọng vì dataset mất cân bằng (20% Viral / 80% Non-Viral)."""
    },
    {
        "id": "model_comparison",
        "tags": ["so sánh", "decision tree", "logistic regression", "so với", "tốt hơn", "tại sao chọn"],
        "content": """So sánh 3 mô hình trên cùng tập test:

Random Forest (được chọn):
- AUC: 0.9964, Accuracy: 95.41%, F1: 95.57%

Decision Tree:
- AUC: 0.9312, Accuracy: 90.89%, F1: 91.03%
- Kém hơn RF: AUC -6.52pp, Accuracy -4.52pp

Logistic Regression:
- AUC: 0.8124, Accuracy: 78.43%, F1: 77.98%
- Kém hơn RF rất nhiều: AUC -18.40pp, vì không xử lý được tương tác phi tuyến.

Lý do chọn Random Forest:
1. Hiệu suất vượt trội trên mọi chỉ số.
2. Kháng overfitting nhờ Bootstrap Sampling + Feature Randomness (100 cây đa dạng).
3. Xử lý phi tuyến tự động — phù hợp data TikTok có nhiều tương tác phức tạp.
4. Cung cấp feature importance để giải thích.
5. Tương thích hoàn toàn với scikit-learn + Streamlit, predict < 1ms/video."""
    },
    {
        "id": "ollama_rag_setup",
        "tags": ["ollama", "cài đặt", "setup", "chạy", "offline", "rag", "chatbot", "trợ lý"],
        "content": f"""Chatbot RAG (Retrieval-Augmented Generation) trong app:
Công nghệ: Ollama (chạy LLM local) + ChromaDB (vector database) + sentence-transformers (embedding).
Model LLM: {OLLAMA_MODEL} — chạy hoàn toàn offline trên máy tính, không cần internet.
Ngôn ngữ: Tiếng Việt.

Cách hoạt động RAG:
1. Câu hỏi của bạn được chuyển thành vector embedding.
2. Tìm kiếm trong ChromaDB để lấy đúng chunks kiến thức liên quan.
3. Ghép chunks đó vào prompt → gửi cho Ollama.
4. Ollama trả lời dựa trên kiến thức được cung cấp — không bịa thêm.
5. Nếu câu hỏi ngoài phạm vi dự án → từ chối lịch sự.

Cài đặt (1 lần):
1. Tải Ollama tại ollama.com/download → cài như phần mềm thường.
2. Mở CMD: ollama pull {OLLAMA_MODEL}
3. Mở CMD: ollama serve
4. Refresh lại trang Streamlit → chatbot sẵn sàng."""
    },
    {
        "id": "viral_criteria",
        "tags": ["tiêu chí", "yếu tố", "peak hour", "giờ vàng", "âm nhạc", "watch time", "nội dung"],
        "content": """6 yếu tố ảnh hưởng đến khả năng viral TikTok:
1. Shares (×2.0): Yếu tố lan truyền mạnh nhất. Mục tiêu: ≥ 2-5% share/view.
2. Comments (×1.5): Phản ánh kích thích cảm xúc. Mục tiêu: ≥ 1-3% comment/view.
3. Likes (×1.0): Tín hiệu nền tảng. Mục tiêu: ≥ 5-10% like/view.
4. Watch Time: Tỉ lệ xem hết video. Mục tiêu: ≥ 70%. Video 15-30s dễ đạt hơn.
5. Âm nhạc trending: Dùng sound trending trong Top 100 giúp TikTok push lên FYP.
6. Thời điểm đăng (Peak Hours): 7-9h sáng, 12-14h trưa, 19-23h tối.
   2 giờ đầu sau đăng quyết định algorithm có push tiếp hay không."""
    },
]

# ── Từ khóa ngoài phạm vi — từ chối trả lời ──────────────────────────────
OUT_OF_SCOPE_KEYWORDS = [
    # Anime / manga / game / phim
    "naruto", "anime", "manga", "one piece", "dragon ball", "genshin",
    "pokemon", "minecraft", "valorant", "liên quân", "lol", "game",
    "phim", "series", "netflix", "youtube", "twitch",
    # Thời tiết / địa lý
    "thời tiết", "nhiệt độ", "mưa", "nắng", "bão", "lũ",
    "địa lý", "thủ đô", "quốc gia", "dân số",
    # Ẩm thực
    "nấu ăn", "công thức nấu", "món ăn", "ẩm thực", "restaurant",
    "bánh", "phở", "bún", "cơm", "nước uống",
    # Thể thao
    "bóng đá", "bóng rổ", "tennis", "cầu lông", "olympic",
    "world cup", "champions league", "ngoại hạng anh",
    # Chính trị / kinh tế / xã hội
    "chính trị", "bầu cử", "tổng thống", "thủ tướng",
    "kinh tế", "gdp", "lạm phát", "chứng khoán",
    "crypto", "bitcoin", "ethereum", "nft", "coin",
    # Y tế / sức khỏe
    "sức khỏe", "bệnh", "thuốc", "y tế", "bác sĩ",
    "covid", "vaccine", "ung thư", "đau đầu",
    # Tình cảm / xã hội
    "tình yêu", "hẹn hò", "crush", "người yêu", "chia tay",
    "bạn bè", "gia đình", "tâm sự",
    # Khoa học khác
    "toán học", "vật lý", "hóa học", "sinh học",
    "lịch sử", "triết học", "tôn giáo",
    # Lập trình ngoài phạm vi
    "java", "c++", "php", "ruby", "swift", "kotlin",
    "react", "angular", "vue", "nodejs", "spring boot",
    "blockchain", "devops", "docker", "kubernetes",
    # Sáng tác
    "làm thơ", "viết văn", "viết truyện", "dịch thuật",
    "vẽ tranh", "âm nhạc", "ca sĩ", "diễn viên",
    # Nhân vật / người nổi tiếng không liên quan
    "là ai", "sinh năm", "tiểu sử", "profile",
]

# ── Từ khóa BẮT BUỘC phải có trong câu hỏi liên quan dự án ──────────────
IN_SCOPE_KEYWORDS = [
    # Core project terms
    "tiktok", "viral", "er", "engagement", "weighted",
    "p80", "ngưỡng", "threshold",
    # Features
    "app", "ứng dụng", "tab", "link", "phân tích", "nhập",
    "fetch", "tikwm", "kết quả", "cách dùng", "hướng dẫn",
    # ML/AI
    "random forest", "mô hình", "model", "auc", "accuracy",
    "f1", "precision", "recall", "machine learning", "ai",
    "scikit", "sklearn", "predict", "dự đoán",
    # Data
    "pyspark", "spark", "dataset", "dữ liệu", "feature",
    "train", "test", "huấn luyện", "tiền xử lý",
    # Metrics
    "views", "likes", "comments", "shares", "lượt xem",
    "lượt thích", "bình luận", "chia sẻ",
    # What-if
    "gợi ý", "cải thiện", "what-if", "tăng", "delta",
    "phương án", "cần thêm",
    # General project questions
    "công thức", "tính", "trọng số", "shares", "comments",
    "dự án", "project", "streamlit", "python",
    "chatbot", "rag", "ollama", "knowledge",
]


def is_out_of_scope(question: str) -> bool:
    """
    Kiểm tra 3 lớp:
    Lớp 1 — Blacklist: câu hỏi chứa từ khóa cấm → từ chối ngay
    Lớp 2 — Whitelist: câu hỏi chứa từ khóa dự án → cho qua
    Lớp 3 — Default: không rõ → từ chối an toàn
    """
    q_lower = question.lower().strip()

    # Lớp 1: blacklist check
    if any(kw in q_lower for kw in OUT_OF_SCOPE_KEYWORDS):
        return True

    # Lớp 2: whitelist check — nếu có từ khóa dự án thì cho qua
    if any(kw in q_lower for kw in IN_SCOPE_KEYWORDS):
        return False

    # Lớp 3: câu quá ngắn hoặc không rõ chủ đề → từ chối an toàn
    # Ngoại lệ: câu hỏi chào hỏi ngắn thì cho qua
    greetings = ["xin chào", "hello", "hi", "chào", "hey",
                 "bạn là ai", "bạn là gì", "app này", "ứng dụng này"]
    if any(g in q_lower for g in greetings):
        return False

    # Nếu câu hỏi < 4 từ và không có từ khóa dự án → từ chối
    words = q_lower.split()
    if len(words) < 4:
        return True

    return True  # Default: an toàn hơn khi từ chối

SYSTEM_PROMPT = f"""Bạn là TikTok Viral Assistant — trợ lý AI chuyên biệt CHỈ hỗ trợ dự án "TikTok Viral Detector".

══════════════════════════════════════════
DANH TÍNH VÀ PHẠM VI (TUYỆT ĐỐI KHÔNG VI PHẠM)
══════════════════════════════════════════
Bạn LÀ một trợ lý chuyên biệt về dự án TikTok Viral Detector.
Bạn KHÔNG PHẢI là chatbot đa năng, KHÔNG PHẢI là AI tổng quát.
Bạn KHÔNG CÓ kiến thức về bất kỳ chủ đề nào ngoài dự án này.

NẾU người dùng hỏi bất kỳ điều gì NGOÀI danh sách chủ đề bên dưới:
→ PHẢI từ chối NGAY LẬP TỨC với câu: "Mình chỉ hỗ trợ các câu hỏi về dự án TikTok Viral Detector thôi bạn nhé! Bạn có thể hỏi mình về [gợi ý 2-3 chủ đề liên quan]."
→ KHÔNG được trả lời dù chỉ một phần.
→ KHÔNG được giải thích tại sao bạn không biết.
→ KHÔNG được nói "tôi không có thông tin về..."

══════════════════════════════════════════
CHỦ ĐỀ ĐƯỢC PHÉP TRẢ LỜI (chỉ những chủ đề này)
══════════════════════════════════════════
✅ Công thức Weighted ER = (Likes×1 + Comments×1.5 + Shares×2) / Views × 100
✅ Ngưỡng viral P80 = {P80:.4f}% (top 20% dataset 10M video)
✅ Cách dùng Tab 1: phân tích từ link TikTok qua tikwm.com
✅ Cách dùng Tab 2: nhập thủ công Views/Likes/Comments/Shares
✅ What-If Engine: 4 phương án tăng ER (Shares÷2, Comments÷1.5, Likes÷1, Combo 4:3:2)
✅ Mô hình Random Forest: AUC=0.9964, Accuracy=95.41%, F1=95.57%
✅ Tiền xử lý PySpark: 10M → 9.985.538 bản ghi, 16 features
✅ So sánh RF vs Decision Tree vs Logistic Regression
✅ Các yếu tố ảnh hưởng viral: shares, comments, likes, watch time, peak hours
✅ Giải thích kết quả phân tích cụ thể của video

══════════════════════════════════════════
QUY TẮC TRẢ LỜI
══════════════════════════════════════════
- Luôn dùng TIẾNG VIỆT
- Xưng "mình", gọi người dùng là "bạn"
- Trả lời ngắn gọn, rõ ràng, có số liệu cụ thể
- Chỉ dùng thông tin từ CONTEXT bên dưới, KHÔNG bịa thêm
- Nếu CONTEXT không đủ thông tin → nói "Mình chưa có thông tin chi tiết về điều này trong knowledge base"

══════════════════════════════════════════
CONTEXT TỪ KNOWLEDGE BASE
══════════════════════════════════════════
{{context}}

══════════════════════════════════════════
CÂU HỎI: {{question}}
══════════════════════════════════════════"""


def check_ollama_status():
    """Kiểm tra Ollama có đang chạy và model có sẵn không."""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        if r.status_code == 200:
            models = [m["name"] for m in r.json().get("models", [])]
            model_ready = any(OLLAMA_MODEL.split(":")[0] in m for m in models)
            return "online" if model_ready else "model_missing"
        return "offline"
    except Exception:
        return "offline"


def is_out_of_scope(question: str) -> bool:
    """Kiểm tra câu hỏi có ngoài phạm vi dự án không."""
    q_lower = question.lower()
    return any(kw in q_lower for kw in OUT_OF_SCOPE_KEYWORDS)


def retrieve_chunks(question: str, top_k: int = 3) -> list:
    """
    RAG Retrieval — tìm chunks liên quan nhất bằng keyword scoring.
    Không cần ChromaDB hay embedding model — dùng TF-IDF đơn giản.
    Phù hợp chạy offline 100% không cần cài thêm gì.
    """
    q_lower = question.lower()
    # Tách từ trong câu hỏi
    q_words = set(re.findall(r'\w+', q_lower))

    scored = []
    for chunk in KB_CHUNKS:
        score = 0
        # Score theo tags (trọng số cao hơn)
        for tag in chunk["tags"]:
            if tag in q_lower:
                score += 3          # tag khớp chính xác
            elif any(w in tag for w in q_words):
                score += 1          # từ khớp một phần
        # Score theo nội dung chunk
        content_lower = chunk["content"].lower()
        for word in q_words:
            if len(word) >= 3 and word in content_lower:
                score += 0.5        # từ xuất hiện trong nội dung
        scored.append((score, chunk))

    # Sort giảm dần, lấy top_k chunks có điểm cao nhất
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [c for score, c in scored[:top_k] if score > 0]

    # Nếu không tìm thấy gì, trả về chunk tổng quan
    if not top:
        top = [KB_CHUNKS[0]]
    return top


def build_rag_prompt(question: str, chunks: list) -> list:
    """Xây dựng messages list cho Ollama với RAG context."""
    context = "\n\n---\n\n".join(c["content"] for c in chunks)
    filled_prompt = SYSTEM_PROMPT.replace("{context}", context).replace("{question}", question)
    return [
        {"role": "system", "content": filled_prompt},
        {"role": "user",   "content": question},
    ]


def chat_with_rag(question: str, history: list) -> str:
    """Pipeline RAG đầy đủ: check scope → retrieve → generate."""

    # 1. Kiểm tra out-of-scope
    if is_out_of_scope(question):
        return (
            "Mình chỉ hỗ trợ các câu hỏi liên quan đến dự án "
            "**TikTok Viral Detector** thôi bạn nhé! 😊\n\n"
            "Bạn có thể hỏi về:\n"
            "- 📊 Công thức Weighted ER và ngưỡng P80\n"
            "- 🔗 Cách dùng app phân tích video\n"
            "- 🤖 Mô hình Random Forest và kết quả\n"
            "- 💡 Cách cải thiện ER để video viral"
        )

    # 2. Retrieve chunks liên quan
    chunks = retrieve_chunks(question, top_k=3)

    # 3. Build prompt với context
    messages = build_rag_prompt(question, chunks)

    # 4. Thêm 4 turns lịch sử gần nhất (nếu có) vào giữa system và user
    if history:
        recent = [m for m in history if m["role"] in ("user", "assistant")][-8:]
        # Chèn history sau system prompt, trước user message cuối
        messages = [messages[0]] + recent + [messages[1]]

    # 5. Gọi Ollama
    payload = {
        "model":   OLLAMA_MODEL,
        "messages": messages,
        "stream":  False,
        "options": {"temperature": 0.3, "num_predict": 600},
    }
    try:
        r = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=60)
        r.raise_for_status()
        reply = r.json()["message"]["content"].strip()
        # Đính kèm nguồn chunks đã dùng (để debug/hiển thị)
        return reply
    except requests.exceptions.Timeout:
        return "⏱️ Model phản hồi quá lâu. Thử lại nhé bạn!"
    except requests.exceptions.ConnectionError:
        return "❌ Không kết nối được Ollama. Kiểm tra `ollama serve` đang chạy chưa?"
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"


# Quick-reply buttons
QUICK_REPLIES = [
    ("📊", "Công thức tính Weighted ER là gì?"),
    ("🎯", "Ngưỡng viral P80 nghĩa là sao?"),
    ("🔗", "Cách dán link TikTok vào app?"),
    ("🔁", "Tại sao Shares quan trọng hơn Likes?"),
    ("📈", "Làm sao tăng ER của video nhanh nhất?"),
    ("🤖", "Mô hình Random Forest chính xác bao nhiêu?"),
    ("📂", "Dữ liệu được tiền xử lý như thế nào?"),
    ("⚖️", "Random Forest tốt hơn Decision Tree ở điểm nào?"),
]



def render_result(views, likes, comments, shares):
    """Render kết quả phân tích + What-If nếu chưa viral."""
    errors = validate(views, likes, comments, shares)
    if errors:
        items = "".join(f'<div class="ve-item">⚠ {e}</div>' for e in errors)
        st.markdown(f'<div class="val-error"><div class="ve-title">❌ Dữ liệu không hợp lệ</div>{items}</div>',
                    unsafe_allow_html=True)
        return

    er       = calc_er(views, likes, comments, shares)
    is_viral = er >= P80
    weighted = (likes * 1.0) + (comments * 1.5) + (shares * 2.0)
    bar_pct  = min(er / (P80 * 2) * 100, 100)
    bar_col  = "linear-gradient(90deg,#ff3358,#ff7090)" if is_viral else "linear-gradient(90deg,#3d3d6b,#6b6baa)"

    if is_viral:
        diff          = (er - P80) / P80 * 100
        verdict_class = "result-viral"
        icon, title   = "🔥", "VIRAL!"
        sub           = f"Cao hơn ngưỡng +{diff:.1f}% &nbsp;·&nbsp; Top 20% toàn dataset"
    else:
        gap           = P80 - er
        verdict_class = "result-safe"
        icon, title   = "📉", "Chưa Viral"
        sub           = f"Cần thêm <strong>{gap:.2f}%</strong> ER để đạt ngưỡng &nbsp;·&nbsp; Thuộc nhóm 80% phổ thông"

    verdict_word = '<span class="verdict-ok">✅ VIRAL</span>' if is_viral else '<span class="verdict-no">❌ Chưa Viral</span>'

    # ── Result banner ──
    st.markdown(f"""
    <div class="{verdict_class}">
      <div class="result-head">
        <div class="res-icon">{icon}</div>
        <div><div class="res-title">{title}</div><div class="res-sub">{sub}</div></div>
      </div>
      <div class="m4-grid">
        <div class="m-tile"><div class="mi">👁️</div><div class="ml">Views</div><div class="mv">{fmt(views)}</div></div>
        <div class="m-tile"><div class="mi">❤️</div><div class="ml">Likes</div><div class="mv">{fmt(likes)}</div></div>
        <div class="m-tile"><div class="mi">💬</div><div class="ml">Comments</div><div class="mv">{fmt(comments)}</div></div>
        <div class="m-tile"><div class="mi">🔁</div><div class="ml">Shares</div><div class="mv">{fmt(shares)}</div></div>
      </div>
      <div class="er-gauge">
        <div class="er-row">
          <div class="er-left">
            <div class="erl-title">Weighted Engagement Rate</div>
            <div class="erl-sub">(likes×1 + comments×1.5 + shares×2) ÷ views × 100</div>
          </div>
          <div class="er-num">{er:.2f}<sub>%</sub></div>
        </div>
        <div class="er-track-wrap">
          <div class="er-track"><div class="er-bar" style="width:{bar_pct:.1f}%;background:{bar_col};"></div></div>
          <div class="er-marker" style="left:50%;"></div>
        </div>
        <div class="er-axis">
          <span>0%</span>
          <span class="axis-mid">▲ Ngưỡng Viral (P80) = {P80:.2f}%</span>
          <span>{P80*2:.1f}%</span>
        </div>
      </div>
      <div class="fbox">
        <div class="fbox-title">🧮 Chi tiết tính toán</div>
        <div class="fbox-body">
          Weighted = ({fmt(likes)}×1) + ({fmt(comments)}×1.5) + ({fmt(shares)}×2) = <strong>{weighted:,.0f}</strong><br>
          ER = {weighted:,.0f} ÷ {fmt(views)} × 100 = <strong>{er:.4f}%</strong><br>
          Kết luận: {er:.4f}% {'≥' if is_viral else '<'} {P80:.2f}% (P80) → {verdict_word}
        </div>
      </div>
    """, unsafe_allow_html=True)

    if metrics.get("auc_roc"):
        st.markdown(f"""
      <div class="model-strip">
        <span class="ms-icon">🤖</span>
        <div class="ms-label"><strong>Model Performance</strong><br>Random Forest · 100 trees · 10M videos</div>
        <div class="ms-metrics">
          <div class="ms-m"><div class="msv">{metrics['auc_roc']:.3f}</div><div class="msl">AUC-ROC</div></div>
          <div class="ms-m"><div class="msv">{metrics['accuracy']:.3f}</div><div class="msl">Accuracy</div></div>
          <div class="ms-m"><div class="msv">{metrics['f1_score']:.3f}</div><div class="msl">F1-Score</div></div>
        </div>
      </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── What-If (chỉ hiện khi chưa viral) ──
    if not is_viral:
        suggestions = whatif_suggestions(views, likes, comments, shares, P80, er)
        if suggestions:
            best = suggestions[0]  # phương án ít tốn công nhất

            st.markdown("""
            <div class="whatif-box">
              <div class="wi-header">
                <div class="wi-badge">💡 Gợi ý cải thiện</div>
                <div>
                  <div class="wi-title">Cần làm gì để video Viral?</div>
                  <div class="wi-sub">App tự tính con số cụ thể bạn cần tăng thêm cho từng chỉ số</div>
                </div>
              </div>
              <div class="wi-rows">
            """, unsafe_allow_html=True)

            for i, s in enumerate(suggestions):
                is_best   = (i == 0)
                row_class = "wi-row wi-focus" if is_best else "wi-row"
                need_class = "wi-need"

                if s.get("combo"):
                    current_txt = f"Shares: {fmt(shares)} · Comments: {fmt(comments)} · Likes: {fmt(likes)}"
                    need_txt    = s["label"]
                    er_txt      = f"ER mới: {s['er_new']:.2f}%"
                else:
                    current_txt = f"Hiện tại: {fmt(s['current'])} → Cần đạt: {fmt(s['target'])}"
                    need_txt    = f"+{fmt(s['need'])}"
                    er_txt      = f"ER mới: {s['er_new']:.2f}%"

                best_tag = ' <span style="color:var(--purple);font-size:0.65rem;">★ Dễ nhất</span>' if is_best else ""

                st.markdown(f"""
                <div class="{row_class}">
                  <div class="wi-icon">{s['icon']}</div>
                  <div class="wi-info">
                    <div class="wi-metric">{s['metric']} {s['weight']}{best_tag}</div>
                    <div class="wi-current">{current_txt} &nbsp;·&nbsp; {er_txt}</div>
                  </div>
                  <div class="wi-action">
                    <div class="{need_class}">{need_txt}</div>
                    <div class="wi-need-lbl">{'cần thêm' if not s.get('combo') else 'kết hợp'}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            gap_er = P80 - er
            st.markdown(f"""
              </div>
              <div class="wi-summary">
                Video hiện tại cách ngưỡng viral <strong>{gap_er:.2f}%</strong> ER.<br>
                <strong>Phương án tối ưu nhất:</strong> {best['label']} → ER sẽ đạt <strong>{best['er_new']:.2f}%</strong>
                <span class="wi-best">→ Tập trung vào Shares trước vì mỗi share có trọng số ×2.0 — hiệu quả nhất!</span>
              </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RENDER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="wrap">', unsafe_allow_html=True)

# ── TOPBAR ──
st.markdown(f"""
<div class="topbar">
  <div class="topbar-brand">
    <div class="topbar-icon">🔥</div>
    <div>
      <div class="topbar-name">TikTok <span>Viral Detector</span></div>
      <div class="topbar-sub">Random Forest · 10M Videos Dataset</div>
    </div>
  </div>
  <div class="topbar-pills">
    <div class="pill red-pill">Live Model</div>
    <div class="pill">🌲 <strong>100</strong> trees</div>
    <div class="pill">🗃️ <strong>10M</strong> videos</div>
    <div class="pill">📍 P80 = <strong>{P80:.2f}%</strong></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── THRESHOLD INFO ──
st.markdown(f"""
<div class="threshold-info">
  <span class="ti-icon">📊</span>
  <div class="ti-body">
    <strong>Ngưỡng Viral tính từ dữ liệu thực tế:</strong>
    Mô hình phân tích 10,000,000 video TikTok, ngưỡng Weighted ER ở phân vị <strong>P80</strong>
    — chỉ <strong>20% video hàng đầu</strong> đạt mức này.
    <span class="ti-val">{P80:.4f}%</span>
    Video có ER ≥ <strong>{P80:.2f}%</strong> → <strong>Viral</strong> · Thấp hơn → phổ thông (80% còn lại).
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TABS — 2 tính năng
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs([
    "🔗  Phân tích từ Link TikTok",
    "✏️  Nhập thủ công",
    "🤖  Trợ lý AI",
])


# ────────────────────────────────────────────────────────────────────────────
# TAB 1 — LINK TIKTOK
# ────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("""
    <div class="sec-title">Phân tích từ Link TikTok</div>
    <div class="sec-sub">Dán link video bất kỳ — app tự động lấy số liệu và phân tích · Không cần API Key</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="url-hint">
      <span class="url-hint-icon">💡</span>
      <div>
        Hỗ trợ mọi dạng link TikTok:<br>
        <code>https://www.tiktok.com/@username/video/1234567890</code><br>
        <code>https://vm.tiktok.com/XXXXXXX/</code> &nbsp;(link rút gọn)<br>
        <code>https://vt.tiktok.com/XXXXXXX/</code> &nbsp;(link share từ app)
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-label"><span class="dot"></span>Nhập link video</div>',
                unsafe_allow_html=True)

    tiktok_url = st.text_input(
        "🔗  Link Video TikTok",
        placeholder="https://www.tiktok.com/@username/video/...",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    fetch_btn = st.button("🔍  LẤY SỐ LIỆU & PHÂN TÍCH", use_container_width=True, key="fetch_btn")

    if fetch_btn:
        if not tiktok_url.strip():
            st.markdown('<div class="fetch-error">⚠️ <strong>Chưa nhập link video TikTok</strong></div>',
                        unsafe_allow_html=True)

        elif not is_tiktok_url(tiktok_url):
            st.markdown("""
            <div class="fetch-error">
              <strong>⚠️ Link không hợp lệ</strong><br>
              Link phải chứa <code>tiktok.com</code>, <code>vm.tiktok.com</code> hoặc <code>vt.tiktok.com</code>
            </div>
            """, unsafe_allow_html=True)

        else:
            with st.spinner("⏳ Đang lấy dữ liệu từ TikTok..."):
                try:
                    data = fetch_tiktok_stats(tiktok_url.strip())

                    # Hiển thị thông tin video đã fetch
                    st.markdown(f"""
                    <div class="fetched-info">
                      <div class="fi-title">✅ Đã lấy dữ liệu thành công</div>
                      <div class="fi-meta">
                        👤 @{data['author']} &nbsp;·&nbsp;
                        📝 {data['title']}
                      </div>
                      <div class="fi-stats">
                        <div class="fi-stat"><div class="fis-icon">👁️</div><div class="fis-val">{fmt(data['views'])}</div><div class="fis-lbl">Views</div></div>
                        <div class="fi-stat"><div class="fis-icon">❤️</div><div class="fis-val">{fmt(data['likes'])}</div><div class="fis-lbl">Likes</div></div>
                        <div class="fi-stat"><div class="fis-icon">💬</div><div class="fis-val">{fmt(data['comments'])}</div><div class="fis-lbl">Comments</div></div>
                        <div class="fi-stat"><div class="fis-icon">🔁</div><div class="fis-val">{fmt(data['shares'])}</div><div class="fis-lbl">Shares</div></div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Phân tích ngay
                    render_result(data["views"], data["likes"], data["comments"], data["shares"])

                except requests.exceptions.Timeout:
                    st.markdown("""
                    <div class="fetch-error">
                      <strong>⏱️ Timeout</strong> — TikTok mất quá lâu để phản hồi. Thử lại sau vài giây.
                    </div>
                    """, unsafe_allow_html=True)

                except requests.exceptions.HTTPError as e:
                    code = e.response.status_code if e.response is not None else "?"
                    if code == 401:
                        msg = "API Key không hợp lệ hoặc đã hết hạn — kiểm tra lại trên RapidAPI"
                    elif code == 429:
                        msg = "Đã dùng hết quota miễn phí tháng này (500 req/tháng) — nâng cấp gói trên RapidAPI"
                    elif code == 403:
                        msg = "Chưa subscribe API này — vào RapidAPI → Subscribe gói Free trước"
                    else:
                        msg = f"Lỗi HTTP {code} từ API"
                    st.markdown(f'<div class="fetch-error"><strong>❌ {msg}</strong></div>',
                                unsafe_allow_html=True)

                except ValueError as e:
                    st.markdown(f'<div class="fetch-error"><strong>⚠️ {e}</strong></div>',
                                unsafe_allow_html=True)

                except Exception as e:
                    st.markdown(f"""
                    <div class="fetch-error">
                      <strong>❌ Lỗi không xác định:</strong> {str(e)}<br>
                      Kiểm tra lại API Key và link video rồi thử lại.
                    </div>
                    """, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
# TAB 2 — NHẬP THỦ CÔNG
# ────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("""
    <div class="sec-title">Nhập thủ công</div>
    <div class="sec-sub">Nhập số liệu từ video TikTok của bạn · Tối thiểu 1,000 lượt xem</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-label"><span class="dot"></span>Thông số đầu vào</div>',
                unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        views    = st.number_input("👁️  Lượt xem (Views)",    min_value=0, value=500_000, step=10_000, format="%d")
    with c2:
        likes    = st.number_input("❤️  Lượt thích (Likes)",  min_value=0, value=45_000,  step=1_000,  format="%d")
    with c3:
        comments = st.number_input("💬 Bình luận (Comments)", min_value=0, value=3_200,   step=100,    format="%d")
    with c4:
        shares   = st.number_input("🔁 Lượt chia sẻ (Shares)",min_value=0, value=8_500,   step=100,    format="%d")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("⚡  PHÂN TÍCH NGAY", use_container_width=True, key="manual_btn"):
        render_result(views, likes, comments, shares)



# ────────────────────────────────────────────────────────────────────────────
# TAB 3 — CHATBOT TRỢ LÝ AI (Ollama local)
# ────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("""
    <div class="sec-title">🤖 Trợ lý AI RAG — TikTok Viral Assistant</div>
    <div class="sec-sub">Chỉ trả lời câu hỏi về dự án · RAG: tìm đúng kiến thức trước khi trả lời · Chạy offline hoàn toàn</div>
    """, unsafe_allow_html=True)

    # ── Khởi tạo session state ──
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "ollama_status" not in st.session_state:
        st.session_state.ollama_status = None
    if "quick_fired" not in st.session_state:
        st.session_state.quick_fired = None

    # ── Kiểm tra Ollama status ──
    status = check_ollama_status()
    st.session_state.ollama_status = status

    if status == "online":
        status_html = f"""
        <div class="chat-status">
          <div class="chat-status-dot online"></div>
          <div class="chat-status-text">
            <strong>RAG Chatbot sẵn sàng</strong> · Model: {OLLAMA_MODEL} ·
            Knowledge base: {len(KB_CHUNKS)} chunks · Chạy offline 100%
          </div>
        </div>"""
    elif status == "model_missing":
        status_html = f"""
        <div class="chat-status">
          <div class="chat-status-dot offline"></div>
          <div class="chat-status-text"><strong>Ollama đang chạy nhưng chưa có model</strong> · Chạy: <code>ollama pull {OLLAMA_MODEL}</code></div>
        </div>"""
    else:
        status_html = """
        <div class="chat-status">
          <div class="chat-status-dot offline"></div>
          <div class="chat-status-text"><strong>Ollama chưa chạy</strong> · Xem hướng dẫn cài đặt bên dưới</div>
        </div>"""

    st.markdown(status_html, unsafe_allow_html=True)

    # ── Hướng dẫn cài đặt nếu offline ──
    if status != "online":
        st.markdown(f"""
        <div class="ollama-setup">
          <div class="setup-title">⚙️ Cài đặt Ollama (chỉ cần làm 1 lần)</div>
          <div class="setup-step">
            <div class="setup-num">1</div>
            <div class="setup-text">
              Tải Ollama tại <strong>ollama.com/download</strong> → chọn Windows → cài như phần mềm thường
            </div>
          </div>
          <div class="setup-step">
            <div class="setup-num">2</div>
            <div class="setup-text">
              Mở <strong>Command Prompt</strong>, chạy lệnh:<br>
              <code>ollama pull {OLLAMA_MODEL}</code><br>
              (tải model ~2GB, chỉ 1 lần duy nhất)
            </div>
          </div>
          <div class="setup-step">
            <div class="setup-num">3</div>
            <div class="setup-text">
              Mở CMD thứ 2, chạy:<br>
              <code>ollama serve</code><br>
              Sau đó <strong>refresh lại trang Streamlit</strong> → chatbot tự động kết nối.
            </div>
          </div>
          <div class="setup-step">
            <div class="setup-num">4</div>
            <div class="setup-text">
              Lần sau: mở CMD → <code>ollama serve</code> → mở app → chatbot sẵn sàng ngay.
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Tin nhắn chào ──
    if not st.session_state.chat_history:
        greeting = (
            f"Xin chào! Mình là trợ lý AI RAG của **TikTok Viral Detector** 🤖\n\n"
            f"Mình được xây dựng theo kiến trúc **RAG (Retrieval-Augmented Generation)** — "
            f"mỗi câu hỏi của bạn sẽ được tìm kiếm trong knowledge base {len(KB_CHUNKS)} chunks "
            f"trước khi trả lời, giúp câu trả lời chính xác và bám sát dự án.\n\n"
            f"Mình **chỉ trả lời** các câu hỏi liên quan đến dự án phát hiện video viral:\n"
            f"- 📊 Công thức **Weighted ER** và ngưỡng **P80 = {P80:.2f}%**\n"
            f"- 🔗 Cách dùng app (Tab 1, Tab 2)\n"
            f"- 🤖 Mô hình Random Forest (AUC = 0.9964)\n"
            f"- 📂 Tiền xử lý dữ liệu PySpark\n"
            f"- 💡 Gợi ý cải thiện ER\n\n"
            f"Bạn muốn hỏi gì, cứ tự nhiên nhé! 😊"
        )
        st.session_state.chat_history.append({"role": "assistant", "content": greeting})

    # ── Cửa sổ chat ──
    from datetime import datetime
    import re as _re
    now_str = datetime.now().strftime("%H:%M")

    chat_html = '<div class="chat-window" id="chat-window">'
    for msg in st.session_state.chat_history:
        role    = msg["role"]
        content = msg["content"]
        t       = msg.get("time", now_str)
        if role == "assistant":
            display = _re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            display = _re.sub(r'`(.+?)`', r'<code>\1</code>', display)
            display = display.replace("\n", "<br>")
            chat_html += f"""
            <div class="msg-row bot">
              <div class="msg-avatar bot-av">🤖</div>
              <div>
                <div class="msg-bubble bot">{display}</div>
                <div class="msg-time">{t}</div>
              </div>
            </div>"""
        else:
            display = content.replace("\n", "<br>")
            chat_html += f"""
            <div class="msg-row user">
              <div class="msg-avatar user-av">👤</div>
              <div>
                <div class="msg-bubble user">{display}</div>
                <div class="msg-time">{t}</div>
              </div>
            </div>"""
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    # ── Quick reply — 8 nút, 4 cột ──
    st.markdown('<div class="quick-btn-label">💬 Câu hỏi gợi ý nhanh</div>', unsafe_allow_html=True)
    qcols = st.columns(4)
    for idx, (icon, qtext) in enumerate(QUICK_REPLIES):
        with qcols[idx % 4]:
            if st.button(f"{icon} {qtext}", key=f"qr_{idx}", use_container_width=True):
                st.session_state.quick_fired = qtext

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    # ── Input form ──
    with st.form("chat_form", clear_on_submit=True):
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            user_input = st.text_input(
                "Nhập câu hỏi",
                placeholder="Ví dụ: Tại sao video của tôi không viral? Công thức ER tính như thế nào?",
                label_visibility="collapsed",
            )
        with col_btn:
            send_btn = st.form_submit_button("Gửi ➤", use_container_width=True)

    if st.button("🗑️ Xóa lịch sử chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()

    # ── Xử lý & gửi RAG ──
    final_input = ""
    if send_btn and user_input.strip():
        final_input = user_input.strip()
    elif st.session_state.quick_fired:
        final_input = st.session_state.quick_fired
        st.session_state.quick_fired = None

    if final_input:
        from datetime import datetime as _dt
        t_now = _dt.now().strftime("%H:%M")

        st.session_state.chat_history.append({
            "role": "user", "content": final_input, "time": t_now,
        })

        if status != "online":
            bot_reply = (
                "⚠️ RAG Chatbot chưa sẵn sàng — Ollama chưa chạy hoặc chưa có model.\n"
                "Bạn làm theo hướng dẫn cài đặt ở trên nhé! Chỉ 3 bước là xong 😊"
            )
        else:
            # ── RAG Pipeline ──────────────────────────────────────────
            # Bước 1: Lấy lịch sử (bỏ greeting dài, chỉ giữ Q&A)
            history_for_rag = [
                m for m in st.session_state.chat_history
                if m["role"] in ("user", "assistant")
            ][-8:]

            with st.spinner("🔍 Đang tìm kiếm knowledge base..."):
                # Bước 2: Retrieve chunks liên quan
                chunks = retrieve_chunks(final_input, top_k=3)

            with st.spinner("🤖 Đang tạo câu trả lời..."):
                # Bước 3: Generate với RAG context
                bot_reply = chat_with_rag(final_input, history_for_rag)

            # Hiển thị nguồn chunks đã dùng (transparency)
            if chunks and status == "online" and not is_out_of_scope(final_input):
                src_ids = " · ".join(f"`{c['id']}`" for c in chunks)
                bot_reply += f"\n\n_📚 Nguồn: {src_ids}_"

        st.session_state.chat_history.append({
            "role": "assistant", "content": bot_reply, "time": _dt.now().strftime("%H:%M"),
        })
        st.rerun()


# ── VIRAL GUIDE ───────────────────────────────────────────────────────────────
st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="sec-title">Tiêu chí để Video Viral</div>
<div class="sec-sub">6 yếu tố cốt lõi tác động đến Weighted Engagement Rate — dựa trên phân tích 10M video thực tế</div>
""", unsafe_allow_html=True)

def g_row(icon, name, desc, target, unit, bar_w, bar_col, weight_label):
    return f"""
    <div class="g-row">
      <div class="g-icon">{icon}</div>
      <div>
        <div class="g-name">{name}</div>
        <div class="g-desc">{desc}</div>
      </div>
      <div class="g-target">
        <div class="g-val">{target}</div>
        <div class="g-unit">{unit}</div>
      </div>
      <div class="g-weight">
        <div class="wbar-wrap"><div class="wbar" style="width:{bar_w}%;background:{bar_col};"></div></div>
        <div class="wlabel">{weight_label}</div>
      </div>
    </div>"""

CRITERIA = [
    ("🔁","Lượt Chia sẻ (Shares)","Yếu tố lan truyền mạnh nhất · Mỗi share đưa video đến audience mới · Algorithm TikTok ưu tiên content được share nhiều","≥ 2–5%","share / view",100,"linear-gradient(90deg,#ff3358,#ff7090)","×2.0 — Quan trọng nhất"),
    ("💬","Bình luận (Comments)","Phản ánh mức độ kích thích cảm xúc · Video gây tò mò, gây sốc, hài hước thường comment cao · Algorithm đọc được tín hiệu này","≥ 1–3%","comment / view",75,"linear-gradient(90deg,#00cfff,#0099cc)","×1.5 — Quan trọng cao"),
    ("❤️","Lượt Thích (Likes)","Tín hiệu nền tảng cần thiết · Tỉ lệ like/view cao cho thấy nội dung được đón nhận · Thường chiếm phần lớn weighted score","≥ 5–10%","like / view",50,"linear-gradient(90deg,#ffcc00,#ff9900)","×1.0 — Cơ bản"),
    ("⏱️","Watch Time (Tỉ lệ xem hết)","Algorithm đo % người xem đến cuối · Video 15–30s dễ đạt cao hơn · 3 giây hook đầu quyết định 70% kết quả phân phối","≥ 70%","completion rate",85,"linear-gradient(90deg,#2ecc71,#27ae60)","Signal mạnh FYP"),
    ("🎵","Âm nhạc & Trending Sound","Dùng nhạc trending tăng khả năng xuất hiện FYP · TikTok push video dùng sound phổ biến · Nhạc gốc cũng có thể viral","Top 100","trending sounds",60,"linear-gradient(90deg,#bf5af2,#9933cc)","Boost FYP"),
    ("🕐","Thời điểm đăng (Peak Hours)","7–9h sáng · 12–14h trưa · 19–23h tối · 2 giờ đầu quyết định algorithm có push tiếp hay không","Peak ±30m","khung giờ vàng",45,"linear-gradient(90deg,#ff9500,#cc7700)","Timing boost"),
]

st.markdown(f"""
<div class="card">
  <div class="guide-desc">
    Random Forest học từ <strong>10,000,000 video TikTok</strong>, xác định ngưỡng Viral tại
    <strong>P80 = {P80:.2f}%</strong>. Công thức Weighted ER ưu tiên <strong>Shares (×2)</strong>
    và <strong>Comments (×1.5)</strong> vì chúng phản ánh mức độ lan truyền thực sự.
  </div>
  <div class="g-header">
    <div></div><div>Tiêu chí</div>
    <div class="right">Mục tiêu</div>
    <div class="right">Trọng số trong ER</div>
  </div>
  <div class="g-rows">
""", unsafe_allow_html=True)

for c in CRITERIA:
    st.markdown(g_row(*c), unsafe_allow_html=True)

st.markdown("""
  </div>
  <div class="ex-card">
    <div class="ex-head">
      <div class="ex-badge">✅ Ví dụ thực tế</div>
      <div>
        <div class="ex-title">Video Cooking Hack — "3 nguyên liệu làm bánh mì siêu tốc"
          <small>28 giây · Đăng 20:30 thứ 6 · Trending sound · Không cần verified</small>
        </div>
      </div>
    </div>
    <div class="ex-stats">
      <div class="ex-s"><div class="esi">👁️</div><div class="esv">2.4M</div><div class="esl">Views</div></div>
      <div class="ex-s"><div class="esi">❤️</div><div class="esv">186K</div><div class="esl">Likes</div></div>
      <div class="ex-s"><div class="esi">💬</div><div class="esv">9.2K</div><div class="esl">Comments</div></div>
      <div class="ex-s"><div class="esi">🔁</div><div class="esv">52K</div><div class="esl">Shares</div></div>
      <div class="ex-s"><div class="esi">📊</div><div class="esv">13.46%</div><div class="esl">Weighted ER</div></div>
    </div>
    <div class="ex-result">
      <div><div class="exr-label">Weighted ER</div><div class="exr-val">13.46%</div></div>
      <div class="exr-calc">(186K×1) + (9.2K×1.5) + (52K×2) = 323,800<br>323,800 ÷ 2,400,000 × 100 = <strong style="color:#2ecc71">13.46%</strong></div>
      <div class="exr-chip">🔥 VIRAL — gấp 2× ngưỡng P80</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ──
st.markdown(f"""
<div class="footer">
  <div class="fl">
    TikTok Viral Detector · Random Forest Classifier<br>
    Weighted ER = (Likes×1 + Comments×1.5 + Shares×2) / Views × 100
  </div>
  <div class="fr">
    Dataset: 10,000,000 videos · P80 = {P80:.4f}%<br>
    TikTok data by tikwm.com · Miễn phí · Không cần API Key
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FLOATING CHAT WIDGET — HTML/JS (ngoài .wrap, fixed position)
# ══════════════════════════════════════════════════════════════════════════════
OLLAMA_OK = check_ollama_status() == "online"


# ══════════════════════════════════════════════════════════════════════════════
# FLOATING CHAT WIDGET
# ══════════════════════════════════════════════════════════════════════════════
OLLAMA_OK = check_ollama_status() == "online"
_ok_js    = "true" if OLLAMA_OK else "false"
_kb_count = len(KB_CHUNKS)
_status_txt = "🟢 Ollama online" if OLLAMA_OK else "🔴 Ollama offline"

# ── HTML part (f-string ok, no JS regex here) ──
st.markdown(f"""
<button id="fcw-btn" title="Hỏi về dự án" aria-label="Mở trợ lý AI">
  <span class="fcw-icon-open">
    <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/></svg>
  </span>
  <span class="fcw-icon-close">
    <svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
  </span>
  <span id="fcw-badge">1</span>
</button>

<div id="fcw-panel">
  <div id="fcw-header">
    <div class="fcw-avatar">🤖</div>
    <div class="fcw-hinfo">
      <div class="fcw-hname">TikTok Viral Assistant</div>
      <div class="fcw-hsub">RAG · {_kb_count} chunks · {_status_txt}</div>
    </div>
    <div class="fcw-hdot"></div>
  </div>
  <div id="fcw-msgs">
    <div class="fcw-msg bot">
      <div class="fcw-av-sm">🤖</div>
      <div class="fcw-bubble bot">
        Xin chào! Mình là trợ lý AI của dự án.<br><br>
        Mình có thể giúp bạn:<br>
        📊 <strong>Công thức Weighted ER</strong> &amp; ngưỡng viral<br>
        🔗 <strong>Cách dùng</strong> Tab 1, Tab 2<br>
        🤖 <strong>Random Forest</strong> (AUC = 0.9964)<br>
        💡 <strong>Cách cải thiện ER</strong><br><br>
        Bạn hỏi gì đi nha! 😊
      </div>
    </div>
  </div>
  <div id="fcw-chips">
    <span class="fcw-chip" onclick="fcwAsk(this.textContent)">📊 Công thức ER?</span>
    <span class="fcw-chip" onclick="fcwAsk(this.textContent)">🎯 Ngưỡng P80?</span>
    <span class="fcw-chip" onclick="fcwAsk(this.textContent)">🔗 Cách dán link?</span>
    <span class="fcw-chip" onclick="fcwAsk(this.textContent)">🔁 Tại sao Shares × 2?</span>
    <span class="fcw-chip" onclick="fcwAsk(this.textContent)">📈 Làm sao tăng ER?</span>
    <span class="fcw-chip" onclick="fcwAsk(this.textContent)">🤖 Độ chính xác RF?</span>
  </div>
  <div id="fcw-input-row">
    <input id="fcw-input" type="text" placeholder="Hỏi về dự án..." />
    <button id="fcw-send" onclick="fcwSend()" title="Gửi">
      <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
    </button>
  </div>
  <div id="fcw-powered">Powered by Ollama · {OLLAMA_MODEL} · RAG local</div>
</div>
""", unsafe_allow_html=True)

# ── JS part — plain string, inject Python vars via .format() ──
_js = """
<script>
const OLLAMA_OK  = OLLAMA_OK_PY;
const OLLAMA_URL = 'http://localhost:11434/api/chat';
const MODEL      = 'MODEL_PY';
const P80_VAL    = P80_PY;

const KB = [
  { id:'app_overview', tags:['app','tổng quan','giới thiệu','là gì','tính năng','gồm gì'],
    content:'TikTok Viral Detector là ứng dụng Streamlit dùng Random Forest phân tích 10M video. 3 tab: Tab 1 phân tích từ link, Tab 2 nhập thủ công, Tab 3 trợ lý RAG.' },
  { id:'weighted_er', tags:['er','weighted er','công thức','tính','trọng số','engagement','likes','shares','comments'],
    content:'Công thức: Weighted ER = (Likes*1 + Comments*1.5 + Shares*2) / Views * 100. Shares*2 vì lan truyền mạnh nhất, Comments*1.5 kích thích cảm xúc, Likes*1 dễ bấm nhất.' },
  { id:'viral_threshold', tags:['p80','ngưỡng','viral','threshold','top 20','bao nhiêu','phân vị'],
    content:'Ngưỡng P80 = P80_PY%. Chỉ 20% video hàng đầu đạt mức này. ER >= P80_PY% → VIRAL. ER < P80_PY% → Chua Viral. P80 tinh bang PySpark tren 10M video.' },
  { id:'tab1_link', tags:['tab 1','link','dan link','url','fetch','cach dung','tikwm','copy link'],
    content:'Tab 1: Dan link TikTok (tiktok.com, vm.tiktok.com, vt.tiktok.com) → bam LAY SO LIEU → app tu fetch qua tikwm.com mien phi → tinh ER → ket qua.' },
  { id:'tab2_manual', tags:['tab 2','nhap thu cong','manual','nhap tay','nhập thủ công'],
    content:'Tab 2: Nhap 4 so (Views toi thieu 1000, Likes, Comments, Shares) → bam PHAN TICH NGAY. Validate tu dong: likes/comments/shares khong duoc > views.' },
  { id:'whatif', tags:['goi y','cai thien','what-if','tang er','can them','phuong an','gợi ý','cải thiện'],
    content:'What-If Engine: tinh delta = (P80/100 * views) - weighted_hien_tai. 4 phuong an: (1) Chi Shares = delta/2 de nhat, (2) Chi Comments = delta/1.5, (3) Chi Likes = delta/1.0, (4) Combo 4:3:2.' },
  { id:'random_forest', tags:['random forest','mo hinh','ai','auc','accuracy','f1','chinh xac','mô hình'],
    content:'Random Forest: 100 cay, max_depth=15, min_samples_leaf=100, class_weight=balanced. AUC=0.9964, Accuracy=95.41%, F1=95.57%, Precision=96.16%. Train 7.988.430 / Test 1.997.108.' },
  { id:'model_compare', tags:['so sanh','decision tree','logistic','tot hon','tai sao chon','so sánh'],
    content:'RF (AUC 0.9964) > Decision Tree (AUC 0.9312) > Logistic Regression (AUC 0.8124). Chon RF vi khang overfitting, xu ly phi tuyen, predict < 1ms.' },
  { id:'preprocessing', tags:['tien xu ly','spark','pyspark','du lieu','16 features','lam sach','tiền xử lý'],
    content:'PySpark: 10M → 9.985.538 ban ghi. 4 buoc: cast kieu, filter, IQR P1-P99, tao time features. 16 features: log_play_count, log_digg_count, duration, vq_score, post_hour, is_weekend, v.v.' },
  { id:'viral_tips', tags:['tieu chi','yeu to','peak hour','gio vang','am nhac','meo','tiêu chí'],
    content:'6 yeu to: Shares >=2-5%, Comments >=1-3%, Likes >=5-10%, Watch Time >=70%, Nhac trending Top100, Peak Hours 7-9h/12-14h/19-23h. 2h dau sau dang quyet dinh algorithm.' },
];

const OUT_SCOPE = [
  'naruto','anime','manga','one piece','dragon ball','genshin','pokemon',
  'minecraft','valorant','game','phim','series','netflix','youtube',
  'thoi tiet','nhiet do','mua','nang','bao',
  'nau an','mon an','am thuc','banh','pho','bun',
  'bong da','bong ro','tennis','world cup','olympic',
  'chinh tri','bau cu','tong thong','thu tuong',
  'kinh te','gdp','lam phat','chung khoan','crypto','bitcoin','ethereum','nft',
  'suc khoe','benh','thuoc','y te','bac si','covid','vaccine',
  'tinh yeu','hen ho','crush','nguoi yeu','chia tay','tam su',
  'toan hoc','vat ly','hoa hoc','sinh hoc','lich su','triet hoc',
  'java','c++','php','ruby','swift','kotlin','react','angular','vue','nodejs',
  'blockchain','docker','kubernetes',
  'lam tho','viet van','dich thuat','ve tranh','ca si','dien vien',
  'la ai','sinh nam','tieu su',
];

const IN_SCOPE = [
  'tiktok','viral','er','engagement','weighted','p80','nguong','threshold',
  'app','ung dung','tab','link','phan tich','nhap','fetch','tikwm','ket qua',
  'cach dung','huong dan','random forest','mo hinh','model','auc','accuracy',
  'f1','machine learning','ai','scikit','sklearn','du doan',
  'pyspark','spark','dataset','du lieu','feature','train','test','huan luyen',
  'views','likes','comments','shares','luot xem','luot thich','binh luan','chia se',
  'goi y','cai thien','what-if','tang er','delta','phuong an','can them',
  'cong thuc','tinh','trong so','du an','project','streamlit','python',
  'chatbot','rag','ollama','knowledge',
];

function removeAccents(str) {
  return str.toLowerCase()
    .replace(/[àáạảãâầấậẩẫăằắặẳẵ]/g,'a')
    .replace(/[èéẹẻẽêềếệểễ]/g,'e')
    .replace(/[ìíịỉĩ]/g,'i')
    .replace(/[òóọỏõôồốộổỗơờớợởỡ]/g,'o')
    .replace(/[ùúụủũưừứựửữ]/g,'u')
    .replace(/[ỳýỵỷỹ]/g,'y')
    .replace(/[đ]/g,'d')
    .replace(/[^a-z0-9 ]/g,' ');
}

function isOutScope(q) {
  var ql = removeAccents(q);

  // Lop 1: blacklist
  if (OUT_SCOPE.some(function(k){ return ql.indexOf(k) >= 0; })) return true;

  // Lop 2: whitelist du an
  if (IN_SCOPE.some(function(k){ return ql.indexOf(k) >= 0; })) return false;

  // Lop 3: chao hoi ngan
  var greetings = ['xin chao','hello','hi ','chao','hey','ban la ai','app nay','ung dung nay'];
  if (greetings.some(function(g){ return ql.indexOf(g) >= 0; })) return false;

  // Default: tu choi an toan
  return true;
}

function retrieveChunks(q, topK) {
  topK = topK || 3;
  const ql = q.toLowerCase();
  const qwords = ql.split(/\\s+/).filter(w => w.length >= 2);
  const scored = KB.map(function(chunk) {
    var score = 0;
    chunk.tags.forEach(function(tag) {
      if (ql.indexOf(tag) >= 0) score += 3;
      else if (qwords.some(function(w){ return tag.indexOf(w) >= 0; })) score += 1;
    });
    var cl = chunk.content.toLowerCase();
    qwords.forEach(function(w){ if (cl.indexOf(w) >= 0) score += 0.5; });
    return { score: score, chunk: chunk };
  });
  scored.sort(function(a,b){ return b.score - a.score; });
  var top = scored.slice(0, topK).filter(function(x){ return x.score > 0; }).map(function(x){ return x.chunk; });
  return top.length ? top : [KB[0]];
}

var panel  = document.getElementById('fcw-panel');
var btn    = document.getElementById('fcw-btn');
var badge  = document.getElementById('fcw-badge');
var msgs   = document.getElementById('fcw-msgs');
var inp    = document.getElementById('fcw-input');
var sendBt = document.getElementById('fcw-send');
var isOpen = false;

function togglePanel() {
  isOpen = !isOpen;
  btn.classList.toggle('open', isOpen);
  panel.classList.toggle('open', isOpen);
  if (isOpen) { badge.style.display='none'; inp.focus(); scrollBottom(); }
}
btn.addEventListener('click', togglePanel);

function scrollBottom() {
  setTimeout(function(){ msgs.scrollTop = msgs.scrollHeight; }, 60);
}

function addMsg(role, html) {
  var row = document.createElement('div');
  row.className = 'fcw-msg ' + role;
  if (role === 'bot') {
    row.innerHTML = '<div class="fcw-av-sm">🤖</div><div class="fcw-bubble bot">' + html + '</div>';
  } else {
    row.innerHTML = '<div class="fcw-bubble user">' + html + '</div>';
  }
  msgs.appendChild(row);
  scrollBottom();
}

function showTyping() {
  var row = document.createElement('div');
  row.className = 'fcw-msg bot'; row.id = 'fcw-typing';
  row.innerHTML = '<div class="fcw-av-sm">🤖</div><div class="fcw-bubble bot"><div class="fcw-typing"><div class="fcw-dot"></div><div class="fcw-dot"></div><div class="fcw-dot"></div></div></div>';
  msgs.appendChild(row); scrollBottom();
}
function hideTyping() {
  var t = document.getElementById('fcw-typing');
  if (t) t.remove();
}

function mdRender(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>');
}

async function callOllama(question, context) {
  var sys = 'Ban la tro ly AI tieng Viet cua TikTok Viral Detector. Chi tra loi ve du an. Luon TIENG VIET. Xung minh, goi ban. Ngan gon.\\nCONTEXT:\\n' + context;
  var res = await fetch(OLLAMA_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: MODEL,
      messages: [{ role:'system', content:sys }, { role:'user', content:question }],
      stream: false,
      options: { temperature:0.3, num_predict:400 }
    })
  });
  if (!res.ok) throw new Error('HTTP ' + res.status);
  var data = await res.json();
  return data.message.content.trim();
}

async function fcwSend() {
  var q = inp.value.trim();
  if (!q) return;
  inp.value = '';
  sendBt.disabled = true;
  addMsg('user', q.replace(/</g, '&lt;'));
  showTyping();
  var reply = '';
  try {
    if (isOutScope(q)) {
      reply = 'Mình chỉ hỗ trợ câu hỏi về dự án <strong>TikTok Viral Detector</strong> thôi bạn nhé! 😊';
    } else {
      var chunks = retrieveChunks(q);
      var context = chunks.map(function(c){ return c.content; }).join('\\n---\\n');
      if (OLLAMA_OK) {
        var raw = await callOllama(q, context);
        reply = mdRender(raw);
      } else {
        reply = '📚 <strong>Knowledge base:</strong><br><br>' + mdRender(chunks[0].content) +
                '<br><br><em style="color:rgba(236,234,246,0.4);font-size:0.75rem">⚠️ Ollama offline — rule-based fallback</em>';
      }
    }
  } catch(e) {
    reply = '❌ Lỗi: ' + e.message + '<br><em style="font-size:0.75rem">Kiểm tra <code>ollama serve</code></em>';
  }
  hideTyping();
  addMsg('bot', reply);
  sendBt.disabled = false;
  inp.focus();
}

function fcwAsk(text) {
  inp.value = text.replace(/^[^a-zA-Z\u00C0-\u024F\u1E00-\u1EFF]+/, '').trim();
  fcwSend();
}

inp.addEventListener('keydown', function(e){ if(e.key==='Enter') fcwSend(); });
</script>
"""

# Inject Python values into JS string (safe — no f-string regex conflict)
_js_final = _js.replace('OLLAMA_OK_PY', _ok_js) \
               .replace('MODEL_PY', OLLAMA_MODEL) \
               .replace('P80_PY', f'{P80:.4f}')

st.markdown(_js_final, unsafe_allow_html=True)