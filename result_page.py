import requests
import streamlit as st
import pandas as pd

# 설정 및 데이터
st.set_page_config(page_title="WISET F5 연구 페이지", page_icon="🕺", layout="wide")
st.markdown(
    "<style>[data-testid='stDecoration'] { display: none; }</style>",
    unsafe_allow_html=True,
)

DEFAULT_IMG = "image/임시.webp"

TEAM = {
    "연구 책임자": [
        dict(emoji="🐰", name="권보미", org="숙명여자대학교", birth="2001.??.??", mbti="ENFP..?"),
    ],
    "연구 팀원": [
        dict(emoji="🐱", name="박세은", org="숙명여자대학교", birth="2005.09.16", mbti="ISTP?"),
        dict(emoji="👻", name="박윤지", org="숙명여자대학교", birth="2005.12.28", mbti="INFP",
             img="image/profile/박윤지.jpg", center_img=True),
    ],
    "중고등학생 팀원": [
        dict(emoji="🍀", name="이하은", org="채드윅국제학교", birth="2010.10.01", mbti="INTP"),
        dict(emoji="🍒", name="장희원", org="민족사관고등학교", birth="2010.04.08", mbti="ESTJ"),
    ],
}

MENTORING = [
    ("1차 멘토링 (26.05.30)", "연구 소개 및 Python 기초 문법 학습",
     [f"./image/mentoring/1차멘토링{i}.jpg" for i in range(1, 5)]),
    ("2차 멘토링 (26.08.01)", "데이터 시각화 실습 및 결과 보고 웹페이지 구현",
     [f"./image/mentoring/2차멘토링{i}.jpg" for i in range(1, 5)]),
    ("3차 멘토링 (26.10.10)", "연구 결과 분석 및 성과 공유",
     [DEFAULT_IMG, DEFAULT_IMG]),
]

EXAMPLES = [
    "A humanoid robot stands in a wide stance, with the left arm raised and bent at the elbow and the right arm stretched out to the side.",
    "A humanoid robot stands with the feet together, with both arms stretched fully overhead.",
    "A humanoid robot stands with feet about shoulder-width apart, with the left arm extended forward and the right arm hanging straight down.",
    "A humanoid robot stands in a wide stance, with both arms stretched out to the side at shoulder level.",
]

DATASET_STEPS = [
    "**1. AMASS**   \n: CMU, DanceDB 2,235개 시퀀스 사용",
    "**2. 자세 샘플링**   \n: 직립 제약 없이 35,628개 후보 확보",
    "**3. 리타겟팅**   \n: 뼈 방향 정합 최적화를 사용   \n(평균 오차 3.30°)",
    "**4. 충돌 필터링**   \n: MuJoCo 관통 5mm 초과 56.6% 제외   \n→ 15,458 최종 G1 자세",
    "**5. 캡션**   \n: G1 자세에서 기하 특징 재측정  \n→ 87,296 고유 텍스트 캡션",
]

RESULT_1 = {
    "자세표현": ["유계표현, 제안", "Clipping", "무제약"],
    "자기충돌률 (미적용 → 적용)": ["41.8% → 3.6%", "43.2% → 4.2%", "44.4% → 5.4%"],
    "관절 한계 위반율": ["0.0%", "0.0%", "37.4% → 33.4%"],
    "경계도달율": ["0.0%", "37.8%", "--"],
}
RESULT_2 = {
    "방법": ["Random", "Retrieval", "MLP", "cVAE, β=0.2", "Diffusion", "Diffusion+자기 충돌 guidance"],
    "지시이행률 IC": ["0.332", "0.563", "0.863", "0.840", "0.785", "0.784"],
    "다양성 (°)": ["16.33", "15.09", "0.00", "7.47", "10.93", "10.17"],
    "자기 충돌률": ["0.00%", "0.00%", "1.23%", "4.48%", "44.52%", "3.86%"],
}


# 공통 레이아웃
def show_images(paths, n_cols=4):
    """이미지 경로 리스트를 n_cols 열 그리드로 표시"""
    cols = st.columns(n_cols)
    for col, path in zip(cols, paths):
        col.image(path)

