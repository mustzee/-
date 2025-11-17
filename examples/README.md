# 🎨 HTML Examples

이 폴더에는 브라우저에서 바로 실행 가능한 HTML/JavaScript 데모 파일들이 포함되어 있습니다.

## 🚀 빠른 시작

아무 HTML 파일이나 브라우저에서 열어보세요!

```bash
# 권장: 단일 파일 버전
open standalone.html

# 또는 웹 서버로 실행
python -m http.server 8000
# 브라우저에서 http://localhost:8000 접속
```

## 📄 파일 설명

### `standalone.html` ⭐ **권장!**
**완전 독립형 버전**
- 모든 코드가 하나의 파일에 포함
- 외부 의존성 없음
- CodePen, JSFiddle 등에 복사 가능
- 마우스 드래그/줌 지원

**사용 사례:**
- 빠른 데모
- 오프라인 실행
- 교육/발표 자료

---

### `index.html`
**외부 JavaScript 연결 버전**
- `src/javascript/hyperbolic.js` 파일 참조
- 코드 분리로 가독성 향상
- 개발 시 편리

**사용 사례:**
- 코드 수정/개선 작업
- 로컬 개발 환경

---

### `heptagon-tiling-fixed.html`
**BFS 알고리즘 수정 버전**
- Layer 2 타일 생성 로직 개선
- 중복 타일 제거
- 더 정확한 타일링

---

### `heptagon-tiling-topology-fixed.html`
**토폴로지 수정 버전**
- 타일 연결성 개선
- 인접 타일 관계 정확도 향상

---

### `heptagonal-tiling-advanced.html`
**고급 기능 포함 버전**
- 추가 시각화 옵션
- 실험적 기능 포함
- 개발 중인 기능 테스트용

---

## 🎮 공통 기능

모든 HTML 파일은 다음 기능을 지원합니다:

### 컨트롤
- **Depth 슬라이더**: 타일링 재귀 깊이 조절 (1-6)
- **Show Edges**: 타일 경계선 표시/숨김
- **Color Tiles**: 타일 색상 모드 전환
- **Reset View**: 초기 뷰로 복귀

### 인터랙션 (standalone.html, index.html)
- **마우스 드래그**: 뷰 이동 (Pan)
- **마우스 휠**: 줌 인/아웃
- **터치 지원**: 모바일/태블릿 호환

## 🔧 커스터마이징

### 색상 변경
```javascript
// 타일 색상 팔레트 수정
const COLORS = [
    '#FFE5E5', // 빨강 계열
    '#E5F3FF', // 파랑 계열
    '#E8FFE5', // 초록 계열
    // ... 원하는 색상 추가
];
```

### 캔버스 크기 조정
```javascript
canvas.width = 1200;  // 너비
canvas.height = 900;  // 높이
```

### 초기 깊이 설정
```javascript
let depth = 4;  // 1-6 사이 값
```

## 📱 브라우저 호환성

- ✅ Chrome/Edge (권장)
- ✅ Firefox
- ✅ Safari
- ✅ 모바일 브라우저

**최소 요구사항:**
- HTML5 Canvas 지원
- ES6 JavaScript 지원

## 🐛 문제 해결

### 파일이 로드되지 않음
- 브라우저 콘솔(F12) 확인
- CORS 에러 발생 시 → 웹 서버로 실행
- `index.html`의 경우 `src/javascript/hyperbolic.js` 경로 확인

### 성능 이슈
- Depth를 낮춤 (3-4 권장)
- Depth 6은 800+ 타일로 느릴 수 있음
- 브라우저 하드웨어 가속 활성화

### 모바일에서 느림
- Depth 3-4 사용
- Show Edges 비활성화로 성능 향상

## 🎓 학습 가이드

### 코드 구조 이해하기
1. **Complex 클래스**: 복소수 연산
2. **MobiusTransform**: 쌍곡 등거리 변환
3. **drawGeodesic**: 측지선 그리기
4. **generateTiles**: BFS로 타일 생성

### 실험해보기
- Depth 값 변경 → 타일 개수 변화 관찰
- 색상 팔레트 수정 → 시각적 효과 확인
- 정칠각형 → 정육각형으로 변경 ({6,4} 타일링)

## 📚 관련 리소스

- [Poincaré disk model - Wikipedia](https://en.wikipedia.org/wiki/Poincar%C3%A9_disk_model)
- [Hyperbolic geometry - 쌍곡 기하학](https://en.wikipedia.org/wiki/Hyperbolic_geometry)
- [Order-3 heptagonal tiling](https://en.wikipedia.org/wiki/Order-3_heptagonal_tiling)

## 💡 다른 구현 버전

더 고급 기능을 원한다면:
- **React 버전**: `../react-hyperbolic/` - 애니메이션, 컴포넌트 구조
- **Python 버전**: `../src/python/` - matplotlib 시각화
- **Java 버전**: `../java-hyperbolic/` - 네이티브 데스크톱 앱
