# 수학 & AI 시각화 프로젝트 모음

**초보자도 이해할 수 있는 교육용 프로젝트**

---

## 📚 프로젝트 목록

### 🧠 똑똑한 AI - 자연어 이해 + 재귀적 사고 (NEWEST! 🔥)
**사람처럼 대화하는 진짜 똑똑한 AI**

자연어를 이해하고, 과거를 기억하고, 패턴을 스스로 발견합니다.

**혁신적인 차이:**
- 🗣️ **자연어 이해** - "오늘 기분 안 좋고 잠 못 잤어" → AI가 이해!
- 🔄 **재귀적 예측** - 과거 7일 데이터를 기억하여 더 정확한 예측
- 🧐 **자동 해석** - "왜 그럴까?" → AI가 패턴을 발견하고 설명
- 🤔 **의도 파악** - 설명/비교/예측/조언 자동 구분
- 💡 **인사이트 생성** - 상관관계와 트렌드 자동 분석

**빠른 시작:**
```bash
# HTML 버전 (브라우저에서 바로 실행)
open smart-ai.html

# Python 버전 (터미널)
python smart_ai.py
```

**사용된 AI 기술:**
- 자연어 처리 (NLP) - 감정 분석, 엔티티 추출, 의도 파악
- 재귀 신경망 (Recursive NN) - LSTM 스타일 메모리
- 자동 인사이트 생성 - 상관관계 분석, 트렌드 감지
- 의사결정 트리 + 신경망 하이브리드

📖 **상세 문서:** [README_SMART_AI.md](README_SMART_AI.md)

---

### 🤖 일상생활 AI 도우미
**초보자를 위한 규칙 기반 AI 에이전트**

논리적인 의사결정을 돕는 대화형 AI 도우미입니다.

**주요 기능:**
- 📊 할 일 우선순위 분석 (아이젠하워 매트릭스)
- 🤔 의사결정 도우미 (5단계 프로세스)
- ⏰ 시간 관리 조언 (포모도로, 80/20 법칙)
- 💪 건강 습관 추천 (수면, 운동, 식습관)

**빠른 시작:**
```bash
# HTML 버전 (브라우저에서 바로 실행)
open ai-agent.html

# Python 버전 (터미널)
python ai_agent.py
```

📖 **상세 문서:** [README_AI_AGENT.md](README_AI_AGENT.md)

---

### 🧠 나만의 학습하는 AI (NEWEST! ⭐)
**진짜 학습하는 AI를 무료로, 오프라인으로!**

당신의 데이터로 학습하는 개인 맞춤형 AI입니다.

**특별한 점:**
- 🆓 **100% 무료** - 유료 API 절대 없음
- 🔌 **완전 오프라인** - 인터넷 필요 없음
- 🧠 **진짜 학습** - 신경망이 실제로 학습합니다
- 🔐 **개인정보 안전** - 모든 데이터는 로컬에만
- 📖 **교육용** - 코드로 AI 원리 학습

**주요 기능:**
- 개인 습관 패턴 학습 (기분, 수면, 날씨 → 운동 예측)
- 실시간 학습 시각화
- 예측 확률 및 신뢰도 표시
- 학습 데이터 관리 및 백업

**빠른 시작:**
```bash
# HTML 버전 (브라우저에서 바로 실행) - 가장 쉬움!
open my-learning-ai.html

# Python 버전 (터미널)
python my_learning_ai.py
```

**사용된 AI 기술:**
- 로지스틱 회귀 (Logistic Regression)
- 경사하강법 (Gradient Descent)
- 단층 신경망 (Single-layer Neural Network)
- 시그모이드 활성화 함수

📖 **상세 문서:** [README_MY_LEARNING_AI.md](README_MY_LEARNING_AI.md)

---

### 🔷 Order-3 Heptagonal Tiling - Poincaré Disk Visualization

수학적으로 정확한 쌍곡 기하학 시각화: **{7,3} 타일링**

**다양한 플랫폼 구현: HTML/JS, React, Python, Java**

이 프로젝트는 Poincaré disk 모델을 사용하여 Order-3 heptagonal tiling을 시각화합니다. 이는 각 꼭짓점에 3개의 정칠각형이 만나는 쌍곡 평면의 정규 타일링입니다.

## 🚀 구현 버전

