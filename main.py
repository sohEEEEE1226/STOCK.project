import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StockLens | 글로벌 주식 분석",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg:        #0a0a0f;
    --surface:   #111118;
    --border:    #1e1e2e;
    --accent:    #00e5ff;
    --accent2:   #ff6b6b;
    --green:     #00e676;
    --red:       #ff5252;
    --text:      #e8e8f0;
    --muted:     #6b6b85;
    --gold:      #ffd700;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}
.stApp { background: var(--bg); }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem 2rem; max-width: 1400px; }

.hero-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
    position: relative;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 8vw, 6rem);
    letter-spacing: 0.08em;
    background: linear-gradient(135deg, var(--accent) 0%, var(--gold) 50%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 0;
}
.hero-sub {
    font-size: 0.95rem;
    color: var(--muted);
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}
.hero-line {
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--gold));
    margin: 1rem auto 0;
    border-radius: 2px;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent);
}
.metric-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
}
.metric-label {
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.metric-ticker {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--accent);
    font-weight: 600;
    margin-bottom: 0.2rem;
}
.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.4rem;
    font-weight: 600;
    color: var(--text);
    line-height: 1;
}
.metric-change-pos {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: var(--green);
    margin-top: 0.3rem;
}
.metric-change-neg {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: var(--red);
    margin-top: 0.3rem;
}
.badge-kr {
    display: inline-block;
    font-size: 0.6rem;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    background: rgba(0, 229, 255, 0.1);
    color: var(--accent);
    border: 1px solid rgba(0, 229, 255, 0.3);
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}
.badge-us {
    display: inline-block;
    font-size: 0.6rem;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    background: rgba(255, 107, 107, 0.1);
    color: var(--accent2);
    border: 1px solid rgba(255, 107, 107, 0.3);
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}
.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    letter-spacing: 0.1em;
    color: var(--text);
    margin: 0;
}
.section-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--accent);
    flex-shrink: 0;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label {
    color: var(--muted) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
.sidebar-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 0.1em;
    background: linear-gradient(135deg, var(--accent), var(--gold));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
}
.sidebar-version {
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.sidebar-divider {
    height: 1px;
    background: var(--border);
    margin: 1.5rem 0;
}

.stSpinner > div { border-top-color: var(--accent) !important; }

.info-box {
    background: rgba(0,229,255,0.06);
    border: 1px solid rgba(0,229,255,0.2);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.85rem;
    color: var(--muted);
    margin: 1rem 0;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--surface);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    color: var(--muted);
    border-radius: 8px;
    padding: 0.5rem 1rem;
}
.stTabs [aria-selected="true"] {
    background: var(--border) !important;
    color: var(--accent) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Stock Definitions ──────────────────────────────────────────────────────────
KR_STOCKS = {
    "삼성전자":    "005930.KS",
    "SK하이닉스":  "000660.KS",
    "LG에너지솔루션": "373220.KS",
    "현대차":      "005380.KS",
    "카카오":      "035720.KS",
    "NAVER":      "035420.KS",
    "셀트리온":    "068270.KS",
    "기아":        "000270.KS",
    "POSCO홀딩스": "005490.KS",
    "KB금융":      "105560.KS",
    "KOSPI":       "^KS11",
}

US_STOCKS = {
    "Apple":      "AAPL",
    "Microsoft":  "MSFT",
    "NVIDIA":     "NVDA",
    "Amazon":     "AMZN",
    "Alphabet":   "GOOGL",
    "Meta":       "META",
    "Tesla":      "TSLA",
    "Berkshire":  "BRK-B",
    "S&P 500":    "^GSPC",
    "NASDAQ":     "^IXIC",
    "Dow Jones":  "^DJI",
}

PERIOD_MAP = {
    "1주": "5d",
    "1개월": "1mo",
    "3개월": "3mo",
    "6개월": "6mo",
    "1년": "1y",
    "2년": "2y",
    "5년": "5y",
}

COLOR_PALETTE = [
    "#00e5ff", "#ffd700", "#ff6b6b", "#00e676", "#b388ff",
    "#ff80ab", "#69f0ae", "#ffab40", "#40c4ff", "#ea80fc",
    "#f06292", "#aed581",
]

# ── Helpers ───────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_stock_data(ticker: str, period: str) -> pd.DataFrame:
    try:
        df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_info(ticker: str) -> dict:
    try:
        info = yf.Ticker(ticker).fast_info
        return {
            "last_price": getattr(info, "last_price", None),
            "previous_close": getattr(info, "previous_close", None),
        }
    except Exception:
        return {}

def calc_return(df: pd.DataFrame):
    if df.empty or len(df) < 2:
        return None
    try:
        first = float(df["Close"].dropna().iloc[0])
        last  = float(df["Close"].dropna().iloc[-1])
        return (last - first) / first * 100
    except Exception:
        return None

def normalize_series(df: pd.DataFrame) -> pd.Series:
    s = df["Close"].dropna()
    return (s / s.iloc[0]) * 100

def fmt_return(v) -> str:
    if v is None:
        return "N/A"
    sign = "+" if v >= 0 else ""
    return f"{sign}{v:.2f}%"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">StockLens</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-version">Global Market Analyzer v1.0</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown("**🇰🇷 한국 주식 선택**")
    kr_selected = st.multiselect(
        "한국 종목",
        options=list(KR_STOCKS.keys()),
        default=["삼성전자", "SK하이닉스", "KOSPI"],
        label_visibility="collapsed",
    )

    st.markdown("**🇺🇸 미국 주식 선택**")
    us_selected = st.multiselect(
        "미국 종목",
        options=list(US_STOCKS.keys()),
        default=["Apple", "NVIDIA", "S&P 500"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    period_label = st.selectbox(
        "📅 기간",
        options=list(PERIOD_MAP.keys()),
        index=3,
    )
    period = PERIOD_MAP[period_label]

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    chart_type = st.radio(
        "📊 차트 타입",
        ["수익률 비교 (정규화)", "캔들스틱", "수익률 바 차트"],
        index=0,
    )

    show_volume = st.checkbox("거래량 표시", value=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.7rem;color:#6b6b85;line-height:1.6;">'
        '데이터: Yahoo Finance<br>갱신: 5분 캐시<br>'
        '⚠️ 투자 참고용으로만 사용하세요</div>',
        unsafe_allow_html=True
    )

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-title">StockLens</div>
    <div class="hero-sub">한국 · 미국 글로벌 주식 실시간 비교 분석</div>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# ── Gather selection ──────────────────────────────────────────────────────────
all_selected = []
for name in kr_selected:
    all_selected.append((name, KR_STOCKS[name], "KR"))
for name in us_selected:
    all_selected.append((name, US_STOCKS[name], "US"))

if not all_selected:
    st.markdown('<div class="info-box">👈 왼쪽 사이드바에서 종목을 선택하세요.</div>', unsafe_allow_html=True)
    st.stop()

# ── Fetch data ────────────────────────────────────────────────────────────────
with st.spinner("📡 시장 데이터 불러오는 중..."):
    stock_data = {}
    for name, ticker, _ in all_selected:
        stock_data[name] = fetch_stock_data(ticker, period)

# ── Metric Cards ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header"><div class="section-dot"></div><div class="section-title">현재 시세 스냅샷</div></div>', unsafe_allow_html=True)

cards_html = '<div class="metric-grid">'
for name, ticker, market in all_selected:
    df = stock_data.get(name, pd.DataFrame())
    ret = calc_return(df)
    badge = f'<span class="badge-kr">🇰🇷 KR</span>' if market == "KR" else f'<span class="badge-us">🇺🇸 US</span>'

    if not df.empty and "Close" in df.columns:
        last_price = float(df["Close"].dropna().iloc[-1])
        currency = "₩" if market == "KR" else "$"
        if market == "KR" and last_price > 10000:
            price_str = f"{last_price:,.0f}"
        else:
            price_str = f"{last_price:,.2f}"
        price_display = f"{currency}{price_str}"
    else:
        price_display = "N/A"

    if ret is not None:
        ch_class = "metric-change-pos" if ret >= 0 else "metric-change-neg"
        sign = "▲" if ret >= 0 else "▼"
        ch_html = f'<div class="{ch_class}">{sign} {abs(ret):.2f}%</div>'
    else:
        ch_html = '<div class="metric-change-pos">N/A</div>'

    cards_html += f"""
    <div class="metric-card">
        {badge}
        <div class="metric-ticker">{ticker}</div>
        <div class="metric-label">{name}</div>
        <div class="metric-value">{price_display}</div>
        {ch_html}
        <div class="metric-label" style="margin-top:0.3rem">{period_label} 수익률</div>
    </div>"""

cards_html += "</div>"
st.markdown(cards_html, unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header"><div class="section-dot" style="background:var(--gold)"></div><div class="section-title">차트 분석</div></div>', unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#e8e8f0", size=12),
    xaxis=dict(
        gridcolor="#1e1e2e", showgrid=True,
        tickfont=dict(size=10, color="#6b6b85"),
        linecolor="#1e1e2e",
    ),
    yaxis=dict(
        gridcolor="#1e1e2e", showgrid=True,
        tickfont=dict(size=10, color="#6b6b85"),
        linecolor="#1e1e2e",
    ),
    legend=dict(
        bgcolor="rgba(17,17,24,0.8)",
        bordercolor="#1e1e2e",
        borderwidth=1,
        font=dict(size=11),
    ),
    hovermode="x unified",
    margin=dict(l=10, r=10, t=40, b=10),
)

tab1, tab2, tab3 = st.tabs(["📈 메인 차트", "📊 수익률 비교", "🔍 개별 상세"])

with tab1:
    if chart_type == "수익률 비교 (정규화)":
        fig = go.Figure()
        for i, (name, ticker, market) in enumerate(all_selected):
            df = stock_data.get(name, pd.DataFrame())
            if df.empty or "Close" not in df.columns:
                continue
            norm = normalize_series(df)
            dash = "solid" if market == "US" else "dot"
            fig.add_trace(go.Scatter(
                x=norm.index,
                y=norm.values,
                name=f"{'🇰🇷' if market=='KR' else '🇺🇸'} {name}",
                line=dict(color=COLOR_PALETTE[i % len(COLOR_PALETTE)], width=2, dash=dash),
                hovertemplate=f"<b>{name}</b><br>%{{x|%Y-%m-%d}}<br>정규화: %{{y:.1f}}<extra></extra>",
            ))

        fig.add_hline(y=100, line_dash="dash", line_color="#6b6b85", line_width=1)
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text=f"정규화 수익률 비교 (기준=100) | {period_label}", font=dict(size=14, color="#e8e8f0"), x=0.01),
            yaxis_title="정규화 가격 (시작=100)",
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "캔들스틱":
        names = [n for n, _, _ in all_selected]
        sel_name = st.selectbox("종목 선택", names)
        sel_market = next(m for n, _, m in all_selected if n == sel_name)
        df = stock_data.get(sel_name, pd.DataFrame())

        if not df.empty and all(c in df.columns for c in ["Open", "High", "Low", "Close"]):
            rows = 2 if (show_volume and "Volume" in df.columns) else 1
            row_heights = [0.75, 0.25] if rows == 2 else [1]
            fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=row_heights)

            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df["Open"].squeeze(),
                high=df["High"].squeeze(),
                low=df["Low"].squeeze(),
                close=df["Close"].squeeze(),
                name=sel_name,
                increasing=dict(fillcolor="#00e676", line=dict(color="#00e676")),
                decreasing=dict(fillcolor="#ff5252", line=dict(color="#ff5252")),
            ), row=1, col=1)

            if show_volume and "Volume" in df.columns and rows == 2:
                vol = df["Volume"].squeeze()
                close_s = df["Close"].squeeze()
                open_s  = df["Open"].squeeze()
                colors_v = ["#00e676" if float(c) >= float(o) else "#ff5252"
                            for c, o in zip(close_s, open_s)]
                fig.add_trace(go.Bar(
                    x=df.index, y=vol,
                    name="거래량",
                    marker_color=colors_v,
                    opacity=0.7,
                ), row=2, col=1)

            fig.update_layout(
                **PLOTLY_LAYOUT,
                title=dict(text=f"{sel_name} 캔들스틱 차트 | {period_label}", font=dict(size=14, color="#e8e8f0"), x=0.01),
                xaxis_rangeslider_visible=False,
                height=560 if rows == 2 else 460,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("데이터를 불러올 수 없습니다.")

    else:
        data_rows = []
        for name, ticker, market in all_selected:
            df = stock_data.get(name, pd.DataFrame())
            ret = calc_return(df)
            if ret is not None:
                data_rows.append({"종목": name, "수익률(%)": ret, "시장": "🇰🇷 한국" if market == "KR" else "🇺🇸 미국"})

        if data_rows:
            df_ret = pd.DataFrame(data_rows).sort_values("수익률(%)", ascending=True)
            fig = go.Figure(go.Bar(
                x=df_ret["수익률(%)"],
                y=df_ret["종목"],
                orientation="h",
                marker=dict(
                    color=df_ret["수익률(%)"],
                    colorscale=[[0, "#ff5252"], [0.5, "#6b6b85"], [1, "#00e676"]],
                    cmid=0,
                    showscale=True,
                    colorbar=dict(title="수익률%", tickfont=dict(size=10, color="#6b6b85")),
                ),
                text=[fmt_return(v) for v in df_ret["수익률(%)"]],
                textposition="outside",
                textfont=dict(size=11, color="#e8e8f0"),
                hovertemplate="<b>%{y}</b><br>수익률: %{x:.2f}%<extra></extra>",
            ))
            fig.add_vline(x=0, line_color="#6b6b85", line_width=1)
            fig.update_layout(
                **PLOTLY_LAYOUT,
                title=dict(text=f"수익률 비교 | {period_label}", font=dict(size=14, color="#e8e8f0"), x=0.01),
                xaxis_title="수익률 (%)",
                height=max(350, len(data_rows) * 45 + 80),
            )
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("#### 수익률 상세 비교")

    periods_compare = {"1주": "5d", "1개월": "1mo", "3개월": "3mo", "6개월": "6mo", "1년": "1y"}
    table_rows = []

    with st.spinner("다중 기간 수익률 계산 중..."):
        for name, ticker, market in all_selected:
            row = {
                "시장": "🇰🇷" if market == "KR" else "🇺🇸",
                "종목명": name,
                "티커": ticker,
            }
            for p_label, p_code in periods_compare.items():
                df_p = fetch_stock_data(ticker, p_code)
                ret = calc_return(df_p)
                row[p_label] = fmt_return(ret)
            table_rows.append(row)

    df_table = pd.DataFrame(table_rows)
    st.dataframe(
        df_table.set_index("티커"),
        use_container_width=True,
        height=min(400, 40 + len(table_rows) * 35),
    )

    st.markdown("#### 수익률 히트맵")
    heat_data = []
    heat_names = []
    with st.spinner("히트맵 생성 중..."):
        for name, ticker, market in all_selected:
            heat_names.append(f"{'🇰🇷' if market=='KR' else '🇺🇸'} {name}")
            row_vals = []
            for p_label, p_code in periods_compare.items():
                df_p = fetch_stock_data(ticker, p_code)
                row_vals.append(calc_return(df_p))
            heat_data.append(row_vals)

    heat_array = np.array([[v if v is not None else 0 for v in row] for row in heat_data])
    text_array = [[fmt_return(v) for v in row] for row in heat_data]

    fig_heat = go.Figure(go.Heatmap(
        z=heat_array,
        x=list(periods_compare.keys()),
        y=heat_names,
        text=text_array,
        texttemplate="%{text}",
        textfont=dict(size=11),
        colorscale=[[0, "#ff5252"], [0.4, "#1e1e2e"], [0.5, "#2a2a3e"], [0.6, "#1e2e1e"], [1, "#00e676"]],
        zmid=0,
        showscale=True,
        colorbar=dict(title="수익률%", tickfont=dict(size=10, color="#6b6b85")),
        hovertemplate="<b>%{y}</b><br>기간: %{x}<br>수익률: %{text}<extra></extra>",
    ))
    fig_heat.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="다중 기간 수익률 히트맵", font=dict(size=14, color="#e8e8f0"), x=0.01),
        height=max(300, len(heat_names) * 45 + 100),
        xaxis=dict(side="top"),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

