import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import copy

st.set_page_config(
    page_title="반도체 섹터 분석",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Syne:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg:       #060612;
    --surface:  #0d0d1f;
    --surface2: #12122a;
    --border:   #1a1a3e;
    --neon:     #7b2fff;
    --neon2:    #00d4ff;
    --neon3:    #ff2d78;
    --green:    #00ffa3;
    --red:      #ff3d5a;
    --text:     #e2e2f5;
    --muted:    #5a5a80;
    --gold:     #f5c518;
}

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}
.stApp {
    background:
        radial-gradient(ellipse at 20% 20%, rgba(123,47,255,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(0,212,255,0.06) 0%, transparent 50%),
        var(--bg);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem 2rem; max-width: 1400px; }

/* ── Hero ── */
.hero {
    position: relative;
    padding: 3rem 0 2rem 0;
    text-align: center;
    overflow: hidden;
}
.hero-chip {
    display: inline-block;
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    color: var(--neon2);
    border: 1px solid rgba(0,212,255,0.3);
    background: rgba(0,212,255,0.06);
    padding: 0.3rem 1rem;
    border-radius: 2px;
    margin-bottom: 1rem;
    text-transform: uppercase;
}
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(2rem, 6vw, 4.5rem);
    font-weight: 900;
    letter-spacing: 0.05em;
    line-height: 1.1;
    margin: 0;
    background: linear-gradient(135deg, var(--neon2) 0%, var(--neon) 50%, var(--neon3) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 0.85rem;
    color: var(--muted);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 0.75rem;
}
.hero-line {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    margin-top: 1.5rem;
}
.hero-line-seg {
    height: 1px;
    width: 60px;
    background: linear-gradient(90deg, transparent, var(--neon));
}
.hero-line-seg.right {
    background: linear-gradient(90deg, var(--neon2), transparent);
}
.hero-line-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--neon2);
    box-shadow: 0 0 8px var(--neon2);
}

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 0.85rem;
    margin: 1.5rem 0;
}
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.1rem 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s, box-shadow 0.25s;
    cursor: default;
}
.metric-card::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(123,47,255,0.04), transparent);
    pointer-events: none;
}
.metric-card:hover {
    border-color: var(--neon);
    box-shadow: 0 0 20px rgba(123,47,255,0.15);
}
.mc-corner {
    position: absolute;
    top: 0; left: 0;
    width: 20px; height: 20px;
    border-top: 2px solid var(--neon2);
    border-left: 2px solid var(--neon2);
    border-radius: 2px 0 0 0;
}
.mc-corner.br {
    top: auto; left: auto;
    bottom: 0; right: 0;
    border-top: none; border-left: none;
    border-bottom: 2px solid var(--neon);
    border-right: 2px solid var(--neon);
    border-radius: 0 0 2px 0;
}
.mc-region {
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--neon2);
    margin-bottom: 0.5rem;
    font-family: 'Orbitron', monospace;
}
.mc-region.us { color: var(--neon3); }
.mc-name {
    font-size: 0.78rem;
    color: var(--muted);
    margin-bottom: 0.25rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.mc-ticker {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--neon);
    margin-bottom: 0.4rem;
}
.mc-price {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text);
    line-height: 1;
}
.mc-change-up {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--green);
    margin-top: 0.35rem;
}
.mc-change-dn {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--red);
    margin-top: 0.35rem;
}

/* ── Section Header ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2.5rem 0 1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}
.sec-head-bar {
    width: 3px; height: 1.2rem;
    background: linear-gradient(180deg, var(--neon2), var(--neon));
    border-radius: 2px;
    flex-shrink: 0;
}
.sec-head-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.9rem;
    letter-spacing: 0.15em;
    color: var(--text);
    text-transform: uppercase;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
.sb-logo {
    font-family: 'Orbitron', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    background: linear-gradient(135deg, var(--neon2), var(--neon));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.15rem;
}
.sb-sub {
    font-size: 0.6rem;
    color: var(--muted);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.sb-div { height: 1px; background: var(--border); margin: 1.2rem 0; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface2);
    border-radius: 6px;
    padding: 3px;
    gap: 3px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Syne', sans-serif;
    font-size: 0.82rem;
    letter-spacing: 0.05em;
    color: var(--muted);
    border-radius: 5px;
    padding: 0.45rem 1rem;
}
.stTabs [aria-selected="true"] {
    background: var(--border) !important;
    color: var(--neon2) !important;
}

/* ── Info box ── */
.info-box {
    background: rgba(0,212,255,0.04);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-size: 0.85rem;
    color: var(--muted);
}