@st.dialog("프로필")
def show_profile(p):
    img = p.get("img", DEFAULT_IMG)
    if p.get("center_img"):
        st.columns([1, 2, 1])[1].image(img)
    else:
        st.image(img)
    st.write(f"이름: {p['name']}")
    st.write(f"소속: {p['org']}")
    st.write(f"생년월일: {p['birth']}")
    st.write(f"MBTI: {p['mbti']}")


# 사이드바
def render_sidebar():
    with st.sidebar:
        st.title("👥 팀원 소개")
        for group, members in TEAM.items():
            st.subheader(group)
            for p in members:
                if st.button(f"{p['emoji']} {p['name']}"):
                    show_profile(p)

# 각 탭 
def render_intro():
    st.subheader("텍스트 조건 휴머노이드 정적 자세 생성")
    st.markdown("""
    본 연구는 **자연어 문장을 입력하면 휴머노이드 로봇 Unitree G1의 자세(Pose)를 생성 기술** 연구입니다.

    예를 들어,
    - "A humanoid robot stands with Left arm stretched fully overhead."
    - "A humanoid robot is raising right hand."

    와 같은 문장을 입력하면 텍스트 조건부 확산 모델이 해당 문장을 분석하여 로봇의 자세를 생성합니다.
    """)

    st.subheader("전체 프레임워크")
    st.columns([2, 1])[0].image("./image/프레임워크.png")
    st.markdown("""
    본 연구에서는 **텍스트 조건부 확산 모델**을 활용하여 입력 문장에 적합한 로봇 자세를 생성합니다.

    - **텍스트 조건:** BGE-M3 텍스트 인코더와 27차원 자세 속성 벡터를 활용합니다.
    - **자세 생성:** 조건부 MLP-denoiser와 100-step DDPM을 통해 G1의 31차원 자세를 생성합니다.
    - **조건 반영:** CFG(Classifier-Free Guidance)를 적용하여 텍스트 조건의 반영 정도를 조절합니다.

    또한, 로봇의 관절 가동 범위와 자기 충돌을 고려하여 생성 과정에 제약 조건을 적용합니다.

    - **관절 가동 범위:** 유계 자세 표현을 통해 관절 한계를 준수하도록 설계합니다.
    - **자기 충돌:** 충돌 예측기의 guidance를 역확산 과정에 적용하여 자기 충돌을 줄입니다.
    """)

def render_process():
    st.subheader("데이터셋 구축")
    for col, step in zip(st.columns(5), DATASET_STEPS):
        col.markdown(f"> {step}")

    st.subheader("모델 설계")
    st.text("성질이 다른 로봇의 두 물리적 제약을 두 단계로 나눠 처리했습니다.")
    col1, col2 = st.columns(2)
    with col1, st.container(border=True):
        st.markdown("**관절 범위 : 출력 파라미터에 내재화**")
        st.latex(r"q_i = l_i + (h_i - l_i) \cdot \sigma(u_i)")
        st.markdown("""
        - $u$: 확산이 다루는 무제약 변수
        - $l$, $h$ : 관절 하한, 상한
        - $\\sigma$ : sigmoid
        """)
    with col2, st.container(border=True):
        st.markdown("**자기 충돌 : 역확산에서 guidance로 완화**")
        st.latex(r"E = s \cdot \sum \operatorname{ReLU}\left(f(q_{1:29}) + m\right)")
        st.markdown("""
        - $f$: 링크 간 관통량 예측 MLP
        - $m$: 기하 여유 5mm
        - $s$: 가중치 16
        """)

    st.subheader("실험 및 결과 분석")
    st.write("실험 결과 1: 자세 표현과 자기 충돌 guidance의 영향")
    st.table(pd.DataFrame(RESULT_1))
    st.write("실험 결과 2: 최종 생성 성능 비교")
    st.table(pd.DataFrame(RESULT_2))


