# 💻 Source Code

이 폴더에는 쌍곡 타일링 시각화의 핵심 소스 코드가 포함되어 있습니다.

## 📂 폴더 구조

```
src/
├── javascript/          # JavaScript 구현
│   └── hyperbolic.js   # 공통 쌍곡 기하학 라이브러리
└── python/             # Python 구현
    ├── hyperbolic_tiling.py  # 메인 프로그램
    └── requirements.txt      # 의존성 목록
```

---

## 🟨 JavaScript

### `javascript/hyperbolic.js`

**쌍곡 기하학 핵심 구현**

HTML 예제들에서 공통으로 사용하는 JavaScript 라이브러리입니다.

#### 주요 클래스/함수

**Complex 클래스**
```javascript
class Complex {
    constructor(re, im)
    add(other)
    sub(other)
    mul(other)
    div(other)
    conj()
    abs()
}
```

**MobiusTransform 클래스**
```javascript
class MobiusTransform {
    constructor(a, b, c, d)
    apply(z)              // f(z) = (az + b) / (cz + d)
    compose(other)
    inverse()
}
```

**유틸리티 함수**
- `hyperbolicDistance(z1, z2)`: 쌍곡 거리 계산
- `drawGeodesic(ctx, z1, z2)`: 측지선 그리기
- `generateTiles(depth)`: BFS로 타일 생성

#### 사용 예시

```html
<script src="../src/javascript/hyperbolic.js"></script>
<script>
    // 복소수 생성
    const z1 = new Complex(0.5, 0.3);
    const z2 = new Complex(-0.2, 0.6);

    // 쌍곡 거리
    const dist = hyperbolicDistance(z1, z2);

    // Möbius 변환
    const transform = new MobiusTransform(
        new Complex(1, 0),
        new Complex(0.5, 0),
        new Complex(0.5, 0),
        new Complex(1, 0)
    );
    const z3 = transform.apply(z1);
</script>
```

#### 외부에서 사용하기

이 라이브러리는 독립적으로 사용 가능합니다:

1. HTML 파일에 포함
2. 다른 쌍곡 기하학 프로젝트에 활용
3. Canvas 기반 시각화 구현

---

## 🐍 Python

### `python/hyperbolic_tiling.py`

**matplotlib 기반 쌍곡 타일링 시각화**

#### 실행 방법

```bash
cd src/python

# 의존성 설치
pip install -r requirements.txt

# 실행
python hyperbolic_tiling.py
```

#### 주요 클래스

**Complex 클래스**
```python
class Complex:
    def __init__(self, re, im)
    def __add__(self, other)
    def __sub__(self, other)
    def __mul__(self, other)
    def __truediv__(self, other)
    def conj(self)
    def abs(self)
```

**MobiusTransform 클래스**
```python
class MobiusTransform:
    def __init__(self, a, b, c, d)
    def apply(self, z)
    def compose(self, other)
```

**HyperbolicTiling 클래스**
```python
class HyperbolicTiling:
    def __init__(self, depth=3)
    def generate_tiles(self)
    def draw_geodesic(self, z1, z2)
    def plot(self)
```

#### 기능

- **인터랙티브 슬라이더**: Depth 실시간 조절
- **체크박스 컨트롤**:
  - Show Edges (경계선 표시)
  - Color Tiles (타일 색상)
- **고품질 렌더링**: matplotlib의 안티앨리어싱
- **Jupyter 호환**: 노트북에서 실행 가능

#### 커스터마이징

**타일 색상 변경**
```python
# 색상 팔레트
COLORS = ['#FFE5E5', '#E5F3FF', '#E8FFE5', '#FFFFE5', '#FFE5FF']
```

**캔버스 크기 조정**
```python
fig, ax = plt.subplots(figsize=(10, 10))  # 인치 단위
```

**초기 설정**
```python
tiling = HyperbolicTiling(depth=4)  # 깊이 설정
```

#### Jupyter Notebook에서 사용

