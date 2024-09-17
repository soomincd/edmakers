import streamlit as st
import subprocess  # subprocess 모듈을 임포트합니다.

st.set_page_config(
    page_title="EduMakers Code page",
    page_icon="favicon.png",
)

st.markdown("""
    <h2 style="color: black; text-align: center;"> 관리자 페이지입니다. </h2>
    <p style="text-align: justify; text-align: center"> 원하시는 항목을 선택해주세요. </p>
    """, unsafe_allow_html=True)

# 스타일 정의
st.markdown("""
    <style>
    .box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;  
        padding: 30px;  /* 패딩을 줄여서 세부사항 넣기 */
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px; 
        background-color: #f0f0f0;
        text-align: center;
        height: auto;  
    }
    .box:hover {
        background-color: #e0e0e0;
    }
    .button-container {
        margin-top: 10px;
        text-align: right;
    }
    .button-container button {
        color: white; 
        border: none; 
        border-radius: 5px; 
        padding: 10px 20px;
        cursor: pointer;
        font-size: 16px; 
    }
    </style>
    """, unsafe_allow_html=True)

# GPT-4o-mini 페이지
with st.container():
    col1, col2 = st.columns([5, 1]) 
    with col1:
        st.markdown(
            f"""
            <div class="box">
                <div style="font-size: 20px;">GPT-4o-mini 페이지</div>
                <p>GPT-4o-mini 모델에 접근하여 다양한 기능을 사용할 수 있습니다.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if st.button("이동", key="gpt_move"):
            st.success("GPT-4o-mini")  # 페이지 이동 피드백
            subprocess.Popen(["streamlit", "run", "new.py"]) 

# 관리자 모드
with st.container():
    col1, col2 = st.columns([5, 1])  
    with col1:
        st.markdown(
            f"""
            <div class="box">
                <div style="font-size: 20px;">관리자 모드</div>
                <p>사용자 관리 및 삭제를 할 수 있습니다.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if st.button("이동", key="admin_move"):
            st.success("관리자 모드")  # 페이지 이동 피드백
            subprocess.Popen(["streamlit", "run", "gov.py"])  

# 계정 생성 페이지
with st.container():
    col1, col2 = st.columns([5, 1]) 
    with col1:
        st.markdown(
            f"""
            <div class="box">
                <div style="font-size: 20px;">계정 생성 페이지</div>
                <p>새로운 사용자의 계정을 생성할 수 있습니다.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if st.button("이동", key="signup_move"):
            st.success("계정 생성") 
            subprocess.Popen(["streamlit", "run", "ma.py"])

# 암호코드 변경
with st.container():
    col1, col2 = st.columns([5, 1]) 
    with col1:
        st.markdown(
            f"""
            <div class="box">
                <div style="font-size: 20px;"> 암호 코드 설정 </div>
                <p> 암호 코드를 변경할 수 있습니다.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if st.button("이동", key="code_make"):
            st.success("암호 변경") 
            subprocess.Popen(["streamlit", "run", "set.py"])