/* ── Supply chain badge ── */
.chain-badge {
    display: inline-block;
    font-size: 0.6rem;
    font-family: 'Orbitron', monospace;
    letter-spacing: 0.1em;
    padding: 0.12rem 0.5rem;
    border-radius: 3px;
    margin-left: 0.4rem;
    vertical-align: middle;
}
.chain-fab    { background: rgba(123,47,255,0.15); color: var(--neon);  border: 1px solid rgba(123,47,255,0.3); }
.chain-design { background: rgba(0,212,255,0.12);  color: var(--neon2); border: 1px solid rgba(0,212,255,0.25); }
.chain-equip  { background: rgba(245,197,24,0.1);  color: var(--gold);  border: 1px solid rgba(245,197,24,0.25); }
.chain-mem    { background: rgba(0,255,163,0.1);   color: var(--green); border: 1px solid rgba(0,255,163,0.25); }
.chain-mat    { background: rgba(255,45,120,0.1);  color: var(--neon3); border: 1px solid rgba(255,45,120,0.25); }
</style>
""", unsafe_allow_html=True)

# ── 반도체 종목 정의 ────────────────────────────────────────────────────────────
KR_SEMI = {
    "삼성전자":    ("005930.KS", "mem",    "메모리·파운드리"),
    "SK하이닉스":  ("000660.KS", "mem",    "메모리"),
    "DB하이텍":    ("000990.KS", "fab",    "파운드리"),
    "리노공업":    ("058470.KS", "equip",  "반도체 소켓"),
    "원익IPS":     ("240810.KS", "equip",  "증착장비"),
    "HPSP":        ("403870.KS", "equip",  "고압수소소결"),
    "한미반도체":  ("042700.KS", "equip",  "패키징장비"),
    "이오테크닉스":("039030.KS", "equip",  "레이저장비"),
    "솔브레인":    ("357780.KS", "mat",    "소재·케미컬"),
    "동진쎄미켐":  ("005290.KS", "mat",    "포토레지스트"),
    "SK머티리얼즈":("036490.KS", "mat",    "특수가스"),
}

US_SEMI = {
    "NVIDIA":      ("NVDA",   "design", "GPU·AI칩"),
    "TSMC":        ("TSM",    "fab",    "파운드리"),
    "ASML":        ("ASML",   "equip",  "노광장비"),
    "Broadcom":    ("AVGO",   "design", "네트워크칩"),
    "Qualcomm":    ("QCOM",   "design", "모바일AP"),
    "Intel":       ("INTC",   "fab",    "CPU·파운드리"),
    "AMD":         ("AMD",    "design", "CPU·GPU"),
    "Applied Mat": ("AMAT",   "equip",  "증착·식각"),
    "Lam Research":("LRCX",   "equip",  "식각장비"),
    "KLA Corp":    ("KLAC",   "equip",  "검사장비"),
    "Micron":      ("MU",     "mem",    "메모리"),
    "ON Semi":     ("ON",     "design", "전력반도체"),
    "SOXX ETF":    ("SOXX",   "design", "반도체ETF"),
    "SMH ETF":     ("SMH",    "design", "반도체ETF"),
}

CHAIN_LABEL = {
    "fab":    ("FAB", "chain-fab"),
    "design": ("DESIGN", "chain-design"),
    "equip":  ("EQUIP", "chain-equip"),
    "mem":    ("MEM", "chain-mem"),
    "mat":    ("MAT", "chain-mat"),
}

PERIOD_MAP = {
    "1주": "5d", "1개월": "1mo", "3개월": "3mo",
    "6개월": "6mo", "1년": "1y", "2년": "2y", "5년": "5y",
}

COLOR_PALETTE = [
    "#00d4ff", "#7b2fff", "#ff2d78", "#00ffa3", "#f5c518",
    "#ff8c42", "#a78bfa", "#34d399", "#f87171", "#60a5fa",
    "#fbbf24", "#c084fc",
]

# ── Helpers ───────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch(ticker, period):
    try:
        df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except Exception:
        return pd.DataFrame()

def calc_ret(df):
    if df.empty or len(df) < 2:
        return None
    try:
        return (float(df["Close"].dropna().iloc[-1]) - float(df["Close"].dropna().iloc[0])) \
               / float(df["Close"].dropna().iloc[0]) * 100
    except Exception:
        return None

def norm(df):
    s = df["Close"].dropna()
    return (s / s.iloc[0]) * 100

def fmt(v):
    if v is None: return "N/A"
    return f"{'+'if v>=0 else ''}{v:.2f}%"

def base_layout(**kw):
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Syne, sans-serif", color="#e2e2f5", size=12),
        xaxis=dict(gridcolor="#1a1a3e", showgrid=True,
                   tickfont=dict(size=10, color="#5a5a80"), linecolor="#1a1a3e"),
        yaxis=dict(gridcolor="#1a1a3e", showgrid=True,
                   tickfont=dict(size=10, color="#5a5a80"), linecolor="#1a1a3e"),
        legend=dict(bgcolor="rgba(13,13,31,0.85)", bordercolor="#1a1a3e",
                    borderwidth=1, font=dict(size=11)),
        hovermode="x unified",
        margin=dict(l=10, r=10, t=45, b=10),
    )
    layout.update(kw)
    return layout

def chain_badge(code):
    label, cls = CHAIN_LABEL.get(code, ("ETC", "chain-design"))
    return f'<span class="chain-badge {cls}">{label}</span>'

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-logo">⬡ SEMI LENS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">Semiconductor Sector Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)

    st.markdown("**🇰🇷 한국 반도체**")
    kr_sel = st.multiselect("KR", list(KR_SEMI.keys()),
                             default=["삼성전자", "SK하이닉스", "한미반도체", "리노공업"],
                             label_visibility="collapsed")

    st.markdown("**🇺🇸 미국 반도체**")
    us_sel = st.multiselect("US", list(US_SEMI.keys()),
                             default=["NVIDIA", "TSMC", "ASML", "SOXX ETF"],
                             label_visibility="collapsed")

    st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)

    period_label = st.selectbox("📅 기간", list(PERIOD_MAP.keys()), index=3)
    period = PERIOD_MAP[period_label]

    st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)

    chart_mode = st.radio("📊 메인 차트",
                          ["정규화 수익률", "캔들스틱", "수익률 바차트"], index=0)
    show_vol = st.checkbox("거래량 표시", value=True)
    show_ma  = st.checkbox("이동평균선(MA)", value=True)

    st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)

    chain_filter = st.multiselect(
        "🔗 공급망 필터",
        ["FAB (파운드리)", "DESIGN (팹리스)", "EQUIP (장비)", "MEM (메모리)", "MAT (소재)"],
        default=[]
    )
    st.markdown('<div style="font-size:0.65rem;color:#5a5a80;line-height:1.7;margin-top:0.5rem;">'
                '데이터: Yahoo Finance<br>캐시: 5분<br>⚠️ 투자 참고용만</div>', unsafe_allow_html=True)

# ── Chain filter map ──────────────────────────────────────────────────────────
FILTER_MAP = {
    "FAB (파운드리)": "fab", "DESIGN (팹리스)": "design",
    "EQUIP (장비)": "equip", "MEM (메모리)": "mem", "MAT (소재)": "mat",
}
active_chains = [FILTER_MAP[f] for f in chain_filter] if chain_filter else None

def passes_chain(code):
    if not active_chains:
        return True
    return code in active_chains

# Build master list
all_stocks = []
for name in kr_sel:
    ticker, chain, desc = KR_SEMI[name]
    if passes_chain(chain):
        all_stocks.append((name, ticker, "KR", chain, desc))
for name in us_sel:
    ticker, chain, desc = US_SEMI[name]
    if passes_chain(chain):
        all_stocks.append((name, ticker, "US", chain, desc))

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-chip">⬡ Semiconductor Sector · Global Analysis</div>
    <div class="hero-title">SEMI LENS</div>
    <div class="hero-sub">한국 · 미국 반도체 공급망 실시간 분석 플랫폼</div>
    <div class="hero-line">
        <div class="hero-line-seg"></div>
        <div class="hero-line-dot"></div>
        <div class="hero-line-seg right"></div>
    </div>
</div>
""", unsafe_allow_html=True)

