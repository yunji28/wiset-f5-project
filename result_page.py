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
        st.markdown("""
            ### 정보
            ### 역할
            """)

    @st.dialog("장희원")
    def profile_heewon():
        st.image("image/임시.webp")
        st.markdown("""
            ### 정보
            ### 역할
            """)

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


# 탭
t1, t2, t3, t4, t5 = st.tabs([
    '📖 연구 소개', '👩‍💻 진행 과정', '🕺연구 결과 시연', '🖼️활동 사진', '💬Review'
    ])
with t1:
    st.header("연구 소개")

    st.markdown("""
    ## Text-to-Pose란?

    Text-to-Pose는 **자연어 문장을 입력하면 사람의 자세(Pose)를 생성하는 AI 기술**입니다.

    예를 들어,

    - "A person is sitting on a chair."
    - "A person is raising one hand."

    와 같은 문장을 입력하면 AI가 해당 내용을 이해하여 사람의 자세를 생성합니다.
    """)

    st.markdown("""
    ### 이번 연구에서는

    기존에는 관절의 **좌표**를 직접 생성하는 방식이 많이 사용되었습니다.

    이번 연구에서는 사람의 자세를 **관절의 각도**로 표현하여
    더 자연스럽고 안정적인 자세를 생성하는 방법을 연구했습니다.
    """)

with t2:
    st.header("연구 과정")
    st.write("연구 과정 작성")

    st.divider()

    st.header("활동 내용")
    st.write("활동 내용 작성")


with t3:
    # 제목
    st.header("Text-to-Pose Generation Demo")
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
    st.caption("멘토링과 연구 활동 과정을 사진으로 확인할 수 있습니다.")
    st.header("1차 멘토링 (26.05.30)")
    col1, col2 = st.columns(2)
    with col1:
        st.image("image/임시.webp", caption="1차 멘토링 활동")

    with col2:
        st.image("image/임시.webp", caption="연구실 및 학교 견학")

    st.header("2차 멘토링 (26.08.01)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("image/임시.webp")

    with col2:
        st.image("image/임시.webp")

    with col3:
        st.image("image/임시.webp")


with t5:
    st.header("💬 활동 후기")
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.subheader("🐰 권보미")
            st.markdown("""
            ㅎㅎ
            """)

        with st.container(border=True):
            st.subheader("🍀 이하은")
            st.markdown("""
            ㅎㅎ
            """)

    with col2:
        with st.container(border=True):
            st.subheader("🐱 박세은")
            st.markdown("""
            ㅎㅎ
            """)
        with st.container(border=True):
            st.subheader("🍒 장희원")
            st.markdown("""
            ㅎㅎ
            """)

    with col3:
        with st.container(border=True):
            st.subheader("👻 박윤지")
            st.markdown("""
            ㅎㅎ
            """)