def call_generate_api(prompt):
    """API 호출. 성공 시 Response, 실패 시 None (에러는 화면에 표시)"""
    url = st.secrets.get("API_URL", "http://localhost:8001")
    headers = {
        "X-API-Key": st.secrets.get("API_KEY", "change-me"),
        "ngrok-skip-browser-warning": "true",
    }
    try:
        r = requests.post(f"{url}/generate", json={"text": prompt}, headers=headers, timeout=180)
    except requests.exceptions.RequestException as e:
        st.error(f"서버 연결 실패: {e}")
        return None

    if r.status_code == 401:
        st.error("API 키가 틀렸습니다. 담당자에게 키를 확인하세요.")
    elif r.status_code != 200:
        st.error(f"에러 {r.status_code}: {r.text}")
    else:
        return r
    return None


def render_demo():
    st.subheader("Text → 휴머노이드 로봇 자세 생성 데모")
    st.caption("영어 문장으로 자세를 설명하면 Unitree G1 로봇 자세를 생성해 정면·측면으로 보여줍니다.")
    with st.expander("예시 문장 (클릭해서 복사)"):
        for e in EXAMPLES:
            st.code(e, language=None)
    st.caption("팔 높이(down / side / forward / raised / overhead), 팔꿈치(bent / straight), "
               "발 간격(feet together / shoulder-width / wide)을 직접 말하는 문장이 잘 됩니다.")
    prompt = st.text_input("자세 설명 (영어)", EXAMPLES[0])
    if not st.button("생성", type="primary"):
        return
    if not prompt.strip():
        st.warning("문장을 입력해주세요.")
        return
    with st.spinner("모델 실행 중... (약 3~5초)"):
        r = call_generate_api(prompt)
    if r is None:
        return

    h = r.headers
    pen = float(h.get("X-Penetration-mm", "0"))
    img_col, metric_col = st.columns([3, 2])
    img_col.image(r.content, use_container_width=True)
    with metric_col, st.container(border=True):
        c1, c2, c3 = st.columns(3)
        c1.metric("지시 이행", h.get("X-Compliance", "?"))
        c2.metric("관절 한계 위반", "0" if h.get("X-Limit-Violation", "0.0") == "0.0" else "있음")
        c3.metric("자기 충돌", "없음" if pen <= 5 else f"{pen:.1f} mm 관통")
        st.caption(f"측정된 자세 속성: `{h.get('X-Posecode', '?')}`")

def render_activities():
    r = "./image/research/"
    st.subheader("정기 회의 및 연구 진행")
    show_images([r + "줌회의.jpg", r + "회의록.png", r + "연구진행상황.png"])
    show_images([r + f"회의{i}.jpg" for i in range(1, 5)])
    st.subheader("KCC 2026 참가 (06.24~06.26)")
    show_images([r + n for n in ("KCC.jpg", "KCC2.jpg", "KCC3.jpg")])
    st.subheader("한국인공지능학술대회 KICS 논문 제출 (09.29~10.02) 및 발표")
    show_images([r + f"논문{i}.png" for i in range(1, 4)])

def render_mentoring():
    for title, caption, images in MENTORING:
        st.subheader(title)
        st.caption(caption)
        show_images(images, n_cols=len(images) if len(images) > 2 else 4)

def render_review():
    members = [p for group in TEAM.values() for p in group]
    cols = st.columns(3)
    for i, p in enumerate(members):
        with cols[i % 3], st.container(border=True):
            st.markdown(f"#### {p['emoji']} {p['name']}\nㅎㅎ")


# 메인
render_sidebar()
st.header("산업 안전 연구를 위한 물리적 제약을 고려한 텍스트 조건 휴머노이드 정적 자세 생성")
st.caption("WISET 여대학원생 공학연구팀제 숙명여자대학교 F5")

TABS = [
    ("📖 연구 소개", render_intro),
    ("👩‍💻 연구 과정", render_process),
    ("🕺결과 시연", render_demo),
    ("🧪 연구 활동", render_activities),
    ("🖼️멘토링", render_mentoring),
    ("💬Review", render_review),
]
for tab, (_, render) in zip(st.tabs([label for label, _ in TABS]), TABS):
    with tab:
        render()