```python
import matplotlib.pyplot as plt
from hyperbolic_tiling import HyperbolicTiling

# 인라인 출력
%matplotlib widget

# 타일링 생성 및 표시
tiling = HyperbolicTiling(depth=3)
tiling.plot()
plt.show()
```

---

## 🔬 수학적 배경

두 구현 모두 동일한 수학적 원리를 따릅니다:

### 복소수 연산
쌍곡 기하학을 복소 평면에서 구현합니다.

```
z = x + iy (복소수)
|z| = √(x² + y²) (절댓값)
```

### Möbius 변환
```
f(z) = (az + b) / (cz + d)
여기서 a, b, c, d는 복소수
```

### 쌍곡 거리 (Poincaré disk)
```
d(z₁, z₂) = acosh(1 + 2|z₁ - z₂|² / ((1 - |z₁|²)(1 - |z₂|²)))
```

### 측지선
Poincaré disk에서 측지선은 단위원과 직교하는 원의 호입니다.

---

## 🆚 JavaScript vs Python

| 특징 | JavaScript | Python |
|------|-----------|--------|
| **실행 환경** | 브라우저 | 데스크톱 |
| **렌더링** | Canvas API | matplotlib |
| **성능** | ⭐⭐⭐⭐⭐ 매우 빠름 | ⭐⭐⭐⭐ 빠름 |
| **인터랙션** | 드래그/줌 | 슬라이더 |
| **설치** | 불필요 | pip 필요 |
| **사용 사례** | 웹 데모 | 연구/분석 |
| **코드 스타일** | 프로토타입 | OOP |

### 선택 가이드

**JavaScript를 선택하세요:**
- 웹 브라우저에서 실행하고 싶을 때
- 설치 없이 바로 사용하고 싶을 때
- 모바일 지원이 필요할 때
- 빠른 인터랙션이 중요할 때

**Python을 선택하세요:**
- 데이터 분석/연구 목적
- Jupyter Notebook 환경
- 고품질 정적 이미지 생성
- 논문/발표 자료용 그래픽

---

## 🔧 개발 가이드

### 새로운 타일링 추가하기

#### 1. 정N각형으로 변경

**JavaScript (hyperbolic.js)**
```javascript
const N = 6;  // 정육각형으로 변경
const angle = 2 * Math.PI / N;
```

**Python (hyperbolic_tiling.py)**
```python
N = 6  # 정육각형
angle = 2 * math.pi / N
```

#### 2. 타일 생성 알고리즘 수정

BFS 깊이 제한 변경, 중복 제거 로직 개선 등

### 성능 최적화

**JavaScript**
- `requestAnimationFrame` 사용
- 오프스크린 캔버스 활용
- Path2D 객체로 경로 재사용

**Python**
- NumPy 벡터화 연산
- `@lru_cache` 데코레이터
- Cython으로 핵심 루프 최적화

### 테스트

**수학적 정확성 확인**
```python
# 쌍곡 거리 삼각 부등식 테스트
d12 = hyperbolic_distance(z1, z2)
d23 = hyperbolic_distance(z2, z3)
d13 = hyperbolic_distance(z1, z3)
assert d13 <= d12 + d23
```

---

## 📚 참고 자료

### 수학
- "Hyperbolic Geometry" - James W. Anderson
- "Indra's Pearls" - Mumford, Series, Wright

### 구현
- [Canvas API - MDN](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
- [matplotlib documentation](https://matplotlib.org/)
- [Complex numbers in Python](https://docs.python.org/3/library/cmath.html)

### 논문
- Poincaré, H. (1882). "Théorie des groupes fuchsiens"
- Escher's hyperbolic tessellations

---

## 🤝 기여

코드 개선, 버그 수정, 새로운 기능 추가는 언제든 환영합니다!

### 코딩 스타일
- **JavaScript**: JSDoc 주석, camelCase
- **Python**: PEP 8, Google docstring

### 커밋 메시지
```
feat: Add hexagonal tiling support
fix: Correct geodesic calculation
docs: Update API documentation
```