### 1. 📄 HTML/JavaScript (Standalone)
**가장 간단함 - 브라우저에서 바로 실행!**
```bash
# 그냥 파일 열기
open standalone.html
```
- ✅ 설치 불필요
- ✅ 온라인 환경 지원 (CodePen, JSFiddle)
- ✅ 마우스 드래그/줌 인터랙션

**파일**: `standalone.html`, `index.html`, `hyperbolic.js`

### 2. ⚛️ React
**모던 웹 프레임워크 + 애니메이션**
```bash
cd react-hyperbolic
npm install
npm start
```
- ✅ 컴포넌트 기반 구조
- ✅ **단계별 타일 생성 애니메이션** 🎬
- ✅ React Hooks 활용
- ✅ 반응형 디자인

**폴더**: `react-hyperbolic/`

### 3. 🐍 Python
**데이터 과학자/연구자용**
```bash
pip install numpy matplotlib
python hyperbolic_tiling.py
```
- ✅ matplotlib 기반 고품질 렌더링
- ✅ 인터랙티브 슬라이더
- ✅ Jupyter Notebook 호환 가능

**파일**: `hyperbolic_tiling.py`, `requirements.txt`

### 4. ☕ Java Swing
**데스크톱 네이티브 애플리케이션**
```bash
cd java-hyperbolic
mvn clean package
java -jar target/hyperbolic-tiling.jar
```
- ✅ 네이티브 데스크톱 앱
- ✅ **단계별 생성 애니메이션** 🎬
- ✅ 고성능 Graphics2D 렌더링
- ✅ 크로스플랫폼 JAR 배포

**폴더**: `java-hyperbolic/`

## 수학적 배경

- **Schläfli 기호**: {7,3}
- **기하학**: 쌍곡 기하학 (H²)
- **구조**: 각 꼭짓점에 정확히 3개의 정칠각형이 만남
- **모델**: Poincaré disk - 쌍곡 평면을 단위 원판에 투영

### 왜 쌍곡 기하학인가?

정칠각형의 내각은 약 128.57°입니다. 유클리드 평면에서 3개의 정칠각형을 한 점에 모으면 385.71°가 되어 평면에 맞지 않습니다. 쌍곡 공간의 음의 곡률이 이를 가능하게 합니다.

## 주요 기능

### 수학적 정확성
- **복소수 기반 계산**: 복소 평면에서의 Möbius 변환
- **측지선 렌더링**: 쌍곡 기하학에서의 "직선" (Poincaré disk에서는 원호)
- **정확한 타일 배치**: 쌍곡 등거리 변환을 통한 타일 생성

### 시각화 특징
- 정교한 타일 경계 표현
- 각 타일의 색상 구분
- 타일 깊이 조절 가능 (Depth 1-6)
- 인터랙티브 컨트롤

## 📁 파일 구조

```
.
├── standalone.html              # 단일 파일 HTML 버전 (권장) ⭐
├── index.html                   # HTML + 외부 JS
├── hyperbolic.js                # 쌍곡 기하학 구현
├── hyperbolic_tiling.py         # Python 구현
├── requirements.txt             # Python 의존성
├── README.md                    # 메인 문서
├── README_PYTHON.md             # Python 전용 문서
│
├── react-hyperbolic/            # React 버전
│   ├── src/
│   │   ├── App.js              # 메인 컴포넌트
│   │   ├── hyperbolic.js       # 로직
│   │   └── App.css             # 스타일
│   ├── package.json
│   └── README.md
│
└── java-hyperbolic/             # Java Swing 버전
    ├── src/main/java/hyperbolic/
    │   ├── HyperbolicViewer.java      # 메인 애플리케이션
    │   ├── PoincarePanel.java         # 렌더링 패널
    │   ├── HeptagonalTiling.java      # 타일링 생성
    │   ├── Complex.java               # 복소수
    │   └── MobiusTransform.java       # Möbius 변환
    ├── pom.xml                         # Maven 빌드
    ├── build.sh                        # 빌드 스크립트
    └── README.md
```

## 구현 세부사항

### 핵심 알고리즘

1. **Complex 클래스**: 복소수 연산 (덧셈, 곱셈, 나눗셈, 켤레)
2. **MobiusTransform**: Möbius 변환으로 쌍곡 등거리 변환 구현
3. **측지선 계산**: 두 점을 잇는 쌍곡 "직선" (단위원과 직교하는 원호)
4. **타일 생성**: BFS 알고리즘으로 중앙에서 확장