if not all_stocks:
    st.markdown('<div class="info-box">👈 사이드바에서 종목을 선택하세요. 공급망 필터를 모두 해제하면 전체 종목이 표시됩니다.</div>',
                unsafe_allow_html=True)
    st.stop()

# ── Fetch ─────────────────────────────────────────────────────────────────────
with st.spinner("⚡ 반도체 시장 데이터 수신 중..."):
    stock_data = {name: fetch(ticker, period) for name, ticker, *_ in all_stocks}

# ── Metric Cards ──────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head"><div class="sec-head-bar"></div><div class="sec-head-title">시세 스냅샷</div></div>',
            unsafe_allow_html=True)

cards = '<div class="metric-grid">'
for name, ticker, market, chain, desc in all_stocks:
    df  = stock_data.get(name, pd.DataFrame())
    ret = calc_ret(df)
    region_cls = "" if market == "KR" else " us"
    region_txt = "🇰🇷 KR" if market == "KR" else "🇺🇸 US"
    cl, cb = CHAIN_LABEL.get(chain, ("ETC", "chain-design"))

    if not df.empty and "Close" in df.columns:
        lp = float(df["Close"].dropna().iloc[-1])
        cur = "₩" if market == "KR" else "$"
        pstr = f"{lp:,.0f}" if (market == "KR" and lp > 1000) else f"{lp:,.2f}"
        price_disp = f"{cur}{pstr}"
    else:
        price_disp = "N/A"

    if ret is not None:
        cc = "mc-change-up" if ret >= 0 else "mc-change-dn"
        arrow = "▲" if ret >= 0 else "▼"
        ch_html = f'<div class="{cc}">{arrow} {abs(ret):.2f}% <span style="font-size:0.65rem;opacity:0.6">{period_label}</span></div>'
    else:
        ch_html = '<div class="mc-change-up" style="color:#5a5a80">N/A</div>'

    cards += f"""
    <div class="metric-card">
        <div class="mc-corner"></div>
        <div class="mc-corner br"></div>
        <div class="mc-region{region_cls}">{region_txt} <span class="chain-badge {cb}">{cl}</span></div>
        <div class="mc-name">{name}</div>
        <div class="mc-ticker">{ticker}</div>
        <div class="mc-price">{price_disp}</div>
        {ch_html}
        <div style="font-size:0.62rem;color:#5a5a80;margin-top:0.3rem">{desc}</div>
    </div>"""
