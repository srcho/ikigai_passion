import os
from openai import OpenAI
import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="빈센트 이키가이 열정편", page_icon="🌟", layout="centered")

# CSS를 사용하여 버튼 스타일 변경
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #9370DB;
    color: white;
}
div.stButton > button:hover {
    background-color: #7B68EE;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# OpenAI 클라이언트 생성
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 세션 상태 초기화
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'nickname' not in st.session_state:
    st.session_state.nickname = ""
if 'like_1' not in st.session_state:
    st.session_state.like_1 = ""
if 'like_2' not in st.session_state:
    st.session_state.like_2 = ""
if 'like_3' not in st.session_state:
    st.session_state.like_3 = ""
if 'good_1' not in st.session_state:
    st.session_state.good_1 = ""
if 'good_2' not in st.session_state:
    st.session_state.good_2 = ""
if 'good_3' not in st.session_state:
    st.session_state.good_3 = ""

def analyze_ikigai():
    if not st.session_state.nickname or not all([st.session_state.like_1, st.session_state.like_2, st.session_state.like_3, 
                                                 st.session_state.good_1, st.session_state.good_2, st.session_state.good_3]):
        st.warning("모든 질문에 답해주세요!")
    else:
        st.session_state.show_result = True

def reset_to_start():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

if not st.session_state.show_result:
    st.title("🌟 빈센트 이키가이 열정편")

    st.markdown("---")
    st.session_state.nickname = st.text_input("👤 당신을 뭐라고 불러드릴까요?", value=st.session_state.nickname)
    st.markdown("---")

    st.header("💖 좋아하는 것에 관한 질문")
    st.markdown("<br>", unsafe_allow_html=True)

    st.session_state.like_1 = st.text_area("1. 시간가는 줄 모르고 하는 즐거운 일은 무엇인가요?", value=st.session_state.like_1, height=100)
    st.markdown("<br>", unsafe_allow_html=True)

    st.session_state.like_2 = st.text_area("2. 당신의 마음을 설레이게하는 것은 어떤 것인가요?", value=st.session_state.like_2, height=100)
    st.markdown("<br>", unsafe_allow_html=True)

    st.session_state.like_3 = st.text_area("3. 가장 즐겁게 대화하는 소재는 무엇인가요?", value=st.session_state.like_3, height=100)
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.header("🏆 잘하는 것에 관한 질문")
    st.markdown("<br>", unsafe_allow_html=True)

    st.session_state.good_1 = st.text_area("1. 다른 사람들이 칭찬하는 당신이 잘하는 일은 무엇인가요?", value=st.session_state.good_1, height=100)
    st.markdown("<br>", unsafe_allow_html=True)

    st.session_state.good_2 = st.text_area("2. 학교나 회사 단체에서 내가 맡았던 직책이나 업무는 무엇인가요?", value=st.session_state.good_2, height=100)
    st.markdown("<br>", unsafe_allow_html=True)

    st.session_state.good_3 = st.text_area("3. 지치지 않고 꾸준히 할 수 있는 일은 어떤 것인가요?", value=st.session_state.good_3, height=100)

    st.markdown("---")

    if st.button("분석하기", key="submit", on_click=analyze_ikigai):
        pass

if st.session_state.show_result:
    with st.spinner('분석 중...'):
        prompt = f"""
        You are an AI assistant tasked with helping users discover their Ikigai - the Japanese concept of finding purpose and fulfillment in life. Your goal is to analyze the user's responses to six questions and identify their passions and strengths to formulate their Ikigai.

        Here are the user's responses to the six questions:

        <user_responses>
        nickname : {st.session_state.nickname}

        Find what you love to do
        -What are the things you enjoy doing that pass the time? {st.session_state.like_1}
        -What makes your heart flutter? {st.session_state.like_2}
        -What do you enjoy talking about the most? {st.session_state.like_3}

        Find what you are good at
        -What are the things you do well that others praise you for? {st.session_state.good_1}
        -What positions or tasks have you held in school or work organisations? {st.session_state.good_2}
        -What is something you can do consistently without getting tired? {st.session_state.good_3}
        </user_responses>

        Based on the respondents' questions, find out what they like and are good at, organise them, and present them as keywords. Find the intersection of the two to find the passion areas in Ikigai. Organise the respondent's passions into keywords. Answer in Korean.

        Present your findings in the following format:

        ## 열정🔥
        - 유저의 응답을 바탕으로 뷸렛 포인트로 정리.
        - 500자 분량

        ## 강점💪🏻
        - 유저의 응답을 바탕으로 뷸렛 포인트로 정리.
        - 500자 분량

        ## ✨가치찾기
        - {st.session_state.nickname}의 열정과 강점을 이키가이식으로 표현.
        - 500자 분량

        ## 🔑키워드
        - 잘하는 것과 좋아하는 것이 겹치는 키워드들을 나열.
        - 7~10개 키워드

        Remember to base your analysis solely on the information provided in the user's responses. Do not make assumptions or introduce information not present in the user's answers. Answer in Korean.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 이키가이 분석 전문가입니다. 사용자의 답변을 바탕으로 그들의 이키가이(인생의 목적)를 찾아주세요. 친근한 말투로 한글 문법에 주의해서 답변해주세요."},
                {"role": "user", "content": prompt}
            ]
        )
        
        analysis = response.choices[0].message.content
        
    st.success("분석이 완료되었습니다! 🎉")
    
    # 분석 결과를 마크다운으로 표시
    st.markdown(f"""
    <div id="result" style="padding: 20px; border: 2px solid #7B68EE;">
    <h1>🌟 빈센트 이키가이 열정편</h1>
    <h2>📌 {st.session_state.nickname} 열정 분석</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # analysis 내용을 별도로 마크다운으로 렌더링
    st.markdown(analysis)

    # 버튼 위에 패딩 추가
    st.markdown("<br>", unsafe_allow_html=True)

    # 이미지로 저장하기 버튼 (JavaScript 코드)
    capture_component = """
    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
    <script>
    function captureAndDownload() {
        const element = document.getElementById('result');
        html2canvas(element, {
            scale: 2,
            useCORS: true,
            backgroundColor: null
        }).then(canvas => {
            const imgData = canvas.toDataURL('image/png');
            const link = document.createElement('a');
            link.href = imgData;
            link.download = 'ikigai_analysis.png';
            link.click();
        });
    }
    </script>
    """
    components.html(capture_component, height=0)

    # Streamlit 버튼으로 이미지 다운로드 기능 호출
    if st.button("분석 결과 이미지로 저장하기", key="download_image"):
        components.html(
            """
            <script>
            captureAndDownload();
            </script>
            """,
            height=0
        )

    # 웨이트리스트 등록 섹션
    st.markdown("---")
    st.markdown("## 이 서비스가 마음에 드셨나요? 더 발전된 서비스가 나오면 알려드릴게요. 빈센트에게 메일을 적어주세요!")
    email = st.text_input("이메일 주소를 입력해주세요:")

    def send_to_webhook(email):
        webhook_url = "https://hook.us1.make.com/l7y4h8oyj6phluopbtd35bvxk2lagstt"  # 실제 웹훅 URL로 교체해주세요
        data = {"email": email}
        response = requests.post(webhook_url, json=data)
        return response.status_code == 200

    if st.button("다음버전 대기리스트 등록", key="waitlist"):
        if email:
            if send_to_webhook(email):
                st.success("대기리스트에 등록되었습니다!")
            else:
                st.error("등록 중 오류가 발생했습니다. 나중에 다시 시도해주세요.")
        else:
            st.warning("이메일 주소를 입력해주세요.")
    # 처음으로 돌아가기 버튼 (전체 너비)
    st.markdown("---")
    if st.button("처음으로 돌아가기", on_click=reset_to_start, use_container_width=True):
        pass