with tab3:
    st.markdown("#### 개별 종목 상세")

    detail_name = st.selectbox("종목", [n for n, _, _ in all_selected], key="detail_sel")
    detail_market = next(m for n, _, m in all_selected if n == detail_name)
    df_detail = stock_data.get(detail_name, pd.DataFrame())

    if not df_detail.empty and "Close" in df_detail.columns:
        close_s = df_detail["Close"].squeeze()
        ret_detail = calc_return(df_detail)

        c1, c2, c3, c4 = st.columns(4)
        currency = "₩" if detail_market == "KR" else "$"
        with c1:
            last_p = float(close_s.iloc[-1])
            st.metric("현재가", f"{currency}{last_p:,.2f}")
        with c2:
            st.metric(f"{period_label} 수익률", fmt_return(ret_detail),
                      delta=f"{ret_detail:.2f}%" if ret_detail else None)
        with c3:
            if "High" in df_detail.columns:
                st.metric("기간 최고가", f"{currency}{float(df_detail['High'].max()):,.2f}")
        with c4:
            if "Low" in df_detail.columns:
                st.metric("기간 최저가", f"{currency}{float(df_detail['Low'].min()):,.2f}")

        fig_area = go.Figure()
        fig_area.add_trace(go.Scatter(
            x=close_s.index, y=close_s.values,
            fill="tozeroy",
            fillcolor="rgba(0,229,255,0.08)",
            line=dict(color="#00e5ff", width=2),
            name=detail_name,
            hovertemplate=f"<b>{detail_name}</b><br>%{{x|%Y-%m-%d}}<br>{currency}%{{y:,.2f}}<extra></extra>",
        ))
        if len(close_s) >= 20:
            ma20 = close_s.rolling(20).mean()
            fig_area.add_trace(go.Scatter(
                x=ma20.index, y=ma20.values,
                name="MA 20",
                line=dict(color="#ffd700", width=1.5, dash="dot"),
                hovertemplate="MA20: %{y:,.2f}<extra></extra>",
            ))
        if len(close_s) >= 60:
            ma60 = close_s.rolling(60).mean()
            fig_area.add_trace(go.Scatter(
                x=ma60.index, y=ma60.values,
                name="MA 60",
                line=dict(color="#ff6b6b", width=1.5, dash="dot"),
                hovertemplate="MA60: %{y:,.2f}<extra></extra>",
            ))

        fig_area.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text=f"{detail_name} 주가 추이 + 이동평균선", font=dict(size=14, color="#e8e8f0"), x=0.01),
            yaxis_title=f"주가 ({currency})",
            height=400,
        )
        st.plotly_chart(fig_area, use_container_width=True)

        if show_volume and "Volume" in df_detail.columns:
            vol_s = df_detail["Volume"].squeeze()
            fig_vol = go.Figure(go.Bar(
                x=vol_s.index, y=vol_s.values,
                name="거래량",
                marker_color="#00e5ff",
                opacity=0.6,
            ))
            fig_vol.update_layout(
                **PLOTLY_LAYOUT,
                title=dict(text="거래량", font=dict(size=12, color="#e8e8f0"), x=0.01),
                height=180,
                showlegend=False,
            )
            st.plotly_chart(fig_vol, use_container_width=True)
    else:
        st.warning(f"{detail_name} 데이터를 불러올 수 없습니다.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2.5rem 0 1rem;border-top:1px solid #1e1e2e;margin-top:3rem;">
    <span style="font-family:'Bebas Neue',sans-serif;font-size:1.2rem;letter-spacing:0.1em;
        background:linear-gradient(135deg,#00e5ff,#ffd700);-webkit-background-clip:text;
        -webkit-text-fill-color:transparent;background-clip:text;">StockLens</span>
    <div style="font-size:0.7rem;color:#6b6b85;margin-top:0.4rem;letter-spacing:0.15em;">
        DATA BY YAHOO FINANCE · FOR INFORMATIONAL PURPOSES ONLY · NOT FINANCIAL ADVICE
    </div>
</div>
""", unsafe_allow_html=True)
