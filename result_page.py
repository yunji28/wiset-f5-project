import requests
import streamlit as st

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
        st.write("학교: 채드윅 국제학교")
        st.write("생년월일: 2010년 10월 1일")
        st.write("MBTI: INTP")


    @st.dialog("장희원")
    def profile_heewon():
        st.image("image/임시.webp")
        st.write("이름: 장희원")
        st.write("학교: 민족사관고등학교")
        st.write("생년월일: 2010.04.08")
        st.write("MBTI: ESTJ")

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


st.header("산업 안전 연구를 위한 물리적 제약을 고려한 텍스트 조건 휴머노이드 정적 자세 생성")
st.caption("WISET 여대학원생 공학연구팀제 숙명여자대학교 F5")

# 탭
t1, t2, t3, t4, t5, t6 = st.tabs([
    '📖 연구 소개', '👩‍💻 연구 과정', '🕺결과 시연', '🧪 연구 활동 ', '🖼️멘토링', '💬Review'
    ])
with t1:
    st.subheader("텍스트 조건 휴머노이드 정적 자세 생성")
    st.markdown("""
    본 연구는 **자연어 문장을 입력하면 휴머노이드 로봇의 자세(Pose)를 생성 기술** 연구입니다.
    
    예를 들어,
    - "A humanoid robot stands with Left arm stretched fully overhead."
    - "A humanoid robot is raising right hand."

    와 같은 문장을 입력하면 텍스트 조건부 확산 모델이 해당 문장을 분석하여 로봇의 자세를 생성합니다.
    """)
    
    st.subheader("전체 프레임워크")
    c1, c2 = st.columns([2,1])
    with c1:
            st.image("./image/프레임워크.png")

with t2:
    st.subheader("데이터셋 구축")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        with st.container():
            st.markdown("""
            >  **1. AMASS**   
            : CMU, DanceDB 2,235개 시퀀스 사용
            """)
    with c2:
        with st.container():
            st.markdown("""
            > **2. 자세 샘플링**   
            : 직립 제약 없이 35,628개 후보 확보
            """)
    with c3:
        with st.container():
            st.markdown("""
            > **3. 리타겟팅**   
            : 뼈 방향 정합 최적화를 사용   
            (평균 오차 3.30°)
            """)
    with c4:
        with st.container():
            st.markdown("""
            > **4. 충돌 필터링**   
            : MuJoCo 관통 5mm 초과 56.6% 제외   
            → 15,458 최종 G1 자세
            """)
    with c5:
        with st.container():
            st.markdown("""
            > **5. 캡션**   
            : G1 자세에서 기하 특징 재측정  
            → 87,296 고유 텍스트 캡션
            """)            
    
    st.subheader("모델 설계")
    st.text("성질이 다른 로봇의 두 물리적 제약을 두 단계로 나눠 처리했습니다.")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("**관절 범위 : 출력 파라미터에 내재화**")
            st.latex(r"q_i = l_i + (h_i - l_i) \cdot \sigma(u_i)")
            st.markdown("""
            - $u$: 확산이 다루는 무제약 변수
            - $l$, $h$ : 관절 하한, 상한
            - $\sigma$ : sigmoid
            """)   
    with col2:
        with st.container(border=True):
            st.markdown("**자기 충돌 : 역확산에서 guidance로 완화**")
            st.latex(r"E = s \cdot \sum \operatorname{ReLU}\left(f(q_{1:29}) + m\right)")
            st.markdown("""
            - $f$: 링크 간 관통량 예측 MLP
            - $m$: 기하 여유 5mm
            - $s$: 가중치 16
            """)

    st.subheader("실험 및 결과 분석")



with t3:
    API_URL = st.secrets.get("API_URL", "http://localhost:8001")
    API_KEY = st.secrets.get("API_KEY", "change-me")
    HEADERS = {"X-API-Key": API_KEY, "ngrok-skip-browser-warning": "true"}

    EXAMPLES = [
        "A humanoid robot stands in a wide stance, with the left arm raised and bent at the elbow and the right arm stretched out to the side.",
        "A humanoid robot stands with the feet together, with both arms stretched fully overhead.",
        "A humanoid robot stands with feet about shoulder-width apart, with the left arm extended forward and the right arm hanging straight down.",
        "A humanoid robot stands in a wide stance, with both arms stretched out to the side at shoulder level.",
    ]
    
    # 제목
    st.subheader("Text → 휴머노이드 로봇 자세 생성 데모")
    st.caption("영어 문장으로 자세를 설명하면 Unitree G1 로봇 자세를 생성해 정면·측면으로 보여줍니다.")

    # 입력 예시
    with st.expander("예시 문장 (클릭해서 복사)"):
        for e in EXAMPLES:
            st.code(e, language=None)
    st.caption("팔 높이(down / side / forward / raised / overhead), 팔꿈치(bent / straight), "
               "발 간격(feet together / shoulder-width / wide)을 직접 말하는 문장이 잘 됩니다.")

    # 입력
    prompt = st.text_input("자세 설명 (영어)", placeholder=EXAMPLES[0])

    # 생성 버튼
    if st.button("생성", type="primary"):
        # 공백을 제거했을 때 입력이 빈 문자열인 경우
        if not prompt.strip():            # text.strip : 공백 제거
            st.warning("문장을 입력해주세요.")
        # 정상적으로 입력이 된 경우
        else:
            # 포즈를 생성하는 동안 spinner 작동
            with st.spinner("모델 실행 중... (약 3~5초)"):
                try:
                    r = requests.post(f"{API_URL}/generate", json={"text": prompt},
                                    headers=HEADERS, timeout=180)
                except requests.exceptions.RequestException as e:
                    st.error(f"서버 연결 실패: {e}")
                else:
                    if r.status_code == 200:
                        img, perform = st.columns([3,2])
                        with img:
                            st.image(r.content, use_container_width=True)
                        with perform:
                            with st.container(border=True):
                                c1, c2, c3 = st.columns(3)
                                c1.metric("지시 이행", r.headers.get("X-Compliance", "?"))
                                c2.metric("관절 한계 위반", "0" if r.headers.get("X-Limit-Violation", "0.0") == "0.0" else "있음")
                                pen = float(r.headers.get("X-Penetration-mm", "0"))
                                c3.metric("자기 충돌", "없음" if pen <= 5 else f"{pen:.1f} mm 관통")
                                st.caption(f"측정된 자세 속성: `{r.headers.get('X-Posecode', '?')}`")
                    elif r.status_code == 401:
                        st.error("API 키가 틀렸습니다. 담당자에게 키를 확인하세요.")
                    else:
                        st.error(f"에러 {r.status_code}: {r.text}")
with t4:
    st.subheader("정기 회의 진행")
    st.subheader("연구 진행 상황 공유")
    st.subheader("KCC 2026 참가 (06.24~06.26)")
    st.subheader("한국인공지능학술대회 KICS 논문 제출 (09.29~10.02) 및 발표")
    

with t5:
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


with t6:
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