cards += "</div>"
st.markdown(cards, unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head"><div class="sec-head-bar"></div><div class="sec-head-title">차트 분석</div></div>',
            unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📈 메인 차트", "📊 수익률 비교", "🔗 공급망 히트맵", "🔍 개별 상세"])

# ── Tab1 ──────────────────────────────────────────────────────────────────────
with tab1:
    if chart_mode == "정규화 수익률":
        fig = go.Figure()
        for i, (name, ticker, market, chain, desc) in enumerate(all_stocks):
            df = stock_data.get(name, pd.DataFrame())
            if df.empty or "Close" not in df.columns:
                continue
            ns = norm(df)
            dash = "dot" if market == "KR" else "solid"
            fig.add_trace(go.Scatter(
                x=ns.index, y=ns.values,
                name=f"{'🇰🇷' if market=='KR' else '🇺🇸'} {name}",
                line=dict(color=COLOR_PALETTE[i % len(COLOR_PALETTE)], width=2, dash=dash),
                hovertemplate=f"<b>{name}</b><br>%{{x|%Y-%m-%d}}<br>%{{y:.1f}}<extra></extra>",
            ))
        fig.add_hline(y=100, line_dash="dash", line_color="#5a5a80", line_width=1)
        fig.update_layout(**base_layout(
            title=dict(text=f"정규화 수익률 비교 (시작=100) · {period_label}",
                       font=dict(size=13, family="Orbitron, monospace", color="#e2e2f5"), x=0.01),
            yaxis_title="정규화 (시작=100)", height=520,
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("🇰🇷 점선 = 한국 · 🇺🇸 실선 = 미국")

    elif chart_mode == "캔들스틱":
        sel = st.selectbox("종목", [n for n, *_ in all_stocks])
        sel_info = next((t, m) for n, t, m, *_ in all_stocks if n == sel)
        df = stock_data.get(sel, pd.DataFrame())
        if not df.empty and all(c in df.columns for c in ["Open","High","Low","Close"]):
            rows = 2 if (show_vol and "Volume" in df.columns) else 1
            fig = make_subplots(rows=rows, cols=1, shared_xaxes=True,
                                vertical_spacing=0.03,
                                row_heights=[0.75, 0.25] if rows == 2 else [1])
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df["Open"].squeeze(), high=df["High"].squeeze(),
                low=df["Low"].squeeze(),  close=df["Close"].squeeze(),
                name=sel,
                increasing=dict(fillcolor="#00ffa3", line=dict(color="#00ffa3")),
                decreasing=dict(fillcolor="#ff3d5a", line=dict(color="#ff3d5a")),
            ), row=1, col=1)
            if rows == 2:
                cv = ["#00ffa3" if float(c) >= float(o) else "#ff3d5a"
                      for c, o in zip(df["Close"].squeeze(), df["Open"].squeeze())]
                fig.add_trace(go.Bar(x=df.index, y=df["Volume"].squeeze(),
                                     marker_color=cv, opacity=0.6, name="거래량"), row=2, col=1)
            fig.update_layout(**base_layout(
                title=dict(text=f"{sel} 캔들스틱 · {period_label}",
                           font=dict(size=13, family="Orbitron, monospace", color="#e2e2f5"), x=0.01),
                xaxis_rangeslider_visible=False,
                height=580 if rows == 2 else 460,
            ))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("데이터 없음")

    else:  # 바차트
        rows = [(n, calc_ret(stock_data.get(n, pd.DataFrame())), m)
                for n, _, m, *_ in all_stocks
                if calc_ret(stock_data.get(n, pd.DataFrame())) is not None]
        if rows:
            rows.sort(key=lambda x: x[1])
            fig = go.Figure(go.Bar(
                x=[r[1] for r in rows],
                y=[f"{'🇰🇷' if r[2]=='KR' else '🇺🇸'} {r[0]}" for r in rows],
                orientation="h",
                marker=dict(
                    color=[r[1] for r in rows],
                    colorscale=[[0,"#ff3d5a"],[0.5,"#1a1a3e"],[1,"#00ffa3"]],
                    cmid=0, showscale=True,
                    colorbar=dict(title="수익률%", tickfont=dict(size=9, color="#5a5a80")),
                ),
                text=[fmt(r[1]) for r in rows],
                textposition="outside",
                textfont=dict(size=11, color="#e2e2f5"),
                hovertemplate="<b>%{y}</b><br>%{x:.2f}%<extra></extra>",
            ))
            fig.add_vline(x=0, line_color="#5a5a80", line_width=1)
            fig.update_layout(**base_layout(
                title=dict(text=f"수익률 바차트 · {period_label}",
                           font=dict(size=13, family="Orbitron, monospace", color="#e2e2f5"), x=0.01),
                xaxis_title="수익률 (%)",
                height=max(380, len(rows) * 44 + 80),
            ))
            st.plotly_chart(fig, use_container_width=True)

# ── Tab2 ──────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("#### 다기간 수익률 테이블")
    periods_cmp = {"1주":"5d","1개월":"1mo","3개월":"3mo","6개월":"6mo","1년":"1y"}
    tbl = []
    with st.spinner("계산 중..."):
        for name, ticker, market, chain, desc in all_stocks:
            cl, cb = CHAIN_LABEL.get(chain, ("ETC","chain-design"))
            row = {"시장": "🇰🇷" if market=="KR" else "🇺🇸",
                   "공급망": cl, "종목": name, "티커": ticker, "분류": desc}
            for pl, pc in periods_cmp.items():
                row[pl] = fmt(calc_ret(fetch(ticker, pc)))
            tbl.append(row)
    df_tbl = pd.DataFrame(tbl)
    st.dataframe(df_tbl.set_index("티커"), use_container_width=True,
                 height=min(500, 45 + len(tbl) * 36))

    # 산점도: 1개월 vs 3개월
    st.markdown("#### 수익률 산점도 (1개월 vs 3개월)")
    scatter_data = []
    for name, ticker, market, chain, desc in all_stocks:
        r1 = calc_ret(fetch(ticker, "1mo"))
        r3 = calc_ret(fetch(ticker, "3mo"))
        if r1 is not None and r3 is not None:
            cl, _ = CHAIN_LABEL.get(chain, ("ETC",""))
            scatter_data.append({"name": name, "r1": r1, "r3": r3,
                                  "market": market, "chain": cl})
    if scatter_data:
        fig_sc = go.Figure()
        chain_colors = {"FAB":"#7b2fff","DESIGN":"#00d4ff","EQUIP":"#f5c518",
                        "MEM":"#00ffa3","MAT":"#ff2d78","ETC":"#aaaaaa"}
        for item in scatter_data:
            cc = chain_colors.get(item["chain"], "#aaaaaa")
            fig_sc.add_trace(go.Scatter(
                x=[item["r1"]], y=[item["r3"]],
                mode="markers+text",
                name=item["chain"],
                text=[f"{'🇰🇷' if item['market']=='KR' else '🇺🇸'}{item['name']}"],
                textposition="top center",
                textfont=dict(size=9, color="#e2e2f5"),
                marker=dict(size=12, color=cc,
                            line=dict(color="rgba(255,255,255,0.3)", width=1),
                            symbol="circle" if item["market"]=="US" else "diamond"),
                showlegend=False,
                hovertemplate=f"<b>{item['name']}</b><br>1개월: {fmt(item['r1'])}<br>3개월: {fmt(item['r3'])}<extra></extra>",
            ))
        fig_sc.add_hline(y=0, line_dash="dash", line_color="#5a5a80", line_width=1)
        fig_sc.add_vline(x=0, line_dash="dash", line_color="#5a5a80", line_width=1)
        fig_sc.update_layout(**base_layout(
            title=dict(text="수익률 포지셔닝 (◆=KR · ●=US)",
                       font=dict(size=13, family="Orbitron, monospace", color="#e2e2f5"), x=0.01),
            xaxis_title="1개월 수익률 (%)",
            yaxis_title="3개월 수익률 (%)",
            height=480,
        ))
        st.plotly_chart(fig_sc, use_container_width=True)

# ── Tab3 ─────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("#### 공급망별 히트맵")
    periods_h = {"1주":"5d","1개월":"1mo","3개월":"3mo","6개월":"6mo","1년":"1y"}
    heat_names, heat_data = [], []
    with st.spinner("히트맵 생성 중..."):
        for name, ticker, market, chain, desc in all_stocks:
            cl, _ = CHAIN_LABEL.get(chain, ("ETC",""))
            heat_names.append(f"{'🇰🇷' if market=='KR' else '🇺🇸'} [{cl}] {name}")
            heat_data.append([calc_ret(fetch(ticker, pc)) for pc in periods_h.values()])

    heat_arr  = np.array([[v if v is not None else 0 for v in r] for r in heat_data])
    text_arr  = [[fmt(v) for v in r] for r in heat_data]

    fig_heat = go.Figure(go.Heatmap(
        z=heat_arr, x=list(periods_h.keys()), y=heat_names,
        text=text_arr, texttemplate="%{text}", textfont=dict(size=10),
        colorscale=[[0,"#ff3d5a"],[0.35,"#1a1a3e"],[0.5,"#12122a"],
                    [0.65,"#0d1f1a"],[1,"#00ffa3"]],
        zmid=0, showscale=True,
        colorbar=dict(title="수익률%", tickfont=dict(size=9, color="#5a5a80")),
        hovertemplate="<b>%{y}</b><br>기간: %{x}<br>수익률: %{text}<extra></extra>",
    ))
    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Syne, sans-serif", color="#e2e2f5", size=12),
        legend=dict(bgcolor="rgba(13,13,31,0.85)", bordercolor="#1a1a3e", borderwidth=1),
        hovermode="x unified",
        margin=dict(l=10, r=10, t=45, b=10),
        title=dict(text="공급망 포지션별 다기간 수익률 히트맵",
                   font=dict(size=13, family="Orbitron, monospace", color="#e2e2f5"), x=0.01),
        height=max(320, len(heat_names) * 42 + 100),
        xaxis=dict(side="top", gridcolor="#1a1a3e",
                   tickfont=dict(size=10, color="#5a5a80"), linecolor="#1a1a3e"),
        yaxis=dict(gridcolor="#1a1a3e",
                   tickfont=dict(size=10, color="#5a5a80"), linecolor="#1a1a3e"),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    # 공급망 포지션별 평균 수익률 바
    st.markdown("#### 공급망 포지션별 평균 수익률")
    chain_avg = {}
    for name, ticker, market, chain, desc in all_stocks:
        r = calc_ret(stock_data.get(name, pd.DataFrame()))
        if r is not None:
            chain_avg.setdefault(chain, []).append(r)
    if chain_avg:
        ch_labels = [CHAIN_LABEL[c][0] for c in chain_avg]
        ch_vals   = [np.mean(v) for v in chain_avg.values()]
        fig_ca = go.Figure(go.Bar(
            x=ch_labels, y=ch_vals,
            marker=dict(
                color=ch_vals,
                colorscale=[[0,"#ff3d5a"],[0.5,"#1a1a3e"],[1,"#00ffa3"]],
                cmid=0,
            ),
            text=[fmt(v) for v in ch_vals],
            textposition="outside",
            textfont=dict(size=12, color="#e2e2f5"),
            hovertemplate="<b>%{x}</b><br>평균: %{y:.2f}%<extra></extra>",
        ))
        fig_ca.add_hline(y=0, line_dash="dash", line_color="#5a5a80", line_width=1)
        fig_ca.update_layout(**base_layout(
            title=dict(text=f"공급망 포지션 평균 수익률 · {period_label}",
                       font=dict(size=13, family="Orbitron, monospace", color="#e2e2f5"), x=0.01),
            yaxis_title="평균 수익률 (%)", height=340,
        ))
        st.plotly_chart(fig_ca, use_container_width=True)

# ── Tab4 ──────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("#### 개별 종목 상세")
    detail_name = st.selectbox("종목 선택", [n for n, *_ in all_stocks], key="detail")
    detail_info = next((t, m, ch, d) for n, t, m, ch, d in all_stocks if n == detail_name)
    d_ticker, d_market, d_chain, d_desc = detail_info
    df_d = stock_data.get(detail_name, pd.DataFrame())
    currency = "₩" if d_market == "KR" else "$"
    cl, cb = CHAIN_LABEL.get(d_chain, ("ETC","chain-design"))

    st.markdown(f'**{detail_name}** &nbsp; <span class="chain-badge {cb}">{cl}</span> &nbsp;'
                f'<span style="color:#5a5a80;font-size:0.85rem">{d_desc} · {d_ticker}</span>',
                unsafe_allow_html=True)

    if not df_d.empty and "Close" in df_d.columns:
        close_s = df_d["Close"].squeeze()
        ret_d   = calc_ret(df_d)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("현재가", f"{currency}{float(close_s.iloc[-1]):,.2f}")
        with c2: st.metric(f"{period_label} 수익률", fmt(ret_d),
                            delta=f"{ret_d:.2f}%" if ret_d else None)
        with c3:
            if "High" in df_d.columns:
                st.metric("기간 최고가", f"{currency}{float(df_d['High'].max()):,.2f}")
        with c4:
            if "Low" in df_d.columns:
                st.metric("기간 최저가", f"{currency}{float(df_d['Low'].min()):,.2f}")

        # 가격 + MA 차트
        fig_d = go.Figure()
        fig_d.add_trace(go.Scatter(
            x=close_s.index, y=close_s.values,
            fill="tozeroy", fillcolor="rgba(0,212,255,0.06)",
            line=dict(color="#00d4ff", width=2), name=detail_name,
            hovertemplate=f"<b>{detail_name}</b><br>%{{x|%Y-%m-%d}}<br>{currency}%{{y:,.2f}}<extra></extra>",
        ))
        if show_ma:
            if len(close_s) >= 20:
                fig_d.add_trace(go.Scatter(
                    x=close_s.rolling(20).mean().index,
                    y=close_s.rolling(20).mean().values,
                    name="MA20", line=dict(color="#f5c518", width=1.5, dash="dot")))
            if len(close_s) >= 60:
                fig_d.add_trace(go.Scatter(
                    x=close_s.rolling(60).mean().index,
                    y=close_s.rolling(60).mean().values,
                    name="MA60", line=dict(color="#ff2d78", width=1.5, dash="dot")))
            if len(close_s) >= 120:
                fig_d.add_trace(go.Scatter(
                    x=close_s.rolling(120).mean().index,
                    y=close_s.rolling(120).mean().values,
                    name="MA120", line=dict(color="#7b2fff", width=1.5, dash="dot")))
        fig_d.update_layout(**base_layout(
            title=dict(text=f"{detail_name} 주가 추이",
                       font=dict(size=13, family="Orbitron, monospace", color="#e2e2f5"), x=0.01),
            yaxis_title=f"주가 ({currency})", height=420,
        ))
        st.plotly_chart(fig_d, use_container_width=True)

        # 볼린저밴드
        if len(close_s) >= 20:
            ma20 = close_s.rolling(20).mean()
            std20 = close_s.rolling(20).std()
            upper = ma20 + 2 * std20
            lower = ma20 - 2 * std20
            fig_bb = go.Figure()
            fig_bb.add_trace(go.Scatter(
                x=upper.index, y=upper.values, name="Upper Band",
                line=dict(color="rgba(123,47,255,0.5)", width=1), showlegend=True))
            fig_bb.add_trace(go.Scatter(
                x=lower.index, y=lower.values, name="Lower Band",
                fill="tonexty", fillcolor="rgba(123,47,255,0.05)",
                line=dict(color="rgba(123,47,255,0.5)", width=1)))
            fig_bb.add_trace(go.Scatter(
                x=close_s.index, y=close_s.values,
                name=detail_name, line=dict(color="#00d4ff", width=2)))
            fig_bb.update_layout(**base_layout(
                title=dict(text="볼린저밴드 (20일)",
                           font=dict(size=13, family="Orbitron, monospace", color="#e2e2f5"), x=0.01),
                yaxis_title=f"주가 ({currency})", height=320,
            ))
            st.plotly_chart(fig_bb, use_container_width=True)

        # 거래량
        if show_vol and "Volume" in df_d.columns:
            vol_s = df_d["Volume"].squeeze()
            fig_v = go.Figure(go.Bar(
                x=vol_s.index, y=vol_s.values,
                marker_color="#7b2fff", opacity=0.65, name="거래량"))
            fig_v.update_layout(**base_layout(
                title=dict(text="거래량",
                           font=dict(size=12, family="Orbitron, monospace", color="#e2e2f5"), x=0.01),
                height=190, showlegend=False,
            ))
            st.plotly_chart(fig_v, use_container_width=True)
    else:
        st.warning(f"{detail_name} 데이터를 불러올 수 없습니다.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2.5rem 0 1rem;border-top:1px solid #1a1a3e;margin-top:3rem;">
    <span style="font-family:'Orbitron',monospace;font-size:1rem;letter-spacing:0.15em;
        background:linear-gradient(135deg,#00d4ff,#7b2fff);-webkit-background-clip:text;
        -webkit-text-fill-color:transparent;background-clip:text;">⬡ SEMI LENS</span>
    <div style="font-size:0.65rem;color:#5a5a80;margin-top:0.5rem;letter-spacing:0.15em;">
        DATA BY YAHOO FINANCE · SEMICONDUCTOR SECTOR ANALYSIS · NOT FINANCIAL ADVICE
    </div>
</div>
""", unsafe_allow_html=True)
