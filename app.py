import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="가구소득 시각화",
    page_icon="☁️",
    layout="wide"
)

# ✅ 하늘 감성 스타일 (CSS)
st.markdown("""
    <style>
        body {
            background: linear-gradient(to bottom, #dff1ff, #ffffff);
        }
        .main {
            background-color: rgba(255,255,255,0.6) !important;
            backdrop-filter: blur(6px);
        }
        .stSelectbox, .stPlotlyChart, .stDataFrame {
            border-radius: 12px;
        }
        h1, h2, h3 {
            color: #2b6cb0 !important;
            font-weight: 700;
        }
        .stButton>button {
            background-color: #6bb8ff;
            color: white;
            border-radius: 10px;
            padding: 8px 18px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #4da3f7;
        }
        .css-1d391kg, .css-1gsen4l {
            color: #2b6cb0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("가구특성별_소득원천별_가구소득_20251031184640.csv", encoding="cp949")
    df.columns = ["가구특성별", "원천별", "평균소득(만원)", "중앙값소득(만원)"]
    df = df.replace("-", None)
    df["평균소득(만원)"] = pd.to_numeric(df["평균소득(만원)"], errors="coerce")
    return df

df = load_data()

# 제목
st.markdown("<h1 style='text-align:center;'>☁️ 가구 특성별 · 소득원천별 가구소득 대시보드 ☁️</h1>", unsafe_allow_html=True)
st.write("")

# 선택 박스
col1, col2 = st.columns([1.3, 3])
with col1:
    selected_household = st.selectbox("가구 특성을 선택하세요:", df["가구특성별"].unique())

filtered_df = df[df["가구특성별"] == selected_household]

# Plotly 그래프
fig = px.bar(
    filtered_df,
    x="원천별",
    y="평균소득(만원)",
    title=f"🌤 {selected_household} 가구의 소득원천별 평균 소득",
    labels={"평균소득(만원)": "평균소득 (만원)", "원천별": "소득원천"},
)

fig.update_layout(
    plot_bgcolor="rgba(255,255,255,0.5)",
    paper_bgcolor="rgba(255,255,255,0.0)",
    font=dict(size=14, color="#2b6cb0")
)

st.plotly_chart(fig, use_container_width=True)

# 테이블
with st.expander("📄 데이터 테이블 보기"):
    st.dataframe(filtered_df, use_container_width=True)
