import json
import streamlit as st
from openai import OpenAI
import pandas as pd
import io

# API 클라이언트 설정
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# 페이지 설정
st.set_page_config(
    page_title="EdMakers Code page",
    page_icon="favicon.png",
)

# 페이지 설명
st.markdown("""
    <h2 style="color: black; text-align: center;"> Chat GPT </h2>
    <p style="text-align: justify; text-align: center"> 이 페이지는 ChatGPT-4o-mini 버전을 사용하고 있습니다. </p>
""", unsafe_allow_html=True)

# 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_contents" not in st.session_state:
    st.session_state.file_contents = []

# 파일 업로드 및 처리
uploaded_files = st.file_uploader("파일 업로드", type=["txt", "pdf", "xlsx", "xls", "png", "pptx", "ppt"], accept_multiple_files=True)

# 파일 내용 처리
if uploaded_files:
    if len(uploaded_files) > 10:  # 파일 개수 제한
        st.error("최대 10개의 파일을 업로드할 수 있습니다.")
    else:
        st.session_state.file_contents = []
        for uploaded_file in uploaded_files:
            if uploaded_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
                # 엑셀 파일 처리
                try:
                    df = pd.read_excel(uploaded_file)
                    st.session_state.file_contents.append(df.to_csv(index=False))
                except Exception as e:
                    st.error(f"엑셀 파일 처리 중 오류가 발생했습니다: {str(e)}")
            elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.ms-powerpoint"]:
                st.session_state.file_contents.append("PPT 파일이 업로드되었습니다.")
            elif uploaded_file.type == "image/png":
                st.session_state.file_contents.append("PNG 파일이 업로드되었습니다.")

        st.success("파일 업로드가 완료되었습니다.")

# 사용자 입력
prompt = st.chat_input("메시지 ChatGPT")

if prompt:
    # 파일 내용이 있을 경우 OpenAI에 전송 (화면에 표시하지 않음)
    if st.session_state.file_contents:
        file_content = '\n'.join(st.session_state.file_contents)
        full_prompt = f"여기에 첨부된 데이터:\n{file_content}\n\n사용자 메시지: {prompt}"
    else:
        full_prompt = prompt

    # 사용자 메시지 표시 (화면에 표시)
    st.session_state.messages.append({"role": "user", "content": full_prompt})

    # OpenAI API 요청
    try:
        # 대화 컨텍스트를 포함하기
        messages_to_send = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]

        # OpenAI API 요청
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_to_send + [{"role": "user", "content": prompt}]
        )
        generated_response = response.choices[0].message.content

        # OpenAI의 응답을 그대로 표시
        st.session_state.messages.append({"role": "assistant", "content": generated_response})

    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")

# 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