### 수학 공식

**쌍곡 거리**:
```
d(z₁, z₂) = acosh(1 + 2|z₁ - z₂|² / ((1 - |z₁|²)(1 - |z₂|²)))
```

**Möbius 변환**:
```
f(z) = (az + b) / (cz + d)
```

**측지선**: Poincaré disk에서 측지선은 단위원과 직교하는 원의 호

## 🔧 기술 스택

### HTML/JS
- **순수 JavaScript**: 외부 라이브러리 없음
- **HTML5 Canvas**: 고성능 렌더링

### React
- **React 18**: 최신 Hooks API
- **Canvas API**: 2D 렌더링
- **ES6 Modules**: 모듈화

### Python
- **NumPy**: 수치 계산
- **matplotlib**: 시각화
- **복소수**: 내장 complex 타입

### Java
- **Java Swing**: GUI 프레임워크
- **Graphics2D**: 안티앨리어싱 렌더링
- **Maven**: 빌드 도구

### 공통 수학
- 복소수 연산
- Möbius 변환
- 쌍곡 기하학 (Poincaré disk)

## 성능

- Depth 4: ~100-200 타일
- Depth 5: ~300-500 타일
- Depth 6: ~800-1000 타일 (최대 제한)

## 🆚 버전 비교표

| 특징 | HTML/JS | React | Python | Java |
|------|---------|-------|--------|------|
| 설치 필요 | ❌ | npm | pip | JDK |
| 실행 환경 | 브라우저 | 브라우저 | 데스크톱 | 데스크톱 |
| 애니메이션 | ❌ | ✅ | ❌ | ✅ |
| 드래그/줌 | ✅ | ⚠️ | ❌ | ❌ |
| 성능 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 코드 구조 | 단순 | 모듈화 | 클래스 | OOP |
| 배포 | 파일 공유 | 웹 호스팅 | exe/app | JAR |
| 모바일 지원 | ✅ | ✅ | ❌ | ❌ |

### 사용 시나리오별 추천

- **빠른 데모**: `standalone.html` 👈 **가장 추천!**
- **웹 앱 개발**: `React` 버전
- **연구/분석**: `Python` 버전
- **교육/배포**: `Java` 버전

## 🎬 애니메이션 기능

React와 Java 버전에서 지원하는 **단계별 타일 생성 애니메이션**:

1. BFS 순서대로 타일이 하나씩 나타남
2. 진행률 표시
3. Play/Pause 제어
4. 속도 자동 조절

## 컨트롤

### HTML/JS
- **Depth 슬라이더**: 타일링의 재귀 깊이 조절 (1-6)
- **Show Edges**: 타일 경계선 표시/숨김
- **Color Tiles**: 타일 색상 모드 전환
- **마우스 드래그**: 뷰 이동 (팬)
- **마우스 휠**: 줌 인/아웃
- **Reset View**: 초기 뷰로 복귀

### React & Java
위 컨트롤 + **Animate Generation** (애니메이션 모드)

### Python
- **Depth 슬라이더**: 깊이 조절
- **체크박스**: Show Edges, Color Tiles
- **Reset 버튼**: 초기화

## 🎓 교육적 가치

이 프로젝트로 배울 수 있는 내용:
- 🔢 **쌍곡 기하학**: Poincaré disk 모델의 이해
- 🧮 **복소수 연산**: 기하학적 변환
- 📐 **측지선**: 쌍곡 공간에서의 "직선"
- 🔄 **BFS 알고리즘**: 타일 생성
- 💻 **다중 플랫폼 개발**: 동일 알고리즘, 다양한 언어
- 🎨 **그래픽스 프로그래밍**: Canvas, Graphics2D, matplotlib

## 참고 자료

- [Order-3 heptagonal tiling - Verse and Dimensions Wiki](https://verse-and-dimensions.fandom.com/wiki/Order-3_heptagonal_tiling)
- Poincaré disk model - Wikipedia
- Hyperbolic geometry - 쌍곡 기하학 이론
- Schläfli symbol {p,q}

## 📝 라이선스

MIT License

## 🙋 작성자

Claude Code - Hyperbolic Geometry Visualization Project
