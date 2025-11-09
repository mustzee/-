# Order-3 Heptagonal Tiling - React

React로 구현한 쌍곡 기하학 시각화 with 애니메이션!

## 🚀 설치 및 실행

### 방법 1: npm 사용
```bash
cd react-hyperbolic
npm install
npm start
```

### 방법 2: yarn 사용
```bash
cd react-hyperbolic
yarn install
yarn start
```

브라우저에서 자동으로 `http://localhost:3000` 열림!

## ✨ 특징

### 🎬 애니메이션 기능
- **Animate Generation**: 타일이 하나씩 그려지는 과정 시각화
- **Play/Pause**: 애니메이션 제어
- **Progress Bar**: 생성 진행률 표시

### 🎮 인터랙티브 컨트롤
- **Depth 슬라이더** (1-6): 타일링 깊이 실시간 조절
- **Show Edges**: 경계선 표시/숨김
- **Color Tiles**: 다양한 색상으로 타일 구분
- **Reset View**: 초기 상태로 복귀

### 📱 반응형 디자인
- 데스크톱, 태블릿, 모바일 모두 지원
- 자동 크기 조절

## 🏗️ 프로젝트 구조

```
react-hyperbolic/
├── public/
│   └── index.html
├── src/
│   ├── App.js          # 메인 React 컴포넌트
│   ├── App.css         # 스타일
│   ├── hyperbolic.js   # 쌍곡 기하학 로직
│   ├── index.js        # 엔트리 포인트
│   └── index.css       # 글로벌 스타일
├── package.json
└── README.md
```

## 🎨 주요 기능

### 1. 단계별 타일 생성 애니메이션
```javascript
// Animate Generation 체크박스 활성화
// Play 버튼으로 애니메이션 시작
// 타일이 BFS 순서대로 하나씩 나타남
```

### 2. 실시간 파라미터 조절
```javascript
// Depth 슬라이더를 움직이면 즉시 재생성
// 체크박스로 즉시 표시 옵션 변경
```

### 3. React Hooks 활용
- `useState`: 상태 관리
- `useEffect`: 렌더링 동기화
- `useRef`: Canvas 및 객체 참조

## 🔧 기술 스택

- **React 18**: 최신 React 기능
- **Canvas API**: 고성능 2D 렌더링
- **ES6 Modules**: 모듈화된 코드 구조
- **CSS3**: 현대적인 스타일링

## 📦 빌드

```bash
npm run build
```

빌드된 파일은 `build/` 폴더에 생성됩니다.

## 🎯 사용 예시

### 애니메이션 보기
1. **Animate Generation** 체크
2. Depth 변경 (예: 5)
3. **Play** 버튼 클릭
4. 타일이 하나씩 그려지는 과정 관찰!

### 정적 이미지
1. **Animate Generation** 체크 해제
2. Depth 조절
3. Show Edges, Color Tiles로 스타일 변경

## 🌟 React vs HTML

| 특징 | React | HTML |
|------|-------|------|
| 컴포넌트화 | ✅ 우수 | ❌ 없음 |
| 상태 관리 | ✅ Hooks | ⚠️ 전역 변수 |
| 애니메이션 | ✅ 단계별 | ❌ 없음 |
| 재사용성 | ✅ 매우 높음 | ⚠️ 보통 |
| 개발 서버 | ✅ 핫 리로드 | ⚠️ 수동 새로고침 |

## 📝 라이선스

MIT License
