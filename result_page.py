import requests
import streamlit as st
import pandas as pd
from itertools import count
from pathlib import Path

BASE_DIR = Path(__file__).parent
_grid_id = count()

# 설정 및 데이터
st.set_page_config(page_title="WISET F5 연구 페이지", page_icon="🕺", layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stDecoration"] { display: none; }

    /* 표가 화면보다 넓으면 가로 스크롤 */
    [data-testid="stTable"] { overflow-x: auto; }

    /* 프로필 다이얼로그 사진: 모두 같은 크기, 가운데 정렬 */
    [data-testid="stDialog"] [data-testid="stImage"] img {
        width: 209px !important;
        height: 261px !important;
        object-fit: cover;        /* 비율이 다르면 가장자리를 잘라서 채움 */
        object-position: top;     /* 얼굴이 위쪽이니 위를 기준으로 자름 */
        border-radius: 12px;
    }

    @media (max-width: 640px) {
        /* 여백 줄이기 */
        .block-container { padding: 4rem 0.8rem 3rem !important; }

        /* 제목/캡션 크기 */
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.3rem !important; line-height: 1.35 !important; }
        h3 { font-size: 1.1rem !important; }

        /* 탭: 글자·간격 줄이고 가로 스크롤 */
        button[data-baseweb="tab"] { padding: 0.4rem 0.6rem !important; }
        button[data-baseweb="tab"] p { font-size: 0.85rem !important; }

        /* 표 글자 작게 */
        [data-testid="stTable"] table { font-size: 0.75rem; }

        /* 이미지 그리드만 2열 유지 (show_images에서 key로 표시한 영역) */
        [class*="st-key-imggrid"] [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 0.5rem !important;
        }
        [class*="st-key-imggrid"] [data-testid="stColumn"],
        [class*="st-key-imggrid"] [data-testid="column"] {
            flex: 1 1 calc(50% - 0.5rem) !important;
            min-width: calc(50% - 0.5rem) !important;
            width: calc(50% - 0.5rem) !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

DEFAULT_IMG = "image/임시.webp"

TEAM = {
    "연구 책임자": [
        dict(emoji="🐰", name="권보미", org="숙명여자대학교",
             role="연구 기획, 운영 / 예산 총괄 / 생성 모델 설계 및 실험 총괄",
             birth="2001.09.20", mbti="ENFP", img="image/profile/권보미.jpg",
             review="지난 7개월간의 WISET 활동은 연구자로서도, 연구책임자로서도 많은 것을 배우고 성장할 수 있었던 소중한 시간이었습니다. 석사과정 3학기 동안 주로 혼자 연구를 진행해 오다가, 처음으로 연구책임자가 되어 연구를 기획하고 팀원들과 역할을 나누어 함께 진행하는 과정이 쉽지만은 않았습니다. 하지만 여러 시행착오 끝에 연구 성과를 만들어내고, 학술대회 논문 투고와 발표까지 이어갈 수 있어 더욱 뜻깊었습니다. 이번 활동을 통해 모든 팀원이 공동의 목표에 공감하고 같은 방향을 바라보며 나아갈 수 있도록 이끄는 것이 리더의 중요한 역할임을 깨달았습니다. 무엇보다 연구와 활동에 누구보다 열정적으로 참여해 준 대학생 팀원들에게 실제 연구를 경험할 기회를 제공하고, 앞으로의 진로와 목표를 구체화하는 데 조금이나마 도움을 줄 수 있었다는 점이 가장 큰 보람으로 남습니다. 함께해 준 모든 팀원들에게 진심으로 고맙고, 이런 소중한 기회를 만들어 주신 WISET에도 감사드립니다. 앞으로도 이번 경험을 바탕으로 함께 성장하며, 사회에 긍정적인 영향을 줄 수 있는 연구자가 되고 싶습니다."),],
    "연구 팀원": [
        dict(emoji="🐱", name="박세은", org="숙명여자대학교",
             role="자세 데이터셋 구축 및 전처리 / 1차 멘토링 주관",
             birth="2005.09.16", mbti="INTP", img="image/profile/박세은.png",
             review="팀원들과 함께 연구를 처음부터 끝까지 진행하며, 데이터를 준비하는 과정이 결과만큼 중요하다는 것을 배웠습니다. 또한 멘토링을 통해 제가 아는 내용을 다른 사람에게 쉽게 전달하는 일이 생각보다 어렵지만 보람 있다는 것을 느꼈습니다. 이렇듯 다같이 연구를 해보고 함께 나눈 이 경험이 앞으로의 연구 생활에 큰 도움이 될것같습니다!"),
        dict(emoji="👻", name="박윤지", org="숙명여자대학교",
             role="평가 검증 및 비교 실험 / 2차 멘토링 주관",
             birth="2005.12.28", mbti="INFP", img="image/profile/박윤지.jpg",
             review="컴퓨터과학전공 특성상 학부생 때 연구를 직접 경험할 기회가 많지 않은데, 여대학원생 공학연구팀제를 통해 팀원들과 함께 하나의 연구를 진행할 수 있어 뜻깊었습니다. 특히 직접 데이터를 다루고 생성 모델을 연구하며 AI 분야에 흥미를 갖게 되었고, 멘토링을 통해 지식을 나누는 보람도 느꼈습니다. 연구 경험을 쌓는 것을 넘어, 진로에 대한 새로운 가능성을 발견할 수 있었던 소중한 시간이었습니다."),
    ],
    "중고등학생 팀원": [
        dict(emoji="🍀", name="이하은", org="채드윅국제학교",
             role="생성 결과 분석 / 연구 결과 시각화 / 웹페이지 구현",
             birth="2010.10.01", mbti="INTP", img="image/profile/이하은.jpg",
             review="이번 멘토링을 통해 파이썬의 기초를 배우고 직접 코딩을 실습하며 프로그래밍이 실제 문제 해결에 어떻게 활용되는지 경험할 수 있었습니다. 변수, 연산자, 조건문, 반복문 등의 개념을 익히고 코드를 직접 작성하면서 논리적으로 사고하는 방법을 배웠습니다. 특히 코딩을 단순히 명령어를 입력하는 과정으로 생각하는 것이 아니라, 데이터를 처리하고 원하는 결과를 얻기 위해 문제를 단계적으로 해결하는 과정으로 이해하게 되었습니다. 또한 코딩과 데이터 분석이 다양한 분야에서 활용될 수 있다는 점을 알게 되었고, 이를 제가 관심을 가진 분야에 어떻게 적용할 수 있을지 고민해 보는 계기가 되었습니다. 이번 멘토링은 새로운 기술을 배우는 것뿐만 아니라, 제가 관심 있는 분야와 진로를 더 구체적으로 탐색할 수 있었던 의미 있는 경험이었습니다. 앞으로도 배운 내용을 바탕으로 다양한 기술의 활용 가능성을 알아가고 싶습니다."),
        dict(emoji="🍒", name="장희원", org="민족사관고등학교",
             role="생성 결과 분석 / 연구 결과 시각화 / 웹페이지 구현",
             birth="2010.04.08", mbti="ESTJ", img="image/profile/장희원.jpg",
             review="여성 과학자 선배님들께서 학부와 대학원 과정에서 어떤 연구를 하고 계시는지 직접 보고 들을 수 있어 정말 뜻깊고 감사한 시간이었습니다. 숙대 과학자 선배 언니들의 연구를 접하며 기초 과학의 중요성을 깊이 깨달았고, 과학의 여러 세부 전공을 열린 눈으로 융합하고 적용하는 것을 두려워하지 말자는 각오를 다지게 되었습니다. 이번 경험을 통해 과학적 연구 방법이 문·이과를 뛰어넘어 모든 학문 연구의 든든한 기초가 된다는 것을 배웠습니다. 앞으로 문·이과에 얽매이지 않고 편견 없이 폭넓게 학습할 것입니다."),
    ],
}

MENTORING = [
    ("1차 멘토링 (26.05.30)", "연구 소개 및 Python 기초 문법 학습",
     [f"./image/mentoring/1차멘토링{i}.jpg" for i in range(1, 5)]),
    ("2차 멘토링 (26.08.01)", "데이터 시각화 실습 및 결과 보고 웹페이지 구현",
     [f"./image/mentoring/2차멘토링{i}.jpg" for i in range(1, 5)]),
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
    """이미지 경로 리스트를 n_cols 열 그리드로 표시 (모바일에서는 2열)"""
    with st.container(key=f"imggrid-{next(_grid_id)}"):
        cols = st.columns(n_cols)
        for col, path in zip(cols, paths):
            p = BASE_DIR / path
            if p.exists():
                col.image(str(p), use_container_width=True)
            else:
                col.warning(f"이미지 없음: {path}")

@st.dialog("프로필")
def show_profile(p):
    st.image(str(BASE_DIR / p.get("img", DEFAULT_IMG)))
    st.write(f"이름: {p['name']}")
    st.write(f"소속: {p['org']}")
    st.write(f"역할: {p['role']}")
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
            st.markdown(f"#### {p['emoji']} {p['name']}\n{p['review']}")


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