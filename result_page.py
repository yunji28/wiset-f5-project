import requests
import streamlit as st

# 사진 크기 조절을 위한 라이브러리~
from PIL import Image
import io

# 페이지 세팅
st.set_page_config(
    page_title="WISET F5 연구 페이지",
    page_icon="🕺",
    layout="wide"       # 레이아웃을 전체로 설정
)

# 사이드바
with st.sidebar:
    st.title("👥 팀원 소개")
    @st.dialog("권보미")
    def profile_bomi():
        st.image("image/임시.webp")
        st.markdown("""
            ### 정보
            ### 역할
            """)
        

    @st.dialog("박세은")
    def profile_saeeun():
        st.image("image/임시.webp")
        st.markdown("""
            ### 정보
            ### 역할
            """)

    @st.dialog("박윤지")
    def profile_yunji():
        st.image("image/임시.webp")
        st.markdown("""
            ### 정보
            ### 역할
            """)

    @st.dialog("이하은")
    def profile_haeun():
        st.image("image/임시.webp")
        st.write("이름: 이하은")


    @st.dialog("장희원")
    def profile_heewon():
        st.image("image/임시.webp")
        st.write("이름: 장희원")

    st.subheader("연구 책임자")
    if st.button("🐰 권보미"):
        profile_bomi()

    st.subheader("연구 팀원")
    if st.button("🐱 박세은"):
        profile_saeeun()
    if st.button("👻 박윤지"):
        profile_yunji()

    st.subheader("중고등학생 팀원")
    if st.button("🍀 이하은"):
        profile_haeun()
    if st.button("🍒 장희원"):
        profile_heewon()


st.header("「산업 안전 연구를 위한 물리적 제약을 고려한 텍스트 조건 휴머노이드 정적 자세 생성」")
st.caption("WISET 여대학원생 공학연구팀제 숙명여자대학교 F5")

# 탭
t1, t2, t3, t4, t5 = st.tabs([
    '📖 연구 소개', '👩‍💻 진행 과정', '🕺연구 결과 시연', '🖼️활동 사진', '💬Review'
    ])
with t1:
    st.subheader("텍스트 조건 휴머노이드 정적 자세 생성")
    st.markdown("""
    해당 연구는 **자연어 문장을 입력하면 휴머노이드 로봇의 자세(Pose)를 생성하는 AI 기술**입니다.
    
    예를 들어,
    - "A robot is sitting on a chair."
    - "A robot is raising one hand."

    와 같은 문장을 입력하면 텍스트 조건부 확산 모델이 해당 내용을 분석하여 로봇의 자세를 생성합니다.

    """)
    st.subheader("전체 프레임워크")
    st.image("image/임시.webp")

with t2:
    st.subheader("연구 과정")
    st.markdown("""
    #### 데이터셋 구축
    #### 모델 설계
    #### 실험 및 결과 분석
    """)

    st.divider()
    
    st.subheader("활동 내용")
    st.markdown("""
    #### 정기 회의 진행
    #### KCC 2026 참가 (06.24~06.26)
    #### 한국인공지능학술대회 KICS 논문 제출 (09.29~10.02)
    """)



with t3:
    # 제목
    st.subheader("Text-to-Pose Generation Demo")
    st.caption("영어 문장으로 자세를 설명하면 지정한 개수의 스켈레톤 포즈를 생성합니다.")

    # 입력
    prompt = st.text_input("포즈 설명 (영어)", placeholder="A person is sitting on a chair.")
    n = st.slider("생성 개수", 1, 8, 5)

    API_URL = st.secrets.get("API_URL", "http://localhost:8000")
    API_KEY = st.secrets.get("API_KEY", "change-me")

    # 생성 버튼
    if st.button("생성", type="primary"):
        # 공백을 제거했을 때 입력이 빈 문자열인 경우
        if not prompt.strip():            # text.strip : 공백 제거
            st.warning("문장을 입력해주세요.")
        # 정상적으로 입력이 된 경우
        else:
            # 포즈를 생성하는 동안 spinner 작동
            with st.spinner("모델 실행 중..."):
                try:
                    r = requests.post(      # requests.post() : 서버에게 데이터를 보내는 함수
                        f"{API_URL}/generate",
                        json={"text": prompt, "n_samples": n},
                        headers={"X-API-Key": API_KEY},
                        timeout=180,        # 최대 3분 기다림
                    )
                except requests.exceptions.RequestException as e:
                    st.error(f"서버 연결 실패: {e}")
                # 서버가 정상적으로 응답한 경우
                else:
                    if r.status_code == 200:        # 성공
                        # st.image(r.content, use_container_width=True)
                        # 사진 크기 조절
                        img = Image.open(io.BytesIO(r.content))
                        target_height = 250
                        w, h = img.size
                        new_w = int(w * target_height / h)
                        img = img.resize((new_w, target_height))
                        st.image(img)
                        st.success(f"분류 결과: **{r.headers.get('X-Pose-Class', '?')}**")
                    elif r.status_code == 401:
                        st.error("API 키가 틀렸습니다. 담당자에게 키를 확인하세요.")
                    else:
                        st.error(f"에러 {r.status_code}: {r.text}")

with t4:
    st.subheader("1차 멘토링 (26.05.30)")
    st.caption("연구 소개 및 Python 기초 문법 학습")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("image/임시.webp")
    with col2:
        st.image("image/임시.webp")

    st.subheader("2차 멘토링 (26.08.01)")
    st.caption("데이터 시각화 실습 및 결과 보고 웹페이지 구현")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("image/임시.webp")
    with col2:
        st.image("image/임시.webp")
    with col3:
        st.image("image/임시.webp")

    st.subheader("3차 멘토링 (26.10.10)")
    st.caption("연구 결과 분석 및 성과 공유")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("image/임시.webp")
    with col2:
        st.image("image/임시.webp")


with t5:
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("""
            #### 🐰 권보미
            ㅎㅎ
            """)

        with st.container(border=True):
            st.markdown("""
            #### 🍀 이하은
            ㅎㅎ
            """)

    with col2:
        with st.container(border=True):
            st.markdown("""
            #### 🐱 박세은
            ㅎㅎ
            """)
        with st.container(border=True):
            st.markdown("""
            #### 🍒 장희원
            ㅎㅎ
            """)

    with col3:
        with st.container(border=True):
            st.markdown("""
            #### 👻 박윤지
            ㅎㅎ
            """)